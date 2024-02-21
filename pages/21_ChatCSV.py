import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, time

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

def chat_with_csv(df, prompt, openai_api_key):
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt)
    print(result)
    return result

def main():
    OPENAI_API_KEY = st.session_state.openai_api_key

    st.set_page_config(
        page_title="ChatCSV",
        page_icon="",
        layout="wide"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        I'm a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)
        
    st.title("ChatCSV powered by LLM")

    st.write("An LLM powered ChatCSV Streamlit app so you can chat with your CSV files. [ChatCSV-Streamlit-App](https://github.com/AIAnytime/ChatCSV-Streamlit-App)")

    input_csv = st.file_uploader("Upload your CSV file. :red[(ChatCSV-2019.csv)]", type=['csv'])

    if input_csv is not None:

        col1, col2 = st.columns([1,1])

        with col1:
            st.info("CSV Uploaded Successfully")
            data = pd.read_csv(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:

            st.info("Chat Below")
            
            input_text = st.text_area("Enter your query:", value="where is the highest score?")

            if input_text is not None:
                if st.button("Chat with CSV"):
                    with st.spinner("PandasAI is generating an answer, please wait..."):
                        st.info("Your Query: "+input_text)
                        result = chat_with_csv(data, input_text, OPENAI_API_KEY)
                        st.success(result)

if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()
