import pickle
import numpy as np
from sklearn.preprocessing import QuantileTransformer

COLS_ORDER = [
'avg_len', 'day_cos', 'day_cos_US', 'day_cos_is_weekend', 'day_sin', 'day_sin_US', 
'day_sin_is_weekend', 'domain_freq', 'end_domain_freq', 'frac_alpha_in_email', 
'frac_numbers_in_email', 'frac_other_in_email', 'fw', 'fw_has_cash', 'has_cash', 'high_income', 
'high_income_cash', 'hour_cos', 'hour_cos_US', 'hour_cos_is_weekend', 'hour_sin', 'hour_sin_US', 
'hour_sin_is_weekend', 'is_IN_code', 'is_IN_email', 'is_UAE_code', 'is_UK_code', 'is_USA_code', 
'is_european_code', 'is_sales', 'len_domain', 'len_local', 'log_geo_avg_len', 'low_income', 
'maybe_IN', 'maybe_UK', 'month_cos', 'month_cos_US', 'month_cos_is_weekend', 'month_sin', 
'month_sin_US', 'month_sin_is_weekend', 'name_len', 'name_spaces', 'non_fw_has_cash', 
'numbers_in_email', 'numbers_in_phone', 'occ_alnum_frac', 'occ_avg_word_len', 'occ_compound', 
'occ_count_,', 'occ_count_manager', 'occ_freq_,', 'occ_freq_-', 'occ_freq_/', 'occ_freq_coach', 
'occ_freq_company', 'occ_freq_it', 'occ_freq_manager', 'occ_freq_sales', 'occ_freq_teacher', 
'occ_freq_tech', 'occ_len', 'occ_neu', 'occ_pos', 'occ_stopword_freq', 'phone_code_freq', 
'profession_len', 'profession_len_no_ws', 'q_alnum_frac', 'q_avg_word_len', 'q_compound', 
"q_count_'s", "q_count_'ve", 'q_count_)', 'q_count_an', 'q_count_because', 'q_count_career', 
'q_count_coaching', 'q_count_connected', 'q_count_everyone', 'q_count_feel', 'q_count_for', 
'q_count_getting', 'q_count_help', 'q_count_it', 'q_count_life', 'q_count_living', 
'q_count_make', 'q_count_months', 'q_count_most', 'q_count_on', 'q_count_other', 
'q_count_others', 'q_count_path', 'q_count_people', 'q_count_something', 'q_count_through', 
'q_count_to', 'q_count_was', 'q_count_would', 'q_freq_!', "q_freq_'s", "q_freq_'ve", 'q_freq_)', 
'q_freq_2', 'q_freq_advice', 'q_freq_ago', 'q_freq_an', 'q_freq_because', 'q_freq_best', 
'q_freq_build', 'q_freq_career', 'q_freq_change', 'q_freq_coaching', 'q_freq_connected', 
'q_freq_content', 'q_freq_continue', 'q_freq_could', 'q_freq_course', 'q_freq_did', 
'q_freq_difference', 'q_freq_discuss', 'q_freq_else', 'q_freq_enough', 'q_freq_everyone', 
'q_freq_exploring_discovery', 'q_freq_feel', 'q_freq_finally', 'q_freq_for', 'q_freq_get', 
'q_freq_getting', 'q_freq_grow', 'q_freq_grow_growth', 'q_freq_growth', 'q_freq_healthy', 
'q_freq_help', 'q_freq_his', 'q_freq_hope', 'q_freq_it', 'q_freq_joy', 'q_freq_just', 
'q_freq_knowledge', 'q_freq_last', 'q_freq_leave', 'q_freq_level', 'q_freq_life', 
'q_freq_living', 'q_freq_longer', 'q_freq_make', 'q_freq_making', 'q_freq_many', 'q_freq_may', 
'q_freq_meaning', 'q_freq_mom', 'q_freq_months', 'q_freq_most', 'q_freq_next', 'q_freq_old', 
'q_freq_on', 'q_freq_other', 'q_freq_others', 'q_freq_path', 'q_freq_people', 'q_freq_personal', 
'q_freq_possible', 'q_freq_really', 'q_freq_relationship', 'q_freq_respect', 'q_freq_right', 
'q_freq_share', 'q_freq_she', 'q_freq_shetty', 'q_freq_skills', 'q_freq_some', 
'q_freq_something', 'q_freq_started', 'q_freq_support', 'q_freq_than', 'q_freq_themselves', 
'q_freq_there', 'q_freq_thought', 'q_freq_through', 'q_freq_to', 'q_freq_true', 'q_freq_up', 
'q_freq_was', 'q_freq_while', 'q_freq_would', 'q_freq_year', 'q_len', 'q_lines', 
'q_mention_coach', 'q_mention_j', 'q_neg', 'q_neu', 'q_pos', 'q_stopword_freq', 
'q_unique_word_freq', 'read_b', 'shared_email_substring_frac_geo', 
'shared_email_substring_frac_geo_domain', 'shared_email_substring_frac_local', 
'shared_email_substring_frac_local_domain', 'shared_email_substring_frac_name', 
'shared_email_substring_frac_name_domain', 'shared_email_substring_len', 
'shared_email_substring_len_domain', 'total_occ_counts', 'total_occ_freq', 'total_q_counts', 
'total_q_freq', 'week_cos', 'week_cos_US', 'week_cos_is_weekend', 'week_sin', 'week_sin_US', 
'week_sin_is_weekend',"len_email", "occ_pos-neg", "q_pos-neg"
]

class Model:
	def __init__(self, filename, dist_filename, score=100):

		with open(filename, 'rb') as f:
			self.model = pickle.load(f)
		with open(dist_filename, 'r') as f:
			self.dist = np.array([float(line.strip()) for line in f]).reshape(-1,1)

		self.transformer = QuantileTransformer(
			n_quantiles=1000, output_distribution='uniform', random_state=0
		)
		self.score=score
		self.transformer.fit(self.dist)
	
	def predict(self, data):
		
		score = self.model.predict_proba(
			[[data[f][col] for col in COLS_ORDER] for f in range(len(data))]
		)[:,1]

		if score.shape == (1,):
			return score[0], int(self.score * self.transformer.transform(np.array([[score[0]]]))[0,0])
		else:
			return list(score), list((self.score * self.transformer.transform(score.reshape(-1, 1))[:,0]).astype(int))
