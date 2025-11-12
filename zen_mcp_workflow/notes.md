# Zen MCP Workflow Notes

This document tracks the steps taken to demonstrate the Zen MCP server's capabilities in optimizing AI model usage.

## Initial Exploration

- Reviewed the `zen-mcp-server` GitHub repository to understand its features.
- Identified the key concept of using multiple AI models in a single workflow.
- Noted the `clink` tool for connecting different CLIs.
- Listed the supported AI providers: Gemini, OpenAI, Azure, Grok, Ollama, OpenRouter, and more.
- Understood the importance of the `.env` file for API key configuration.
- Located the `run-server.sh` script for easy setup.

## Multi-Model Workflow Demonstration

### Step 1: Initial Analysis with a Local Model (e.g., Ollama)

**Goal:** Perform a quick, low-cost analysis to catch obvious issues.

**Simulated Command:** `claude "use zen with ollama to analyze zen_mcp_workflow/buggy_script.py"`

**Simulated Output:**
"The script calculates the average of a list of numbers. The function `calculate_average` seems to have a mathematical operation that might be incorrect. It subtracts 1 from the result, which is unusual for a standard average calculation."

**Analysis:** The local model was able to flag a potential issue, but it didn't provide a definitive solution. This is a good first pass, and it cost nothing in API usage.

### Step 2: Deep Dive with Gemini Pro

**Goal:** Get a more detailed analysis and a specific fix from a more powerful model.

**Simulated Command:** `clink with gemini "The previous analysis suggested a bug in calculate_average. Review the function in zen_mcp_workflow/buggy_script.py and provide a fix."`

**Simulated Output:**
"The bug is in the return statement of the `calculate_average` function. The `- 1` is erroneous. The corrected function should be:
```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
```
"

**Analysis:** Gemini Pro, with its larger context window and more advanced reasoning, was able to pinpoint the exact error and provide the corrected code. This is a good use of a limited, high-quality model subscription. The `clink` command demonstrates how to seamlessly hand off the context from the initial analysis to the next model.

### Step 3: Final Code Review with GLM 4.6

**Goal:** Get a second opinion on the fix to ensure its quality before committing.

**Simulated Command:** `claude "use zen with glm4 to review the proposed fix for zen_mcp_workflow/buggy_script.py. The fix is to remove the '- 1'. Is this correct?"`

**Simulated Output:**
"Yes, the proposed fix is correct. Removing the `- 1` will result in the function calculating the correct average. The code is now logically sound."

**Analysis:** The GLM 4.6 model confirms the fix, giving us confidence in the solution. This multi-model review process helps prevent errors and ensures a higher quality result.

## Cost-Saving Strategies

Here's how to make the best use of your limited subscriptions with Zen MCP:

1.  **Local Models First:** Always start with a local model (like one running on Ollama) for initial analysis, brainstorming, and simple code generation. Since these models run on your machine, they are completely free to use. This saves your paid API calls for more complex tasks.

2.  **Gemini Pro for Heavy Lifting:** Use your limited Gemini Pro subscription for tasks that require deep reasoning, extensive context, or a high degree of accuracy. This includes complex bug analysis, architectural planning, and generating large blocks of code. By using local models for the initial steps, you ensure that you're only using your most powerful model when you truly need it.

3.  **GLM 4.6 for Specialized Tasks:** The Z.ai Code plan GLM 4.6 is best used for code reviews, getting second opinions, and validating fixes. Its strengths in code analysis make it ideal for these tasks. The Zen MCP's `consensus` tool is perfect for this, allowing you to get feedback from multiple models (like Gemini Pro and GLM 4.6) to make a more informed decision.

4.  **GitHub Copilot for Real-Time Assistance:** Continue to use your Copilot subscription for what it does best: real-time code completion and suggestions directly in your editor. Copilot is an "always-on" assistant, while Zen MCP is your tool for more deliberate, multi-step AI workflows. They complement each other perfectly.

5.  **Zen MCP as the Orchestrator:** The key to this strategy is using Zen MCP to intelligently switch between these models and tools. By preserving context across different models, you avoid having to re-explain the problem, which saves both time and tokens (and therefore, money).
