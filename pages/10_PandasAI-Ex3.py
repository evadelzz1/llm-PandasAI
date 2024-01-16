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
        
    st.title("pandas-ai streamlit interface")

    st.write("A demo interface for [PandasAI](https://devocean.sk.com/blog/techBoardDetail.do?ID=165102&boardType=techBlog)")

    df = pd.read_csv("https://raw.githubusercontent.com/yunwoong7/toy_datasets/main/csv/titanic.csv")
    st.dataframe(df, use_container_width=True)

    # df = pd.DataFrame({
    #     "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
    #     "gdp": [21400000, 2940000, 2830000, 3870000, 2160000, 1350000, 1780000, 1320000, 516000, 14000000],
    #     "happiness_index": [7.3, 7.2, 6.5, 7.0, 6.0, 6.3, 7.3, 7.3, 5.9, 5.0]
    # })
    # st.write("Dataframe : ")
    # st.dataframe(df.style.highlight_max(axis=0) ) 

    llm = OpenAI(api_token=OPENAI_API_KEY)
    pandas_ai = PandasAI(llm)

    question = st.selectbox(
        "Select the quiz type",
        ["What is the average age of passengers?",
         "승객들의 평균 연령은?",
         "Calculate the number of survivors by room class and gender.",
         "We are trying to create a model that predicts the Survived column using data. Which column is the most important?",
         "Show the survival rate by sex in a graph.",
         "Plot the histogram of Age.",
        ]
    )

    if st.button("Generate"):
        response = pandas_ai.run(df, prompt=question, show_code=True)
        st.info(response)
       
    # response = pandas_ai.run(df, prompt='What are the 5 happiest countries')
    # st.write(response)
    # pandas_ai.run(df, "Plot the histogram of countries showing for each the gpd, using different colors for each bar")
    
if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()

### https://discuss.streamlit.io/t/are-there-any-ways-to-clear-file-uploader-values-without-using-streamlit-form/40903


                