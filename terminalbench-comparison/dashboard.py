import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tbench_lib import fetch_leaderboard_data, fetch_registry_metadata, fetch_leaderboard_list

# Set page config
st.set_page_config(page_title="TerminalBench 2.0 Comparison Dashboard", layout="wide")

st.title("TerminalBench 2.0 Comparison Dashboard")

# Initialize session state for runs
if 'runs' not in st.session_state:
    st.session_state.runs = {}

# Sidebar for inputs
with st.sidebar:
    st.header("Add Run")
    run_url = st.text_input("Leaderboard URL", placeholder="https://www.tbench.ai/leaderboard/...")

    if st.button("Load Run"):
        if run_url:
            with st.spinner("Fetching data..."):
                data = fetch_leaderboard_data(run_url)
                if data:
                    meta = data['metadata']
                    # Construct a unique name
                    run_name = f"{meta['agentName']} / {meta['modelName']}"
                    # Fallback if unknown
                    if "Unknown" in run_name:
                         parts = run_url.split('/')
                         if len(parts) >= 3:
                             run_name = f"{parts[-3]} / {parts[-1].split('%40')[0]}"

                    st.session_state.runs[run_name] = data
                    st.success(f"Loaded: {run_name}")
                else:
                    st.error("Failed to fetch data. Check URL.")

    st.divider()

    st.header("Quick Load")
    if st.button("Load Top 5 Models"):
        with st.spinner("Fetching top models from leaderboard..."):
            top_models = fetch_leaderboard_list()
            if top_models:
                # Take top 5
                for entry in top_models[:5]:
                    if entry['name'] not in st.session_state.runs:
                        st.write(f"Fetching {entry['name']}...")
                        data = fetch_leaderboard_data(entry['url'])
                        if data:
                            st.session_state.runs[entry['name']] = data
                st.success("Loaded top 5 models.")
                st.rerun()
            else:
                st.error("Could not fetch leaderboard list.")

    st.divider()
    st.subheader("Settings")
    exclude_impossible = st.checkbox("Exclude Impossible Tasks", value=False, help="Remove tasks where all loaded agents have 0% success rate.")

    st.divider()
    st.subheader("Loaded Runs")
    if st.session_state.runs:
        for name in st.session_state.runs.keys():
            st.text(f"• {name}")

        if st.button("Clear All"):
            st.session_state.runs = {}
            st.rerun()
    else:
        st.info("No runs loaded.")

# Main content
if not st.session_state.runs:
    st.info("Please load at least one run from the sidebar to view the dashboard.")
    st.markdown("""
    **Example URLs:**
    - Droid GPT 5.2: `https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/gpt-5.2%40openai`
    - Droid Opus 4.5: `https://www.tbench.ai/leaderboard/terminal-bench/2.0/Factory%20Droid/unknown/claude-opus-4-5-20251101%40anthropic`

    **Or use the 'Load Top 5 Models' button in the sidebar.**
    """)
