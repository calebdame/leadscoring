import numpy as np
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('punkt')
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import datetime 
from datetime import date, timedelta
import re
import json
from model import Model

def largest_shared_substring(str1, str2):
    str1, str2 = re.sub(" +", "", str1).upper(), re.sub(" +", "", str2).upper()
    longest_substring = ""
    for i in range(len(str1)):
        for j in range(i+1, len(str1)+1):
            sub = str1[i:j]
            if sub in str2 and len(sub) > len(longest_substring):
                longest_substring = sub
    return longest_substring

def get_unique_word_freq(string):
    try:
        return len(set(string.split()))/len(string.split())
    except: return 0
    
def count_stopwords_freq(text):  
    word_tokens = word_tokenize(text)
    stopwords_x = [w for w in word_tokens if w.lower() in STOP_WORDS]
    try:
        return len(stopwords_x)/len(word_tokens)
    except: return 0
    
SIA = SentimentIntensityAnalyzer()
STOP_WORDS = set(stopwords.words('english'))

CODES = {'AFG': '+93', 'AIA': '+1', 'ALB': '+355', 'ALD': '+358', 'ALG': '+213', 'AND': '+376', 'ANG': '+244', 'ANT': '+599', 'ARG': '+54', 'ARM': '+374', 'ARU': '+297', 'ASA': '+1', 'ATG': '+1', 'AUS': '+61', 'AUT': '+43', 'AZE': '+994', 'BAH': '+1', 'BAN': '+880', 'BDI': '+257', 'BEL': '+32', 'BEN': '+229', 'BER': '+1', 'BFA': '+226', 'BHR': '+973', 'BHU': '+975', 'BIH': '+387', 'BLR': '+375', 'BLZ': '+501', 'BOL': '+591', 'BOT': '+267', 'BRA': '+55', 'BRB': '+1', 'BRU': '+673', 'BUL': '+359', 'CAM': '+855', 'CAN': '+1', 'CAY': '+1', 'CCK': '+61', 'CGO': '+242', 'CHA': '+235', 'CHI': '+56', 'CHN': '+86', 'CIV': '+225', 'CMR': '+237', 'COD': '+243', 'COK': '+682', 'COL': '+57', 'COM': '+269', 'CPV': '+238', 'CRC': '+506', 'CRO': '+385', 'CTA': '+236', 'CUB': '+53', 'CXR': '+61', 'CYP': '+357', 'CZE': '+420', 'DEN': '+45', 'DJI': '+253', 'DMA': '+1', 'DOM': '+1', 'ECU': '+593', 'EGY': '+20', 'ENG': '+44', 'EQG': '+240', 'ERI': '+291', 'ESP': '+34', 'EST': '+372', 'ETH': '+251', 'FIJ': '+679', 'FIN': '+358', 'FLK': '+500', 'FRA': '+33', 'FRO': '+298', 'FSM': '+691', 'GAB': '+241', 'GAM': '+220', 'GBG': '+44', 'GBJ': '+44', 'GBM': '+44', 'GBZ': '+350', 'GEO': '+995', 'GER': '+49', 'GHA': '+233', 'GLP': '+590', 'GNB': '+245', 'GRE': '+30', 'GRL': '+299', 'GRN': '+1', 'GUA': '+502', 'GUF': '+594', 'GUI': '+224', 'GUM': '+1', 'GUY': '+592', 'HAI': '+509', 'HKG': '+852', 'HON': '+504', 'HUN': '+36', 'IDN': '+62', 'IND': '+91', 'IRL': '+353', 'IRN': '+98', 'IRQ': '+964', 'ISL': '+354', 'ISR': '+972', 'ITA': '+39', 'JAM': '+1', 'JOR': '+962', 'JPN': '+81', 'KAZ': '+7', 'KEN': '+254', 'KGZ': '+996', 'KIR': '+686', 'KOR': '+82', 'KSA': '+966', 'KUW': '+965', 'LAO': '+856', 'LBR': '+231', 'LBY': '+218', 'LCA': '+1', 'LES': '+266', 'LIB': '+961', 'LIE': '+423', 'LTU': '+370', 'LUX': '+352', 'LVA': '+371', 'MAC': '+853', 'MAD': '+261', 'MAR': '+212', 'MAS': '+60', 'MDA': '+373', 'MDV': '+960', 'MEX': '+52', 'MHL': '+692', 'MKD': '+389', 'MLI': '+223', 'MLT': '+356', 'MNE': '+382', 'MNG': '+976', 'MON': '+377', 'MOZ': '+258', 'MRI': '+230', 'MSR': '+1', 'MTN': '+222', 'MTQ': '+596', 'MWI': '+265', 'MYA': '+95', 'MYT': '+262', 'NAM': '+264', 'NCA': '+505', 'NCL': '+687', 'NED': '+31', 'NEP': '+977', 'NFK': '+672', 'NGA': '+234', 'NIG': '+227', 'NIR': '+44', 'NIU': '+683', 'NMI': '+1', 'NOR': '+47', 'NRU': '+674', 'NZL': '+64', 'OMA': '+968', 'PAK': '+92', 'PAN': '+507', 'PAR': '+595', 'PCN': '+870', 'PER': '+51', 'PHI': '+63', 'PLE': '+970', 'PLW': '+680', 'PNG': '+675', 'POL': '+48', 'POR': '+351', 'PRK': '+850', 'PUR': '+1', 'QAT': '+974', 'REU': '+262', 'ROS': '+672', 'ROU': '+40', 'RSA': '+27', 'RUS': '+7', 'RWA': '+250', 'SAH': '+212', 'SAM': '+685', 'SCO': '+44', 'SEN': '+221', 'SEY': '+248', 'SHN': '+290', 'SIN': '+65', 'SKN': '+1', 'SLE': '+232', 'SLV': '+503', 'SMR': '+378', 'SOL': '+677', 'SOM': '+252', 'SPM': '+508', 'SRB': '+381', 'SRI': '+94', 'STP': '+239', 'SUD': '+249', 'SUI': '+41', 'SUR': '+597', 'SVK': '+421', 'SVN': '+386', 'SWE': '+46', 'SWZ': '+268', 'SYR': '+963', 'TAH': '+689', 'TAN': '+255', 'TCA': '+1', 'TGA': '+676', 'THA': '+66', 'TJK': '+992', 'TKL': '+690', 'TKM': '+993', 'TLS': '+670', 'TOG': '+228', 'TPE': '+886', 'TRI': '+1', 'TUN': '+216', 'TUR': '+90', 'TUV': '+688', 'UAE': '+971', 'UGA': '+256', 'UKR': '+380', 'URU': '+598', 'USA': '+1', 'UZB': '+998', 'VAN': '+678', 'VAT': '+39', 'VEN': '+58', 'VGB': '+1', 'VIE': '+84', 'VIN': '+1', 'VIR': '+1', 'WAL': '+44', 'WLF': '+681', 'YEM': '+967', 'ZAM': '+260', 'ZIM': '+263'}

