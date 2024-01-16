import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, time

import pandas as pd
#from pandasai import PandasAI
#from pandasai.llm.openai import OpenAI
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# https://www.youtube.com/watch?v=R8zpK1yFA60
# https://github.com/InsightEdge01/MutiChatCSVPandasAI


def chat_with_csv(df,prompt,openai_api_key):
    llm = OpenAI(api_token=openai_api_key)
    pandas_ai = SmartDataframe(df, config={"llm": llm})
    #pandas_ai = PandasAI(llm, save_charts=True)
    result = pandas_ai.chat(prompt)
    #result = pandas_ai.run(df,prompt=prompt)
    return result

def main():
    OPENAI_API_KEY = st.session_state.openai_api_key

    st.set_page_config(
        page_title="Multiple-CSV",
        page_icon="",
        layout="wide"
    )

    with st.sidebar:
        st.header("👨‍💻 About the Author")
        st.write("""
        :orange[**Daniel**] is a tech enthusiast and coder. Driven by passion and a love for sharing knowledge, I'm created this platform to make learning more interactive and fun.
        """)

    st.title("Multiple-CSV ChatApp powered by LLM")
    st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    st.subheader('Built for All Data Analysis and Visualizations')
    st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

    st.write("Analyze Multiple CSV files with PandasAI and OpenAI [Multi-ChatCSV Streamlit App](https://www.youtube.com/watch?v=R8zpK1yFA60) [github](https://github.com/InsightEdge01/MutiChatCSVPandasAI/tree/master)")

    # Upload multiple CSV files
    input_csvs = st.sidebar.file_uploader("Upload your CSV files", type=['csv'], accept_multiple_files=True)

    if input_csvs:
        # Select a CSV file from the uploaded files using a dropdown menu
        selected_file = st.selectbox("Select a CSV file", [file.name for file in input_csvs])
        selected_index = [file.name for file in input_csvs].index(selected_file)

        #load and display the selected csv file 
        st.info("CSV uploaded successfully")
        data = pd.read_csv(input_csvs[selected_index])
        st.dataframe(data,use_container_width=True)

        #Enter the query for analysis
        st.info("Chat Below")
        input_text = st.text_area("Enter the query")

        #Perform analysis
        if input_text:
            if st.button("Chat with csv"):
                st.info("Your Query: "+ input_text)
                result = chat_with_csv(data,input_text,OPENAI_API_KEY)
                fig_number = plt.get_fignums()
                if fig_number:
                    st.pyplot(plt.gcf())
                else:
                    st.success(result)
                 
    # uploaded_file = st.file_uploader(
    #     "Choose a CSV file. This should be in long format (one datapoint per row).",
    #     type="csv",
    # )

    # if uploaded_file is not None:
    #     df = pd.read_csv(uploaded_file)
    #     st.write("mean of Fare : " + str(df['Fare'].mean()))
    #     st.write(df.head(3))

    #     prompt = st.text_input(
    #         "Question : ",
    #         value="Plot the survival counts for males and females",
    #         # value="What was the average fare price?",
    #         type="default"
    #     )
        
    #     if st.button("Generate"):
    #         with st.spinner("PandasAI is generating an answer, please wait..."):
    #             if prompt:
                    
    #                 llm = OpenAI(api_token=OPENAI_API_KEY)
    #                 pandas_ai = PandasAI(llm)
    #                 response = pandas_ai.run(df, prompt=prompt)
    #                 st.write(response)
    #             else:
    #                 st.warning("Please enter a prompt.")

    #     if st.button("Generate2"):
    #         with st.spinner("PandasAI is generating an answer, please wait..."):
    #             if prompt:
                    
    #                 llm = OpenAI(api_token=OPENAI_API_KEY)
    #                 pandas_ai = PandasAI(llm)
    #                 response = pandas_ai.run(df, prompt=prompt)
    #                 st.write(response)
    #             else:
    #                 st.warning("Please enter a prompt.")
                      
if __name__=="__main__":
    if "openai_api_key" not in st.session_state:
        st.error("Need a OPENAI_API_KEY! Go to the Home.", icon="🚨")
        time.sleep(2)
        switch_page('Home')

    main()



                