import streamlit as st
import sqlite3
import json
import pandas as pd
import os
import agent

DB_PATH = os.path.join("data", "articles.db")

def load_articles():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM articles ORDER BY processed_date DESC", conn
    )
    conn.close()
    return df

def threat_color(level):
    return {
        "High": "#ff4b4b",
        "Medium": "#ffa500",
        "Low": "#29b6f6",
        "Info": "#6c757d",
    }.get(level, "#6c757d")

def main():
    st.set_page_config(page_title="Cyber‑Geopolitical Intel", layout="wide")
    st.title("🛡️ Cyber‑Geopolitical Intel Dashboard")
    st.markdown("*AI‑powered summaries of cybersecurity and geopolitical news.*")

    # Attempt to load data
    with st.sidebar:
        if st.button("🔄 Fetch & Analyze New Articles (Manual)"):
            with st.spinner("Processing feeds..."):
                import agent  # import is fine here; move to top for cleanliness
                agent.fetch_and_process()
            st.success("Done. Refresh the page to see updated data.")
            st.rerun()
    try:
        df = load_articles()
    except Exception:
        st.warning("Database not found. Run `agent.py` first to ingest some news.")
        return

    if df.empty:
        st.info("No articles processed yet. Fetching happens automatically on container start.")
        return

    # --- Filters ---
    col1, col2 = st.columns(2)
    with col1:
        threats = ["High", "Medium", "Low", "Info"]
        selected_threats = st.multiselect("Threat Level", threats, default=threats)
    with col2:
        sources = df["source"].unique().tolist()
        selected_sources = st.multiselect("Source", sources, default=sources)

    filtered = df[
        df["threat_level"].isin(selected_threats)
        & df["source"].isin(selected_sources)
    ]

    # --- Display Cards ---
    for _, row in filtered.iterrows():
        color = threat_color(row["threat_level"])
        entities = json.loads(row["entities"]) if row["entities"] else []
        entities_str = ", ".join(entities) if entities else "None"

        card_html = f"""
        <div style="border-left: 5px solid {color}; padding: 1rem;
                    margin-bottom: 1rem; background-color: #f8f9fa;
                    border-radius: 5px;">
            <h4>{row['title']}</h4>
            <p>
                <strong>Source:</strong> {row['source']} &nbsp;|&nbsp;
                <strong>Threat:</strong> <span style="color:{color}; font-weight:bold;">
                {row['threat_level']}</span> &nbsp;|&nbsp;
                <strong>Published:</strong> {row['published']}
            </p>
            <p>{row['summary']}</p>
            <p><strong>Entities:</strong> {entities_str}</p>
            <p><strong>Geopolitical Impact:</strong> {row['geopolitical_impact']}</p>
            <a href="{row['link']}" target="_blank">Read original →</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