else:
    # Fetch Registry Metadata (cached ideally, but here just once per reload is fine)
    if 'registry_meta' not in st.session_state:
         with st.spinner("Fetching Registry Metadata..."):
             st.session_state.registry_meta = fetch_registry_metadata()

    reg_meta = st.session_state.registry_meta

    # Process Data into DataFrame
    # Rows: Tasks
    # Cols: Run Names (Success Rates) + Metadata

    # Get all unique tasks
    all_tasks = set()
    for run_data in st.session_state.runs.values():
        all_tasks.update(run_data['results'].keys())

    data_rows = []
    run_cols = list(st.session_state.runs.keys())

    for task in all_tasks:
        row = {'Task': task}
        # Add metadata
        meta = reg_meta.get(task, {'category': 'Unknown', 'difficulty': 'Unknown'})
        row['Category'] = meta['category']
        row['Difficulty'] = meta['difficulty']

        # Add run data
        for run_name in run_cols:
            run_data = st.session_state.runs[run_name]
            res = run_data['results'].get(task)
            if res:
                row[run_name] = res['avgResolutionRate'] * 100 # percentage
            else:
                row[run_name] = 0.0 # Assume 0 if missing or not run?

        data_rows.append(row)

    df = pd.DataFrame(data_rows)

    # Filter Impossible Tasks if requested
    if exclude_impossible:
        # Check max value across run columns
        # If max is 0, it means all are 0
        df = df[df[run_cols].max(axis=1) > 0]
        st.info(f"Filtered out tasks with 0% success across all agents. Remaining tasks: {len(df)}")

    # --- Visualization Section ---

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Detailed Comparison", "Recommendations", "Raw Data"])

    with tab1:
        st.subheader("Performance Overview")

        # 1. Total Average Resolution Rate
        # Calculate mean of all tasks for each run
        if not df.empty:
            avg_scores = df[run_cols].mean().sort_values(ascending=False)

            fig_avg = px.bar(
                x=avg_scores.index,
                y=avg_scores.values,
                labels={'x': 'Run', 'y': 'Average Resolution Rate (%)'},
                title="Global Average Resolution Rate",
                color=avg_scores.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_avg, use_container_width=True)

            # 2. Category Breakdown
            st.subheader("Category Breakdown")
            # Melt for seaborn/plotly style grouping
            df_melt = df.melt(id_vars=['Task', 'Category', 'Difficulty'], value_vars=run_cols, var_name='Run', value_name='Success Rate')

            # Group by Category and Run
            cat_group = df_melt.groupby(['Category', 'Run'])['Success Rate'].mean().reset_index()

            fig_cat = px.bar(
                cat_group,
                x='Category',
                y='Success Rate',
                color='Run',
                barmode='group',
                title="Success Rate by Category"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("No data available after filtering.")

    with tab2:
        st.subheader("Baseline vs Challenger Analysis")

        col1, col2 = st.columns(2)
        with col1:
            baseline = st.selectbox("Select Baseline", options=run_cols, index=0)
        with col2:
            challenger = st.selectbox("Select Challenger", options=run_cols, index=1 if len(run_cols) > 1 else 0)

        if baseline and challenger and baseline != challenger and not df.empty:
            # Calculate Delta
            df['Delta'] = df[challenger] - df[baseline]

            # Filter for significant differences
            # Show only tasks where delta != 0
            df_diff = df[df['Delta'] != 0].copy()
            df_diff = df_diff.sort_values(by='Delta', ascending=False)

            st.metric(
                label=f"Average Improvement ({challenger} vs {baseline})",
                value=f"{df[challenger].mean() - df[baseline].mean():.2f}%"
            )

            # Chart of Deltas
            if not df_diff.empty:
                fig_delta = px.bar(
                    df_diff,
                    x='Delta',
                    y='Task',
                    orientation='h',
                    color='Delta',
                    hover_data=['Category'],
                    title=f"Performance Delta by Task ({challenger} - {baseline})",
                    height=max(500, len(df_diff) * 20) # Dynamic height
                )
                st.plotly_chart(fig_delta, use_container_width=True)

                st.write("### Tasks with Changed Outcomes")
                st.dataframe(
                    df_diff[['Task', 'Category', 'Difficulty', baseline, challenger, 'Delta']]
                    .style.format({baseline: "{:.0f}%", challenger: "{:.0f}%", 'Delta': "{:+.0f}%"})
                    .background_gradient(subset=['Delta'], cmap='RdYlGn')
                )
            else:
                st.info("No performance differences found between these runs.")

        elif df.empty:
             st.warning("No data available.")
        else:
            st.info("Select two different runs to compare.")

    with tab3:
        st.subheader("Task Recommendations")
        st.markdown("Select one or more categories to find the best performing agent+model combination for your specific workflow.")

        if not df.empty:
            # Get unique categories
            categories = sorted(df['Category'].dropna().unique())

            selected_cats = st.multiselect("Select Categories", options=categories)

            if selected_cats:
                # Filter Dataframe
                df_filtered = df[df['Category'].isin(selected_cats)]

                if not df_filtered.empty:
                    # Calculate mean score for each run on these tasks
                    scores = df_filtered[run_cols].mean().sort_values(ascending=False)

                    # Display Rank Table
                    rank_df = pd.DataFrame({
                        'Rank': range(1, len(scores) + 1),
                        'Agent / Model': scores.index,
                        'Score': scores.values
                    })

                    st.write(f"### Ranking for {', '.join(selected_cats)}")
                    st.dataframe(rank_df.style.format({'Score': "{:.1f}%"}))

                    if not rank_df.empty:
                        best_model = rank_df.iloc[0]['Agent / Model']
                        st.success(f"**Recommendation:** The best performing model for these categories is **{best_model}**.")

                    # Show breakdown by task for the best model
                    with st.expander("See Detailed Task Breakdown"):
                        st.dataframe(df_filtered[['Task', 'Category', 'Difficulty'] + run_cols])
                else:
                    st.warning("No tasks found for the selected categories.")
            else:
                st.info("Please select at least one category to see recommendations.")
        else:
             st.warning("No data available.")

    with tab4:
        st.subheader("Full Task Data")
        st.dataframe(df)
