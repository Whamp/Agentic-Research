# AI Task Allocation Guide: A Data-Driven Playbook for Your Subscriptions

This guide provides a detailed breakdown of which AI tool to use for specific development tasks, tailored to your subscriptions and informed by industry model performance leaderboards.

*   **The Core Principle:** Start with your most abundant, powerful resource (unlimited GPT-5 Mini) and escalate to your quota-limited resources only for specialized tasks or when you need a different "perspective."

---

## 1. Copilot Pro (GPT-5 Mini & CLI)

*   **Quota:** Unlimited (for GPT-5 Mini)
*   **Leaderboard Insights:** GPT-5 Mini is a highly capable model, making your "free" tier incredibly powerful. The models powering the CLI (variants of GPT-4) are top-tier for code generation.
*   **Strengths:** This is your **default tool for almost everything**. With unlimited access to a powerful model, you can be much more liberal with your requests.
*   **Weaknesses:** While excellent, it may not match the absolute peak performance of Gemini 2.5 Pro for the most complex, multi-disciplinary reasoning.

**Best-Fit Tasks:**
*   **ALL initial analysis, brainstorming, and code-reading tasks.**
*   **The bulk of your iterative coding:** refining functions, generating boilerplate, asking syntax questions.
*   **Generating documentation and unit tests.**
*   **Direct code generation via the CLI:** "Implement the `calculate_average` function we just discussed."
*   **Explaining code via the CLI:** A powerful and convenient way to understand new code.

**Advanced Integration Note:**
For an even more seamless workflow, you can use the third-party `copilot-api` tool to expose your Copilot subscription as a direct, OpenAI-compatible API. This allows you to add it as a native provider in Zen MCP, enabling direct model calls (e.g., `use model copilot-gpt5-mini`) instead of relying on the `clink` command. See the main `README.md` for more details.

---

## 2. Z.ai Lite Plan (GLM 4.6)

*   **Quota:** ~120 prompts every 5 hours
*   **Leaderboard Insights:** GLM-4 is a very strong, well-rounded model, competitive with other top-tier models. Its different training and architecture mean it can provide a valuable "second opinion."
*   **Strengths:** A high-quality alternative perspective. Use it when GPT-5 Mini gets stuck, or you want to double-check a critical piece of logic.
*   **Weaknesses:** The quota, while generous, is not unlimited.

**Best-Fit Tasks:**
*   **Getting a "Second Opinion":** "GPT-5 Mini suggested this approach. Do you see any flaws or have a better alternative?"
*   **Code Review Cross-Check:** "Please review this critical function. I want to be extra sure it's correct."
*   **Alternative Solutions:** "I'm not happy with the first solution I got. Can you provide a completely different way to solve this problem?"
*   **When one model seems "stuck":** If you're not getting the results you want from your primary tool, switching to another high-quality model is a great strategy.

---

## 3. Google AI Pro Plan (Gemini 2.5 Pro)

*   **Quota:** 100 requests per 24 hours
*   **Leaderboard Insights:** Gemini 2.5 Pro consistently ranks as a top model across the board, with particular strengths in complex reasoning, multi-disciplinary knowledge, and handling difficult, nuanced instructions.
*   **Strengths:** The most powerful and creative model in your toolkit. Your "chief architect" or "senior consultant" for the most critical tasks.
*   **Weaknesses:** The hard daily limit means every request must provide high value.

**Best-Fit Tasks (Budget your 100 requests wisely):**
*   **High-Level System Design:** "I need to design a microservice for user authentication. What are the key components, database schema, and API endpoints I should consider?"
*   **The Most Complex Bug Analysis:** "I have a race condition that neither GPT-5 Mini nor GLM-4 could solve. Here is all the context. Can you find the bug?"
*   **Final Architectural Review:** Before committing to a major design, use one of your premium requests to get a final review from the best model.
*   **"Greenfield" Project Planning:** "I'm starting a new project to build a [describe project]. What would be the ideal technology stack, project structure, and development roadmap?"
*   **Creative Problem Solving & Algorithm Design:** "The current approach is too slow. Can you suggest three alternative algorithms to solve this problem and list the pros and cons of each?"