COUNTRIES = ['Afghanistan',
 "Aland Islands",
 'Albania',
 'Algeria',
 'Andorra',
 'Angola',
 'Antigua & Deps',
 'Argentina',
 'Armenia',
 'Australia',
 'Austria',
 'Azerbaijan',
 'Bahamas',
 'Bahrain',
 'Bangladesh',
 'Barbados',
 'Belarus',
 'Belgium',
 'Belize',
 'Benin',
 'Bhutan',
 'Bolivia',
 'Bosnia Herzegovina',
 'Botswana',
 'Brazil',
 'Brunei',
 'Bulgaria',
 'Burkina',
 'Burundi',
 'Cambodia',
 'Cameroon',
 'Canada',
 'Cape Verde',
 'Central African Rep',
 'Chad',
 'Chile',
 'China',
 'Colombia',
 'Comoros',
 'Congo',
 'Congo {Democratic Rep}',
 'Costa Rica',
 'Croatia',
 'Cuba',
 'Cyprus',
 'Czech Republic',
 'Denmark',
 'Djibouti',
 'Dominica',
 'Dominican Republic',
 'East Timor',
 'Ecuador',
 'Egypt',
 'El Salvador',
 'Equatorial Guinea',
 'Eritrea',
 'Estonia',
 'Ethiopia',
 'Fiji',
 'Finland',
 'France',
 'Gabon',
 'Gambia',
 'Georgia',
 'Germany',
 'Ghana',
 'Greece',
 'Grenada',
 'Guatemala',
 'Guinea',
 'Guinea-Bissau',
 'Guyana',
 'Haiti',
 'Honduras',
 'Hong Kong',
 'Hungary',
 'Iceland',
 'India',
 'Indonesia',
 'Iran',
 'Iraq',
 'Ireland',
 'Israel',
 'Italy',
 'Ivory Coast',
 'Jamaica',
 'Japan',
 'Jordan',
 'Kazakhstan',
 'Kenya',
 'Kiribati',
 'Korea North',
 'Korea South',
 'Kosovo',
 'Kuwait',
 'Kyrgyzstan',
 'Laos',
 'Latvia',
 'Lebanon',
 'Lesotho',
 'Liberia',
 'Libya',
 'Liechtenstein',
 'Lithuania',
 'Luxembourg',
 'Macedonia',
 'Madagascar',
 'Malawi',
 'Malaysia',
 'Maldives',
 'Mali',
 'Malta',
 'Marshall Islands',
 'Mauritania',
 'Mauritius',
 'Mexico',
 'Micronesia',
 'Moldova',
 'Monaco',
 'Mongolia',
 'Montenegro',
 'Morocco',
 'Mozambique',
 'Myanmar, {Burma}',
 'Namibia',
 'Nauru',
 'Nepal',
 'Netherlands',
 'New Zealand',
 'Nicaragua',
 'Niger',
 'Nigeria',
 'Norway',
 'Oman',
 'Pakistan',
 'Palau',
 'Panama',
 'Papua New Guinea',
 'Paraguay',
 'Peru',
 'Philippines',
 'Poland',
 'Portugal',
 'Qatar',
 'Romania',
 'Russia',
 'Rwanda',
 'St Kitts & Nevis',
 'St Lucia',
 'Saint Vincent & the Grenadines',
 'Samoa',
 'San Marino',
 'Sao Tome & Principe',
 'Saudi Arabia',
 'Senegal',
 'Serbia',
 'Seychelles',
 'Sierra Leone',
 'Singapore',
 'Slovakia',
 'Slovenia',
 'Solomon Islands',
 'Somalia',
 'South Africa',
 'South Sudan',
 'Spain',
 'Sri Lanka',
 'Sudan',
 'Suriname',
 'Swaziland',
 'Sweden',
 'Switzerland',
 'Syria',
 'Taiwan',
 'Tajikistan',
 'Tanzania',
 'Thailand',
 'Togo',
 'Tonga',
 'Trinidad and Tobago',
 'Tunisia',
 'Turkey',
 'Turkmenistan',
 'Tuvalu',
 'Uganda',
 'Ukraine',
 'United Arab Emirates',
 'United Kingdom',
 'United States',
 'Uruguay',
 'Uzbekistan',
 'Vanuatu',
 'Vatican City',
 'Venezuela',
 'Vietnam',
 'Yemen',
 'Zambia',
 'Zimbabwe']

