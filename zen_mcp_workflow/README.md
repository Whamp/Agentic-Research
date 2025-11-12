# Maximizing Your AI Subscriptions with the Zen MCP Server

This report provides a tailored strategy for using the Zen MCP server to make the best use of your specific AI subscriptions: **Copilot Pro (unlimited GPT-5 Mini access)**, the **Z.ai Lite plan (~120 prompts/5 hours for GLM 4.6)**, and the **Google AI Pro plan (100 Gemini 2.5 Pro requests/day)**. By orchestrating these services, you can create an incredibly powerful and efficient development workflow.

## A Practical, High-Power Workflow Tailored to Your Plans

Here is an effective workflow designed around your powerful subscriptions:

1.  **Default for Everything (Copilot Pro - GPT-5 Mini):** For any and all tasks, your default starting point is the unlimited GPT-5 Mini. Use it for initial analysis, brainstorming, code generation, refactoring, and documentation.

2.  **Second Opinion & Alternative Approaches (Z.ai Lite Plan - GLM 4.6):** When you want to double-check a critical piece of logic, or if GPT-5 Mini's approach isn't quite right, use one of your **~120 prompts/5 hours** to get a second opinion from GLM 4.6.

3.  **The Final Word & Complex Strategy (Google AI Pro Plan - Gemini 2.5 Pro):** Your **100 daily requests** for Gemini 2.5 Pro are reserved for the most important tasks that require the absolute best performance. Use them for final architectural reviews, solving the most complex bugs, or high-level strategic planning.

## Detailed Task Allocation Guide

For a more detailed breakdown of which tool to use for specific tasks (e.g., system design vs. unit test generation), please refer to the **[AI Task Allocation Guide](./task_allocation_guide.md)**. This guide is informed by industry model performance leaderboards to help you make the best, data-driven decisions.

## Getting Started & Advanced Integration

There are two ways to integrate your Copilot Pro subscription with Zen MCP:

### 1. Standard Method (CLI Chaining)

This is the simplest and recommended starting point.
1.  **Install the Zen MCP Server:** Follow the instructions in the [official repository](https://github.com/BeehiveInnovations/zen-mcp-server).
2.  **Configure Your API Keys & CLIs:** Use the `sample_config.md` file in this directory as a template for setting up your `.env` file for Gemini and Z.ai. Ensure the GitHub Copilot CLI is installed and working in your environment.
3.  **Use `clink`:** Use the `clink with copilot` command within your main CLI to send requests to Copilot.

### 2. Advanced Method (Direct API Integration)

For a more seamless "power-user" setup, you can use the third-party `copilot-api` tool to expose your Copilot subscription as a direct, OpenAI-compatible API. This allows you to add it as a native provider in Zen MCP.

1.  **Set up `copilot-api`:** Follow the instructions on the [copilot-api GitHub repository](https://github.com/ericc-ch/copilot-api) to run it as a local server.
2.  **Configure Zen MCP:** Add your new local Copilot API endpoint to your Zen MCP configuration, likely as a custom OpenAI provider.
3.  **Direct Calls:** You can now make direct calls within Zen MCP (e.g., `use model copilot-gpt5-mini`) without needing to use `clink`.

**Disclaimer:** The `copilot-api` tool is a reverse-engineered, third-party project. Use it at your own risk and be mindful of GitHub's acceptable use policies.

By using Zen MCP to orchestrate your AI subscriptions this way, you can leverage the unique strengths and limits of each plan to create a highly efficient and economical development process.
