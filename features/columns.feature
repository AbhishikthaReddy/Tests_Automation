
Feature: To check whether the columns exists,column names match,column order match and compare the row counts.

@all
Scenario: Proper columns present
   Given  a file
    Then  control file check

@all
Scenario: Proper columns present
   Given  a file
    Then  row count should match

@all
Scenario: To check if the column names in partner file and definition file match
   Given  a file
    Then  column names should match

@all
Scenario: To check if the order of the column names match in partner file and definition file
   Given  a file
    Then  column order should match

@all
Scenario: Check for null values
  Given   a file
  Then    null values are not allowed

@all
Scenario: check for empty rows
   Given  a file
    Then  empty rows

@all
Scenario: SQL and python comparison
   Given a file
     Then  query result matched with partner file result

@all
Scenario: data type check for columns in a file
   Given  a file
    Then  data type check

@all
Scenario: check for special characters
  Given   a file
   Then   special characters