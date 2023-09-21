import streamlit as st

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
page_name = "Jay Shetty Sign Up"
page_title = "Jay Shetty Coaching Enrollment"
page_favicon = "https://icons.iconarchive.com/icons/microsoft/fluentui-emoji-mono/256/Rightwards-Hand-Default-icon.png"

st.set_page_config(page_title=page_name, page_icon = page_favicon)
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title(page_title)
st.markdown("Tell us about yourself, and we will send you a calendar invite to chat!")

qs = [ 
    "Full Name", "Phone Number", "Email Address",
    "Country", "What is your Occupation?",
    "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?",
    "What best describes your financial situation?",
    "Please confirm you have read our Program Brochure before booking the Enrollment Interview"
]

money_qs = [
    "I have the cash and/or credit to invest in myself",
    "I don’t have much money right now or access to credit",
    ""
]
b_qs = [
    "Yes", "No", ""
]

thresh = 0.45
url1 = "https://pages.jayshettycoaching.com/test-jscs-qualified-booking/"
url2 = "https://pages.jayshettycoaching.com/test-jscs-unqualified-lead/"

import datetime
from featurizer import *
import streamlit.components.v1 as components
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

vals = {
    qs[0]: 1, qs[1]: 1, qs[2]: 1, qs[4]: 1, qs[5]: 1, qs[6]: 1, qs[7]: 1
}

with st.form("Answers"):
    name_cols = st.columns(2)
    with name_cols[0]:
        name = st.text_input(f"{qs[0]}")
    phone_number = st.text_input(f"{qs[1]}")
    email = st.text_input(f"{qs[2]}")
    home_country = st.selectbox(qs[3],COUNTRIES,index=COUNTRIES.index('United States'))
    occupation = st.text_input(f"{qs[4]}")
    long_question_response = st.text_area(f"{qs[5]}", height=225)
    has_money = st.selectbox(f"{qs[6]}", money_qs, index=2)
    read_brochure = st.selectbox(f"{qs[7]}", b_qs, index=2)
    cols=st.columns([1,4,5])
    with cols[0]:
        a = st.selectbox("Country Code", [1,2,3], index=1)
    with cols[1]:
        b = st.text_input("Phone")
    
    if st.form_submit_button("Sign Up"):
        vals = {
            qs[0]: len(name), qs[1]: len(phone_number), qs[2]: len(email),
            qs[4]: len(occupation), qs[5]: len(long_question_response),
            qs[6]: len(has_money), qs[7]: len(read_brochure)
        }  
        if all(i != 0 for i in vals.values()):    
            features = [
                name, phone_number, home_country, email, occupation,
                long_question_response, int("cash" in has_money), 
                int("Yes" in read_brochure), datetime.datetime.now()
            ]
            f = Featurizer(
                *features
            )
            feats = f.generate_feature_dict()
            score, int_score = model.predict([feats])
            st.success(f"Thank you for submitting the survey!\n\nYou are more likely to convert than {int_score}% of other leads!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > thresh else url2})", icon="✅")
        else:
            error =  "**Please be sure to complete the following fields:**"
            for name, count in vals.items():
                if count == 0:
                    error = error + f"\n\n{name}"
            st.error(error, icon="🚨")
            
# st.success(st.experimental_get_query_params())
# from streamlit_gsheets import GSheetsConnection
# conn = st.experimental_connection("gsheets", type=GSheetsConnection)
# data = conn.read(worksheet="Sheet1")
# st.dataframe(data)
