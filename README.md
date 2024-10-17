# User Eligibility Rule Engine with AST

A web-based application that evaluates user eligibility based on predefined rules using an Abstract Syntax Tree (AST). This rule engine allows users to create, update, combine, and evaluate rules against user data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Design Choices](#design-choices)
- [Contributing](#contributing)

## Features

- Create and manage user-defined eligibility rules.
- Combine multiple rules into a single rule set.
- Evaluate user eligibility based on the combined rules.
- Display an Abstract Syntax Tree (AST) for each rule.
- Store user data in a MySQL database.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Database:** MySQL


## Setup Instructions

### Prerequisites

Make sure you have the following installed on your machine:

- [Python 3.x](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/) (for frontend dependencies)
- [MySQL](https://www.mysql.com/downloads/)
- [Git](https://git-scm.com/downloads)

### 1. Clone the Repository

```
git clone https://github.com/Logeshwar-S/rule-engine-ast.git
cd rule-engine-ast
 ```


### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Database Configuration

- Create a MySQL database named database (you can choose any name) and a user with appropriate permissions.
- Ensure that you update the database connection settings in the app.py file:

```
conn = mysql.connector.connect(
    host='localhost',  # Change if your DB is hosted elsewhere
    user='username',  # Replace with your DB username
    password='password',  # Replace with your DB password
    database='database'  # Replace with your DB name
)
```
### 4. Run the Application

```
flask run
```
Your application will be accessible at http://127.0.0.1:5000.



## Usage

- Access the application through a web browser.
- Enter user data and define rules using the provided interface.
- Combine and evaluate the rules to determine user eligibility.

## Design Choices

- Abstract Syntax Tree (AST): The use of an AST allows for flexible rule definition and evaluation.
- Flask Framework: Chosen for its simplicity and ease of use for building web applications in Python.
- MySQL Database: Used for persistent storage of user data and rules.

## Contributing

- Contributions are welcome! Please open an issue or submit a pull request.
