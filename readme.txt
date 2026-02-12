======================================================================
API TEST AUTOMATION PROJECT - REQRES.IN
======================================================================

PROJECT OVERVIEW:
This project contains automated API tests for the Reqres.in system 
under test. It covers two primary scenarios:
1. GET - List Users (Pagination, Data Integrity, and Type Validation)
2. POST - Create User (Data-driven creation and Schema Validation)

TECH STACK:
- Language: Python 3.x
- Framework: Pytest
- Libraries: Requests, JSONSchema, Re (Regex)

FILE STRUCTURE:
- config.py                : Global configuration (Base URL, Headers)
- external_users_data.json : Test data source for creating users
- test_get_users.py        : GET request test suite
- test_create_user.py      : POST request test suite

----------------------------------------------------------------------
PREREQUISITES:
----------------------------------------------------------------------
Ensure you have Python installed on your system. You will need the 
'requests' and 'jsonschema' libraries.

1. Install required packages:
   pip install requests pytest jsonschema

----------------------------------------------------------------------
HOW TO RUN THE TESTS:
----------------------------------------------------------------------
Open your terminal/command prompt in the project root directory and 
use the following commands:

1. Run all tests:
   pytest -v

2. Run tests with console output (to see response times and debug info):
   pytest -v -s

3. Run a specific test file:
   pytest test_get_users.py -v

----------------------------------------------------------------------
TEST SCENARIO DETAILS:
----------------------------------------------------------------------
- GET List Users: 
  Validates HTTP 200, checks "total" count logic, asserts "last_name" 
  presence for the first two users, and performs strict regex 
  validation on email formats and data types.

- POST Create User:
  Uses a module-scoped fixture to perform data-driven testing via an 
  external JSON file. Asserts HTTP 201, creation timestamps (ISO 8601), 
  and enforces a JSON Schema to ensure the API contract is met. 
  Includes a performance check (Response Time < 1000ms).
======================================================================