FINAL_COLS = {
 'hour_sin', 'hour_cos', 'day_sin', 'day_cos', 'week_sin',
 'week_cos', 'month_sin', 'month_cos', 'hour_sin_US', 'hour_sin_is_weekend', 'hour_cos_US', 'hour_cos_is_weekend', 'day_sin_US', 
 'day_sin_is_weekend', 'day_cos_US', 'day_cos_is_weekend', 'week_sin_US', 'week_sin_is_weekend', 'week_cos_US', 'week_cos_is_weekend',
 'month_sin_US', 'month_sin_is_weekend', 'month_cos_US', 'month_cos_is_weekend', 'occ_neu', 'occ_pos', 'occ_compound', 'q_neg',
 'q_neu', 'q_pos', 'q_compound', 'q_count_to', 'q_count_feel', 'q_count_people', 'q_count_would', 'q_count_months', 'q_count_)',
 'q_count_other', 'q_count_others', 'q_count_for', 'q_count_an', 'q_count_because', 'q_count_life', 'q_count_on', 'q_count_help',
 'q_count_most', 'q_count_path', 'q_count_getting', 'q_count_everyone', 'q_count_was', 'q_count_it', "q_count_'ve", 'q_count_career',
 'q_count_through', 'q_count_coaching', 'q_count_living', "q_count_'s", 'q_count_connected', 'q_count_something', 'q_count_make',
 'q_freq_support', 'q_freq_just', 'q_freq_personal', 'q_freq_to', 'q_freq_healthy', 'q_freq_some', 'q_freq_his', 'q_freq_difference',
 'q_freq_relationship', 'q_freq_feel', 'q_freq_people', 'q_freq_would', 'q_freq_mom', 'q_freq_really', 'q_freq_did',
 'q_freq_she', 'q_freq_there', 'q_freq_discuss', 'q_freq_hope', 'q_freq_level', 'q_freq_months', 'q_freq_)', 'q_freq_knowledge',
 'q_freq_making', 'q_freq_other', 'q_freq_content', 'q_freq_others', 'q_freq_for', 'q_freq_meaning', 'q_freq_advice', 'q_freq_an',
 'q_freq_because', 'q_freq_could', 'q_freq_finally', 'q_freq_life', 'q_freq_get', 'q_freq_enough', 'q_freq_on', 'q_freq_2',
 'q_freq_next', 'q_freq_help', 'q_freq_most', 'q_freq_path', 'q_freq_else', 'q_freq_getting', 'q_freq_joy', 'q_freq_everyone',
 'q_freq_share', 'q_freq_was', 'q_freq_growth', 'q_freq_course', 'q_freq_it', 'q_freq_last', "q_freq_'ve", 'q_freq_best',
 'q_freq_leave', 'q_freq_career', 'q_freq_ago', 'q_freq_through', 'q_freq_skills', 'q_freq_change', 'q_freq_coaching', 'q_freq_grow',
 'q_freq_many', 'q_freq_living', 'q_freq_respect', 'q_freq_longer', 'q_freq_possible', 'q_freq_right', 'q_freq_true', "q_freq_'s",
 'q_freq_connected', 'q_freq_than', 'q_freq_themselves', 'q_freq_while', 'q_freq_!', 'q_freq_shetty', 'q_freq_thought',
 'q_freq_continue', 'q_freq_build', 'q_freq_started', 'q_freq_something', 'q_freq_year', 'q_freq_up', 'q_freq_may',
 'q_freq_old', 'q_freq_make', 'occ_count_manager', 'occ_count_,', 'occ_freq_manager', 'occ_freq_sales', 'occ_freq_/',
 'occ_freq_teacher', 'occ_freq_tech', 'occ_freq_it', 'occ_freq_-', 'occ_freq_coach', 'occ_freq_company', 'occ_freq_,',
 'total_q_counts', 'total_occ_counts', 'total_q_freq', 'total_occ_freq', 'q_freq_grow_growth', 'q_freq_exploring_discovery',
 'numbers_in_phone', 'is_USA_code', 'is_UK_code', 'is_IN_code', 'is_UAE_code', 'is_european_code',
 'phone_code_freq', 'name_spaces', 'name_len', 'shared_email_substring_len', 'shared_email_substring_frac_local',
 'shared_email_substring_frac_name', 'shared_email_substring_frac_geo', 'shared_email_substring_len_domain',
 'shared_email_substring_frac_local_domain', 'shared_email_substring_frac_name_domain', 'shared_email_substring_frac_geo_domain',
 'numbers_in_email', 'frac_numbers_in_email', 'frac_alpha_in_email', 'frac_other_in_email', 'domain_freq',
 'end_domain_freq', 'is_IN_email', 'len_domain', 'len_local', 'fw', 'fw_has_cash', 'non_fw_has_cash', 'maybe_UK', 'maybe_IN',
 'low_income', 'is_sales', 'high_income', 'profession_len_no_ws', 'profession_len', 'has_cash', 'read_b', 'high_income_cash',
 'occ_avg_word_len', 'occ_len', 'occ_alnum_frac', 'occ_stopword_freq', 'q_mention_j', 'q_mention_coach', 'q_avg_word_len',
 'q_len', 'q_lines', 'q_alnum_frac', 'q_unique_word_freq', 'q_stopword_freq', 'avg_len', 'log_geo_avg_len', "len_email",
 "occ_pos-neg", "q_pos-neg"}

