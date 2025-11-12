# Maximizing Your AI Subscriptions with the Zen MCP Server

This report provides a tailored strategy for using the Zen MCP server to make the best use of your specific AI subscriptions: the **Google AI Pro plan (100 Gemini 2.5 Pro requests/day)**, the **Z.ai Lite plan (~120 prompts/5 hours)**, and **GitHub Copilot Pro (with CLI access)**. By orchestrating these services, you can create a powerful and cost-effective development workflow.

## Key Benefits of Using Zen MCP

*   **Multi-Model Orchestration:** Zen MCP, especially with its `clink` tool, allows you to seamlessly switch between different AI CLIs. This means you can use a free local model for a first pass, your Z.ai plan for frequent tasks, the Copilot CLI for specific code generation, and carefully budget your Gemini Pro requests.

*   **Context Preservation:** The server maintains the full conversation history across all models and CLIs. When you hand off a task between models, it receives the entire context, saving you time, effort, and token usage.

*   **Cost & Quota Optimization:** By using free local models and the generous quota of your Z.ai Lite plan for the bulk of your work, you can ensure your **100 daily Gemini Pro requests** are reserved for the most critical tasks.

*   **Flexibility and Choice:** You have the freedom to choose the best tool for each specific task, all within one terminal session.

## A Practical, Cost-Saving Workflow Tailored to Your Plans

Here is an effective workflow designed around your specific subscriptions:

1.  **Initial Analysis (Local Model - e.g., Ollama):** For any new task, bug, or query, start with a local model. This costs nothing and is perfect for initial exploration and simple questions.

2.  **Code Review and Iteration (Z.ai Lite Plan - GLM 4.6):** Your Z.ai Lite plan, with its quota of **~120 prompts every 5 hours**, is your workhorse for analysis and refinement.

3.  **Targeted Code Generation (Copilot Pro CLI):** When you need to generate specific code, especially boilerplate or implementing a well-defined function, use the Copilot CLI via `clink`.

4.  **High-Impact Tasks (Google AI Pro Plan - Gemini 2.5 Pro):** Your **100 daily requests** for Gemini 2.5 Pro are your most valuable resource. Budget them for tasks that deliver the most value and require maximum intelligence.

## Detailed Task Allocation Guide

For a more detailed breakdown of which tool to use for specific tasks (e.g., system design vs. unit test generation), please refer to the **[AI Task Allocation Guide](./task_allocation_guide.md)**. This guide is informed by industry model performance leaderboards to help you make the best, data-driven decisions.

## Getting Started

To get started with this workflow, you will need to:

1.  **Install the Zen MCP Server:** Follow the instructions in the [official repository](https://github.com/BeehiveInnovations/zen-mcp-server).

2.  **Configure Your API Keys & CLIs:** Use the `sample_config.md` file in this directory as a template for setting up your `.env` file. Ensure your local environment is configured so that Zen MCP can call the Copilot CLI.

3.  **Follow the Workflow:** Start using this tailored multi-model approach in your daily work. The `notes.md` file in this directory provides a detailed, simulated example of this workflow in action.

By using Zen MCP to orchestrate your AI subscriptions this way, you can leverage the unique strengths and limits of each plan to create a highly efficient and economical development process.
