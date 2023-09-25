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
page_favicon = "jsicon.png"

max_width = 1000

st.set_page_config(page_title=page_name, page_icon = page_favicon)#, layout='wide')
st.markdown(
        f"""
<style>
    .appview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: 0rem;
        padding-right: 0rem;
        padding-left: 0rem;
        padding-bottom: rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.markdown(hide_st_style, unsafe_allow_html=True)
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
# _, cent_co, _ = st.columns([1,10,1])
# with cent_co:
#     st.image("js_school_banner.png")
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
visibility: hidden;}
</style>
'''
#     st.markdown(hide_img_fs, unsafe_allow_html=True)
# st.title(page_title)
# st.markdown("Tell us about yourself, and we will send you a calendar invite to chat!")

qs = [ 
    "Full Name*", "Phone Number*", "Email Address*",
    "Country*", "What is your Occupation?*",
    "What’s happening in your life right now that has you potentially considering becoming a life coach? And ultimately what’s your goal?*",
    "What best describes your financial situation?*",
    "Please confirm you have read our Program Brochure before booking the Enrollment Interview*"
]

money_qs = [
    "I have the cash and/or credit to invest in myself",
    "I don’t have much money right now or access to credit",
    ""
]
b_qs = [
    "Yes", "No", ""
]

thresh = 49
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

country_list = [f"{i[0]}: {i[1]}" for i in CODES.items()]
vals = {
    qs[0]: 1, qs[1]: 1, qs[2]: 1, qs[4]: 1, qs[5]: 1, qs[6]: 1, qs[7]: 1
}
# st.markdown("---")
main_columns = st.columns([7,4])
with main_columns[0]:
    st.markdown("""# CONGRATULATIONS!

### You're about to book a call with a friendly enrollment advisor inside Jay Shetty Coaching Certification School! """)
with main_columns[1]:
    st.image("js_profile.png")
    st.markdown(hide_img_fs, unsafe_allow_html=True)
st.write(
    """<style>
    [data-testid="stHorizontalBlock"] {
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<div align=\"center\">This call will be your gateway to find out more about this program and answer any questions you have! We're excited for you to take this step and look forward to speaking with you.</div><br>", unsafe_allow_html=True)
st.markdown("##### Provide your information below:")
with st.form("Answers"):
    cols = st.columns([4,2,4])
    with cols[0]:
        name = st.text_input(f"{qs[0]}")
    with cols[1]:
        country = st.selectbox("Country Code*", country_list, index=226)
        country_code = country.split("+")[-1]
    with cols[2]:
        phone_number = st.text_input("Phone Number*")
    # phone_number = st.text_input(f"{qs[1]}")
    cols2 = st.columns([4,6])
    with cols2[0]:
        email = st.text_input(f"{qs[2]}")
    # home_country = st.selectbox(qs[3],COUNTRIES,index=COUNTRIES.index('United States'))
    with cols2[1]:
        occupation = st.text_input(f"{qs[4]}")
    long_question_response = st.text_area(f"{qs[5]}", height=170)
    has_money = st.selectbox(f"{qs[6]}", money_qs, index=2)
    read_brochure = st.selectbox(f"{qs[7]}", b_qs, index=2)
    check = st.checkbox("I understand my Enrollment Advisor will call me on the number I provided and at the appointment time I will schedule. I will be ready for the call.*")
    
    if st.form_submit_button("Submit"):
        vals = {
            qs[0]: len(name), qs[1]: len(phone_number), qs[2]: len(email),
            qs[4]: len(occupation), qs[5]: len(long_question_response),
            qs[6]: len(has_money), qs[7]: len(read_brochure)
        }  
        if all(i != 0 for i in vals.values()) and check:    
            features = [
                name, country_code+phone_number, None, email, occupation,
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
            if not check:
                error = error + "\n\nI understand my Enrollment Advisor will call me*"
            st.error(error, icon="🚨")
            
# st.success(st.experimental_get_query_params())
# from streamlit_gsheets import GSheetsConnection
# conn = st.experimental_connection("gsheets", type=GSheetsConnection)
# data = conn.read(worksheet="Sheet1")
# st.dataframe(data)
maglr = '''
<div style="text-align: center;"><iframe src="https://embed.maglr.com/oseawedjvb?nav=3501" width="950" height="550" seamless="seamless" scrolling="yes" frameborder="no" allowtransparency="true" allowfullscreen=""></iframe></div>
'''

maglr = '''
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
</body>
'''


st.markdown(maglr, unsafe_allow_html=True)
