from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from initialize import initialize_agent
from python.extensions.hist_add_tool_result import _90_save_tool_call_file as save_tool_call_file

# Override subordinate model.
# - Claude refuses JSON output (interprets system prompt as "prompt injection")
# - GLM-5 ignores task boundaries (e.g. "investigate only" -> deletes containers)
# Gemini 3 Flash follows JSON formatting and respects instruction constraints.
SUBORDINATE_MODEL_OVERRIDES = {
    "chat_model_provider": "other",
    "chat_model_name": "gemini-3-flash-preview",
    "chat_model_api_base": "http://10.0.1.10:4000/v1",
}

# Safety preamble prepended to all subordinate messages to prevent
# destructive actions beyond the delegated scope.
SUBORDINATE_SAFETY_PREAMBLE = """CRITICAL CONSTRAINTS — You are a SUBORDINATE agent. You MUST obey these rules:
1. SCOPE LIMIT: Only perform actions explicitly requested in your task. If the task says
   "investigate", "diagnose", "check", "audit", or "report" — you ONLY gather information
   and report findings. You do NOT fix, modify, restart, or delete anything.
2. DESTRUCTIVE COMMAND BAN: NEVER execute destructive or state-changing commands unless
   your task explicitly says "fix", "apply", "execute", "restart", "remove", or "deploy".
   Banned unless explicitly authorized:
   - docker stop/rm/run/restart, docker-compose up/down
   - systemctl stop/start/restart, service stop/start
   - rm -rf, mkfs, fdisk, dd
   - kill/pkill/killall
   - chmod/chown on system directories
   - Any command that modifies infrastructure state
3. PROPOSE, DON'T ACT: When you find a problem and know the fix, DESCRIBE the fix in
   your report (including exact commands) but DO NOT execute it unless authorized.
4. ASK WHEN UNCERTAIN: If you are unsure whether an action is within scope, STOP and
   report back to your superior asking for explicit permission.

---
YOUR TASK:
"""

# Common hallucinated parameter names the LLM uses instead of "message"
MESSAGE_ALIASES = [
    "visual_representation", "task", "instruction", "prompt",
    "query", "content", "text", "request", "input",
]


class Delegation(Tool):

    async def execute(self, message="", reset="", **kwargs):
        # Resolve hallucinated parameter names to "message"
        if not message:
            for alias in MESSAGE_ALIASES:
                if alias in kwargs and kwargs[alias]:
                    message = kwargs[alias]
                    break

        # Prepend safety preamble to constrain subordinate behavior
        message = SUBORDINATE_SAFETY_PREAMBLE + message

        # create subordinate agent using the data object on this agent and set superior agent to his data object
        if (
            self.agent.get_data(Agent.DATA_NAME_SUBORDINATE) is None
            or str(reset).lower().strip() == "true"
        ):
            # initialize config with subordinate model overrides
            config = initialize_agent(override_settings=SUBORDINATE_MODEL_OVERRIDES)

            # set subordinate prompt profile if provided, if not, keep original
            agent_profile = kwargs.get("profile", kwargs.get("agent_profile", ""))
            if agent_profile:
                config.profile = agent_profile

            # crate agent
            sub = Agent(self.agent.number + 1, config, self.agent.context)
            # register superior/subordinate
            sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
            self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub)

        # add user message to subordinate agent
        subordinate: Agent = self.agent.get_data(Agent.DATA_NAME_SUBORDINATE)  # type: ignore
        subordinate.hist_add_user_message(UserMessage(message=message, attachments=[]))

        # run subordinate monologue
        result = await subordinate.monologue()

        # seal the subordinate's current topic so messages move to `topics` for compression
        subordinate.history.new_topic()

        # hint to use includes for long responses
        additional = None
        if len(result) >= save_tool_call_file.LEN_MIN:
            hint = self.agent.read_prompt("fw.hint.call_sub.md")
            if hint:
                additional = {"hint": hint}

        # result
        return Response(message=result, break_loop=False, additional=additional)

    def get_log_object(self):
        return self.agent.context.log.log(
            type="subagent",
            heading=f"icon://communication {self.agent.agent_name}: Calling Subordinate Agent",
            content="",
            kvps=self.args,
        )
