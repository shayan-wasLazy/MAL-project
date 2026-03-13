async function loadAnime() {

    const response = await fetch("http://127.0.0.1:8000/anime");

    const anime = await response.json();

    const list = document.getElementById("animeList");

    list.innerHTML = "";

    anime.forEach(a => {
        const li = document.createElement("li");
        li.textContent = a.title + " (" + a.release_year + ")";
        list.appendChild(li);
    });
}

function switchTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".form-section").forEach(s => s.classList.remove("active"));
    document.getElementById(tab + "Section").classList.add("active");
    document.querySelectorAll(".tab")[tab === "login" ? 0 : 1].classList.add("active");
    document.getElementById("message").textContent = "";
}

function showMessage(text, isError) {
    const el = document.getElementById("message");
    el.textContent = text;
    el.className = isError ? "error" : "success";
}

async function login() {
    const username = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value;

    if (!username || !password) {
        showMessage("Please fill in all fields.", true);
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        showMessage("Welcome back, " + data.username + "!", false);
    } else {
        showMessage(data.detail || "Login failed.", true);
    }
}

async function register() {
    const username = document.getElementById("registerUsername").value.trim();
    const password = document.getElementById("registerPassword").value;

    if (!username || !password) {
        showMessage("Please fill in all fields.", true);
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        showMessage("Account created! You can now log in.", false);
        switchTab("login");
    } else {
        showMessage(data.detail || "Registration failed.", true);
    }
}