from datetime import datetime
import streamlit as st


def render_serp_generic(item):
    st.markdown(f"""**{item["id"]}**""")
    with st.expander("see content"):
        st.write(item["content"])


def render_serp_pubmed(item):
    st.markdown(f"""
        [**{item["title"]}**](https://pubmed.ncbi.nlm.nih.gov/{item["pmid"]}/)                    
        :green[PMID:{item["pmid"]}&nbsp;&nbsp;&nbsp;{item["publication_type"]}&nbsp;&nbsp;&nbsp;{datetime.fromtimestamp(item["date"])}]
        """)
    if "abstract" in item and item["abstract"] is not None:
        with st.expander("see abstract"):
            st.write(item["abstract"])


def render_serp_iranthology(item):
    st.markdown(f"""
    [**{item["title"]}**]({item["url"]})  
    {", ".join([author for author in item.getlist("authors") if "authors" in item and item["authors"] is not None])}  
    :green[{item["venue"]}&nbsp;{item["year"]}]
    """)
    if "abstract" in item and item["abstract"] is not None:
        with st.expander("see abstract"):
            st.write(item["abstract"])


def render_serp_treccovid(item):
    st.markdown(f"""
    **{item["title"]}**  
    :green[{item["doc_id"]}&nbsp;&nbsp;&nbsp;{datetime.fromtimestamp(item["date"])}&nbsp;&nbsp;&nbsp;{item["doi"] if item["doi"] is not None else ""}]
    """)
    if "abstract" in item and item["abstract"] is not None:
        with st.expander("see abstract"):
            st.write(item["abstract"])
