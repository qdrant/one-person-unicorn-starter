#!/usr/bin/env python
import asyncio
import os

from dotenv import load_dotenv
from mistralai import Mistral
from mistralai.extra.mcp.sse import MCPClientSSE, SSEServerParams
from mistralai.extra.run.context import RunContext

load_dotenv()

# --- Config ----------------------------------------------------

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

AGENT_DESCRIPTION = "Agent that can manage the memory of the user."
AGENT_INSTRUCTIONS = "Always use your tools to manage the memory. Use the 'qdrant-store' tool to save information and 'qdrant-find' to retrieve it."
AGENT_NAME = "qdrant-memory-agent"


async def main():
    # --- 1. Initialize Mistral Client ---
    mistral_client = Mistral(MISTRAL_API_KEY)

    # --- 2. Create the Memory-Enabled Agent ---
    # We create an agent and specifically instruct it to use its tools to manage memory.
    qdrant_memory_agent = mistral_client.beta.agents.create(
        model=MISTRAL_MODEL,
        description=AGENT_DESCRIPTION,
        instructions=AGENT_INSTRUCTIONS,
        name=AGENT_NAME,
    )

    # --- 3. Configure the Qdrant Memory Server ---
    sse_params = SSEServerParams(url=MCP_SERVER_URL, timeout=100)

    # --- 4. Storing a Memory in a first run context ---
    # This block creates and cleanly destroys the context and its dedicated mistral_client.
    async with RunContext(agent_id=qdrant_memory_agent.id, continue_on_fn_error=True) as run_ctx_1:
        await run_ctx_1.register_mcp_client(mcp_client=MCPClientSSE(sse_params=sse_params))
        print("🤖 Telling the agent to remember a secret...")
        store_result = await mistral_client.beta.conversations.run_async(
            run_ctx=run_ctx_1,
            inputs="Remember that the secret code for the hackathon is 'Aurora Penguin'.",
        )
        print(f"✅ Agent confirmed: {store_result.output_as_text}\n")

    # --- 5. Sanity Check: Recalling the Memory in a new run context ---
    # This creates a completely separate run to prove the memory is not from chat history.
    async with RunContext(agent_id=qdrant_memory_agent.id, continue_on_fn_error=True) as run_ctx_2:
        await run_ctx_2.register_mcp_client(mcp_client=MCPClientSSE(sse_params=sse_params))
        print("🤖 Asking the agent to recall the secret in a new context...")
        recall_result = await mistral_client.beta.conversations.run_async(
            run_ctx=run_ctx_2, inputs="What is the secret code for the event?"
        )
        print(f"🧠 Agent recalled: {recall_result.output_as_text}")


if __name__ == "__main__":
    asyncio.run(main())
