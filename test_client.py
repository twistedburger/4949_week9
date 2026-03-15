import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["weather_tools_server.py"],
        env=None,
    )

    async with AsyncExitStack() as stack:
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport

        session = await stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()

        tools_resp = await session.list_tools()
        print("\n*** Tools exposed by server:")
        for t in tools_resp.tools:
            # name + short description
            print(f" - {t.name}: {t.description}")

            # if the tool includes an input schema (often does), show it too
            if getattr(t, "inputSchema", None):
                print(f"   inputSchema: {t.inputSchema}")

        # call a tool
        result = await session.call_tool("get_weather", {"city": "Vancouver"})
        temp = await session.call_tool("get_fahrenheitFromCelsius", {"temp": 24})
        print("\n*** Calling get_fahrenheitFromCelsius(24): ")
        print(f"24C is {temp}F")

if __name__ == "__main__":
    asyncio.run(main())
