import pandas as pd
from pathlib import Path
import json
import os, glob, re
import filecmp


class f_comp(object):
	"""docstring for file comparison"""


	def __init__(self):
		self.fn = None


	def comp(self, date, timestamp, resultsfiles_loc, datafiles_names):

		pass_file_list = os.listdir(resultsfiles_loc+"Pass"+"/")
		fail_file_list = os.listdir(resultsfiles_loc+"Failed"+"/")
		result_line = {}

		results_file = pd.read_csv(resultsfiles_loc+"File_comp/files_result.txt", names=['Filename', 'Result'], header=None, sep="|")

		
		for file in datafiles_names:
			file_name = file.rsplit("/", 1)[1]
			file_name_split = file_name.rsplit(timestamp, 1)[0]

			if len(pass_file_list) > 0 or len(fail_file_list) > 0:
				if len(pass_file_list) > 0:
					for pass_file in pass_file_list:
						if re.search(str(file_name_split), pass_file):
							print("file has passed before")

							if str(file_name_split) == str(pass_file):
								print("The file ")
				elif len(fail_file_list) > 0:
					for fail_file in fail_file_list:
						if re.search(str(file_name_split), pass_file):
							print("file has FAILED before")

				else:
					result_line = ["There are no passed files to make the comparison"]
			else:
				result_line = ["There are no files to make the comparison"]

		with open(resultsfiles_loc+"SUMMARY_FILE.json", 'a') as f2:
			json.dump(result_line, f2, indent=4)
		f2.close()