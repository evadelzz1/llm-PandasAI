import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, time

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

def main():
    OPENAI_API_KEY = st.session_state.openai_api_key

    st.set_page_config(
        page_title="PandasAI",
        page_icon="",
        layout="wide"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        :orange[**Daniel**] is a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)
        
    st.title("Pandas-AI Streamlit Apps 1st")

    # st.write("A demo interface for [PandasAI](https://github.com/gventuri/pandas-ai)")

    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'prompt_history' not in st.session_state:
        st.session_state.prompt_history = []

    # if "openai_api_key" in st.session_state:
    if st.session_state.df is None:
        uploaded_file = st.file_uploader(
            "Choose a CSV file. This should be in long format (one datapoint per row). :red[(titanic.csv)]",
            type="csv",
        )
        if uploaded_file is not None:

            col1, col2 = st.columns([1,1])

            with col1:
                st.info("CSV Uploaded Successfully")
                df = pd.read_csv(uploaded_file)
                st.dataframe(df, use_container_width=True)

            with col2:

                st.info("Chat Below")
                        
                with st.form("Question"):
                    question = st.text_input(
                        "Question : ",
                        value="What is the average age of passengers?",
                        type="default"
                    )
                    
                    submitted = st.form_submit_button("Generate")
                    if submitted:
                        with st.spinner("PandasAI is generating an answer, please wait..."):
                            st.info("Your Query: "+question)
                            try:
                                llm = OpenAI(api_token=OPENAI_API_KEY)
                                pandas_ai = PandasAI(llm)
                                result = pandas_ai.run(df, prompt=question)
                                if result is not None:
                                    st.success(result)
                                st.session_state.prompt_history.append(question)
                            except Exception as e:
                                generated_text = None
                                st.error(f"An error occurred: {e}", icon="🚨")

    st.subheader("Prompt history:")
    st.write(st.session_state.prompt_history)

    if st.button("Clear"):
        st.session_state.prompt_history = []
        st.session_state.df = None
        st.experimental_rerun()
        
if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()