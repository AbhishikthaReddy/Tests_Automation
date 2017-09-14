from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from transformation import scenario
from dir_file import dir_create
# from result_files import files_create



@given('the file')
def step_given_the_file(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	context.files = retrieve_files()
	context.transformation = scenario()
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	assert_that(len(datafiles_names) > 0)
# @when('the job checks for valid columns')
# def step_when_file_generated(context):
#     pass


@then('rows count should match')
def step_rows_count_should_match(context):
	dir_file = dir_create()
	values = dir_file.dir()
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	rows_count_pass_list, rows_count_fail_list = context.transformation.rows_count(datafiles_names, deffiles_names, control_data_file, control_def_file_loc)
	# result_files = 
	# assert_that("pass", equal_to(rows_count))


@then('column names should match')
def step_column_names_should_match(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	column_names_pass_list, column_names_fail_list = context.transformation.column_names(datafiles_names, deffiles_names, control_data_file, control_def_file_loc)
	# assert_that("pass", equal_to(column_names))


@then('column order should match')
def step_column_order_should_match(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	column_order_pass_list, column_order_fail_list = context.transformation.column_order(datafiles_names, deffiles_names, control_data_file, control_def_file_loc)
	# assert_that("pass", equal_to(column_order))
