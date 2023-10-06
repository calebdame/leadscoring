from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from hubspot.crm.contacts.exceptions import ApiException
import streamlit as st
import datetime
from featurizer import *
import re
import os
import time

UTMS = [
    f'booking-{j}-{i}' for i in ["be", "a", "f", "s"] for j in ["rnc", "c2c", "ovsl"]
] + [
    'booking-amb', 'jscs-instant-book', 'booking-be', 'booking-pathway', 'booking-funnel'
]

def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)

def set_streamlit_config():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    st.set_page_config(page_title="Jay Shetty Sign Up", page_icon="jsicon.png")
    st.markdown(hide_st_style, unsafe_allow_html=True)
    set_max_width(950)
    load_external_styles()

def set_max_width(max_width):
    st.markdown(
        f"""
    <style>
        .appview-container .main .block-container{{
            max-width: {max_width}px;
            padding: 0rem;
        }}
        .block-container {{
            padding: 0rem;
        }}
    </style>
    """, unsafe_allow_html=True)

def load_external_styles():
    with open("style.css") as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

def display_header():
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
    visibility: hidden;}
    </style>
    '''
    main_columns = st.columns([7, 4])
    with main_columns[0]:
        st.markdown("""# CONGRATULATIONS!
        
### You're about to book a call with a friendly enrollment advisor inside Jay Shetty Coaching Certification School! """)
    with main_columns[1]:
        st.image("js_profile.png")
        st.markdown(hide_img_fs, unsafe_allow_html=True)

def display_main_content():
    st.markdown("<div align=\"center\">This call will be your gateway to find out more about this program and answer any questions you have! We're excited for you to take this step and look forward to speaking with you.</div><br>", unsafe_allow_html=True)
    st.markdown("##### Provide your information below:")
    with st.form("Answers"):
        fname, lname, country_code, phone_number = get_user_details()
        email, occupation = get_secondary_details()
        long_question_response, has_money, read_brochure = get_additional_details()
        check = st.checkbox("I understand my Enrollment Advisor will call me on the number I provided and at the appointment time I will schedule. I will be ready for the call.*")
        
        process_form(fname, lname, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure, check)

def get_user_details():
    cols = st.columns([5,5,3,7])
    with cols[0]:
        fname = st.text_input("First Name*")
    with cols[1]:
        lname = st.text_input("Last Name*")
    with cols[2]:
        country_list = [f"{i[0]}: {i[1]}" for i in CODES.items()]
        country = st.selectbox("Country Code*", country_list, index=226)
    with cols[3]:
        phone_number = st.text_input("Phone Number*")
    return fname, lname, country, phone_number

def get_secondary_details():
    cols2 = st.columns([5, 5])
    with cols2[0]:
        email = st.text_input("Email Address*")
    with cols2[1]:
        occupation = st.text_input("What is your Occupation?*")
    return email, occupation

def get_additional_details():
    long_question_response = st.text_area("What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?*", height=160)
    money_qs = ["I have the cash and/or credit to invest in myself", "I don’t have much money right now or access to credit", ""]
    has_money = st.selectbox("What best describes your financial situation?*", money_qs, index=2)
    b_qs = ["Yes", "No", ""]
    read_brochure = st.selectbox("Please confirm you have read our Program Brochure before booking the Enrollment Interview*", b_qs, index=2)
    return long_question_response, has_money, read_brochure

def process_form(fname, lname, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure, check):
    if st.form_submit_button("Submit"):
        phone = re.sub("[^0-9]", "", phone_number)
        vals = {
            "First Name*": len(fname),
            "Last Name*": len(lname),
            "Phone Number*": len(phone_number),
            "Email Address*": len(email),
            "What is your Occupation?*": len(occupation),
            "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?*": len(long_question_response),
            "What best describes your financial situation?*": len(has_money),
            "Please confirm you have read our Program Brochure before booking the Enrollment Interview*": len(read_brochure)
        }
        validate_form(vals, check, fname, lname, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure)

def validate_form(vals, check, fname, lname, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure):
    if all(i != 0 for i in vals.values()) and check and (vals["Phone Number*"] >= 7) and (vals["Phone Number*"] <= 15):
        ts = datetime.datetime.now()
        name = fname + " " + lname
        features = [
            name, country_code.split("+")[-1] + " (" + phone_number, None, email, occupation,
            long_question_response, int("cash" in has_money),
            int("Yes" in read_brochure), ts
        ]
        f = Featurizer(*features)
        feats = f.generate_feature_dict()
        score, int_score = model.predict([feats])
        thresh = 49
        url1 = "https://pages.jayshettycoaching.com/test-jscs-qualified-booking/"
        url2 = "https://pages.jayshettycoaching.com/test-jscs-unqualified-lead/"
        vsl = st.experimental_get_query_params()["utm_campaign"][0]
        bad = "" if int_score > thresh else "u-"
        url = f"https://pages.jayshettycoaching.com/" + bad + vsl + "/"
        send_to_hubspot(
            lname, fname, country_code, phone_number, 
            email, occupation, long_question_response, 
            has_money, read_brochure, ts, check, 
            int_score, score, vsl
        )
        time.sleep(0.25)
        st.success(f"Thank you for submitting the survey!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > thresh else url2})", icon="✅")
        nav_to(url)
    else:
        error_message = generate_error_message(vals, check)
        st.error(error_message, icon="🚨")

def send_to_hubspot(lname, fname, country, phone_number, email, occupation, long_question_response, has_money, read_brochure, ts, check, perc_score, score, vsl):

    api_client = HubSpot(access_token=os.environ["hs_access_token"])
    try:
        simple_public_object_input_for_create = SimplePublicObjectInputForCreate(
            properties={"email": email,   #string
                        "firstname": fname,           #string
                        "lastname": lname,          #string
                        "phone": f"+{country_code.split('+')[-1]}-{phone_number}",
                        "jobtitle": occupation,
                        "what_s_your_goal_": long_question_response,
                        "what_best_describes_your_financial_situation_":has_money,
                        "please_confirm_you_have_read_our_program_brochure_before_booking_the_enrollment_interview": read_brochure,
                        "i_will_be_ready_for_the_call": str(check).lower(),
                        "lead_score": score,
                        "lead_percentile_score": perc_score,
                        "vsl_source": vsl,
                         "country": country.split(":")[0]
                         }
        )
        api_response = api_client.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input_for_create
        )
    except ApiException as e:
        st.markdown("Exception when creating contact: %s\n" % e)

def generate_error_message(vals, check):
    error = "**Please be sure to complete the following fields:**"
    for name, count in vals.items():
        if count == 0:
            error = error + f"\n\n{name}"
    if not check:
        error = error + "\n\nI understand my Enrollment Advisor will call me*"
    if (vals["Phone Number*"] < 7) or (vals["Phone Number*"] > 15):
        error = error + "\n\nBad number of digits in phone"
    return error

def display_footer():
    maglr = '''
    <br>
    <body>
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: 0;
                display: flex;
                flex-flow: row nowrap;
                justify-content: center;
                align-items: center;
            }
            iframe {
                width: 950px;
                max-width: 100%;
                height: 550px;
                position: absolute;
                border 0 none;
                padding: 0;
            }
        </style>
        <iframe src="https://embed.maglr.com/oseawedjvb?nav=3501"></iframe>
    </body><br><br><br>
    '''
    st.markdown(maglr, unsafe_allow_html=True)
    st.success(st.experimental_get_query_params())

def main():
    set_streamlit_config()
    display_header()
    display_main_content()
    display_footer()

if __name__ == "__main__":
    main()
