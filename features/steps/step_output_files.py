from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from file_comp import f_comp
from transformation import scenario
from dir_file import dir_create
import pandas as pd
import datetime

@given('a file')
def step_given_the_file(context):
	total_result = []
	context.files = retrieve_files()
	context.transformation = scenario()
	date = context.config.userdata.get("date")
	if len(date) == 8:
		masterfile_loc = context.config.userdata.get("masterfile_loc")
		resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
		if len(resultsfiles_loc) == 0:
			try:
				masterfile = pd.read_json(masterfile_loc)
				resultsfiles_loc = masterfile.resultsfiles_loc.ix[0]
			except:
				print("MasterJSON File Not Found in the specified path")
		timestamp = context.config.userdata.get("timestamp")
		if len(timestamp) >= 6:
			try:
				datafiles_names, deffiles_names, row_count_file, summary_invalid_file, field_separator = context.files.files(date, masterfile_loc, resultsfiles_loc,timestamp)
				if len(datafiles_names) != 0 and len(deffiles_names) != 0 and len(datafiles_names) == len(deffiles_names):
					dir_file = dir_create()
					values = dir_file.dir(resultsfiles_loc)
					
					file_comp = f_comp()
					today_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

					try:
						@then('column names should match')
						def step_column_names_should_match(context):

							global line1
							line1 = context.transformation.column_names(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							pass

						@then('column order should match')
						def step_column_order_should_match(context):

							global line2
							context.transformation = scenario()
							line2 = context.transformation.column_order(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							pass

						@then('check null values')
						def step_check_null_values(context):

							global line3
							context.transformation = scenario()
							line3 = context.transformation.null_values(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							pass

						@then('empty rows')
						def step_empty_rows(context):

							global line4
							context.transformation = scenario()
							line4 = context.transformation.empty_rows(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line4)
							pass

						@then('data type check')
						def step_data_type_check(context):

							global line5
							context.transformation = scenario()
							line5 = context.transformation.data_type(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line5)
							pass

						@then('row count check')
						def step_row_count_check(context):

							global line6
							context.transformation = scenario()
							line6 = context.transformation.row_count(datafiles_names, deffiles_names, row_count_file, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line6)
							pass

						@then('summary data check')
						def step_summary_data_check(context):

							global line7
							context.transformation = scenario()
							line7 = context.transformation.summary_data(datafiles_names, deffiles_names, summary_invalid_file, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line7)
							pass

						@then('data formats')
						def step_data_formats_check(context):

							global line8
							context.transformation = scenario()
							line8 = context.transformation.data_formats(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line8)
							pass

						@then('duplicate values')
						def step_duplicate_values_check(context):

							global line9
							context.transformation = scenario()
							line9 = context.transformation.duplicate_values(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line9)
							pass

						@then('special characters check')
						def step_special_characters_check(context):

							global line10
							context.transformation = scenario()
							line10 = context.transformation.special_characters(datafiles_names, deffiles_names, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line10)
							pass

						@then('invalid-values check')
						def step_invalid_values_check(context):

							global line11
							context.transformation = scenario()
							line11 = context.transformation.invalid_values(datafiles_names, deffiles_names, summary_invalid_file, field_separator, resultsfiles_loc, today_now)
							# total_result.append(line11)
							pass

						@then('generate result files')
						def step_generate_result_files(context):

							context.transformation = scenario()
							# try:
							# 	line1 = line1
							# except NameError:
							# 	line1 = None

							# try:
							# 	line2 = line2
							# except NameError:
							# 	line2 = None

							# try:
							# 	line3 = line3
							# except NameError:
							# 	line3 = None

							# try:
							# 	line4 = line4
							# except NameError:
							# 	line4 = None

							# try:
							# 	line5 = line5
							# except NameError:
							# 	line5 = None

							# try:
							# 	line6 = line6
							# except NameError:
							# 	line6 = None

							# try:
							# 	line7 = line7
							# except NameError:
							# 	line7 = None

							# try:
							# 	line8 = line8
							# except NameError:
							# 	line8 = None

							# try:
							# 	line9 = line9
							# except NameError:
							# 	line9 = None

							# try:
							# 	line10 = line10
							# except NameError:
							# 	line10 = None

							# try:
							# 	line11 = line11
							# except NameError:
							# 	line11 = None

							context.transformation.result(line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11,  resultsfiles_loc, today_now)
							pass

					except Exception as err:
						print("Encountered error: "+str(err))

					comparison = file_comp.comp(date, timestamp, resultsfiles_loc, datafiles_names, today_now)

				else:
					print ("There are no files with the given timestamp")

					@then('column names should match')
					def step_column_names_should_match(context):
						assert context.text, "REQUIRE: correct data input"

					@then('column order should match')
					def step_column_order_should_match(context):
						assert context.text, "REQUIRE: correct data input"

					@then('check null values')
					def step_check_null_values(context):
						assert context.text, "REQUIRE: correct data input"

					@then('empty rows')
					def step_empty_rows(context):
						assert context.text, "REQUIRE: correct data input"

					@then('data type check')
					def step_data_type_check(context):
						assert context.text, "REQUIRE: correct data input"

					@then('row count check')
					def step_row_count_check(context):
						assert context.text, "REQUIRE: correct data input"

					@then('summary data check')
					def step_summary_data_check(context):
						assert context.text, "REQUIRE: correct data input"

					@then('data formats')
					def step_data_formats_check(context):
						assert context.text, "REQUIRE: corrent data input"

					@then('duplicate values')
					def step_duplicate_values_check(context):
						assert context.text, "REQUIRE: correct data input"

					@then('special characters check')
					def step_special_characters_check(context):
						assert context.text, "REQUIRE: correct data input"

					@then('invalid-values check')
					def step_invalid_values_check(context):
						assert context.text, "REQUIRE: correct data input"

			except TypeError as err:
				print ("Error Message: "+str(err))
		else:
			print (len(timestamp) >= 6), "Given timestamp doesn't match"
	else:
		assert (len(date) == 8), "Given Date format doesn't match"