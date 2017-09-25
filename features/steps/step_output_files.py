from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from transformation import scenario
from dir_file import dir_create

@given('a file')
def step_given_the_file(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	context.files = retrieve_files()
	context.transformation = scenario()
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	assert_that(len(datafiles_names) > 0)

@then('control file check')
def step_control_file_check(context):
	dir_file = dir_create()
	values = dir_file.dir()
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc)
	context.transformation.scenario_writing_to_files(datafiles_names, deffiles_names, control_data_file, control_def_file_loc)


@then('row count should match')
def step_rows_count_should_match(context):
	pass


@then('column names should match')
def step_column_names_should_match(context):
	pass


@then('column order should match')
def step_column_order_should_match(context):
	pass

@then('null values are not allowed')
def step_null_should_match(context):
	pass

@then('empty rows')
def step_empty_rows(context):
	pass


@then('data type check')
def step_data_type_check(context):
	pass