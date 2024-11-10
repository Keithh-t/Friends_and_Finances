document.getElementById("add-expense").addEventListener("click", addExpense);
document.getElementById("calculate-split").addEventListener("click", calculateSplit);

// Add expense to the backend
async function addExpense() {
    const name = document.getElementById("name").value;
    const amount = parseFloat(document.getElementById("amount").value);

    if (name && amount) {
        try {
            const response = await fetch("/api/expenses/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name, amount })
            });

            if (response.ok) {
                updateDisplay();
                document.getElementById("name").value = "";
                document.getElementById("amount").value = "";
            } else {
                alert("Failed to add expense.");
            }
        } catch (error) {
            console.error("Error adding expense:", error);
            alert("An error occurred. Please try again.");
        }
    } else {
        alert("Please enter a valid name and amount.");
    }
}

// Fetch and calculate split from backend
async function calculateSplit() {
    try {
        const response = await fetch("/api/expenses/split", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const balanceSummary = await response.json();
            let summaryText = "";
            balanceSummary.forEach(entry => {
                summaryText += `${entry.name} owes ${entry.balance.toFixed(2)}\n`;
            });
            alert(summaryText);
        } else {
            alert("Failed to calculate split.");
        }
    } catch (error) {
        console.error("Error calculating split:", error);
        alert("An error occurred. Please try again.");
    }
}

// Fetch expenses from backend and update display
async function updateDisplay() {
    try {
        const response = await fetch("/api/expenses", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            const expenses = await response.json();
            const displaySection = document.getElementById("display-section");
            displaySection.innerHTML = "";

            expenses.forEach(expense => {
                const entry = document.createElement("p");
                entry.textContent = `${expense.name} spent $${expense.amount.toFixed(2)}`;
                displaySection.appendChild(entry);
            });
        } else {
            alert("Failed to fetch expenses.");
        }
    } catch (error) {
        console.error("Error fetching expenses:", error);
        alert("An error occurred. Please try again.");
    }
}
