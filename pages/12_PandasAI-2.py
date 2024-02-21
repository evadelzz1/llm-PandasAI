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
        page_icon="🧠",
        layout="centered"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        :orange[**Daniel**] is a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)
        
    st.title("Pandas-AI Streamlit Apps 2nd")

    # st.write("A demo interface for [PandasAI](https://github.com/gventuri/pandas-ai)")

    if 'df' not in st.session_state:
        st.session_state.df = None
                
    # if "openai_api_key" in st.session_state:
    if st.session_state.df is None:
        st.session_state.prompt_history = []
        st.session_state.df = None
        uploaded_file = st.file_uploader(
            "Choose a CSV file. This should be in long format (one datapoint per row). :red[(iris.csv)]",
            type="csv",
        )
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df

    with st.form("Question"):
        question = st.text_input(
            "Question : ",
            value="Find the average sepal.length",
            type="default"
        )
        
        submitted = st.form_submit_button("Generate")
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=OPENAI_API_KEY)
                pandas_ai = PandasAI(llm)
                x = pandas_ai.run(st.session_state.df, prompt=question)

                if os.path.isfile('temp_chart.png'):
                    im = plt.imread('temp_chart.png')
                    st.image(im)
                    os.remove('temp_chart.png')

                if x is not None:
                    # st.write(x)
                    st.info(x)
                st.session_state.prompt_history.append(question)

        # initialized = st.form_submit_button("initialized")
        # if initialized:
        #     st.session_state.df = None
        #     st.rerun()
        
            
    if st.session_state.df is not None:
        st.subheader("Current dataframe:")
        st.write(st.session_state.df)

    st.subheader("Prompt history:")
    st.write(st.session_state.prompt_history)

    if st.button("Clear"):
        st.session_state.prompt_history = []
        st.session_state.df = None

if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()



                