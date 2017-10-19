from datetime import date
import pandas as pd
import glob, os, datetime, re
import pypyodbc
import json
from collections import OrderedDict



class scenario(object):


    def __init__(self):
        self.fn = None

    # def control_file_values(control_file, sep_value):

    # 	temp = pd.read_csv(control_file, sep='|')
    # 	df = pd.DataFrame()
    # 	df['NumberOfRows'] = temp['FileName'].apply(lambda x: x.split(sep_value)[1])
    # 	df['FileName'] = temp['FileName'].apply(lambda x: x.split(sep_value)[0])
    # 	df = df.groupby('FileName').sum()
    # 	return df


    def seperator_value(def_file_name):

        sep_value = pd.read_json(def_file_name)
        sep_value = sep_value.fieldseparator.ix[0]
        return sep_value

    def scenario_writing_to_files(self, resultsfilelocation, datafiles_names, deffiles_names, control_def_file_loc,
                                  date, timestamp):

        control_file_sep_value = scenario.seperator_value(control_def_file_loc)
        # control_file = scenario.control_file_values(control_file, control_file_sep_value)

        final_lines_to_file = {}
        pass_control_file_data, fail_control_file_data = [], []

        for i in range(0, len(datafiles_names)):

            client_file = datafiles_names[i]
            json_def = deffiles_names[i]
            sep_value = scenario.seperator_value(json_def)
            client_file_name = client_file.rsplit("/", 1)[1]
            json_def_name = json_def.split('/')[1]
            client_file_name_split = client_file_name[-len(client_file_name):-4]

            text_file_pass = resultsfilelocation + "/" + "Pass/"
            text_file_fail = resultsfilelocation + "/" + "Failed/"
            text_file_result = resultsfilelocation + "/" + "Result/" + client_file_name_split + ".json"
            pass_fail_control_file = resultsfilelocation + "/" + "Summary_Result/"

            client_file_data = pd.read_csv(client_file, sep=sep_value)
            json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)
            json_def_data_no_orderdict = pd.read_json(json_def)



            # column names validation

            client_file_data_columns_list = (list(client_file_data.columns))
            client_file_data_columns_list_case_sensitive = [i.lower() for i in client_file_data_columns_list]
            json_def_data_columns_list = (list(json_def_data["columns"]))
            json_def_data_columns_list_case_sensitive = [i.lower() for i in json_def_data_columns_list]

            if len(set(client_file_data_columns_list_case_sensitive).intersection(
                    json_def_data_columns_list_case_sensitive)) == len(json_def_data_columns_list_case_sensitive):
                line1 = {"Test name": "Column names", "Result": "Passed"}
            else:
                line1 = {"Test name": "Column names", "Result": "Failed",
                         "Output": {"The expected columns are": list(json_def_data_columns_list)},
                         "but the columns in partner file are": list(client_file_data_columns_list)}

            # column order validation

            json_def_data_columns = (json_def_data["columns"])
            temp1 = []
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
                         "but the partner file has these columns with wrong order": list(fail_list.values())}

            else:
                line2 = {"Test name": "Column order", "Result": "Passed"}

            # checking for nulls

            client_file_data_df = pd.DataFrame(client_file_data)
            client_file_data_df.index = client_file_data_df.index + 1
            client_file_data_dff2 = client_file_data_df.isnull().stack()[lambda x: x].index.tolist()
            if (client_file_data_df.isnull().sum().sum()):
                dict1 = {}
                output1 = client_file_data_dff2
                for value, columns in output1:
                    if columns in dict1.keys():
                        b = dict1.get(columns)
                        b.append(value)
                        dict1[columns] = b
                    else:
                        y = []
                        y.append(value)
                        dict1[columns] = y
                line3 = {"Test name": "Check for nulls", "Result": "Failed/Nulls are found",
                         "Null values found in": str(dict1).replace('],', ']],').replace('{', '').replace('}',
                                                                                                          '').replace(
                             "'", "").split('],')}
            else:
                line3 = {"Test name": "Check for nulls", "Result": "Passed"}




            # checking the empty rows

            i = 1
            matches = {}
            empty_rows_list = []

            with open(client_file, 'r') as out:
                for line in out:
                    if line == '\n':
                        matches[i] = "matched"
                        matches.update(matches)
                    else:
                        matches[i] = "not matched"
                        matches.update(matches)
                    i = i + 1

            key = list(matches.keys())
            val = list(matches.values())
            for i in range(len(val)):
                if val[i] == "matched":
                    empty_rows_list.append("The file has empty row at " + str(key[i]))

            if len(empty_rows_list) != 0:
                line4 = {"Test name": "Empty Rows", "Result": "Failed", "Output": empty_rows_list}
            else:
                line4 = {"Test name": "Empty Rows", "Result": "Passed"}

            # check for the data-types

            json_def_data_columns_list_no_orderdict = (json_def_data_no_orderdict["columns"])
            json_def_data_columns_list_index = (list(json_def_data_no_orderdict["columns"].index))

            datatype_col = {}

            result_fail_list, column_pass_list, column_fail_list = [], [], []

            datatype_col_rename = {'INT': 'int64', 'int': 'int64', 'BIGINT': 'int64', 'SMALLINT': 'int64',
                                   'NVARCHAR(50)': 'str', 'CHAR(8)': 'str', 'DECIMAL(18,2)': 'float64', 'BIT': 'bool_',
                                   'DECIMAL(18,4)': 'float64', 'CHAR(2)': 'str', 'VARCHAR(10)': 'str', 'CHAR(1)': 'str',
                                   'VARCHAR(50)': 'str', 'DATE': 'date', 'NVARCHAR(3)': 'str', 'NVARCHAR(500)': 'str',
                                   'NVARCHAR(100)': 'str', 'NVARCHAR(255)': 'str', 'nvarchar(255)': 'str',
                                   'NVARCHAR(25)': 'str', 'NVARCHAR(3000)': 'str', 'NVARCHAR(40)': 'str',
                                   'NVARCHAR(20)': 'str'}

            for index, col in enumerate(json_def_data_columns_list_index):
                datatype_col[col] = json_def_data_columns_list_no_orderdict[col]['dbtype']
                datatype_col.update(datatype_col)

            dict3 = {k: datatype_col_rename[v] for k, v in datatype_col.items()}
            for column in client_file_data_columns_list:
                if column in dict3.keys():
                    for val in client_file_data[column]:
                        if str(val) == "nan" or type(val).__name__ == dict3[column]:
                            column_pass_list.append(column)
                        else:
                            column_fail_list.append(column)
                            result_fail_list.append("the value " + str(val) + " at row " + str(i) + " in column " + str(
                                column) + " doesn't match with datatype " + datatype_col[column])
                        i = i + 1

            if len(set(column_pass_list)) == len(dict3.keys()):
                line5 = {"Test name": "Data type", "Result": "Passed"}
            elif len(client_file_data) == 0:
                line5 = {"Test name": "Data type", "Result": "Failed", "Output": "File doesn't have any data"}
            else:
                line5 = {"Test name": "Data type", "Result": "Failed", "Output": result_fail_list}



            #checking data formats

            l2 = (json_def_data["columns"])
            #ll2=json_def_data["column_names"]
            l3=json_def_data_columns_list
            pass_df_list,fail_df_list,result_df_list=[],[],[]
            list_regex=[]
            line6={}

            for col in l3:
                regex = l2[col]['data-format']
                list_regex.append(regex)

            for column in client_file_data_columns_list:
                i=(client_file_data_columns_list.index(column))
                for row in client_file_data[column]:
                    if list_regex[i] != "":
                        if row!="nan":
                            pattern = re.compile(list_regex[i],re.UNICODE)
                            if pattern.findall(str(row)):
                                pass_df_list.append(column)
                                line6 = {"Test name": "Data Formats", "Result": "Passed"}

                            else:
                                fail_df_list.append(column)
                                result_df_list.append("Data format is invalid at column-name:{},row-element:{}".format(column,row))
                                line6 = {"Test name": "Data Formats", "Result": "Failed","Output":result_df_list}




            # copying the file to passed or fail folder

            if line1["Result"] == "Passed" and line2["Result"] == "Passed" and line3["Result"] == "Passed" and line4[
                "Result"] == "Passed" and line5["Result"] == "Passed" and line6["Result"]=="Passed":
                with open(text_file_pass + client_file_name, 'w') as f1:
                    for line in open(client_file):
                        f1.write(line)
                Summary_line = {"FileName": client_file_name, "Result": "Pass"}

                # pass control file

                pass_control_file_data.append(client_file_name + "|" + str(len(client_file_data)))

            else:
                with open(text_file_fail + client_file_name, 'w') as f1:
                    for line in open(client_file):
                        f1.write(line)

                # failed control file

                fail_control_file_data.append(client_file_name)

            # writing the output to the result file

            final_lines_to_file = {"Test-1": line1, "Test-2": line2, "Test-3": line3, "Test-4": line4, "Test-5": line5,"Test-6":line6}

            # creating a json output file in result folder

            with open(text_file_result, "w") as output:
                json.dump(final_lines_to_file, output, indent=4)
            output.close()

        if len(pass_control_file_data) != 0:
            pass_control_file = 'PassControl_' + date + "_" + timestamp + '.txt'
            with open(pass_fail_control_file + pass_control_file, 'w') as out:
                out.write('Filename|Rowcount')
                for line in pass_control_file_data:
                    out.write('\n' + line)

        if len(fail_control_file_data) != 0:
            fail_file = 'FailedFile_' + date + "_" + timestamp + '.txt'
            with open(pass_fail_control_file + fail_file, 'w') as out2:
                out2.write('Filename')
                for line in fail_control_file_data:
                    out2.write('\n' + line)


        return final_lines_to_file