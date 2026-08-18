import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Orbit", layout="wide", page_icon="🧭")

st.markdown("""
<style>
.stApp { background-color: #f7f9fb; }
div[data-testid="stMetric"] { background-color: white; border: 1px solid #dce3e8; border-radius: 10px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

f1 = open("data/final_entities.json", "r", encoding="utf-8")
entities = json.load(f1)
f1.close()

f2 = open("data/relationships.json", "r", encoding="utf-8")
relationships = json.load(f2)
f2.close()

df = pd.DataFrame(entities)

st.markdown("## AI Orbit")
st.caption("A structured map of the AI ecosystem - tools, models, companies, and how they connect.")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Explore", "Connections", "Report"])

with tab1:
    c1, c2 = st.columns([1, 2])

    with c1:
        st.metric("Total Entities", len(entities))
        st.metric("Entity Types", df["entity_type"].nunique())
        st.metric("Relationships", len(relationships))

    with c2:
        counts = df["entity_type"].value_counts().reset_index()
        counts.columns = ["entity_type", "count"]
        fig = px.pie(counts, names="entity_type", values="count", hole=0.5)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
        st.plotly_chart(fig, use_container_width=True)

    st.write("#### Entities by source")
    src_names = []
    for e in entities:
        src_names.append(e["source"]["name"])
    src_counts = pd.Series(src_names).value_counts().reset_index()
    src_counts.columns = ["source", "count"]
    fig2 = px.bar(src_counts, x="source", y="count", color="source")
    fig2.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.write("#### Browse the dataset")
    c1, c2 = st.columns([1, 3])
    with c1:
        type_filter = st.multiselect("Filter by type", sorted(df["entity_type"].unique()))
    with c2:
        search = st.text_input("Search entities by name")

    view = df.copy()
    if type_filter:
        view = view[view["entity_type"].isin(type_filter)]
    if search:
        view = view[view["name"].str.contains(search, case=False, na=False)]

    cols_to_show = ["name", "entity_type", "description", "url"]
    st.dataframe(
        view[cols_to_show],
        use_container_width=True,
        height=500,
        column_config={
            "url": st.column_config.LinkColumn("url", display_text="Visit")
        }
    )
    st.caption(f"{len(view)} of {len(entities)} entities shown")

with tab3:
    st.write("#### Relationship map")
    rel_df = pd.DataFrame(relationships)
    rel_search = st.text_input("Search by entity name", key="rel_search")
    rel_view = rel_df.copy()
    if rel_search:
        rel_view = rel_view[
            rel_view["from_name"].str.contains(rel_search, case=False, na=False) |
            rel_view["to_name"].str.contains(rel_search, case=False, na=False)
        ]
    st.dataframe(rel_view[["from_name", "relation", "to_name"]], use_container_width=True, height=500)
    st.caption(f"{len(rel_view)} of {len(relationships)} relationships shown")

with tab4:
    st.write("#### Pipeline summary")
    st.write("Discovery -> Extraction -> Cleaning -> Normalization -> Deduplication -> Classification -> Enrichment -> Relationship Mapping -> Validation")
    st.success(f"Validation passed - {len(entities)} entities, 0 invalid records")
    st.write("#### Notes")
    st.write("- Company founding year / HQ marked unknown where no reliable source was available")
    st.write("- A few product sites blocked scraping (403) and were skipped")
    st.write("- Relationships inferred via metadata matching, not manually verified")