COUNTRY_CODES = {
 '1': 5990, '44': 1354, '61': 504, '91': 488, '971': 90, '49': 69, '27': 55, '353': 54, '234': 39, '31': 36,
 '31': 36,'65': 36, '34': 34, '33': 30, '64': 25, '52': 25, '351': 20, '32': 19, '39': 19, '60': 18,
 '63': 18, '92': 15, '47': 14, '57': 14, '40': 13, '46': 13, '977': 12, '41': 12, '254': 12,
 '94': 11, '260': 10, '966': 9, '20': 9, '357': 9, '233': 9, '48': 9, '420': 8, '43': 8,
 '45': 8, '961': 8, '62': 8, '880': 8, '86': 7, '30': 7, '852': 7, '36': 7, '251': 7,
 '256': 7, '66': 7, '90': 6, '974': 6, '55': 5, '962': 5, '56': 5, '255': 5, '81': 5,
 '250': 5, '230': 5, '372': 4, '264': 4, '506': 4, '7': 4, '212': 4, '965': 4, '95': 4,
 '675': 4, '54': 3, '886': 3, '356': 3, '370': 3, '386': 3, '371': 3, '972': 3, '58': 3,
 '84': 2, '358': 2, '261': 2, '352': 2, '855': 2, '509': 2, '592': 2, '213': 2, '973': 2
}

C_TO_CODE = {
 "United States": '1', 'United Kingdom':'44', 'Australia':'61', "India":'91', "United Arab Emirates":'971', 
 "Germany":'49', "South Africa":'27', "Ireland":'353', "Nigeria":'234', 'Netherlands':'31',
 "Singapore":'65', "Spain":'34', "France":'33', "New Zealand":'64', "Mexico":'52', "Portugal":'351', 
 "Belgium":'32', "Italy":'39', "Malaysia":'60',"Philippines":'63', "Pakistan":'92', "Norway":'47', 
 "Colombia":'57', "Romania":'40', "Sweden":'46', "Nepal":'977', "Switzerland":'41', "Somalia":'254',
 "Sri Lanka":'94', "Zambia":'260', "Saudi Arabia":'966', "Egypt":'20', "Cyprus":'357', 
 "Ghana":'233', "Poland":'48', "Czech Republic":'420', "Austria":'43', "Denmark":'45', 
 "Lebanon":'961', "Indonesia":'62', "Bangladesh":'880', "China":'86', "Greece":'30', 
 "Hong Kong":'852', "Hungary":'36', "Ethiopia":'251', "Uganda":'256', "Thailand":'66', 
 "Turkey":'90', "Qatar":'974', "Brazil":'55', "Jordan":'962', "Chile":'56', 'Tanzania':'255',
 "Japan":'81', "Rwanda":'250', 'Mauritius':'230', "Estonia":'372', "Namibia":'264', "Costa Rica":'506', 
 "Russia":'7', "Morocco":'212', "Kuwait":'965', "Myanmar":'95', 'Papua New Guinea':'675', 'Argentina':'54', 
 'Taiwan':'886', "Malta":'356', "Lithuania":'370', "Slovenia":'386', "Latvia":'371', "Israel":'972', 
 "Venezuela":'58',"Vietnam":'84', "Aland Islands":'358', "Madagascar":'261', "Luxembourg":'352', 
 "Cambodia":'855', "Haiti":'509', "Guyana":'592', "Algeria":'213', "Bahrain":'973'}

