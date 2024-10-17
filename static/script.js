// Array to hold the rules
let rules = []; 

// Function to add rule
function addRule() {
    const ruleInput = document.getElementById("ruleInput").value.trim();
    if (!ruleInput) {
        alert("Please enter a rule.");
        return;
    }

    // Validate the rule before adding it
    fetch('/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: ruleInput })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error || 'Error adding rule');
            });
        }
        return response.json();
    })
    .then(data => {
        rules.push(ruleInput);
        updateRulesList();
        document.getElementById("ruleInput").value = "";

        // Display AST for the newly added rule
        document.getElementById("astRepresentation").innerText = JSON.stringify(data, null, 2);
        document.getElementById("astRepresentation").style.display = "block";
    })
    .catch(error => {
        console.error('Error generating AST:', error);
        alert(`Failed to add rule: ${error.message}`);
    });
}

// Function to update the last rule
function updateLastRule() {
    if (rules.length === 0) {
        alert("No rules to update.");
        return;
    }

    const ruleInput = document.getElementById("ruleInput").value.trim();
    if (!ruleInput) {
        alert("Please enter a rule to update.");
        return;
    }

    // Validate the new rule before updating
    fetch('/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: ruleInput })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error || 'Error updating rule');
            });
        }
        return response.json();
    })
    .then(data => {
        rules[rules.length - 1] = ruleInput;
        updateRulesList();
        document.getElementById("ruleInput").value = "";

        // Display AST for the updated rule
        document.getElementById("astRepresentation").innerText = JSON.stringify(data, null, 2);
        document.getElementById("astRepresentation").style.display = "block"; 
    })
    .catch(error => {
        console.error('Error generating AST:', error);
        alert(`Failed to update rule: ${error.message}`);
    });
}

// Function to remove the last rule
function removeLastRule() {
    if (rules.length > 0) {
        rules.pop();
        updateRulesList();

        // Clear AST representation if no rules left
        if (rules.length === 0) {
            document.getElementById("rulesList").innerHTML = ""; 
            document.getElementById("astRepresentation").style.display = "none";
        }
    } else {
        alert("No rules to remove.");
    }
}

// Function to update rule list
function updateRulesList() {
    const rulesList = document.getElementById("rulesList");
    rulesList.innerHTML = "";

    if (rules.length === 0) {
        rulesList.innerHTML = "<p>No rules available.</p>";
        return;
    }

    // Loop through the rules and display them
    rules.forEach((rule, index) => {
        rulesList.innerHTML += `<p>Rule ${index + 1}: "${rule}"</p>`;
    });
}

// Function to generate AST
function generateAstForRule(rule) {
    fetch('/create_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_string: rule })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error || 'Error generating AST');
            });
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("astRepresentation").innerText = JSON.stringify(data, null, 2);
        document.getElementById("astRepresentation").style.display = "block";
    })
    .catch(error => {
        console.error('Error generating AST:', error);
        alert(`Failed to generate AST: ${error.message}`);
    });
}

// Function to combine rules
function combineRules() {
    if (rules.length === 0) {
        alert("No rules to combine.");
        return;
    }

    fetch('/combine_rules', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rules: rules })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("combinedOutput").innerText = JSON.stringify(data, null, 2);
        document.getElementById("combinedAst").value = JSON.stringify(data);
    })
    .catch(error => {
        console.error('Error combining rules:', error);
    });
}

// Function to clear combined rules
function deleteCombinedRules() {
    document.getElementById("combinedOutput").innerText = "";
    document.getElementById("combinedRuleString").innerText = "";
    document.getElementById("combinedAst").value = "";
    alert("Combined rules have been deleted.");
}

// Function to evaluate rule
function evaluateRule() {
    const age = document.getElementById("age").value;
    const salary = document.getElementById("salary").value;
    const experience = document.getElementById("experience").value;
    const department = document.getElementById("department").value;

    if (!age || !salary || !experience || !department) {
        alert("Please enter all user data before evaluating.");
        return;
    }

    const userData = {
        age: parseInt(age),
        salary: parseInt(salary),
        experience: parseInt(experience),
        department: department
    };

    const combinedAst = document.getElementById("combinedAst").value;

    if (!combinedAst) {
        alert("Please combine rules before evaluating.");
        return;
    }

    fetch('/evaluate_rule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rule_ast: JSON.parse(combinedAst), data: userData })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const eligibility = data.result ? "Eligible" : "Not Eligible";
        alert(`Eligibility Status: ${eligibility}`);
    })
    .catch(error => {
        console.error('Error evaluating rule:', error);
    });
}
