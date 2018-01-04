import pandas as pd
import os, fnmatch
from dir_file import dir_create
import re

class retrieve_files(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None


	def path(self, p):
		if os.path.isabs(p):
			return p
		else:
			return os.path.join(os.getcwd(), p)


	def files(self, date, masterfile_loc, resultsfilelocation, timestamp):
		try:
			masterfile = pd.read_json(masterfile_loc)
			control_def_file_loc = self.path(masterfile.controlfile.ix[0])
			data_file_loc = self.path(masterfile.datafilelocation.ix[0])
			text_files = masterfile.files
			these_files = {}

			row_count_file=''
			summary_invalid_file=''
			data_files_all = os.listdir(data_file_loc)
			for file in data_files_all:
				if re.search("kab_row_count_", file):
					if re.search(date, file):
						row_count_file = os.path.join(data_file_loc, file)
			for file in data_files_all:
				if re.search("kab_summary_data_", file):
					if re.search(date, file):
						summary_invalid_file = os.path.join(data_file_loc, file)

			field_separator = masterfile.fieldseparator.ix[0]


			for i in range(0, len(text_files)):
				a = text_files.index[i]
				b = str(text_files[a]['filename'])

				for file in os.listdir(data_file_loc):
					fn = '_'.join([b, date, timestamp])
					if file.startswith(fn) and file.endswith(('.txt', '.csv')):
						these_files[file] = text_files[a]['filedeffile']

			datafiles_names, deffiles_names = zip(*these_files.items())
			return datafiles_names, deffiles_names, row_count_file, summary_invalid_file, field_separator
		except:
			raise
			print("MasterJSON File Not Found in the specified path")
