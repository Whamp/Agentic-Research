# Zen MCP Workflow Notes

This document tracks a simulated workflow to demonstrate how the Zen MCP server can optimize the use of your specific AI subscriptions, starting with your most powerful unlimited resource.

## The Goal

To fix a bug in a Python script by intelligently using your suite of AI tools, starting with your unlimited GPT-5 Mini access.

## The Workflow

### Step 1: Initial Analysis & Fix with Copilot Pro (GPT-5 Mini)

**Goal:** Use your unlimited, powerful default tool to solve the problem directly.
**Cost:** 0 quota-limited requests.

**Simulated Command:** `claude "Analyze zen_mcp_workflow/buggy_script.py for bugs and provide a corrected version."`

**Simulated Output:**
"The script has a bug in the `calculate_average` function where it incorrectly subtracts 1 from the result. Here is the corrected version:
```python
def calculate_average(numbers):
    """Calculates the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```
"

**Analysis:** Your unlimited GPT-5 Mini is powerful enough to solve this problem in a single step. For many daily tasks, this will be the only step you need.

### Step 2: Getting a "Second Opinion" with Z.ai Lite Plan (GLM 4.6)

**Goal:** For a critical or complex piece of code, use your Z.ai plan to get a second opinion on the fix.
**Cost:** 0 Gemini Pro requests.

**Simulated Command:** `clink with zai "Copilot suggested the following fix for the buggy script [paste new function]. Do you agree with this fix, and are there any other improvements you would suggest?"`

**Simulated Output:**
"Yes, the fix is correct. The logic is now sound. For production code, you might consider adding type hints to the function signature for better clarity and static analysis."

**Analysis:** With its high quota, the Z.ai plan is the perfect tool for this kind of validation and cross-checking.

### Step 3: Final Architectural Review with Gemini Pro

**Goal:** Spend one of your premium requests for a final, high-value review of how this function fits into a larger system.
**Cost:** 1 Gemini Pro request (out of your 100/day budget).

**Simulated Command:** `clink with gemini "A function to calculate an average was fixed. In the context of a larger data processing pipeline, what are the potential pitfalls or edge cases for a function like this that I should be aware of?"`

**Simulated Output:**
"In a larger pipeline, consider the following:
1.  **Floating Point Precision:** For financial or scientific calculations, standard floats may not be sufficient. Consider using Python's `Decimal` type.
2.  **Large Datasets:** If the list of numbers is very large, calculating the sum in memory could be inefficient. A streaming average algorithm might be more appropriate.
3.  **Error Propagation:** How should a non-numeric value in the input list be handled? The function should have a clear error handling strategy that doesn't disrupt the entire pipeline."

**Analysis:** We spent just **one** of our **100 daily Gemini Pro requests**. We didn't use it to fix the simple bug, but to get high-level, strategic advice that could prevent much more serious issues down the line. This is the optimal use of your most powerful, limited resource.

---
***Advanced Workflow Note:***
*This example uses `clink` to call the Z.ai and Gemini CLIs. For an even more seamless experience, you could configure the third-party `copilot-api` tool to add your Copilot models as a native provider in Zen MCP. This would allow for direct calls (e.g., `use model gemini-2.5-pro`) for all your models from a single interface.*
