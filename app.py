import streamlit as st
import datetime
from featurizer import *
import webbrowser

# Configurations and Styles
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
        name, country_code, phone_number = get_user_details()
        email, occupation = get_secondary_details()
        long_question_response, has_money, read_brochure = get_additional_details()
        check = st.checkbox("I understand my Enrollment Advisor will call me on the number I provided and at the appointment time I will schedule. I will be ready for the call.*")
        
        process_form(name, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure, check)


def get_user_details():
    cols = st.columns([4, 2, 4])
    with cols[0]:
        name = st.text_input("Full Name*")
    with cols[1]:
        country_list = [f"{i[0]}: {i[1]}" for i in CODES.items()]
        country = st.selectbox("Country Code*", country_list, index=226)
        country_code = country.split("+")[-1]
    with cols[2]:
        phone_number = st.text_input("Phone Number*")
    
    return name, country_code, phone_number


def get_secondary_details():
    cols2 = st.columns([4, 6])
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


def process_form(name, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure, check):
    if st.form_submit_button("Submit"):
        vals = {
            "Full Name*": len(name),
            "Phone Number*": len(phone_number),
            "Email Address*": len(email),
            "What is your Occupation?*": len(occupation),
            "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?*": len(long_question_response),
            "What best describes your financial situation?*": len(has_money),
            "Please confirm you have read our Program Brochure before booking the Enrollment Interview*": len(read_brochure)
        }

        validate_form(vals, check, name, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure)


def validate_form(vals, check, name, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure):
    if all(i != 0 for i in vals.values()) and check and (vals["Phone Number"] > 7) and (vals["Phone Number"] < 15):
        features = [
            name, country_code + " (" + phone_number, None, email, occupation,
            long_question_response, int("cash" in has_money),
            int("Yes" in read_brochure), datetime.datetime.now()
        ]
        f = Featurizer(*features)
        feats = f.generate_feature_dict()
        score, int_score = model.predict([feats])
        thresh = 49
        url1 = "https://pages.jayshettycoaching.com/test-jscs-qualified-booking/"
        url2 = "https://pages.jayshettycoaching.com/test-jscs-unqualified-lead/"
        st.success(f"Thank you for submitting the survey!\n\nYou are more likely to convert than {int_score}% of other leads!\n\nFind your calendar invite below:\n\n[Click Here]({url1 if int_score > thresh else url2})", icon="✅")
        webbrowser.open(url1 if int_score > thresh else url2)
    else:
        error_message = generate_error_message(vals, check)
        st.error(error_message, icon="🚨")


def generate_error_message(vals, check):
    error = "**Please be sure to complete the following fields:**"
    for name, count in vals.items():
        if count == 0:
            error = error + f"\n\n{name}"
    if not check:
        error = error + "\n\nI understand my Enrollment Advisor will call me*"
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


# Main Streamlit App
def main():
    set_streamlit_config()
    display_header()
    display_main_content()
    display_footer()


if __name__ == "__main__":
    main()
