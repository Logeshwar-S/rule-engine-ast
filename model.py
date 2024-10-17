import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        Initializes a Node for the Abstract Syntax Tree (AST).
        
        Parameters:
        - node_type (str): Type of the node (e.g., 'operator', 'operand').
        - left (Node, optional): Left child node.
        - right (Node, optional): Right child node.
        - value (any, optional): Value of the node (e.g., operator or operand value).
        """
        self.node_type = node_type 
        self.left = left 
        self.right = right 
        self.value = value 

    def to_dict(self):
        """
        Converts the Node and its children into a dictionary representation.
        
        Returns:
        - dict: Dictionary representation of the Node.
        """
        return {
            'node_type': self.node_type,
            'left': self.left.to_dict() if isinstance(self.left, Node) else self.left,
            'right': self.right.to_dict() if isinstance(self.right, Node) else self.right,
            'value': self.value
        }

def create_rule(rule_string):
    """
    Creates an Abstract Syntax Tree (AST) from a rule string.
    
    Parameters:
    - rule_string (str): The rule in string format (e.g., "age > 30").
    
    Returns:
    - Node: The root node of the generated AST.
    """
    tokens = tokenize(rule_string)  # Tokenize the rule string
    ast, _ = parse_expression(tokens)  # Parse tokens into an AST
    return ast  # Return the Node representation of the AST

def tokenize(rule_string):
    """
    Tokenizes a rule string into individual components (tokens).
    
    Parameters:
    - rule_string (str): The rule to tokenize.
    
    Returns:
    - list: List of tokens extracted from the rule string.
    """
    token_pattern = r'(\(|\)|AND|OR|<=|>=|<|>|==|=|\w+|\'[^\']*\'|\S)'  # Regex pattern to match tokens
    tokens = re.findall(token_pattern, rule_string)  # Find all matching tokens
    return [token.strip() for token in tokens if token.strip()]  # Return cleaned tokens

def parse_expression(tokens):
    """
    Parses a list of tokens into an expression tree.
    
    Parameters:
    - tokens (list): List of tokens to parse.
    
    Returns:
    - tuple: A tuple containing the root Node of the expression and the remaining tokens.
    """
    if not tokens:
        return None, tokens

    left, tokens = parse_term(tokens)  # Parse the first term

    # Process logical operators (AND, OR)
    while tokens and tokens[0] in ('AND', 'OR'):
        operator = tokens[0]  # Get the operator
        tokens.pop(0)  # Remove the operator from tokens
        right, tokens = parse_term(tokens)  # Parse the next term
        left = Node('operator', left=left, right=right, value=operator)  # Create a new operator node

    return left, tokens  # Return the root of the parsed expression

def parse_term(tokens):
    """
    Parses a term from the token list, which can be a condition or an expression in parentheses.
    
    Parameters:
    - tokens (list): List of tokens to parse.
    
    Returns:
    - tuple: A tuple containing the Node representing the term and the remaining tokens.
    
    Raises:
    - ValueError: If the term is invalid.
    """
    if not tokens:
        return None, tokens

    token = tokens.pop(0)  # Get the next token
    if token == '(':
        node, tokens = parse_expression(tokens)  # Parse an expression within parentheses
        if tokens and tokens[0] == ')':
            tokens.pop(0)  # Remove the closing parenthesis
        return node, tokens
    else:
        # Expect a condition in the form of "attribute operator value"
        condition = token
        if len(tokens) >= 2 and tokens[0] in ('>', '<', '=', '>=', '<=', '=='):
            operator = tokens.pop(0)  # Get the operator
            value = tokens.pop(0)  # Get the value
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]  # Remove quotes from string values
            # Create nodes for the condition
            left_node = Node('operand', value=condition)  # Create an operand node for attribute
            right_node = Node('operand', value=value)  # Create operand node for value
            return Node('operator', left=left_node, right=right_node, value=operator), tokens  # Return operator node
        else:
            raise ValueError(f"Invalid term: {token}")  # Raise an error for invalid terms

def is_valid_rule(rule_string):
    """
    Validates a rule string using a regular expression.
    
    Parameters:
    - rule_string (str): The rule string to validate.
    
    Returns:
    - bool: True if the rule string is valid, otherwise False.
    """
    # Simple regex for basic rule validation
    # Matches patterns like "age > 30" or "salary < 50000"
    pattern = r'^[a-zA-Z_]+\s*[><=]+\s*\d+$'
    return bool(re.match(pattern, rule_string))

def combine_rules(rules):
    """
    Combines multiple rule strings into a single Abstract Syntax Tree (AST).
    
    Parameters:
    - rules (list): List of rule strings to combine.
    
    Returns:
    - Node: The root node of the combined AST.
    """
    combined_ast = None
    
    for rule in rules:
        rule = rule.strip()  # Remove leading/trailing whitespace
        if not rule:
            continue  # Skip empty rules
        current_ast = create_rule(rule)  # Create AST for the current rule
        print(f"AST for current rule '{rule}': {current_ast.to_dict()}")
        if combined_ast is None:
            combined_ast = current_ast  # Initialize combined AST
        else:
            # Combine with the existing AST using AND operator
            combined_ast = Node('operator', left=combined_ast, right=current_ast, value='AND')
    
    if combined_ast:
        print(f"Final Combined AST: {combined_ast.to_dict()}")
    return combined_ast  # Return the combined AST

def evaluate_rule(rule_ast, user_data):
    """
    Evaluates a rule represented as an AST against a user's data.
    
    Parameters:
    - rule_ast (Node or dict): The root node of the rule AST or a dictionary representation.
    - user_data (dict): A dictionary containing user attributes to evaluate against the rule.
    
    Returns:
    - bool: True if the user data satisfies the rule, otherwise False.
    """
    if isinstance(rule_ast, dict):
        # Create Node from dict if needed
        rule_ast = Node(**rule_ast)

    if rule_ast.node_type == 'operator':
        # Evaluate left and right operands
        left_result = evaluate_rule(rule_ast.left, user_data)
        right_result = evaluate_rule(rule_ast.right, user_data)

        print(f"Evaluating: {rule_ast.value}, Left: {left_result}, Right: {right_result}")

        # Evaluate based on operator
        if rule_ast.value == 'AND':
            result = left_result and right_result
            print(f"Result of AND: {result}")
            return result
        elif rule_ast.value == 'OR':
            result = left_result or right_result
            print(f"Result of OR: {result}")
            return result
        elif rule_ast.value == '>':
            result = left_result > right_result
            print(f"Evaluating >: {left_result} > {right_result} = {result}")
            return result
        elif rule_ast.value == '>=':
            result = left_result >= right_result
            print(f"Evaluating >=: {left_result} >= {right_result} = {result}")
            return result
        elif rule_ast.value == '<=':
            result = left_result <= right_result
            print(f"Evaluating <=: {left_result} <= {right_result} = {result}")
            return result
        elif rule_ast.value == '<':
            result = left_result < right_result
            print(f"Evaluating <: {left_result} < {right_result} = {result}")
            return result
        elif rule_ast.value == '==':
            result = left_result == right_result
            print(f"Evaluating ==: {left_result} == {right_result} = {result}")
            return result
        elif rule_ast.value == '=':  # Handle string equality
            return str(left_result) == str(right_result)
        # Add more operators as needed

    elif rule_ast.node_type == 'operand':
        attr = rule_ast.value  # Get the attribute name
        if attr in user_data:
            print(f"Checking attribute: {attr} = {user_data[attr]}")
            return user_data[attr]  # Return the numeric value of the attribute

        # If the operand is a direct number, return it
        try:
            # Convert value to int if it's a number in string format
            return int(attr)  # Ensure numeric comparison
        except ValueError:
            return attr  # If it's not a valid number, return False

    return False  # Default case for any unrecognized rules
