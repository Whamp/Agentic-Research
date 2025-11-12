# AI Task Allocation Guide: A Data-Driven Playbook for Your Subscriptions

This guide provides a detailed breakdown of which AI tool to use for specific development tasks, tailored to your subscriptions and informed by industry model performance leaderboards.

*   **The Core Principle:** Start with the cheapest, most available resource (local models) and escalate to your more powerful, quota-limited resources only when necessary.

---

## 1. Local Models (e.g., Ollama)

*   **Cost:** Free
*   **Strengths:** Instant, private, no usage limits. Perfect for quick, simple tasks.
*   **Weaknesses:** Less powerful reasoning, smaller context windows, lower accuracy on complex tasks.

**Best-Fit Tasks:**
*   **Initial Brainstorming:** "What are some ways I could approach this problem?"
*   **Code "Readability" Checks:** "Can you explain what this block of code does in simple terms?"
*   **Generating Small Snippets:** "Write a Python function that removes duplicates from a list."
*   **Boilerplate Generation:** "Give me the basic structure for a Flask GET endpoint."
*   **Asking Simple Syntax Questions:** "What's the syntax for a list comprehension in Python?"

---

## 2. Z.ai Lite Plan (GLM 4.6)

*   **Quota:** ~120 prompts every 5 hours
*   **Leaderboard Insights:** GLM-4 is a very strong, well-rounded model, competitive with GPT-4 in many areas. It excels at reasoning and following instructions, making it a reliable choice for the majority of your interactive development.
*   **Strengths:** Your "workhorse" model. The high quota makes it perfect for iterative, conversational coding.
*   **Weaknesses:** Ranks slightly behind Gemini 2.5 Pro in the most complex, multi-disciplinary reasoning tasks.

**Best-Fit Tasks:**
*   **Iterative Code Refinement:** "Here's a function. How can I make it more efficient or readable?"
*   **Detailed Code Reviews:** "Please review this pull request for potential bugs, style issues, and improvements." (Its strong reasoning is ideal for this).
*   **Validating Logic:** "I'm thinking of solving the problem this way [describe logic]. Does this make sense? Are there any edge cases I'm missing?"
*   **Writing Unit Tests:** "Please write a set of pytest unit tests for this function."
*   **Translating Code:** "Translate this Java function to Python."
*   **Complex Instruction Following:** When you have a multi-step request that isn't quite complex enough for Gemini Pro, GLM-4 is a great choice.

---

## 3. GitHub Copilot Pro CLI

*   **Cost:** Part of your Copilot Pro subscription
*   **Leaderboard Insights:** The models powering Copilot (variants of GPT-4) are top-tier for code generation. This confirms its role as a specialized "code writer".
*   **Strengths:** Best-in-class for direct code generation and modification.
*   **Weaknesses:** Less suited for open-ended conversation or high-level architectural planning compared to conversational models.

**Best-Fit Tasks:**
*   **"Code-Out" Generation:** "Implement the `calculate_average` function we just discussed."
*   **Generating Documentation:** "Create a docstring for this function."
*   **Explaining Code (`--explain` flag):** A great alternative to local models for quick explanations.
*   **Shell Command Assistance:** "What's the git command to squash the last three commits?"

---

## 4. Google AI Pro Plan (Gemini 2.5 Pro)

*   **Quota:** 100 requests per 24 hours
*   **Leaderboard Insights:** Gemini 2.5 Pro consistently ranks as a top model across the board, with particular strengths in complex reasoning, multi-disciplinary knowledge, and handling difficult, nuanced instructions.
*   **Strengths:** The most powerful and creative model in your toolkit. Your "chief architect" or "senior consultant".
*   **Weaknesses:** The hard daily limit means every request must provide high value.

**Best-Fit Tasks (Budget your 100 requests wisely):**
*   **High-Level System Design:** "I need to design a microservice for user authentication. What are the key components, database schema, and API endpoints I should consider?"
*   **Complex Bug Analysis:** "I have a race condition in my multi-threaded application. Here are the relevant code sections from three different files. Can you help me identify the potential cause?" (Perfect use of its deep reasoning capabilities).
*   **Feature-to-Plan Breakdown:** "My goal is to add real-time notifications to my web app. Break this down into a step-by-step implementation plan, including the frontend and backend changes required."
*   **"Greenfield" Project Planning:** "I'm starting a new project to build a [describe project]. What would be the ideal technology stack, project structure, and development roadmap?"
*   **Creative Problem Solving & Algorithm Design:** "The current approach is too slow. Can you suggest three alternative algorithms to solve this problem and list the pros and cons of each?"
