
Feature: Data validation testing

@all
Scenario: To check if the column names in partner file and definition file match
   Given  a file
    Then  column names should match

@all
Scenario: To check if the order of the column names match in partner file and definition file
    Then  column order should match

@all
Scenario: To check if there are any null values
    Then  check null values

@all
Scenario: check for empty rows
    Then  empty rows

@all
Scenario: data type check for columns in a file
    Then  data type check

@all
Scenario: row count check for columns in a file
    Then  row count check

@all
Scenario: summary data check for provided columns
    Then  summary data check

@all
Scenario: data type check for columns in a file
    Then  data formats

@all
Scenario: duplicate values check for rows in a file
    Then  duplicate values

@all
Scenario: special characters check for data in a file
    Then  special characters check

@all
Scenario: invalid-values check for data in a file
    Then  invalid-values check

@all
Scenario: generate result files
    Then  generate result files