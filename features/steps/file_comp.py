import pandas as pd
from pathlib import Path
import json
import os, glob, re
import filecmp


class f_comp(object):
	"""docstring for file comparison"""


	def __init__(self):
		self.fn = None


	def comp(self, date, timestamp, resultsfiles_loc):

		pass_file_list = os.listdir(os.path.join(resultsfiles_loc, "Pass"))
		fail_file_list = os.listdir(os.path.join(resultsfiles_loc, "Failed"))
		result_line, pass_dict, fail_dict = {}, {}, {}
		for pass_file in range(0, len(pass_file_list)):
			file_name = pass_file_list[pass_file].rsplit(date, 1)[0]
			for file in pass_file_list:
				if re.search(str(file_name), file):
					pass_dict[pass_file_list[pass_file]] = file

		for fail_file in range(0, len(fail_file_list)):
			file_name = fail_file_list[fail_file].rsplit(date, 1)[0]
			for file in pass_file_list:
				if re.search(str(file_name), file):
					fail_dict[fail_file_list[fail_file]] = file


		pass_dict = { k:v for k,v in pass_dict.items() if k!=v }
		fail_dict = { k:v for k,v in fail_dict.items() if k!=v }
		if len(pass_dict) > 0:
			for key, value in pass_dict.items():
				line = filecmp.cmp(os.path.join(resultsfiles_loc, "Pass", key),
                                                   os.path.join(resultsfiles_loc, "Pass", value))
				if line == "False":
					result_line[key] = ["The file is different from the Previous created file"]
				else:
					result_line[key] = ["The file has no conflicts"]
			if len(fail_dict) > 0:
				result_line[key] = ["The file has passed before but failed now"]
		else:
			result_line = ["The current passed files doesn't have any other timestamp files to compare to"]

		with open(resultsfiles_loc+"SUMMARY_FILE.json", 'a') as f2:
			json.dump(result_line, f2, indent=4)
		f2.close()
