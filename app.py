import os
import numpy as np
import datetime
import csv
from featurizer import *
from time import time, sleep

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
        print(score, int_score)
        print(features)
        # You could add code here to save the data, such as writing it to a file or database
        # with open('survey_responses.txt', 'a') as f:
        #     f.write(f"{first_name},{last_name},{phone_number},{home_country},{occupation},{long_question_response},{read_brochure}\n")
        #webbrowser.open("https://www.google.com")
        # sleep(0.75)
        st.success(f"Thank you for submitting the survey!\n\nYou are more likely to convert than {int_score}% of other leads!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > 40 else url2})", icon="✅")
