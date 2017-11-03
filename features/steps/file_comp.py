import pandas as pd
import json, os, re, filecmp, itertools


class f_comp(object):
	"""docstring for file comparison"""


	def __init__(self):
		self.fn = None


	def comp(self, date, timestamp, resultsfiles_loc, datafiles_names):

		pass_file_list = os.listdir(resultsfiles_loc+"Pass"+"/")
		fail_file_list = os.listdir(resultsfiles_loc+"Failed"+"/")
		result_line = {}

		current_files_passfolder, current_files_failfolder = [], []
		result_line = []

		try:
			for file in datafiles_names:
				client_file_name = file.rsplit("/", 1)[1]
				if client_file_name in pass_file_list:
					file_name = client_file_name.rsplit(timestamp, 1)[0]
					for pass_file in pass_file_list:
						if re.search(str(file_name), pass_file):
							current_files_passfolder.append(pass_file)
					for fail_file in fail_file_list:
						if re.search(str(file_name), fail_file):
							current_files_failfolder.append(fail_file)
						
					if len(current_files_passfolder) > 1:
						for a, b in itertools.combinations(current_files_passfolder, 2):
							line = filecmp.cmp(resultsfiles_loc+"Pass"+"/"+a, resultsfiles_loc+"Pass"+"/"+b)
							if line == False:
								result_line.append(a+"--"+b+":"+"The two files are different")
							else:
								result_line.append(a+"--"+b+":"+"The two files are similar")
					else:
						result_line.append("There are no other timestamp files to be compared to "+client_file_name+" in the Pass folder")
				else:
					result_line.append(client_file_name+" passed for first time")
			
			with open(resultsfiles_loc+"SUMMARY_FILE_"+timestamp+".json", 'w') as f2:
				json.dump(result_line, f2, indent=4)
			f2.close()
		except Exception as err:
			print("Encountered error: "+err)
	
		