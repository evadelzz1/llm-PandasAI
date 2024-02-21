# from langchain.llms import OpenAI
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai.callbacks import BaseCallback, StdoutCallback
from pandasai.llm import OpenAI
import streamlit as st
import pandas as pd
import os

### https://github.com/amjadraza/pandasai-app/tree/main/pandasai_app


# Sample DataFrame
df = pd.DataFrame({
    "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
    "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
})

# Instantiate a LLM
llm = OpenAI(api_token="YOUR_API_TOKEN")

df = SmartDataframe(df, config={"llm": llm})
df.chat('Which are the 5 happiest countries?')

file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}

def faq():
    ## Use a shorter template to reduce the number of tokens in the prompt
    template = """Create a final answer to the given questions using the provided document excerpts(in no particular order) as references. ALWAYS include a "SOURCES" section in your answer including only the minimal set of sources needed to answer the question. If you are unable to answer the question, simply state that you do not know. Do not attempt to fabricate an answer and leave the SOURCES section empty.

    ---------

    QUESTION: What  is the purpose of ARPA-H?
    =========
    Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
    Source: 1-32
    Content: While we’re at it, let’s make sure every American can get the health care they need. \n\nWe’ve already made historic investments in health care. \n\nWe’ve made it easier for Americans to get the care they need, when they need it. \n\nWe’ve made it easier for Americans to get the treatments they need, when they need them. \n\nWe’ve made it easier for Americans to get the medications they need, when they need them.
    Source: 1-33
    Content: The V.A. is pioneering new ways of linking toxic exposures to disease, already helping  veterans get the care they deserve. \n\nWe need to extend that same care to all Americans. \n\nThat’s why I’m calling on Congress to pass legislation that would establish a national registry of toxic exposures, and provide health care and financial assistance to those affected.
    Source: 1-30
    =========
    FINAL ANSWER: The purpose of ARPA-H is to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more.
    SOURCES: 1-32

    ---------

    QUESTION: {question}
    =========
    {summaries}
    =========
    FINAL ANSWER:"""

    # STUFF_PROMPT = PromptTemplate(
    #     template=template, input_variables=["summaries", "question"]
    # )

def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


@st.cache_data(ttl="1h")
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None


st.set_page_config(page_title="PandasAI ", page_icon="🐼")
st.title("🐼 PandasAI: Chat with CSV")

uploaded_file = st.file_uploader(
    "Upload a Data file",
    type=list(file_formats.keys()),
    help="Various File formats are Support",
    on_change=clear_submit,
)

if uploaded_file:
    df = load_data(uploaded_file)

openai_api_key = st.sidebar.text_input("OpenAI API Key",
                                        type="password",
                                        placeholder="Paste your OpenAI API key here (sk-...)")

with st.sidebar:
        st.markdown("---")
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Upload a csv file with data📄\n"
            "3. A csv file is read as Pandas Dataframe📄\n"
            "4. Ask a question about to make dataframe conversational💬\n"
        )

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖Pandasai App allows you to ask questions about your "
            "csv / dataframe and get accurate answers"
        )
        st.markdown(
            "Pandasai is in active development so is this tool."
            "You can contribute to the project on [GitHub]() "  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("Made by [DR. AMJAD RAZA](https://www.linkedin.com/in/amjadraza/)")
        st.markdown("---")

        faq()

if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is this data about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    #PandasAI OpenAI Model
    llm = OpenAI(api_token=openai_api_key)
    # llm = OpenAI(api_token=openai_api_key)

    sdf = SmartDataframe(df, config = {"llm": llm,
                                        "enable_cache": False,
                                        "conversational": True,
                                        "callback": StdoutCallback()})

    with st.chat_message("assistant"):
        response = sdf.chat(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
        


# Example Questions
# To test out the APP, Below are Sample Questions for Two Data Files

# test_data.csv
# It is tiny samples of Countries with Happiness Index and gdp

# Which are the 5 happiest countries?
# Loan Payments data.csv
# This is sample of datasets with Loan Repayments.

# How many loans are from men that have been paid off?
# User Specific datasets can be tested, would love to have feedbacks and bugs.
