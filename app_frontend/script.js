const expenses = [];

document.getElementById("add-expense").addEventListener("click", addExpense);
document.getElementById("calculate-split").addEventListener("click", calculateSplit);

function addExpense() {
    const name = document.getElementById("name").value;
    const amount = parseFloat(document.getElementById("amount").value);

    if (name && amount) {
        expenses.push({ name, amount });
        updateDisplay();
        document.getElementById("name").value = "";
        document.getElementById("amount").value = "";
    } else {
        alert("Please enter a valid name and amount.");
    }
}

function calculateSplit() {
    const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
    const split = total / expenses.length;

    let balanceSummary = "";
    expenses.forEach(expense => {
        const balance = expense.amount - split;
        balanceSummary += `${expense.name} owes ${balance.toFixed(2)}\n`;
    });

    alert(balanceSummary);
}

function updateDisplay() {
    const displaySection = document.getElementById("display-section");
    displaySection.innerHTML = "";
    expenses.forEach(expense => {
        const entry = document.createElement("p");
        entry.textContent = `${expense.name} spent $${expense.amount.toFixed(2)}`;
        displaySection.appendChild(entry);
    });
}
