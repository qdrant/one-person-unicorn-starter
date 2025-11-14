# one-person-unicorn-starter

Give your AI startup a memory. This starter uses **Qdrant** for fast vector search so your agent (Mistral) can store and recall facts during the hackathon.

---

## 1) Setup (≈5 minutes)

### Accounts
- **Qdrant Cloud:** https://cloud.qdrant.io → create a free cluster (you’ll get a **QDRANT_URL** and **QDRANT_API_KEY**).
- **Mistral:** https://mistral.ai → create a **MISTRAL_API_KEY**.

### Python env
You can use either **uv** (recommended) or **pip + venv**.

**Using uv**
```bash
# Install uv
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create and activate a venv
cd your-project-folder
uv init
uv venv            # or: uv venv --python 3.12
source .venv/bin/activate  # Windows: .venv\Scripts\activate
````

**Using pip + venv**

```bash
cd your-project-folder
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Install packages

```bash
# uv
uv add datasets python-dotenv qdrant-client "qdrant-client[fastembed]>=1.14.2" "mistralai[agents]"
# If you’re on pip:
pip install datasets python-dotenv qdrant-client "qdrant-client[fastembed]>=1.14.2" "mistralai[agents]"
```

> The MCP server for Qdrant is fetched on-the-fly when you run it via `uvx` (no manual install needed).

### Environment variables

Copy `.env-example` to `.env` and fill in your keys:

```bash
cp .env-example .env
```

Then edit `.env`:

* `QDRANT_URL`, `QDRANT_API_KEY` from Qdrant Cloud
* `MISTRAL_API_KEY` from Mistral
* `COLLECTION_NAME` any name (e.g. `mistral-agent-memory`)
* `EMBEDDING_MODEL` keep default `BAAI/bge-small-en`
* `VECTOR_SIZE` must match the model (bge-small-en = 384)
* `DISTANCE_METRIC` keep `Cosine`
* `MCP_SERVER_URL` leave as `http://127.0.0.1:8000/sse`

---

## 2) Launch the Qdrant Memory Server (Terminal 1)

The MCP server exposes two tools the agent can call: `qdrant-store` and `qdrant-find`.

```bash
# In Terminal 1
source .env
uvx mcp-server-qdrant --transport sse
```

Leave this running.

---

## 3) Upload sample data (Terminal 2, optional but helpful)

This loads a small public dataset and indexes it into your Qdrant collection so you can test search quickly.

```bash
# In Terminal 2
source .env
uv run python upload_data.py
# or: python upload_data.py
```

You should see a confirmation with a top score.

---

## 4) Run the memory agent (Terminal 2)

```bash
# Still in Terminal 2
uv run python memory_agent.py
# or: python memory_agent.py
```

Expected output:

```
🤖 Telling the agent to remember a secret...
✅ Agent confirmed: I've remembered that the secret code for the hackathon is "Aurora Penguin".

🤖 Asking the agent to recall the secret in a new context...
🧠 Agent recalled: The secret code for the event is "Aurora Penguin".
```

Congrats — your Mistral agent now writes and reads long-term memory via Qdrant.

---

## How it works

1. **Agent** — Created with instructions to use tools for memory tasks.
2. **MCP bridge** — `mcp-server-qdrant` runs locally and exposes:

   * `qdrant-store` → embed + upsert
   * `qdrant-find` → embed + nearest-neighbor search
3. **Qdrant** — Stores vectors + payload so the agent can recall facts across runs.

---

## Tips

* Keep **`BAAI/bge-small-en`** unless you know you need another model (FastEmbed models only).
* Make sure **`VECTOR_SIZE`** matches the embedding model (384 for `bge-small-en`).
* If you need local Qdrant instead of Cloud, see the commented option in `.env-example`.

---

## Resources

* Docs: [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)
* Python client: [https://github.com/qdrant/qdrant_client](https://github.com/qdrant/qdrant_client)
* Cookbook: [https://qdrant.tech/documentation/examples/](https://qdrant.tech/documentation/examples/)
* MCP server: [https://github.com/qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant)
* Discord: [https://qdrant.to/discord](https://qdrant.to/discord)
