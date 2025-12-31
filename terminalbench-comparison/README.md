# TerminalBench 2.0: Droid GPT 5.2 vs. Droid Opus 4.5 Comparison

This report analyzes the task-level performance differences between **Droid GPT 5.2** and **Droid Opus 4.5** on the TerminalBench 2.0 leaderboard.

## Executive Summary

While both models show strong performance across many tasks, there are distinct areas where one outperforms the other.

*   **Droid GPT 5.2** excels in:
    *   **Scientific Computing:** Significantly better at `adaptive-rejection-sampler` (+80%) and `protein-assembly` (+80%).
    *   **Security (Web/Network):** Better at `break-filter-js-from-html` (+60%).
    *   **System Administration (Mail/Network):** Better at `mailman` (+60%).
    *   **Games:** Better at `chess-best-move` (+60%).
    *   **Data Science (Stan/R):** Better at `rstan-to-pystan` (+40%) and `sparql-university` (+40%).

*   **Droid Opus 4.5** excels in:
    *   **Data Science (Bayesian/MCMC):** massively outperforms in `mcmc-sampling-stan` (+100%, GPT 5.2 failed completely).
    *   **Low-Level System Engineering:** Better at `extract-elf` (+80%) and `polyglot-rust-c` (+60%).
    *   **Complex File Operations:** Better at `circuit-fibsqrt` (+60%).
    *   **Legacy Systems:** Better at `install-windows-3.11` (+60%).

## Detailed Analysis by Category

### Scientific Computing
GPT 5.2 appears to have a stronger grasp on certain scientific computing tasks, particularly those involving R and specific biological assembly tasks (`protein-assembly`). However, Opus 4.5 completely dominates the `mcmc-sampling-stan` task, suggesting it might handle Stan/Bayesian modeling much better when MCMC sampling is involved.

### System Administration & Engineering
The models trade blows here. GPT 5.2 is better at setting up a mail server (`mailman`), while Opus 4.5 is better at emulating legacy environments (`install-windows-3.11`) and handling low-level binary extraction (`extract-elf`).

### Coding & Debugging
Both models are generally strong, but Opus 4.5 shows an edge in "polyglot" tasks (`polyglot-rust-c`) and complex logic simulation (`circuit-fibsqrt`). GPT 5.2 shows a surprising advantage in `cancel-async-tasks`, indicating it might handle Python async patterns better in this specific harness.

### Data Science & Querying
GPT 5.2 performs better on `sparql-university`, indicating potentially better knowledge graph/SPARQL capabilities. Opus 4.5 is superior in `mcmc-sampling-stan`.

## Tool Usage

A tool `compare_tbench.py` has been created to perform this comparison for any two models/harnesses on the leaderboard.

### Usage

```bash
python3 compare_tbench.py <URL1> <URL2> --name1 "Model Name 1" --name2 "Model Name 2"
```

**Example:**

```bash
python3 compare_tbench.py \
  "https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/gpt-5.2%40openai" \
  "https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/claude-opus-4-5-20251101%40anthropic" \
  --name1 "Droid GPT 5.2" \
  --name2 "Droid Opus 4.5"
```

The tool scrapes the leaderboard pages for detailed task performance and the registry for task metadata (Category, Difficulty), then outputs a Markdown table comparing the success rates.
