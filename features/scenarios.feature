
Feature: To check the null values,column names,column order, empty rows and data-types

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
Scenario: data type check for columns in a file
   Given  a file
    Then  data formats

