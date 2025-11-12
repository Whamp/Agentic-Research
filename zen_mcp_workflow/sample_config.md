# Sample Zen MCP Server Configuration

This file provides a sample configuration to help you get started with the Zen MCP server.

## 1. `.env` File

Create a file named `.env` in the root of the `zen-mcp-server` directory and add the following content. Be sure to replace the placeholder values with your actual API keys.

```bash
# -----------------------------------------------------------------------------
# Zen MCP Server Configuration
# -----------------------------------------------------------------------------

# --- Provider API Keys -------------------------------------------------------
# Add your API keys here. Zen will activate any provider with a valid key.

# Google Gemini
GEMINI_API_KEY="your-gemini-api-key"

# Z.ai (replace with the correct environment variable for your GLM 4.6 plan)
ZAI_API_KEY="your-zai-api-key"

# --- Tool Configuration ------------------------------------------------------
# A comma-separated list of tools to disable. Leave empty to enable all tools.
# For cost-saving, you might disable tools you don't use often.
DISABLED_TOOLS="analyze,refactor,testgen,secaudit,docgen,tracer"

# --- Model Configuration -----------------------------------------------------
# Set the default model for Zen to use. "auto" is a good choice to start with.
DEFAULT_MODEL="auto"

# -----------------------------------------------------------------------------
```

## 2. Claude Code `settings.json`

If you are using Claude Code, you can add the following to your `~/.claude/settings.json` file to integrate the Zen MCP server:

```json
{
  "mcpServers": {
    "zen": {
      "command": "bash",
      "args": ["-c", "./run-server.sh"],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin:~/.local/bin"
      }
    }
  }
}
```

**Note:** This assumes you are running Claude Code from a terminal that has the `zen-mcp-server` directory as its working directory. Adjust the `args` as needed for your setup.