DOMAIN_ENDINGS = {
    'com': 8701, 'org': 24, 'uk': 267, 'ca': 38, 'edu': 48, 'net': 67, 'at': 2,
    'mx': 3, 'ru': 6, 'co': 6, 'au': 47, 'cz': 3, 'be': 2, 'it': 6, 'de': 24,
    'nz': 4, 'life': 4, 'in': 14, 'xyz': 3, 'tr': 2,'gr': 3, 'pt': 3, 'ie': 3,'club': 2,
    'ae': 2, 'za': 6, 'fr': 14, 'con': 3, 'me': 2, 'health': 2, 'io': 2, 'nl': 5
}

DOMAIN_STARTS = {
    'gmail': 6351, 'yahoo': 876, 'hotmail': 673, 'icloud': 259, 'outlook': 201,
    'aol': 97, 'live': 85, 'me': 57, 'msn': 33, 'ymail': 26, 'comcast': 22, 'mail': 21, 'mac': 16,
    'googlemail': 15, 'gmx': 13, 'protonmail': 13, 'sbcglobal': 10, 'rogers': 10, 'btinternet': 10,
    'bigpond': 8, 'att': 7, 'rocketmail': 7, 'sky': 4, 'curativecollection': 4, 'jeffnicely': 4,
    'sap': 3, 'optonline': 3, 'adclass': 3, 'duck': 3, 'oncehub': 3, 'shaw': 3, 'asu': 3, 'myyahoo': 3,
    'scmail': 3, 'pranichealing': 3, 'smarttstrategies': 3, 'lorma': 3, 'thedogtowncollection': 2,
    'fwtdaily': 2, 'kinluv': 2, 'gruppobe': 2, 'thot': 2, 'cox': 2, 'green-dot': 2,
    'acu': 2, 'go': 2, 'email': 2, 'financialsketchers': 2, 'gkmgroup': 2, 'traya': 2,
    'redfin': 2, 'aim': 2, 'usa': 2, 'avendus': 2, 'roshanak': 2, 'saralarsoncoaching': 2,
    'bu': 2, 'grainco': 2, 'charter': 2, 'aliaxis': 2, 'ucla': 2, 'telus': 2,
    'yourlifeinnovated': 2, 'myself': 2, 'bellin': 2, 'mywellnest': 2, 'freebirdgroup': 2,
    'y7mail': 2, 'itsyourtherapy': 2, 'statmark': 2, 'createyourmark': 2, 'qacps': 2,
    'farrahsit': 2, 'inn-av': 2, 'web': 2, 'moonwatersservices': 2, 'daydreamdesigns': 2,
    'laurako': 2, 'hyros': 2, 'columbia': 2, 'fards': 2, 'allclients': 2, 'campus': 2
}

EU_CODES = {
    "39", "43", "44", "353", "33", "41", "31", "46", "47", "377",
    "354", "49", "358", "382", "43", "352", "45", "423", "56"
}

LONG_Q_WORDS = {
 '!', "'s", "'ve", ')', '2', 'advice', 'ago', 'an', 'around', 'aware', 'because', 'best',
 'build','career', 'certification', 'change', 'coaching', 'connected', 'considered', 'content', 'continue',
 'could', 'course', 'did', 'difference', 'discovery', 'discuss', 'dream', 'else', 'enough', 'everyone',
 'experienced', 'exploring', 'feel', 'finally', 'follow', 'for', 'friends', 'get', 'getting', 'gives',
 'good', 'grow', 'growth', 'guide', 'happy', 'hard', 'heal', 'healthy', 'help', 'his', 'hope',
 'it', 'joy', 'just', 'kind', 'knowledge', 'last', 'leave', 'level', 'life', 'listened', 'living',
 'longer', 'make', 'making', 'many', 'may', 'meaning', 'mental', 'mom', 'months', 'most', 'next',
 'noticed', 'old', 'on', 'other', 'others', 'path', 'people', 'person', 'personal', 'possible',
 'profession', 'put', 'really', 'relationship', 'respect', 'right', 'serving', 'share', 'she',
 'shetty', 'situations', 'skills', 'some', 'something', 'started', 'strong', 'support', 'than',
 'themselves', 'there', 'thought', 'through', 'to', 'true', 'up', 'was', 'while', 'would','year'}

