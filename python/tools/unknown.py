from python.helpers.tool import Tool, Response
from python.helpers.mcp_handler import MCPConfig
from python.extensions.system_prompt._10_system_prompt import (
    get_tools_prompt,
)


class Unknown(Tool):
    async def execute(self, **kwargs):
        tools = get_tools_prompt(self.agent)
        # Include MCP tools in the error response so LLM knows they exist
        try:
            mcp_config = MCPConfig.get_instance()
            if mcp_config.servers:
                mcp_tools = mcp_config.get_tools_prompt()
                if mcp_tools:
                    tools += "\n\n" + mcp_tools
        except Exception:
            pass  # Don't let MCP errors break the unknown tool handler
        return Response(
            message=self.agent.read_prompt(
                "fw.tool_not_found.md", tool_name=self.name, tools_prompt=tools
            ),
            break_loop=False,
        )
