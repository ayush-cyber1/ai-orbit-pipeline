import streamlit as st
import json

st.set_page_config(page_title="AI Orbit", layout="wide")

with open("data/final_entities.json", "r", encoding="utf-8") as f:
    entities = json.load(f)

with open("data/relationships.json", "r", encoding="utf-8") as f:
    relationships = json.load(f)

st.title("AI Orbit")
st.caption(f"{len(entities)} entities, {len(relationships)} relationships")

types = sorted(set(e["entity_type"] for e in entities))
selected_type = st.sidebar.selectbox("Entity type", ["All"] + types)

search = st.sidebar.text_input("Search by name")

filtered = entities
if selected_type != "All":
    filtered = [e for e in filtered if e["entity_type"] == selected_type]
if search:
    filtered = [e for e in filtered if search.lower() in e["name"].lower()]

st.write(f"Showing {len(filtered)} entities")

for e in filtered:
    with st.expander(f"{e['name']} ({e['entity_type']})"):
        st.write(e.get("description", ""))
        st.write("Categories:", ", ".join(e.get("categories", [])))
        st.write("Source:", e.get("source", {}).get("name", ""))
        st.write("URL:", e.get("url", ""))

st.sidebar.markdown("---")
st.sidebar.write("Relationships sample")
for r in relationships[:20]:
    st.sidebar.write(f"{r['from_name']} -> {r['relation']} -> {r['to_name']}")