OCC_WORDS = {
 '&', ',', '-', '/', 'coach', 'company', 'coordinator', 'director', 'engineer',
 'entrepreneur', 'for', 'it', 'life', 'manager', 'marketing', 'operations',
 'retired', 'sales', 'senior', 'social', 'software', 'teacher', 'tech', 'yoga', "mom", "mum"
}

LOW_INCOME_WORDS = {
    "unemployed", "student", "between", "disable", "assistant", 
    "stay", "none", "driver", "social w", "teacher", "cna", "nanny",
    "barista", "housekeeper", "wife", "home", "mom", "mum", "n/a",
    "reception", "secretary", "cleanin", "educator", 'labourer' 'nothing',
    "prefer not", "graduate", "homemaker"
}

HIGH_INCOME = {
    "vp", "mba", "coach", "lawyer", "audiologist", "executive", "director", "owner",
    "entrepreneur", "estate", "founder", "attorney", "financial", "consult", "partner", 
    "ceo", "dentist", "doctor", "cfo", "senior", "chief", "portfolio"
}

CREATIVE = {"music", "artist", "paint", "write", "photo", " art", "art ", "design", "sing", }
SALES = {"sales", "business", "marketing", "financ"}
RETIRED = {"retire"}

model = Model("scores_model.pkl", "scores_dist.txt", score=100)

