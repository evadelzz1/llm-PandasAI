import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, time

import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

def main():
    OPENAI_API_KEY = st.session_state.openai_api_key

    st.set_page_config(
        page_title="ChatCSV2",
        page_icon="",
        layout="wide"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        :orange[**Daniel**] is a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)

    st.title("Prompt-driven Analysis with PandasAI")

    st.write("PandasAI, OpenAI and Streamlit - Analyzing File Uploads with User Prompts [ChatCSV](https://www.youtube.com/watch?v=oSC2U2iuMRg)")
 
    uploaded_file = st.file_uploader(
        "Choose a CSV file. This should be in long format (one datapoint per row). :red[(titanic.csv)]",
        type=['csv']
    )
                            
    if uploaded_file is not None:
        col1, col2 = st.columns([1,1])
        with col1:
            st.info("CSV Uploaded Successfully")
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, use_container_width=True)
        # st.write("mean of Fare : " + str(df['Fare'].mean()))
        # st.write(df.head(3))

        with col2:
            st.info("Chat Below")
            
            prompt = st.selectbox("Question : ",
                [
                    "What is the average age of passengers?",
                    "승객들의 평균 연령은?",
                    "Calculate the number of survivors by room class and gender.",
                    "We are trying to create a model that predicts the Survived column using data. Which column is the most important?"
                ]
            )

            # prompt = st.text_input(
            #     "Question : ",
            #     value="Plot the survival counts for males and females",
            #     # value="What was the average fare price?",
            #     type="default"
            # )
            
            if st.button("Generate"):
                if prompt:
                    try:
                        with st.spinner("PandasAI is generating an answer, please wait..."):
                            st.info("Your Query: " + prompt)
                            llm = OpenAI(api_token=OPENAI_API_KEY)
                            pandas_ai = PandasAI(llm)
                            result = pandas_ai.run(df, prompt=prompt)
                            st.success(result)
                    except Exception as e:
                        generated_text = None
                        st.error(f"An error occurred: {e}", icon="🚨")
                else:
                    st.warning("Please enter a prompt.")

                      
if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()



                