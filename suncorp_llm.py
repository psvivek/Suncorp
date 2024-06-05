import streamlit as st
import pandas as pd
import os
import pandas as pd
pd.options.plotting.backend = "plotly"
from pandasai import Agent
import plotly.express as px
import numpy as np

# By default, unless you choose a different LLM, it will use BambooLLM.
os.environ["PANDASAI_API_KEY"] = "$2a$10$avxu2E7rVx4XBEDHRAXw2.ZimD6hncDF6elhA4IyI30upnPK/CAee"

# Function to be called when text input is submitted
def process_prompt_llm(agent, input_text, X, Y):
    pai_output = agent.chat(input_text)
    # print(pai_output.columns)

    # using Plotly Express via the Pandas backend
    fig1 = pai_output.plot.bar(x=X, y=Y)

    # Display the plot using Streamlit
    st.plotly_chart(fig1)

# Streamlit application
def main():
    st.set_page_config(page_title="Suncorp Technical Challenge", layout="centered", initial_sidebar_state="auto")

    st.markdown("<h1 style='color: black;'>Suncorp Technical Challenge</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: black;'>Presentation</h1>", unsafe_allow_html=True)

    st.markdown("""
                    <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
                        padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
                        border-radius: 8px; will-change: transform;">
                        <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
                            src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGHD1IWzfc&#x2F;i7BQd3zbNp0ZBvOdsguPig&#x2F;view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
                        </iframe>
                    </div>
                    <a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGHD1IWzfc&#x2F;i7BQd3zbNp0ZBvOdsguPig&#x2F;view?utm_content=DAGHD1IWzfc&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">Improving Claims Process with Data Science</a> by PABOLU SATYA VIVEK
                """, unsafe_allow_html=True)


    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 12px;
        }
        p {
            color: black;
        }
        .stFileUploaderFileName {
                color: black;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: black;'>Generative Plotting</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['MaritalStatus'] = df['MaritalStatus'].fillna('U')

        df['ClaimNumberInt'] = df['ClaimNumber'].str[2:].astype(int)

        # Generate Some date features
        df['YearOfAccident']  = pd.DatetimeIndex(df['DateTimeOfAccident']).year
        df['MonthOfAccident']  = pd.DatetimeIndex(df['DateTimeOfAccident']).month
        df['DayOfAccident']  = pd.DatetimeIndex(df['DateTimeOfAccident']).day
        df['HourOfAccident']  = pd.DatetimeIndex(df['DateTimeOfAccident']).hour
        df['YearReported']  = pd.DatetimeIndex(df['DateReported']).year

        # Reporting delay in weeks 
        df['DaysReportDelay'] = pd.DatetimeIndex(df['DateReported']).date - pd.DatetimeIndex(df['DateTimeOfAccident']).date
        df['DaysReportDelay'] = (df['DaysReportDelay']  / np.timedelta64(1, 'D')).astype(int)
        df['WeeksReportDelay'] = np.floor(df['DaysReportDelay'] / 7.).astype(int)
        df['WeeksReportDelay'] = np.clip(df['WeeksReportDelay'], a_max=55, a_min=None)

        # drop unnecessary columns
        df.drop(['ClaimNumber','DateTimeOfAccident','DaysReportDelay','DateReported'],axis=1,inplace=True)

        st.write("CSV file successfully uploaded!")
        df = df[['Age',
                'Gender',
                'MaritalStatus',
                'DependentChildren',
                'DependentsOther',
                'WeeklyWages',
                'PartTimeFullTime',
                'HoursWorkedPerWeek',
                'DaysWorkedPerWeek',
                'InitialIncurredClaimsCost',
                'UltimateIncurredClaimCost',
                'ClaimNumberInt',
                'YearOfAccident',
                'MonthOfAccident',
                'DayOfAccident',
                'HourOfAccident',
                'YearReported',
                'WeeksReportDelay']]
        
        st.write(df)

        agent = Agent(df)        

        input_text = st.text_input("Enter some text and press Enter. Example, \nWhich are the top 5 claims by UltimateIncurredClaimCost?", )

        if input_text:
            process_prompt_llm(agent, input_text, 'Gender', 'UltimateIncurredClaimCost')

if __name__ == "__main__":
    main()
