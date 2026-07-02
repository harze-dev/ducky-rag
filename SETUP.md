# Ducky Setup Guide

This guide explains how to configure Ducky with an OpenAI API key and local embeddings.

## Quick Setup

1. **Get your OpenAI API key** from your OpenAI account.

2. **Run the setup tool**:
   ```bash
   uv sync
   uv run python ducky-setup.py --api-key sk-...
   ```

3. **Start Ducky**:
   ```bash
   uv run streamlit run 🏠_Home.py
   ```

That's it! Ducky will now use OpenAI for chat and `sentence-transformers` locally for embeddings.

## Setup Tool Options

### Basic Usage
```bash
uv run python ducky-setup.py --api-key <your_openai_api_key>
```

### Choose a Model
```bash
uv run python ducky-setup.py --api-key sk-... --model gpt-5.5
```
If you omit `--model`, the app will default to `gpt-5.5`.

### Help
```bash
uv run python ducky-setup.py --help
```

## What the Setup Tool Does

1. **Backs up** your existing `.env` file (if any)
1. **Creates** a new `.env` file with:
   - `OPENAI_API_KEY=<your_openai_api_key>`
   - `OPENAI_API_MODEL=<your_model>`
   - optional `OPENAI_API_BASE_URL` if you want a non-default endpoint

## Benefits

- **Simple**: Uses your normal OpenAI API key
- **Current**: Defaults to `gpt-5.5` unless you override it
- **Local Embeddings**: Uses local sentence-transformers models for fast, offline semantic search
- **Simple**: One-time setup, then Ducky works normally


## Troubleshooting

### API Key Problems
- **Check the key is valid** and has access to the chosen model
- **Make sure `.env` exists** in the project root
- **Try a different model** if your account does not have access to the default

### Ducky Won't Start
- **Make sure you ran the setup tool successfully**
- **Check the `.env` file exists** and has the correct format
- **Run setup again** if needed

## Security Notes

- **Never share your API key** - it provides access to your OpenAI account
- **Backup files are created locally** - they contain your previous config
