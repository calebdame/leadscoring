import os
import numpy as np
import datetime
import csv
from featurizer import *
from time import time, sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import streamlit.components.v1 as components

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

qs = [
    "First Name", "Last Name",
    "Phone Number", "Email Address",
    "Home Country", "What is your Occupation?",
    "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?",
    "What best describes your financial situation?",
    "Please confirm you have read our Program Brochure before booking the Enrollment Interview"
]

money_qs = [
    "I have the cash and/or credit to invest in myself",
    "I don’t have much money right now or access to credit",
    ""
]

url1 = "https://pages.jayshettycoaching.com/test-jscs-qualified-booking/"
url2 = "https://pages.jayshettycoaching.com/test-jscs-unqualified-lead/"

# Define your survey fields
st.title("Jay Shetty Coaching Enrollment")
st.markdown("Tell us about yourself, and we will send you a calendar invite to chat!")
with st.form("Answers"):
    first_name = st.text_input(qs[0])
    last_name = st.text_input(qs[1])
    phone_number = st.text_input(qs[2])
    email = st.text_input(qs[3])

    # A dropdown list of countries. You might want to use a more comprehensive list.
    home_country = st.selectbox(qs[4], COUNTRIES, index=COUNTRIES.index('United States'))

    occupation = st.text_input(qs[5])

    # A larger text area for long responses
    long_question_response = st.text_area(qs[6], height=225)

    has_money = st.selectbox(qs[7], money_qs, index=2)

    # A true/false checkbox
    read_brochure = st.checkbox(qs[8])

    # A button to submit the form
    if st.form_submit_button("Sign Up"):
        # Display a message upon submission (you might want to do something more useful with the data)
        
        features = [
            f"{first_name} {last_name}", phone_number, home_country, email, occupation,
            long_question_response, "cash" in has_money, read_brochure, datetime.datetime.now()
        ]
        f = Featurizer(
            *features
        )
        feats = f.generate_feature_dict()
        score, int_score = model.predict([feats])
        st.success(f"Thank you for submitting the survey!\n\nYou are more likely to convert than {int_score}% of other leads!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > 40 else url2})", icon="✅")

st.success(st.experimental_get_query_params())
# from streamlit_gsheets import GSheetsConnection
# conn = st.experimental_connection("gsheets", type=GSheetsConnection)
# data = conn.read(worksheet="Sheet1")
# st.dataframe(data)

from streamlit.runtime.scriptrunner import get_script_run_ctx

def get_remote_ip() -> str:

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = st.runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except:
        return None

    return session_info.request.remote_ip

st.markdown(f"The remote ip is {get_remote_ip()}")
