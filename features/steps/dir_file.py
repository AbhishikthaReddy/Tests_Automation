import pandas as pd
import glob, os, datetime
from datetime import date
import shutil

class dir_create(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None

	def dir(self, resultsfilelocation):
		mydir_pass = os.path.join(resultsfilelocation, "Pass")
		mydir_fail = os.path.join(resultsfilelocation, "Failed")
		mydir_result = os.path.join(resultsfilelocation, "Result")
		mydir_summary_result = os.path.join(resultsfilelocation, "Summary_Result")
		if not os.path.exists(mydir_pass):
		    os.makedirs(mydir_pass)

		if not os.path.exists(mydir_fail):
		    os.makedirs(mydir_fail)

		if not os.path.exists(mydir_result):
		    os.makedirs(mydir_result)

		if not os.path.exists(mydir_summary_result):
		    os.makedirs(mydir_summary_result)

		return  mydir_pass, mydir_fail, mydir_result, mydir_summary_result
