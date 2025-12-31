import streamlit as st
import pandas as pd
import plotly.express as px
from tbench_lib import init_db, save_run_to_db, get_all_runs_from_db, fetch_leaderboard_data, fetch_registry_metadata, fetch_leaderboard_list

# Initialize DB on startup
init_db()

# Set page config
st.set_page_config(page_title="TerminalBench 2.0 Comparison Dashboard", layout="wide")

st.title("TerminalBench 2.0 Comparison Dashboard")

# Initialize session state for runs
if 'runs' not in st.session_state:
    st.session_state.runs = get_all_runs_from_db()

# Sidebar for inputs
with st.sidebar:
    st.header("Add Run")
    run_url = st.text_input("Leaderboard URL", placeholder="https://www.tbench.ai/leaderboard/...")

    if st.button("Load Run"):
        if run_url:
            with st.spinner("Fetching data..."):
                data = fetch_leaderboard_data(run_url)
                if data:
                    if save_run_to_db(run_url, data):
                        st.success(f"Loaded and saved: {data['metadata']['agentName']} / {data['metadata']['modelName']}")
                        # Reload from DB to ensure consistency
                        st.session_state.runs = get_all_runs_from_db()
                    else:
                        st.error("Failed to save to database.")
                else:
                    st.error("Failed to fetch data. Check URL.")

    st.divider()

    st.header("Database Sync")
    if st.button("Sync with Leaderboard"):
        status = st.empty()
        status.info("Fetching leaderboard list...")
        entries = fetch_leaderboard_list()

        if entries:
            progress_bar = st.progress(0)
            count = 0
            for i, entry in enumerate(entries):
                status.text(f"Processing {entry['name']}...")
                data = fetch_leaderboard_data(entry['url'])
                if data:
                    save_run_to_db(entry['url'], data)
                    count += 1
                progress_bar.progress((i + 1) / len(entries))

            st.session_state.runs = get_all_runs_from_db()
            status.success(f"Synced {count} runs from leaderboard.")
            st.rerun()
        else:
            st.error("Could not fetch leaderboard list.")

    st.divider()
    st.subheader("Settings")
    exclude_impossible = st.checkbox("Exclude Impossible Tasks", value=False, help="Remove tasks where all loaded agents have 0% success rate.")

    st.divider()
    st.subheader(f"Loaded Runs ({len(st.session_state.runs)})")

    # Filter runs search
    search_query = st.text_input("Search Runs", "").lower()

    run_keys = sorted(list(st.session_state.runs.keys()))
    if search_query:
        run_keys = [k for k in run_keys if search_query in k.lower()]

    for name in run_keys[:10]: # Show first 10 matches
        st.text(f"• {name}")
    if len(run_keys) > 10:
        st.text(f"... and {len(run_keys) - 10} more")

# Main content
if not st.session_state.runs:
    st.info("No runs loaded in the database. Please use 'Sync with Leaderboard' or load a URL.")
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
        df = df[df[run_cols].max(axis=1) > 0]
        st.info(f"Filtered out tasks with 0% success across all agents. Remaining tasks: {len(df)}")

    # --- Visualization Section ---

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Detailed Comparison", "Recommendations", "Raw Data"])

    with tab1:
        st.subheader("Performance Overview")

        # Filter top N runs for visualization to avoid clutter
        top_n = st.slider("Show Top N Runs", min_value=5, max_value=len(run_cols), value=10)

        if not df.empty:
            avg_scores = df[run_cols].mean().sort_values(ascending=False)
            top_runs = avg_scores.head(top_n).index.tolist()

            fig_avg = px.bar(
                x=top_runs,
                y=avg_scores[top_runs].values,
                labels={'x': 'Run', 'y': 'Average Resolution Rate (%)'},
                title=f"Top {top_n} Agents: Global Average Resolution Rate",
                color=avg_scores[top_runs].values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_avg, use_container_width=True)

            # 2. Category Breakdown
            st.subheader("Category Breakdown (Top 5 Agents)")
            top_5_runs = avg_scores.head(5).index.tolist()

            df_melt = df.melt(id_vars=['Task', 'Category', 'Difficulty'], value_vars=top_5_runs, var_name='Run', value_name='Success Rate')
            cat_group = df_melt.groupby(['Category', 'Run'])['Success Rate'].mean().reset_index()

            fig_cat = px.bar(
                cat_group,
                x='Category',
                y='Success Rate',
                color='Run',
                barmode='group',
                title="Success Rate by Category (Top 5 Agents)"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.warning("No data available.")

    with tab2:
        st.subheader("Baseline vs Challenger Analysis")

        # Default selections to the top 2
        top_2 = df[run_cols].mean().sort_values(ascending=False).head(2).index.tolist()
        idx_base = run_cols.index(top_2[1]) if len(top_2) > 1 and top_2[1] in run_cols else 0
        idx_chall = run_cols.index(top_2[0]) if len(top_2) > 0 and top_2[0] in run_cols else 0

        col1, col2 = st.columns(2)
        with col1:
            baseline = st.selectbox("Select Baseline", options=run_cols, index=idx_base)
        with col2:
            challenger = st.selectbox("Select Challenger", options=run_cols, index=idx_chall)

        if baseline and challenger and baseline != challenger and not df.empty:
            # Calculate Delta
            df['Delta'] = df[challenger] - df[baseline]

            # Filter for significant differences
            df_diff = df[df['Delta'] != 0].copy()
            df_diff = df_diff.sort_values(by='Delta', ascending=False)

            st.metric(
                label=f"Average Improvement ({challenger} vs {baseline})",
                value=f"{df[challenger].mean() - df[baseline].mean():.2f}%"
            )

            if not df_diff.empty:
                fig_delta = px.bar(
                    df_diff,
                    x='Delta',
                    y='Task',
                    orientation='h',
                    color='Delta',
                    hover_data=['Category'],
                    title=f"Performance Delta by Task ({challenger} - {baseline})",
                    height=max(500, len(df_diff) * 20)
                )
                st.plotly_chart(fig_delta, use_container_width=True)

                st.write("### Tasks with Changed Outcomes")
                st.dataframe(
                    df_diff[['Task', 'Category', 'Difficulty', baseline, challenger, 'Delta']]
                    .style.format({baseline: "{:.0f}%", challenger: "{:.0f}%", 'Delta': "{:+.0f}%"})
                    # .background_gradient(subset=['Delta'], cmap='RdYlGn') # Disabled due to matplotlib dep issue on some envs
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
            categories = sorted(df['Category'].dropna().unique())
            selected_cats = st.multiselect("Select Categories", options=categories)

            if selected_cats:
                df_filtered = df[df['Category'].isin(selected_cats)]

                if not df_filtered.empty:
                    scores = df_filtered[run_cols].mean().sort_values(ascending=False)

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
