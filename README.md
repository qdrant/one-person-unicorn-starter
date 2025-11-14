# one-person-unicorn-starter

Every self-running company needs memory. This repo helps you give your AI startup one—using Qdrant for fast, production-ready vector search. Fork it, index your data, and let your agents think with context.

## Step 1: Requirements and setup (5 minutes)

For the hackathon, the easiest way to get started is with Qdrant Cloud. The free tier offers a cluster with 1 GiB of RAM and 4 GiB of Disk, which is sufficient for creating and demonstrating your project.

1. **Get your Qdrant Cloud Free Tier credentials:**
    - [**Sign up for Qdrant Cloud**](https://cloud.qdrant.io). No credit card required.
    - Create a **New Cluster**. You can keep the default settings to get the free 1 GiB instance.
    - Once created, a pop-up containing sample code with **your cluster URL and API key**, will appear. You will need them to connect your application.
2. **Get your Mistral API Key:**
    - Sign up at [mistral.ai](https://mistral.ai/) and get your API key.
3. **Set Up Your Python Environment**
    - We recommend [uv](https://github.com/astral-sh/uv) (an extremely fast Python package and project manager, written in Rust), but standard pip and venv work just as well.
    - 🚀 Recommended: Using `uv`
        
        ```bash
        # Install uv (if you don't have it)
        # On macOS and Linux:
        curl -LsSf https://astral.sh/uv/install.sh | sh 
        # On Windows:
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        
        # Create and activate your project environment
        cd your-project-folder
        uv init
        uv venv # or 'uv venv --python 3.12' to specify a version
        source .venv/bin/activate
        ```
        
    - 🐍 Alternative: Using `pip` and `venv`
        
        ```bash
        # Create and activate your project environment
        cd your-project-folder
        python -m venv .venv
        source .venv/bin/activate
        # On Windows, use: .venv\Scripts\activate
        ```
        
4. **Install the necessary Python libraries:**
    - We need the Mistral client and `python-dotenv` to handle our keys.
        
        ```bash
        uv add datasets python-dotenv qdrant-client "qdrant-client[fastembed]>=1.14.2" "mistralai[agents]" 
        ```
        
    - If you do NOT use uv as environment manager you might need to also `pip install uv` to run the Qdrant mcp server.
        
        ```bash
        # in your activated environment run
        pip install datasets python-dotenv qdrant-client "qdrant-client[fastembed]>=1.14.2" "mistralai[agents]" uv
        ```
        
5. **Create your `.env` file:**
    - In your project directory, create a file named `.env`. This is where you'll store your secret keys so you don't have to paste them into your code.
    - Add your credentials and choose a name for your Qdrant collection.
        
        ```bash
        # .env file
        ## Mistral AI
        MISTRAL_API_KEY="your-mistral-api-key"
        MISTRAL_MODEL="mistral-large-latest"
        
        ## MCP Server
        MCP_SERVER_URL="http://127.0.0.1:8000/sse"
        
        ## Qdrant Vector Store
        COLLECTION_NAME="mistral-agent-memory"
        EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2" # The mcp-server-qdrant currently supports FastEmbed models only.
        
        # --- Choose ONE Qdrant setup ---
        # Option 1: Cloud Qdrant
        QDRANT_URL="https://xyz-123.gcp.cloud.qdrant.io:6333"
        QDRANT_API_KEY="your-qdrant-cloud-api-key"
        
        # Option 2: Local Qdrant (Uncomment and fill in)
        # QDRANT_LOCAL_PATH="./qdrant_db"
        ```
        

## Step 2: **Upload Data***

Run

    ```bash
    # In Terminal 2
    uv run python upload_data.py
    # or if using venv: python upload_data.py 
    ```

## Step 2: **Launch the Memory Server**

The MCP server translates Qdrant's capabilities (storing, finding vectors) into tools (`qdrant-store`, `qdrant-find`) that the agent can execute.

- Open your first terminal window and run the following command:
    
    ```bash
    # In Terminal 1
    source .env && uvx mcp-server-qdrant --transport sse
    ```
    
- Keep this terminal running. It is now serving the tools your agent will use.

## Step 3: Run the Memory Agent
    - In your **second terminal window**, execute the script:
        
        ```bash
        # In Terminal 2
        uv run python memory_agent.py
        # or if using venv: python memory_agent.py 
        ```
        
    - You should see an output similar to this:
        
        ```
        🤖 Telling the agent to remember a secret...
        ✅ Agent confirmed: I've remembered that the secret code for the hackathon is **"Aurora Penguin"**.\n
        🤖 Asking the agent to recall the secret in a new context...
        🧠 Agent recalled: The secret code for the event is **"Aurora Penguin"**.
        ```
        

Congratulations! You have successfully given your Mistral agent a long-term memory using Qdrant vector search engine. You can now build on this to create sophisticated, stateful AI applications for the hackathon.

### How It Works

1. **Create the Agent:** We create a Mistral agent with a clear instruction: `"Always use your tools to manage the memory."`. This tells the agent that when it sees a prompt related to remembering or recalling, it should look for a tool to do the job.
2. **Connect Agent & Memory:** The `RunContext` connects our agent to the `mcp-server-qdrant` process. The agent now has two tools available: `qdrant-store` and `qdrant-find`.
3. **Storing a Memory:** When we send the prompt `"Remember that..."`, the agent follows its instructions. It activates the `qdrant-store` tool, which takes the text, creates a vector embedding, and saves it in your Qdrant Cloud collection.
4. **Recalling the Memory:** Later, when we ask `"What is the secret code...?"`, the agent activates the `qdrant-find` tool. It creates an embedding of the question, searches your Qdrant collection for the most similar memory, and uses the result to answer your question accurately.

## Resources & Help

- [**Qdrant Documentation**](https://qdrant.tech/documentation/): The official source of truth.
- [**Python Client (GitHub)**](https://github.com/qdrant/qdrant_client): See examples and the full API reference.
- [**Qdrant Cookbook**](https://qdrant.tech/documentation/examples/): Jupyter notebooks with advanced examples.
- [**MCP Server (Github)**](https://github.com/qdrant/mcp-server-qdrant): More ways to use `mcp-server-qdrant`.
- [**Discord Community**](https://qdrant.to/discord): Get help from the community and the Qdrant team. We'll be watching for hackathon questions.