class Featurizer:
    def __init__(self, name, phone, country, email, occ, long_question, cash, read_b, ts):
        self.name = name if len(name) < 2 else "No Name"
        self.phone = phone
        self.country = country
        self.email = email if (len(email) > 2 and "@" in email) else "test123456789@test99.test"
        self.domain = self.email.split("@")[1]
        self.local = self.email.split("@")[0]
        self.q = long_question
        self.cash = cash
        self.ts = ts
        self.occ = occ
        self.read_b = read_b
        self.gen_ts_feats()
        self.gen_occ_feats()
        self.gen_nltk_feats()
        self.gen_name_email_phone_feats()
    
    def gen_occ_feats(self):
        
        no_space_occ = re.sub(" +", "", self.occ)
        occ_split = self.occ.split()
        len_occ_split = len(occ_split)
        q_split = self.q.split()
        len_q_split = len(occ_split)

        self.occ_feats = {
            "low_income": int(any(j.lower() in self.occ.lower() for j in LOW_INCOME_WORDS)),
            "is_sales": int(any(j.lower() in self.occ.lower() for j in SALES)),
            "is_retired": int(any(j.lower() in self.occ.lower() for j in RETIRED)),
            "high_income": int(any(j.lower() in self.occ.lower() for j in HIGH_INCOME)),
            "creative": int(any(j in self.occ for j in CREATIVE)),
            "profession_len_no_ws": len(no_space_occ),
            "profession_len": len(self.occ),
            "has_cash": int(self.cash),
            "read_b": int(self.read_b),
            "high_income_cash": int(self.cash * any(j.lower() in self.occ.lower() for j in HIGH_INCOME)),
            "retired_cash": int(self.cash * any(j.lower() in self.occ.lower() for j in RETIRED)),
            "occ_mention_j": sum(i in self.occ.lower() for i in {"jay", "shetty", "a monk"}),
            "occ_mention_coach": int("coach" in self.occ.lower()),
            "occ_avg_word_len": 0 if len(self.occ) == 0 else sum(len(i) for i in occ_split) / len_occ_split,
            "occ_len": len(self.occ),
            "occ_lines": sum(i=="\n" for i in self.occ),
            "occ_alnum_frac": 0 if len(self.occ) == 0 else sum((j != " ")*(j.isalnum()) for j in self.occ)/len(self.occ),
            "occ_unique_word_freq": get_unique_word_freq(self.occ),
            "occ_stopword_freq": count_stopwords_freq(self.occ),
            "q_mention_j": sum(i in self.q.lower() for i in {"jay", "shetty", "a monk"}),
            "q_mention_coach": int("coach" in self.q.lower()),
            "q_avg_word_len": 0 if len_q_split == 0 else sum(len(i) for i in q_split) / len_q_split,
            "q_len": len(self.q),
            "q_lines": sum(i=="\n" for i in self.q),
            "q_alnum_frac": 0 if len(self.q) == 0 else sum((j != " ")*(j.isalnum()) for j in self.q)/len(self.q),  
            "q_unique_word_freq": get_unique_word_freq(self.q),
            "q_stopword_freq": count_stopwords_freq(self.q),
            "avg_len": (len(self.q) + len(self.occ)) / 2,
            "log_geo_avg_len": -99 if (len(self.occ) == 0 | len(self.q) == 0) else max(-99,np.log(len(self.q) * len(self.occ)))
        }
        
    def gen_name_email_phone_feats(self):
        

        if self.country is None:
            country_code = re.sub("\\D", "", self.phone.split(" (")[0])
        else:
            country_code = C_TO_CODE.get(self.country, "999")
            temp_phone = "".join([i for i in self.phone if i.isdigit()])
            if temp_phone[:len(country_code)] != country_code:
                self.phone = country_code + self.phone

        n_country_codes = sum(COUNTRY_CODES.values())

        len_name, len_local, len_domain = len(self.name), len(self.local), len(self.domain)
        start_dom = self.domain.split(".")[0].lower()
        end_dom = self.domain.split(".")[-1].lower()
        
        n_domain_endings = sum(DOMAIN_ENDINGS.values())
        n_domain_starts = sum(DOMAIN_STARTS.values())
        
        shared_sub_local = largest_shared_substring(
            self.name, self.local
        )
        len_shared_sub_local = len(shared_sub_local)
        
        shared_sub_domain = largest_shared_substring(
            self.name, self.domain
        )
        len_shared_sub_domain = len(shared_sub_domain)
        
        self.name_email_phone_feats = {
            "numbers_in_phone": sum(j.isdigit() for j in self.phone),
            "is_USA_code": 1*(country_code == "1"),
            "is_UK_code": 1*(country_code == "44"),
            "is_IN_code": 1*(country_code == "91"),
            "is_AUS_code": 1*(country_code == "61"),
            "is_UAE_code": 1*(country_code == "971"),
            "is_european_code": 1*(country_code in EU_CODES),
            "phone_code_freq": COUNTRY_CODES.get(country_code,0)/n_country_codes, 
            "name_spaces": sum(j == " " for j in self.name),
            "name_punc": sum((j != " ")*(not j.isalnum()) for j in self.name),
            "name_len": len_name,
            "name_count_upper": sum(j.isupper() for j in self.local),
            "name_count_upper_freq": sum(j.isupper() for j in self.local) / len_local,
            'shared_email_substring_len': len_shared_sub_local, 
            'shared_email_substring_frac_local': len_shared_sub_local/len_name,
            'shared_email_substring_frac_name': len_shared_sub_local/len_local,
            'shared_email_substring_frac_geo' : len_shared_sub_local**2 / (len_name * len_local),
            'shared_email_substring_len_domain': len_shared_sub_domain,
            'shared_email_substring_frac_local_domain' : len_shared_sub_domain/len_name,
            'shared_email_substring_frac_name_domain' : len_shared_sub_domain/len_domain,
            'shared_email_substring_frac_geo_domain' : len_shared_sub_domain**2 / (len_name * len_local),
            'numbers_in_email' : sum(j.isdigit() for j in self.local),
            'frac_numbers_in_email' : sum(j.isdigit() for j in self.local) / len_local,
            'frac_alpha_in_email' : sum(j.isalpha() for j in self.local) / len_local,
            'frac_other_in_email' : sum(1-int(j.isalpha())-int(j.isdigit()) for j in self.local) / len_local,
            'email_is_upper' : sum(j.isupper() for j in self.local) / len_local,
            'domain_freq' : DOMAIN_STARTS.get(start_dom,1)/n_domain_starts, 
            "end_domain_freq": DOMAIN_ENDINGS.get(end_dom,1)/n_domain_endings,
            "periods_in_domain": sum(i=="." for i in self.domain),
            "gmail_domain": int("gmail" in self.domain),
            "yahoo_domain": int("yahoo" in self.domain),
            "icloud_domain": int("icloud" in self.domain),
            "is_UK_email": 1*(self.domain[-3:] == ".uk"),
            "is_CA_email": 1*(self.domain[-3:] == ".ca"),
            "is_AUS_email": 1*(self.domain[-3:] == ".au"),
            "is_HU_email": 1*(self.domain[-3:] == ".hu"),
            "is_IN_email": 1*(self.domain[-3:] == ".in"),
            "is_com_email": 1*(self.domain[-4:] == ".com"),
            "is_org_email": 1*(self.domain[-4:] == ".org"),
            "is_net_email": 1*(self.domain[-4:] == ".net"),
            "is_co_email": 1*(self.domain[-3:] == ".co"),
            "is_edu_email": 1*(self.domain[-4:] == ".edu"),
            "len_email_country": len(self.domain.split(".")[-1]),
            "len_domain": len_domain,
            "len_local": len_local,
            "len_email": 1 + len_local + len_domain
        }
        
        self.name_email_phone_feats["fw"] = 1*(self.name_email_phone_feats["is_USA_code"]+
                                               self.name_email_phone_feats["is_AUS_code"]+
                                               self.name_email_phone_feats["is_UK_code"] > 0)

        self.name_email_phone_feats["fw_has_cash"] = self.name_email_phone_feats["fw"] * self.occ_feats["has_cash"]
        self.name_email_phone_feats["non_fw_has_cash"] = (1 - self.name_email_phone_feats["fw"]) * self.occ_feats["has_cash"]
        self.name_email_phone_feats["maybe_UK"] = ((self.name_email_phone_feats["is_UK_code"] + self.name_email_phone_feats["is_UK_email"]) > 0)*1
        self.name_email_phone_feats["maybe_IN"] = ((self.name_email_phone_feats["is_IN_code"] + self.name_email_phone_feats["is_IN_email"]) > 0)*1
        
        for col in [
            "hour_sin","hour_cos","day_sin","day_cos",
            "week_sin","week_cos","month_sin","month_cos"
        ]:
            self.ts_feats[f"{col}_US"] = self.ts_feats[col] * self.name_email_phone_feats["is_USA_code"]
            self.ts_feats[f"{col}_is_weekend"] = self.ts_feats[col] * self.ts_feats["is_weekend"]
    
    def gen_nltk_feats(self):
        
        occ_nltk = SIA.polarity_scores(self.occ)
        occ_nltk = {f"occ_{i[0]}":i[1] for i in occ_nltk.items()}
        occ_nltk["occ_pos-neg"] = occ_nltk["occ_pos"] - occ_nltk["occ_neg"]
        q_nltk = SIA.polarity_scores(self.q)
        q_nltk = {f"q_{i[0]}":i[1] for i in q_nltk.items()}
        q_nltk["q_pos-neg"] = q_nltk["q_pos"] - q_nltk["q_neg"]
        
        q_tokenized = word_tokenize(self.q.lower())
        q_tokenized_len = max(len(q_tokenized),1)
        occ_tokenized = word_tokenize(self.occ.lower())
        occ_tokenized_len = max(len(occ_tokenized),1)
        
        q_counts = {f"q_count_{i}": len([j for j in q_tokenized if j==i]) for i in LONG_Q_WORDS}
        q_freqs = {f"q_freq_{i}": len([j for j in q_tokenized if j==i])/q_tokenized_len for i in LONG_Q_WORDS}
        occ_counts = {f"occ_count_{i}": len([j for j in occ_tokenized if j==i]) for i in OCC_WORDS}
        occ_freqs = {f"occ_freq_{i}": len([j for j in occ_tokenized if j==i])/occ_tokenized_len for i in OCC_WORDS}
        
        total_counts = {
            "total_q_counts": sum(q_counts.values()),
            "total_occ_counts": sum(occ_counts.values()),
        }
        total_counts["total_q_freq"] = total_counts["total_q_counts"] / q_tokenized_len
        total_counts["total_occ_freq"] = total_counts["total_occ_counts"] / occ_tokenized_len
        
        for d in [("grow", "growth"), ('exploring', 'discovery')]:
            total_counts[f"q_count_{d[0]}_{d[1]}"] = q_counts[f"q_count_{d[0]}"] + q_counts[f"q_count_{d[1]}"]
            total_counts[f"q_freq_{d[0]}_{d[1]}"] = total_counts[f"q_count_{d[0]}_{d[1]}"] / q_tokenized_len

        for d in [("mom", "mum")]:
            total_counts[f"occ_count_{d[0]}_{d[1]}"] = occ_counts[f"occ_count_{d[0]}"] + occ_counts[f"occ_count_{d[1]}"]
            total_counts[f"occ_freq_{d[0]}_{d[1]}"] = total_counts[f"occ_count_{d[0]}_{d[1]}"] / occ_tokenized_len

        self.nltk_feats = {
            **occ_nltk, **q_nltk, **q_counts, **q_freqs, **occ_counts, **occ_freqs, **total_counts
        }
        
    def gen_ts_feats(self):
        
        days_in_month = (self.ts.replace(month = self.ts.month % 12 +1, day = 1)-timedelta(days=1)).day
        
        self.ts_feats = {
            "hour_sin" : np.sin(self.ts.minute / 30 * np.pi),
            "hour_cos" : np.cos(self.ts.minute / 30 * np.pi),
            "day_sin" : np.sin((self.ts.minute + self.ts.hour*60) / 1800 * np.pi),
            "day_cos" : np.cos((self.ts.minute + self.ts.hour*60) / 1800 * np.pi),
            "week_sin" : np.sin((self.ts.minute + self.ts.hour*60 + self.ts.weekday()*60*24) / (60*12*7) * np.pi),
            "week_cos" : np.cos((self.ts.minute + self.ts.hour*60 + self.ts.weekday()*60*24) / (60*12*7) * np.pi),
            "month_sin" : np.sin((self.ts.minute + self.ts.hour*60 + (self.ts.day-1)*60*24) / (60*12*days_in_month) * np.pi),
            "month_cos" : np.cos((self.ts.minute + self.ts.hour*60 + (self.ts.day-1)*60*24) / (60*12*days_in_month) * np.pi),
            "is_weekend" : int(self.ts.weekday() in {5,6})
        }

    def generate_feature_dict(self):
        final_dict = {
            **self.ts_feats, **self.nltk_feats,
            **self.name_email_phone_feats, **self.occ_feats, 
            **self.nltk_feats
        }
        
        return {items[0]: items[1] for items in final_dict.items() if items[0] in FINAL_COLS}
