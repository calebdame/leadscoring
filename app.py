import streamlit as st
import datetime
from featurizer import *
import re
import os
import time
import requests
import json
from variables import *
import time
from streamlit_javascript import st_javascript

def client_ip():
    url = 'https://api.ipify.org?format=json'
    script = (f'await fetch("{url}").then('
                'function(response) {'
                    'return response.json();'
                '})')
    try:
        result = st_javascript(script)
        if isinstance(result, dict) and 'ip' in result:
            return result['ip']
        else: return None
    except: return None

def get_user_agent():
    try:
        user_agent = st_javascript(('navigator.userAgent'))
        if user_agent: return user_agent
        else: return None
    except: return None

def get_screen_resolution():
    script = '({width: window.screen.width, height: window.screen.height})'
    try:
        screen_res = st_javascript(script)
        if screen_res:
            width = screen_res.get('width')
            height = screen_res.get('height')
            return f"{width}x{height}"
    except:
        return None

def get_screen_dimensions():
    script = ('{width: window.screen.width, height: window.screen.height}')
    try:
        dimensions = st_javascript(script)
        if dimensions:
            width = dimensions.get('width')
            height = dimensions.get('height')
            return f"{width}x{height}"
    except:
        pass

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
    
    if len(st.session_state) == 0:
        st.session_state["IP"] = []
        st.session_state["UAS"] = []
        st.session_state["SR"] = []
        st.session_state['TIME'] = time.time()
    
    st.session_state['IP'].append(client_ip())
    st.session_state['UAS'].append(get_user_agent())
    st.session_state['SR'].append(get_screen_resolution())

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
        
### You're about to book a call with a friendly enrollment advisor inside Jay Shetty Coaching Certification School! 

#### This call will be your gateway to find out more about this program and answer any questions you have! We're excited for you to take this step and look forward to speaking with you.""")
    with main_columns[1]:
        st.image("js_profile.png")
        st.markdown(hide_img_fs, unsafe_allow_html=True)

def display_main_content():
    # st.markdown("<div align=\"center\"></div><br>", unsafe_allow_html=True)
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
            "Please confirm whether you have read our Program Brochure before booking the Enrollment Interview*": len(read_brochure)
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
        bad = "" if int_score > THRESH else "u-"
        vsl = st.experimental_get_query_params().get("utm_campaign",["None"])[0]
        if vsl in UTMS:
            url = f"https://pages.jayshettycoaching.com/" + bad + vsl + "/"
        else:
            url = "https://pages.jayshettycoaching.com/" + bad + "booking-rnc-be/"
        url = url + f"?email={email}&name={fname}+{lname}"
        send_to_hubspot(
            lname, fname, country_code, phone_number, 
            email, occupation, long_question_response, 
            has_money, read_brochure, ts, check, 
            int_score, score, vsl
        )
        time.sleep(0.25)
        st.success(f"Thank you for submitting the survey!\n\nFind your calendar invite below:\n\n[Click Here]({url})", icon="✅")
        # nav_to(url)
    else:
        error_message = generate_error_message(vals, check)
        st.error(error_message, icon="🚨")

def add_ip_data(prop):
    ip = st.session_state['IP'][-1]
    if ip is not None:
        try:
            prop["ip_data"] = requests.get(f"https://freeipapi.com/api/json/{ip}").text
            ip_data = json.loads(prop["ip_data"])
            prop["ip_latitude"] = ip_data["latitude"]
            prop["ip_longitude"] = ip_data["longitude"]
            prop["ip_version"] = ip_data["ipVersion"]
        except:
            fail = True
    uas = st.session_state['UAS'][-1]
    if uas is not None:
        prop["ip_uas"] = uas
    sr = st.session_state['SR'][-1]
    if sr is not None:
        prop["ip_screen_res"] = sr
    return prop

def create_contact_and_deal(prop, is_SDR):

    prop = add_ip_data(prop)
    # if 'IPDATA' in st.session_state:
    #     if st.session_state['IPDATA'] is not None and st.session_state['IPDATA'] != "":
    #         prop["ip_data"] = st.session_state["IPDATA"]
    #         try:
    #             temp_dict = json.loads(prop["ip_data"])
    #             prop["ip_latitude"] = temp_dict['latitude']
    #             prop["ip_longitude"] = temp_dict['longitude']
    #             prop["ip_version"] = temp_dict['ipVersion']
    #         except:
    #             fail = True
    # if 'UAS' in st.session_state:
    #     if st.session_state['UAS'] is not None and st.session_state['UAS'] != "":
    #         prop["ip_uas"] = st.session_state['UAS']
    
    url = 'https://api.hubapi.com/crm/'
    headers = {'Content-Type':'application/json','Authorization': f'Bearer {os.environ["access_token"]}'}
    r = requests.post(
        data=json.dumps({"properties": prop}), 
        url=f"{url}v3/objects/contacts", headers=headers
    )
    st.success(r.text)
    if r.status_code == 201:
        contact_id = json.loads(r.text)["id"]
    else:
        contact_id = json.loads(r.text)['message'].split("ID: ")[-1]
        r = requests.patch(
            data=json.dumps({"properties": {i:j for i,j in prop.items() if i!="email"}}), 
            url=f"{url}v3/objects/{contact_id}", headers=headers
        )
        st.success(r.text)
        
    deal_data = {
        "amount": AMOUNT,
        "dealname": f"{prop['firstname']} - {prop['email']} - Enrollment Interview",
        "pipeline": "42444382" if is_SDR else "default",
        "dealstage": "89331280" if is_SDR else "appointmentscheduled",
        "raw_score": prop['lead_score'],
        "percentile_score": prop['lead_percentile_score'] 
    }
    if is_SDR:
        deal_data["dealname"] = f"{prop['firstname']} - {prop['lastname']} - Booking Attempt"
    
    r = requests.post(
        data=json.dumps({"properties": deal_data}), 
        url=f"{url}v3/objects/deals", headers=headers
    )
    st.success(r.text)

    deal_id = json.loads(r.text)["id"]

    r = requests.put(
        url=f"{url}v4/objects/contact/{contact_id}/associations/default/deal/{deal_id}", headers=headers
    )
    st.success(r.text)
    pass
    
def send_to_hubspot(lname, fname, country_code, phone_number, email, occupation, long_question_response, has_money, read_brochure, ts, check, perc_score, score, vsl):
    data_dict = {"email": email,   #string
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
                 "country": country_code.split(":")[0],
                "time_on_enrollment_page" : time.time() - st.session_state['TIME']
                         }
    is_SDR = perc_score <= THRESH
    create_contact_and_deal(data_dict, is_SDR)

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

def main():
    set_streamlit_config()
    display_header()
    display_main_content()
    # st.success(st.session_state)
    display_footer()

if __name__ == "__main__":
    main()
