import lucene
import toml
import streamlit as st
from pybool_ir.experiments.retrieval import LuceneSearcher
from streamlit.components.v1 import html

from config import AppConfig

assert lucene.getVMEnv() or lucene.initVM()
jvm = lucene.getVMEnv()
jvm.attachCurrentThread()

# Config ----------------------------------------------------------------------
with open("config.toml", "r") as f:
    app_config = toml.load(f)
config = AppConfig(app_config["config_file"])
parser = config.parser
indexer = config.indexer
default_query = config.default_query
page_title = config.page_title
render_serp_item = config.render_serp_item
# -----------------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = 0
if "serp_rendered" not in st.session_state:
    st.session_state.serp_rendered = False
results_per_page = 10


def util_search():
    assert lucene.getVMEnv() or lucene.initVM()
    jvm = lucene.getVMEnv()
    jvm.attachCurrentThread()

    with LuceneSearcher(indexer) as searcher:
        try:
            query = parser.parse_lucene(inp_query)
        except Exception as e:
            with cnt_results:
                st.error(str(e))
            return
        result_iterator = searcher.index.search(query)
        result_count = searcher.index.count(query)
        return result_iterator, result_count


def search():
    result_iterator, result_count = util_search()
    if st.session_state.page * results_per_page > result_count:
        with cnt_results:
            st.error("no more results")
        st.session_state.page -= 1
        return
    results = [x for x in result_iterator[st.session_state["page"]:st.session_state["page"] + results_per_page]]
    with cnt_results:
        st.write(f"{result_count} results, page {st.session_state['page'] + 1}")
        for result in results:
            render_serp_item(result)


def first_page():
    st.session_state.serp_rendered = True
    st.session_state.page = 0
    search()


def next_page():
    cnt_results.write("")
    st.session_state.page += 1
    search()


def prev_page():
    cnt_results.write("")
    if st.session_state.page > 0:
        st.session_state.page -= 1
    search()


st.title(page_title)

inp_query = st.text_input("Query", default_query)
btn_search = st.button("Search", on_click=first_page)
cnt_results = st.container()
cnt_results.write("")
col_pages1, col_pages2 = st.columns(2)
with col_pages1:
    if st.session_state.page > 0:
        btn_prev = st.button("previous page", on_click=prev_page, use_container_width=True)
with col_pages2:
    if st.session_state.serp_rendered:
        btn_more = st.button("next page", on_click=next_page, use_container_width=True)

# Scroll to top of page when page changes.
html(
    f"""
    <p>{st.session_state.page}</p>
    <script>
        var input = window.parent.document.querySelectorAll("input[type=text]");
        input[0].focus();
    </script>
    """,
    height=0,
)
