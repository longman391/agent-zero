from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from initialize import initialize_agent
from python.extensions.hist_add_tool_result import _90_save_tool_call_file as save_tool_call_file

# Override subordinate model to avoid Claude's JSON formatting resistance.
# Claude subordinates interpret Agent Zero system prompt as "prompt injection"
# and refuse to output JSON, causing infinite misformat loops.
# GLM-5 reliably follows JSON formatting instructions.
SUBORDINATE_MODEL_OVERRIDES = {
    "chat_model_provider": "other",
    "chat_model_name": "glm-5",
    "chat_model_api_base": "http://10.0.1.10:4000/v1",
}

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
