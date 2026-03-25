let tasks = JSON.parse(localStorage.getItem("tasks")) || [];
let currentFilter = "all";

function saveData() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function add() {
    let text = document.getElementById("task").value.trim();
    let priority = document.getElementById("priority").value;
    let date = document.getElementById("date").value;

    if (text === "" || date === "") {
        alert("Enter all fields");
        return;
    }

    let task = {
        id: Date.now(),
        text: text,
        priority: priority,
        date: date,
        done: false
    };

    tasks.push(task);
    saveData();
    display();
}

function display() {
    let list = document.getElementById("list");
    list.innerHTML = "";

    let filtered = tasks.filter(t => {
        if (currentFilter === "done") return t.done;
        if (currentFilter === "pending") return !t.done;
        return true;
    });

    filtered.forEach(t => {
        let div = document.createElement("div");
        div.className = "card p-2 mb-2";

        div.innerHTML = `
            <b>${t.text}</b> <br>
            Priority: ${t.priority} | Date: ${t.date} <br>
            Status: ${t.done ? "Done" : "Pending"} <br>
            <button class="btn btn-sm btn-success" onclick="toggle(${t.id})">✔</button>
            <button class="btn btn-sm btn-danger" onclick="removeTask(${t.id})">✖</button>
        `;

        list.appendChild(div);
    });

    updateCount();
}

function toggle(id) {
    tasks = tasks.map(t => {
        if (t.id === id) {
            t.done = !t.done;
        }
        return t;
    });

    saveData();
    display();
}

function removeTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    saveData();
    display();
}

function filterTask(type) {
    currentFilter = type;
    display();
}

function sortP() {
    let order = { "Low": 1, "Medium": 2, "High": 3 };

    tasks.sort((a, b) => order[b.priority] - order[a.priority]);
    saveData();
    display();
}

function sortD() {
    tasks.sort((a, b) => new Date(a.date) - new Date(b.date));
    saveData();
    display();
}

function updateCount() {
    let total = tasks.length;
    let done = tasks.filter(t => t.done).length;
    let pending = total - done;

    document.getElementById("t").innerText = total;
    document.getElementById("d").innerText = done;
    document.getElementById("p").innerText = pending;
}
display();
