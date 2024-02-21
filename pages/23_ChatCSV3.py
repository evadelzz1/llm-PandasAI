import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, time

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib

# matplotlib.use('TkAgg')
matplotlib.use('Qt5Agg')

def main():
    OPENAI_API_KEY = st.session_state.openai_api_key

    st.set_page_config(
        page_title="ChatCSV3",
        page_icon="",
        layout="wide"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        I'm a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)

    st.title("Prompt-driven Analysis with PandasAI")

    st.write("PandasAI, OpenAI and Streamlit - Analyzing File Uploads with User Prompts [ChatCSV](https://www.youtube.com/watch?v=oSC2U2iuMRg)")
 
    uploaded_file = st.file_uploader(
        "Choose a CSV file. This should be in long format (one datapoint per row).",
        type="csv",
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("mean of Fare : " + str(df['Fare'].mean()))
        st.write(df.head(3))

        prompt = st.text_input(
            "Question : ",
            value="Plot the survival counts for males and females",
            # value="What was the average fare price?",
            type="default"
        )
        
        if st.button("Generate"):
            with st.spinner("PandasAI is generating an answer, please wait..."):
                if prompt:
                    llm = OpenAI(api_token=OPENAI_API_KEY)
                    pandas_ai = PandasAI(llm)
                    response = pandas_ai.run(df, prompt=prompt)
                    st.write(response)
                else:
                    st.warning("Please enter a prompt.")

        if st.button("Generate2"):
            with st.spinner("PandasAI is generating an answer, please wait..."):
                if prompt:
                    llm = OpenAI(api_token=OPENAI_API_KEY)
                    pandas_ai = PandasAI(llm)
                    response = pandas_ai.run(df, prompt=prompt)
                    st.write(response)
                else:
                    st.warning("Please enter a prompt.")
                      
if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()
