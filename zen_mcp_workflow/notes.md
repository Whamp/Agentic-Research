# Zen MCP Workflow Notes

This document tracks a simulated workflow to demonstrate how the Zen MCP server can optimize the use of your specific AI subscriptions.

## The Goal

To fix a bug in a Python script by intelligently using four different tiers of AI tools: a local model, the Z.ai Lite plan, the Copilot Pro CLI, and the Google AI Pro plan.

## The Workflow

### Step 1: Initial Analysis with a Local Model (e.g., Ollama)

**Goal:** Get a quick, free first look at the problem.

**Simulated Command:** `claude "use zen with ollama to analyze zen_mcp_workflow/buggy_script.py"`

**Simulated Output:**
"The script calculates an average. The function `calculate_average` seems to have an error where it subtracts 1 from the result, which is not standard."

**Analysis:** The local model successfully identified the likely source of the bug at no cost.

### Step 2: Code Review & Deeper Understanding with Z.ai Lite Plan (GLM 4.6)

**Goal:** Use the generous quota of the Z.ai plan to get a more detailed confirmation of the bug and the required fix.

**Simulated Command:** `clink with zai "A local model suggested a bug in the calculate_average function in buggy_script.py. Please review the function and confirm the issue."`

**Simulated Output:**
"Confirmed. The `- 1` in the return statement is incorrect for a standard average calculation. It should be removed. The rest of the script is fine."

**Analysis:** Your Z.ai plan is perfect for this kind of iterative review. With **~120 prompts every 5 hours**, you can use it frequently for validation and refinement without worrying about hitting a limit.

### Step 3: Targeted Code Generation with Copilot Pro CLI

**Goal:** Use the Copilot CLI's strength in code generation to write the corrected function.

**Simulated Command:** `clink with copilot "Based on the previous analysis, please generate the corrected version of the calculate_average function from buggy_script.py."`

**Simulated Output:**
```python
def calculate_average(numbers):
    """Calculates the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

**Analysis:** We've now used the Copilot Pro CLI via `clink` for what it does best: generating precise code. Note that it even added a docstring and a check for an empty list—a nice improvement.

### Step 4: Final High-Level Review with Gemini Pro

**Goal:** Before committing, use your most powerful model for a final "sanity check", especially if the change were part of a larger, more complex system.

**Simulated Command:** `clink with gemini "The bug in buggy_script.py has been fixed. The new implementation is [paste new function]. Does this look correct and are there any other potential issues or improvements to consider in a real-world application?"`

**Simulated Output:**
"The corrected function is now accurate for calculating the average. For a real-world application, consider the following improvements:
1.  **Type Hinting:** Add type hints for better code clarity and static analysis (`def calculate_average(numbers: list[float]) -> float:`).
2.  **Error Handling:** The check for an empty list is good. You might also consider if the list could contain non-numeric types and add appropriate error handling.
The fix is solid."

**Analysis:** We reserved our premium Gemini Pro access for a high-level, architectural review. We didn't waste its power on the simple bug fix, but instead used it to get strategic advice, which is the best use of a limited, top-tier model.
