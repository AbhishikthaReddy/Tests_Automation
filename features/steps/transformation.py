import pandas as pd
import re, json, csv
from collections import OrderedDict
import re, json, csv

class scenario(object):

	def __init__(self):
		self.fn = None

	def seperator_value(def_file_name):

		sep_value = pd.read_json(def_file_name)
		sep_value = sep_value.fieldseparator.ix[0]
		return sep_value

	# column names validation

	def column_names(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			line1 = []
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				client_file_data_columns_list = list(client_file_data.columns)
				client_file_data_columns_list_case_sensitive = [i.lower() for i in client_file_data_columns_list]
				json_def_data_columns_list = (list(json_def_data["columns"]))
				json_def_data_columns_list_case_sensitive = [i.lower() for i in json_def_data_columns_list]

				if len(set(client_file_data_columns_list_case_sensitive).intersection(json_def_data_columns_list_case_sensitive)) == len(json_def_data_columns_list_case_sensitive):

					line1.append({"Test name": "Column names", "Result": "Passed", "File-name": client_file_name})
				else:
					line1.append({"Test name": "Column names", "Result": "Failed", 
							 "Output": {"The expected columns are": list(json_def_data_columns_list)}, 
							 "but the columns in partner file are": list(client_file_data_columns_list), "File-name": client_file_name_split})

		except Exception as err:
			print("Encountered error at column-names scenario: "+str(err))

		return line1

	# column order validation

	def column_order(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				client_file_data_columns_list = list(client_file_data.columns)
				client_file_data_columns_list_case_sensitive = [i.lower() for i in client_file_data_columns_list]
				json_def_data_columns_list = (list(json_def_data["columns"]))
				json_def_data_columns_list_case_sensitive = [i.lower() for i in json_def_data_columns_list]
				json_def_data_columns = (json_def_data["columns"])
				def_col, pass_list, fail_list = {}, {}, {}

				for index, col in enumerate(json_def_data_columns_list):
					if int(json_def_data_columns[col]['order']) <= len(client_file_data_columns_list):
						def_col[int(json_def_data_columns[col]['order']) - 1] = col
						def_col.update(def_col)
				if len(def_col.keys()) != len(client_file_data_columns_list_case_sensitive):
					fail_list[-1000] = "Length of the columns doesn't match and the columns present in partner files are"
					for i in range(len(client_file_data_columns_list_case_sensitive)):
						fail_list[i] = str(client_file_data_columns_list_case_sensitive[i])
				else:
					for i in def_col:
						if str(def_col[i]).lower() == str(client_file_data_columns_list_case_sensitive[i]):
							pass_list[i] = str(def_col[i])
						else:
							fail_list[i] = str(def_col[i])
				if len(fail_list) != 0:

					line2 = {"Test name": "Column order", "Result": "Failed",
							 "Output": {"the expected column order is": list(def_col.values())},
							 "but the partner file has these columns with wrong order": list(fail_list.values()), "File-name": client_file_name_split}

				else:
					line2 = {"Test name": "Column order", "Result": "Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error at column-names scenario: "+str(err))

		return line2

	def null_values(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				client_file_data_columns_list = list(client_file_data.columns)
				client_file_data_columns_list_case_sensitive = [i.lower() for i in client_file_data_columns_list]
				json_def_data_columns_list = (list(json_def_data["columns"]))
				json_def_data_columns_list_case_sensitive = [i.lower() for i in json_def_data_columns_list]

				client_file_data_df = pd.DataFrame(client_file_data)
				client_file_data_df.index=client_file_data_df.index+1

				json_def_data_columns_list_no_orderdict = (json_def_data_no_orderdict["columns"])
				json_def_data_columns_list_index = (list(json_def_data_no_orderdict["columns"].index))

				datatype_col, datatype_col_new = {}, {}

				for index, col in enumerate(json_def_data_columns_list_index):
					datatype_col[col] = json_def_data_columns_list_no_orderdict[col]['allowempty']

				datatype_col_new = {k:v for k,v in datatype_col.items() if v == 'No'}

				client_file_data_df = client_file_data_df[list(datatype_col_new.keys())]

				client_file_data_dff2 = client_file_data_df.isnull().stack()[lambda x: x].index.tolist()

				if (client_file_data_df.isnull().sum().sum()):
					dict1={}
					output1 = client_file_data_dff2
					for value,columns in output1:
						if columns in dict1.keys():
							b=dict1.get(columns)
							b.append(value)
							dict1[columns]=b
						else:
							y = []
							y.append(value)
							dict1[columns]=y
					line3 = {"Test name": "Check for nulls", "Result": "Failed/Nulls are found",
							 "Null values found in": str(dict1).replace('],',']],').replace('{','').replace('}','').replace("'","").split('],'), "File-name": client_file_name_split}
				else:
					line3 = {"Test name": "Check for nulls", "Result": "Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error at null-values scenario: "+str(err))

		return line3

	def empty_rows(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)
				i = 1
				matches = {}
				empty_rows_list = []

				with open(client_file,'r') as out:
					for line in out:
						if line == '\n':
							matches[i] = "matched"
							matches.update(matches)

						elif ''.join(line.split(',')).strip() == '':
							matches[i] = "matched"
							matches.update(matches)
						elif len(line) == 3:
							matches[i] = "matched"
							matches.update(matches)
						else:
							matches[i] = "not matched"
							matches.update(matches)
						i = i +1

				key = list(matches.keys())
				val = list(matches.values())
				for i in range(len(val)):
					if val[i] == "matched":
						empty_rows_list.append("The file has empty row at "+str(key[i]))

				if len(empty_rows_list) != 0:
					line4 = {"Test name": "Empty Rows", "Result": "Failed", "Output": empty_rows_list, "File-name": client_file_name_split}
				else:
					line4 = {"Test name": "Empty Rows", "Result": "Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error at empty-rows scenario: "+str(err))

		return line4

	def data_type(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				client_file_data_columns_list = list(client_file_data.columns)
				client_file_data_columns_list_case_sensitive = [i.lower() for i in client_file_data_columns_list]
				json_def_data_columns_list_no_orderdict = (json_def_data_no_orderdict["columns"])
				json_def_data_columns_list_index = (list(json_def_data_no_orderdict["columns"].index))

				datatype_col = {}

				result_fail_list, column_pass_list, column_fail_list = [], [], []

				datatype_col_rename = {'INT' : 'int64', 'int' : 'int64', 'BIGINT' : 'int64', 'SMALLINT' : 'int64', 'NVARCHAR(50)' : 'str', 'CHAR(8)' : 'str', 'DECIMAL(18,2)' : 'float64' , 'BIT' : 'bool_',  'DECIMAL(18,4)' : 'float64', 'CHAR(2)' : 'str', 'VARCHAR(10)' : 'str', 'CHAR(1)' : 'str','VARCHAR(50)':'str', 'DATE' : 'date', 'NVARCHAR(3)' : 'str', 'NVARCHAR(500)' : 'str', 'NVARCHAR(100)' : 'str', 'NVARCHAR(250)' : 'str', 'NVARCHAR(255)' : 'str', 'NVARCHAR(255)' : 'str', 'NVARCHAR(25)' : 'str', 'NVARCHAR(3000)' : 'str', 'NVARCHAR(40)' : 'str', 'NVARCHAR(20)' : 'str', 'NVARCHAR(10)' : 'str', 'NVARCHAR(1000)' : 'str'}

				for index, col in enumerate(json_def_data_columns_list_index):
					datatype_col[col] = json_def_data_columns_list_no_orderdict[col]['dbtype']
					datatype_col.update(datatype_col)

				dict3 = {k:datatype_col_rename[v] for k,v in datatype_col.items()}
				i = 0
				for column in client_file_data_columns_list:
					if column in dict3.keys():
						for val in client_file_data[column]:
							if str(val) == "nan" or type(val).__name__ == dict3[column]:
								column_pass_list.append(column)
							else:
								column_fail_list.append(column)
								result_fail_list.append("the value "+ str(val) + " at row "+ str(i) + " in column "+str(column)+" doesn't match with datatype "+datatype_col[column])
							i = i + 1

				if len(set(column_pass_list)) == len(dict3.keys()):
					line5 = {"Test name": "Data type", "Result": "Passed"}
				elif len(client_file_data) == 0:
					line5 = {"Test name": "Data type", "Result": "Failed", "Output": "File doesn't have any data", "File-name": client_file_name_split}
				else:
					line5 = {"Test name": "Data type", "Result": "Failed", "Output": result_fail_list, "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in data-type scenario: "+str(err))

		return line5

	def row_count(self, datafiles_names, deffiles_names, row_count_file, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)
				row_count_file_data = pd.read_csv(row_count_file, sep=field_separator)

				if str(client_file_name) in list(row_count_file_data['FileName']):

					if int((row_count_file_data[row_count_file_data['FileName'] == client_file_name]['NumberOfRows'].iloc[0])) != int(len(client_file_data)):
						line6 = {"Test name": "Row count", "Result": "Failed", "Output": "The partner file has "+str(int(row_count_file_data.ix(client_file_name)[0]['NumberOfRows']))+" rows but row count file has "+str(int(len(client_file_data)))}
					else:
						line6 = {"Test name": "Row count", "Result": "Passed", "File-name": client_file_name_split}

				else:
					line6 = {"Test name": "Row count", "Result": "Failed", "Output": "Filename not present in Row count file", "File-name": client_file_name_split}
		except Exception as err:
			print("Encountered error in row-count scenario: "+str(err))

		return line6

	def summary_data(self, datafiles_names, deffiles_names, summary_invalid_file, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)
				summary_invalid_data = pd.read_csv(summary_invalid_file, sep=field_separator)

				if str(client_file_name) in list(summary_invalid_data['FileName']):

					if summary_invalid_data.ix(client_file_name)[0]['Aggregation-type'] == 'count':

						if int(len(client_file_data[str(summary_invalid_data[summary_invalid_data['FileName'] == str(client_file_name)]['Column-names'].iloc[0])])) == int(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Assertion-value'].iloc[0]):

							line7 = {"Test name": "Summary Data check", "Result": "Passed", "Output": client_file_name+" with "+ str(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Column-names'].iloc[0])+" column has passed"}
						else:
							line7 = {"Test name": "Summary Data check", "Result": "Failed", "Output": client_file_name+" with "+str(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Column-names'].iloc[0])+" column has not passed the count assertion"}

					elif summary_invalid_data.ix(client_file_name)[0]['Aggregation-type'] == 'sum':

						if int(sum(client_file_data[str(summary_invalid_data[summary_invalid_data['FileName'] == str(client_file_name)]['Column-names'].iloc[0])])) == int(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Assertion-value'].iloc[0]):

							line7 = {"Test name": "Summary Data check", "Result": "Passed", "Output": client_file_name+" with "+ str(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Column-names'].iloc[0])+" column has passed"}
						else:
							line7 = {"Test name": "Summary Data check", "Result": "Failed", "Output": client_file_name+" with "+str(summary_invalid_data[summary_invalid_data['FileName'] == client_file_name]['Column-names'].iloc[0])+" column has not passed the count assertion"}
					else:
						line7 = {"Test name": "Summary Data check", "Result": "Failed"}

			else:
				line7 = {"Test name": "Summary Data check", "Result": "Failed", "Output": "Filename not present in Summary Data File", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in summary-data scenario: "+str(err))

		return line7

	def data_formats(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				pass_list_df, fail_list_df, list_regex=[], [], []
				json_def_data_columns = (json_def_data["columns"])
				json_def_data_columns_list = (list(json_def_data["columns"]))
				client_file_data_columns_list = list(client_file_data.columns)

				for col in json_def_data_columns_list:
					regex = json_def_data_columns[col]['data-format']
					list_regex.append(regex)


				for column in client_file_data_columns_list:
					count = 0
					i = (client_file_data_columns_list.index(column))
					for row in client_file_data[column]:
						count = count + 1
						if list_regex[i] != "":
							if row!="nan":
								pattern = re.compile(list_regex[i],re.UNICODE)
								if pattern.findall(str(row)):
									pass_list_df.append(str(row))
								else:
									fail_list_df.append("Data format is invalid at row:{},column:{}".format(str(row),column))
							else:
								fail_list_df.append("Data format is invalid at row:{},column:{}".format(str(row),column))
						else:
							pass_list_df.append("Data format is not defined for this column:{}".format(column))
							break


				if len(fail_list_df) > 0:
					line8={"Test name": "Data Formats", "Result": "Failed", "Output":fail_list_df, "File-name": client_file_name_split}
				else:
					line8={"Test name": "Data Formats", "Result": "Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in creating data-formats: "+str(err))

		return line8

	def duplicate_values(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				result_dup_list=[]

				client_file_data_df = pd.DataFrame(client_file_data)
				client_file_data_df.index=client_file_data_df.index+1

				dupff = client_file_data_df[client_file_data_df.duplicated(keep='first')]
				row_number = dupff.index+1
				if len(dupff)>0:
					result_dup_list.append("Duplicate row is found in row number:"+str(row_number.tolist()))
					line9 = {"Test name": "Duplicate values", "Result":"Failed","Output":result_dup_list, "File-name": client_file_name_split}
				else:
					line9 = {"Test name":"Duplicate values", "Result":"Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in creating duplicate-values: "+str(err))

		return line9

	def special_characters(self, datafiles_names, deffiles_names, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)

				client_file_data_columns_list = list(client_file_data.columns)
				pass_list3, result_fail_list1 = [], []

				for column in client_file_data_columns_list:
					p=1
					for val in client_file_data[column]:
						if any(char in str(val) for char in ("~", "%", "*", "+", "&","\"","~","`","!","@","#","$","^","(",")","_","-","=","[","]","{","}",":",">",";","'",",","<","/","?")):
							result_fail_list1.append("Special character " + str(val)+ " is found at row " + str(p) + " in " +  str(column))
						else:
							pass_list3.append(column)
						p = p + 1

				if len(result_fail_list1) > 0:
					line10 = {"Test name": "Special characters", "Result": "Failed", "Output": result_fail_list1, "File-name": client_file_name_split}
				else:
					line10 = {"Test name": "Special characters", "Result": "Passed", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in creating duplicate-values: "+str(err))

		return line10

	def invalid_values(self, datafiles_names, deffiles_names, summary_invalid_file, field_separator, resultsfilelocation, today_now):

		try:
			for i in range(0, len(datafiles_names)):

				client_file = datafiles_names[i]
				json_def = deffiles_names[i]
				sep_value = scenario.seperator_value(json_def)
				client_file_name = client_file.rsplit("/", 1)[1]

				json_def_name = json_def.split('/')[1]
				client_file_name_split = client_file_name[-len(client_file_name):-4]

				client_file_data = pd.read_csv(client_file, sep=sep_value)
				json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
				json_def_data_no_orderdict = pd.read_json(json_def)
				summary_invalid_data = pd.read_csv(summary_invalid_file, sep=field_separator)

				range_fail_list, values_fail_list = [], []

				if client_file_name in list(summary_invalid_data['FileName']):
					
					invalid_values = summary_invalid_data[summary_invalid_data['FileName'] == str(client_file_name)]['Invalid-values'].iloc[0]

					invalid_values = invalid_values.split(",")
					invalid_values_list, new_invalid_values_list = [], []
					min_value, max_value = 0, 0

					for i in invalid_values:
						i = i.replace(" ", "")
						invalid_values_list.append(i)

					for i in invalid_values_list:
						if re.search("-", i):
							min_value = int(i.split("-", 1)[0].split("[", 1)[1])
							max_value = int(i.split("-", 1)[1].split(",", 1)[0])
						elif re.search("]", i):
							i = i.split("]", 1)[0]
							new_invalid_values_list.append(int(i))
						else:
							i = i.replace("[", "")
							new_invalid_values_list.append(int(i))

					data_to_be_check = list(client_file_data[str(summary_invalid_data[summary_invalid_data['FileName'] == str(client_file_name)]['Column-names'].iloc[0])])

					for i in data_to_be_check:
						if min_value > 0 and max_value > 0 and i in range(min_value, max_value):
							range_fail_list.append(i)
						else:
							for j in new_invalid_values_list:
								if i == j:
									values_fail_list.append(i)

					if len(range_fail_list) == 0 and len(values_fail_list) == 0:
						line11 = {"Test name": "Invalid-values", "Result": "Passed", "File-name": client_file_name_split}
					elif len(range_fail_list) > 0:
						line11 = {"Test name": "Invalid-values", "Result": "Failed", "Output": "The values "+str(range_fail_list)+" are not in the defined range", "File-name": client_file_name_split}
					else:
						line11 = {"Test name": "Invalid-values", "Result": "Failed", "Output": "The values "+str(values_fail_list)+" exist in the partner file", "File-name": client_file_name_split}
				else:
					line11 = {"Test name": "Invalid-values", "Result": "Failed", "Output": "The FileName not present in data file", "File-name": client_file_name_split}

		except Exception as err:
			print("Encountered error in creating duplicate-values: "+str(err))

		return line11


	def result(self, line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, resultsfilelocation, today_now):

		try:
			text_file_pass = resultsfilelocation + "/" + "Pass/"
			text_file_fail = resultsfilelocation + "/" + "Failed/"
			text_file_result = resultsfilelocation + "/" + "Result/" + client_file_name_split + "_" + today_now + ".json"
			pass_fail_control_file = resultsfilelocation + "/" + "Summary_Result/"

			# creating a json output file in result folder

			# with open(text_file_result, "a") as output:
			# 	json.dump(final_lines_to_file, output, indent=2)
			# output.close()

		except Exception as err:
			print("Encountered error in creating result-files: "+str(err))