from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from file_comp import f_comp
from transformation import scenario
from dir_file import dir_create


@given('a file')
def step_given_the_file(context):
	context.files = retrieve_files()
	context.transformation = scenario()
	date = context.config.userdata.get("date")
	if len(date) == 8:
		masterfile_loc = context.config.userdata.get("masterfile_loc")
		resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
		timestamp = context.config.userdata.get("timestamp")
		if len(timestamp) >= 6:
			try:
				datafiles_names, deffiles_names, control_def_file_loc, row_count_file, summary_invalid_file, field_separator = context.files.files(date, masterfile_loc, resultsfiles_loc,timestamp)
				if len(datafiles_names) != 0 and len(deffiles_names) != 0 and len(datafiles_names) == len(deffiles_names):
					dir_file = dir_create()
					values = dir_file.dir(resultsfiles_loc)
					final_lines_to_file = context.transformation.scenario_writing_to_files(resultsfiles_loc, datafiles_names,deffiles_names, control_def_file_loc, date, timestamp, row_count_file, summary_invalid_file, field_separator)
					file_comp = f_comp()
					comparison = file_comp.comp(date, timestamp, resultsfiles_loc, datafiles_names)

					@then('column names should match')
					def step_column_names_should_match(context):
						pass

					@then('column order should match')
					def step_column_order_should_match(context):
						pass

					@then('check null values')
					def step_check_null_values(context):
						pass

					@then('empty rows')
					def step_empty_rows(context):
						pass

					@then('data type check')
					def step_data_type_check(context):
						pass

					@then('data formats')
					def step_data_type_check(context):
						pass
				else:
					print ("There are no files with the given timestamp")

					@then('column names should match')
					def step_column_names_should_match(context):
						assert context.text, "REQUIRE: corrent data input"

					@then('column order should match')
					def step_column_order_should_match(context):
						assert context.text, "REQUIRE: corrent data input"

					@then('check null values')
					def step_check_null_values(context):
						assert context.text, "REQUIRE: corrent data input"

					@then('empty rows')
					def step_empty_rows(context):
						assert context.text, "REQUIRE: corrent data input"

					@then('data type check')
					def step_data_type_check(context):
						assert context.text, "REQUIRE: corrent data input"


					@then('data formats')
					def step_data_type_check(context):
						assert context.text, "REQUIRE: corrent data input"

			except TypeError as err:
				print ("Error Message: "+str(err))
		else:
			print (len(timestamp) >= 6), "Given timestamp doesn't match"
	else:
		assert (len(date) == 8), "Given Date format doesn't match"