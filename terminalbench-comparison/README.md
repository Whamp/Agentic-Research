# TerminalBench 2.0 Comparison Dashboard

This project provides tools to analyze and compare AI model performance on the TerminalBench 2.0 leaderboard.

## Features

-   **Dashboard:** An interactive web app (`dashboard.py`) to visualize comparisons.
-   **CLI Tool:** A script (`compare_tbench.py`) for quick command-line comparisons.
-   **Library:** Reusable scraping logic in `tbench_lib.py`.

## Quick Start (Dashboard)

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Dashboard:**
    ```bash
    streamlit run dashboard.py
    ```

3.  **Usage:**
    -   **Load Runs:**
        -   Paste a leaderboard URL into the sidebar input and click "Load Run".
        -   Or use the "Load Top 5 Models" button to quickly fetch data from the leaderboard.
    -   **Settings:**
        -   Toggle **"Exclude Impossible Tasks"** to remove tasks where all loaded agents have a 0% success rate, ensuring a fairer comparison on solvable problems.
    -   **Overview Tab:** View global performance charts and category breakdowns.
    -   **Comparison Tab:** Select a "Baseline" and "Challenger" to see the performance delta and tasks with changed outcomes.
    -   **Recommendations Tab:** Select categories (e.g., "scientific-computing") to get a ranked list of the best agents/models for that domain.

## Analysis: Droid vs. Terminus (Opus 4.5)

Based on the automated analysis using the dashboard logic:

When comparing **Droid** (Challenger) against the baseline **Terminus** agent, both using **Claude Opus 4.5**:

*   **Overall:** Droid changes the outcome of 40 tasks compared to Terminus.
*   **Droid Advantages:**
    *   **Polyglot/System Engineering:** Droid massively improves `polyglot-rust-c` (+80%), suggesting better handling of multi-language compilation environments.
    *   **Complex Configuration:** Significant gains in `configure-git-webserver` (+60%) and `build-cython-ext` (+60%).
    *   **Data Querying:** Droid shows a strong advantage (+40% avg delta) in this category.
*   **Droid Weaknesses (Terminus wins):**
    *   **Security Exploitation:** Droid completely fails `break-filter-js-from-html` (-100%) where Terminus succeeds.
    *   **Model Training Recovery:** Droid fails `pytorch-model-recovery` (-100%).
    *   **Scientific Pipelines:** Droid struggles with `dna-assembly` (-40%) compared to Terminus.

This suggests **Droid** is a more capable "SysAdmin/DevOps" agent (better at compiling, configuring servers, and query languages), while **Terminus** might have better specific tooling or sandboxing for security exploits and ML training workflows.

## Previous Analysis: Droid GPT 5.2 vs Opus 4.5

See the generated report in `analysis_data.md` (or run the CLI tool) for the comparison between models within the Droid harness.
