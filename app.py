from flask import Flask, request, jsonify, render_template
import mysql.connector
from model import create_rule, combine_rules, evaluate_rule, is_valid_rule

app = Flask(__name__)

# MySQL database connection
def init_db():
    """
    Initializes the connection to the MySQL database.

    Returns:
    - MySQLConnection: Connection object if successful, otherwise None.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',  # Change if your DB is hosted elsewhere
            user='username',  # Replace with your DB username
            password='password',  # Replace with your DB password
            database='database'  # Replace with your DB name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Fetch rule data from the database
def fetch_rules():
    """
    Fetches all rules from the database.

    Returns:
    - list: List of rules fetched from the database.
    """
    conn = init_db()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rules")
    rules = cursor.fetchall()  # Retrieve all rule records
    cursor.close()
    conn.close()
    return rules

# Fetch user data from the database
def fetch_user_data():
    """
    Fetches all user data from the database.

    Returns:
    - list: List of user data fetched from the database.
    """
    conn = init_db()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserData")
    users = cursor.fetchall()  # Retrieve all user records
    cursor.close()
    conn.close()
    return users

@app.route('/')
def index():
    """
    Renders the index page of the application.

    Returns:
    - Rendered HTML template of the index page.
    """
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    """
    Endpoint to create a new rule in the database.

    Expects a JSON body with the rule string:
    {
        "rule_string": "age > 30"
    }

    Returns:
    - JSON: The AST representation of the created rule or error message.
    """
    # Attempt to get the rule from the JSON request
    rule_string = request.json.get('rule_string')

    # Check if rule_string is None or an empty string
    if not rule_string:
        return jsonify({"error": "Rule string is required"}), 400

    if not is_valid_rule(rule_string):
        return jsonify({"error": "Invalid rule syntax"}), 400
    
    try:
        # Call your create_rule function to generate AST
        ast = create_rule(rule_string)
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string) VALUES (%s)", (rule_string,))
        conn.commit()  # Commit the changes to the database
        cursor.close()
        conn.close()
        # Return the AST representation as a dictionary
        return jsonify(ast.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    """
    Endpoint to combine multiple rules into a single AST.

    Expects a JSON body with an array of rules:
    {
        "rules": ["age > 30", "salary < 50000"]
    }

    Returns:
    - JSON: The combined AST representation of the rules.
    """
    data = request.get_json()
    rules = data.get('rules', [])
    
    # Create the combined AST from the rules
    combined_ast = combine_rules(rules)
    
    # Return the combined AST as a dictionary
    return jsonify(combined_ast.to_dict())

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    """
    Endpoint to evaluate a rule AST against user data.

    Expects a JSON body with the AST and user data:
    {
        "rule_ast": {
            "node_type": "operator",
            "value": "AND",
            ...
        },
        "data": {
            "age": 25,
            "salary": 50000,
            "experience": 3,
            "department": "Sales"
        }
    }

    Returns:
    - JSON: The evaluation result or error message.
    """
    data = request.json
    rule_ast = data['rule_ast']  # Expecting the AST structure as a Node object
    
    if not rule_ast or not isinstance(rule_ast, dict) or 'node_type' not in rule_ast:
        return jsonify({"error": "Invalid rule AST provided"}), 400

    user_data = data['data']
    
    # Evaluate the rule against user data
    result = evaluate_rule(rule_ast, user_data)
    try:
        # Store user data in the database
        conn = init_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO UserData (age, salary, experience, department) VALUES (%s, %s, %s, %s)",
            (user_data['age'], user_data['salary'], user_data['experience'], user_data['department'])
        )
        conn.commit()  # Commit the changes
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error storing user data: {e}")
        return jsonify({'error': str(e)}), 500

    # Return the evaluation result
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
