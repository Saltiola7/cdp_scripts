Use PEP8
write terse code
use .env
use dictionary declarations instead of loops whenever possible
write efficient SQL queries
include the full functionality of the original code
you are not allowed to use placeholders in the code. You have to ask all the fillers into the code so that you can return complete production ready code.
use pytest instead of unittest
use python 3.12

include all these improvements and make the code ready for production with Prefect.
also include the logic that checks if a sheet is already generated into google drive, do not generate a duplicate. 

take into account that these features are to be included next into the codebase
- automatically generate tables in bigquery when new csv files are added to google drive
- automatically generates google sheets per brand when a table is added in bigquery
but before I add them, just make a comment into the code to where these things could be added later on.
also make it so that I can run these separately but also in tandem
- load drive files to bigquery tables
- generate google sheets from bigquery tables

Modularize the Code:

Break down the code into smaller, reusable functions or classes to handle specific tasks (e.g., handling BigQuery operations, processing files from Drive, managing Sheets operations). This makes the code easier to understand, test, and maintain.
Remove Redundant Code:

You have duplicated code for setting up credentials and initializing the BigQuery client. Consolidate this to avoid redundancy and potential inconsistencies.
Use Configurations for Constants:

Move constants and configurations (like PROJECT_ID, DATASET_ID, SERVICE_ACCOUNT_FILE, etc.) to a separate configuration file or environment variables. This makes the code more flexible and secure, especially when dealing with sensitive information like service account keys.
Error Handling:

Implement comprehensive error handling and logging to manage and log exceptions properly. This helps in debugging and ensures the script doesn't fail silently in production.
Optimize Data Handling:

For large datasets, consider processing the data in chunks or using efficient data processing libraries/frameworks to optimize memory usage and speed.
Use Context Managers for Resource Management:

Use context managers (with statement) for handling file streams or other resources to ensure they are properly closed after their use.
Docstrings and Comments:

Add docstrings to functions and classes, and meaningful comments throughout the code to describe the purpose of the code blocks, the parameters, and the expected outcomes.
PEP 8 Compliance:

Ensure the code is PEP 8 compliant for better readability and maintainability. This includes proper naming conventions, line lengths, whitespace usage, etc.
Unit Testing:

Write unit tests for the individual components of the script. This ensures that each part is working correctly and makes it safer to make changes in the future.
Dependency Management:

Clearly define the dependencies and their versions in a requirements file (requirements.txt or use a tool like pipenv), ensuring consistent environments across different setups.
Code Linting and Formatting:

Use tools like flake8 for linting and black or autopep8 for code formatting to maintain a consistent coding style.
Optimize Imports:

Organize and remove unused imports to make the code cleaner and slightly more efficient.
Use Parameterized Queries:

For BigQuery queries, use parameterized queries to prevent SQL injection and improve query performance.
Asynchronous Programming:

If there are IO-bound operations, especially when dealing with APIs or databases, consider using asynchronous programming (asyncio library) to make the program more efficient.



do you have any further questions before refactoring and modifying the code according to instructions so that its production ready code using prefect for workflow orchestration?