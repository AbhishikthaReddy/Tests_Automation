import pandas as pd, os, re
from dir_file import dir_create

class retrieve_files(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None


	def files(self, date, masterfile_loc,resultsfilelocation, timestamp):
		try:
			masterfile = pd.read_json(masterfile_loc)
			control_def_file_loc = masterfile.controlfile.ix[0]
			data_file_loc = masterfile.datafilelocation.ix[0]
			text_files = masterfile.files
			datafiles_names = []
			deffiles_names = []
			data_files_all = os.listdir(data_file_loc+"/")
			for file in data_files_all:
				if re.search("kab_row_count_", file):
					if re.search(date, file):
						row_count_file = data_file_loc+"/"+file
			for file in data_files_all:
				if re.search("kab_summary_data_", file):
					if re.search(date, file):
						summary_invalid_file = data_file_loc+"/"+file

			field_separator = masterfile.fieldseparator.ix[0]

			for i in range(0, len(text_files)):
				file_index = text_files.index[i]
				filename_master_json = str(text_files[file_index]['filename'])
				filedef_master_json = str(text_files[file_index]['filedeffile'])
				if filename_master_json+"_"+date+"_"+timestamp+".txt" in data_files_all:
					datafiles_names.append(data_file_loc+"/"+filename_master_json+"_"+date+"_"+timestamp+".txt")
					deffiles_names.append(filedef_master_json)
				if filename_master_json+"_"+date+"_"+timestamp+".csv" in data_files_all:
					datafiles_names.append(data_file_loc+"/"+filename_master_json+"_"+date+"_"+timestamp+".csv")
					deffiles_names.append(filedef_master_json)
			return datafiles_names, deffiles_names, row_count_file, summary_invalid_file, field_separator
		except:
			print("MasterJSON File Not Found in the specified path")
