import pandas as pd
import os, fnmatch
from dir_file import dir_create
import re

class retrieve_files(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None
		

	def files(self, date, masterfile_loc,resultsfilelocation, timestamp):
		try:
			masterfile = pd.read_json(masterfile_loc)
			control_def_file_loc = masterfile.controlfile.ix[0]
			data_file_loc = masterfile.datafilelocation.ix[0]
			# control_data_file = data_file_loc+"/"+"kab_control_"+date+".txt"
			text_files = masterfile.files
			datafiles_names = []
			deffiles_names = []
			data_files_all = os.listdir(data_file_loc+"/")

			for i in range(0, len(text_files)):
				a = text_files.index[i]
				b = str(text_files[a]['filename'])
				c = str(text_files[a]['filedeffile'])
				if b+"_"+date+"_"+timestamp+".txt" in data_files_all:
					datafiles_names.append(data_file_loc+"/"+b+"_"+date+"_"+timestamp+".txt")
					deffiles_names.append(c)
				if b+"_"+date+"_"+timestamp+".csv" in data_files_all:
					datafiles_names.append(data_file_loc+"/"+b+"_"+date+"_"+timestamp+".csv")
					deffiles_names.append(c)
			return datafiles_names, deffiles_names, control_def_file_loc
		except:
			print("MasterJSON File Not Found in the specified path")
