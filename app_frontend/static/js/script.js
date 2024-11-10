document.getElementById("add-expense").addEventListener("click", addExpense);
document.getElementById("calculate-split").addEventListener("click", calculateSplit);

async function addExpense() {
    const name = document.getElementById("name").value;
    const amount = parseFloat(document.getElementById("amount").value);

    if (name && amount) {
        const response = await fetch("/api/expenses/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, amount }),
        });
        const result = await response.json();
        console.log(result.message);
        updateDisplay();
        document.getElementById("name").value = "";
        document.getElementById("amount").value = "";
    } else {
        alert("Please enter a valid name and amount.");
    }
}

async function calculateSplit() {
    const response = await fetch("/api/expenses/split");
    const balances = await response.json();

    let balanceSummary = "";
    balances.forEach(balance => {
        balanceSummary += `${balance.name} owes ${balance.balance.toFixed(2)}\n`;
    });

    alert(balanceSummary);
}

async function updateDisplay() {
    const response = await fetch("/api/expenses");
    const expenses = await response.json();

    const displaySection = document.getElementById("display-section");
    displaySection.innerHTML = "";
    expenses.forEach(expense => {
        const entry = document.createElement("p");
        entry.textContent = `${expense.name} spent $${expense.amount.toFixed(2)}`;
        displaySection.appendChild(entry);
    });
}
