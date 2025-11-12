# Copilot API Research

This report summarizes the findings of an investigation into the `ericc-ch/copilot-api` repository.

## Project Overview

The `copilot-api` project is a reverse-engineered proxy for the GitHub Copilot API. Its primary function is to make the Copilot API compatible with tools that are designed to work with OpenAI's and Anthropic's APIs. This allows developers to use GitHub Copilot as a backend for a wide range of AI-powered tools, including Anthropic's Claude Code.

### Key Features

*   **API Compatibility:** Exposes GitHub Copilot as an OpenAI-compatible (`/v1/chat/completions`, `/v1/models`, `/v1/embeddings`) and Anthropic-compatible (`/v1/messages`) API.
*   **Claude Code Integration:** Provides a straightforward way to use GitHub Copilot as the language model for Claude Code.
*   **Usage Dashboard:** Includes a web-based dashboard to monitor Copilot API usage.
*   **Rate Limit Control:** Offers options to manage the rate of API requests to avoid hitting GitHub's rate limits.
*   **Flexible Authentication:** Supports both interactive and token-based authentication.

## Using with Claude Code

There are two primary methods for integrating `copilot-api` with Claude Code:

### 1. Interactive Setup

This is the recommended method for first-time use.

1.  Run the following command in your terminal:
    ```bash
    npx copilot-api@latest start --claude-code
    ```
2.  Follow the interactive prompts to select your desired models.
3.  A command will be copied to your clipboard. Paste and run this command in a new terminal to start Claude Code.

### 2. Manual Configuration

For a more permanent setup, you can use a configuration file.

1.  Create a `.claude` directory in your project's root.
2.  Inside this directory, create a `settings.json` file with the following content:
    ```json
    {
      "env": {
        "ANTHROPIC_BASE_URL": "http://localhost:4141",
        "ANTHROPIC_AUTH_TOKEN": "dummy",
        "ANTHROPIC_MODEL": "gpt-4.1",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "gpt-4.1",
        "ANTHROPIC_SMALL_FAST_MODEL": "gpt-4.1",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-4.1",
        "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
        "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
      },
      "permissions": {
        "deny": [
          "WebSearch"
        ]
      }
    }
    ```
3.  Start the `copilot-api` server. Claude Code will now use it automatically.

## Important Limitation

During testing, it was discovered that the `copilot-api` server cannot be started in a non-interactive environment without a pre-generated GitHub token. The server will hang, waiting for an interactive authentication step.

To use this tool in an automated workflow (such as a CI/CD pipeline or a non-interactive shell), you must first generate a GitHub token using the `auth` command and then provide it to the `start` command using the `--github-token` flag.
