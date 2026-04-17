async function loadAnime() {

    const response = await fetch("http://127.0.0.1:8000/anime");

    const anime = await response.json();

    const list = document.getElementById("animeList");

    list.innerHTML = "";

    anime.forEach(a => {
        const card = document.createElement("div");
        card.classList.add("anime-card");

        card.innerHTML = `
            <img src="${a.image_url}" alt="${a.title}">
            <h3>${a.title}</h3>
            <p>${a.start_date}</p>
        `;

        card.addEventListener("click", () => {
            window.location.href = `AnimeInfo.html?id=${a.anime_id}`;
            console.log(`Navigating to anime with ID: ${a.anime_id}`);
        });
        list.appendChild(card);
    }); 
}

console.log("SCRIPT LOADED");

async function displayAnime() {

    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");

    if (!id) {
        console.error("No anime ID found in URL");
        return;
    }

    console.log(`Fetching details for anime ID: ${id}`);

    const response = await fetch(`http://127.0.0.1:8000/anime/${id}`);
    const anime = await response.json();

    const container = document.getElementById("animeInfo");

    if (!container) {
        console.error("animeInfo div not found");
        return;
    }

    container.innerHTML = `
        <div class="detail-card">
            <img src="${anime.image_url}">
            <div>
                <h1>${anime.title}</h1>
                <p><strong>Start Date:</strong> ${anime.start_date}</p>
                <p>${anime.synopsis || "No description available."}</p>

                <div class="anime-controls">

                    <select id="status">
                        <option value="watching">Watching</option>
                        <option value="completed">Completed</option>
                        <option value="dropped">Dropped</option>
                    </select>

                    <input type="number" id="rating" min="1" max="10" placeholder="Rating">

                    <input type="number" id="episodes" min="0" placeholder="Episodes watched">

                    <button onclick="saveAnime(${anime.anime_id})">
                        Save
                    </button>

                </div>

            </div>
        </div>
    `;
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
        localStorage.setItem("user_id", data.user_id);
        showMessage("Welcome back, " + data.username + "!", false);

        window.location.href = `Account.html`;
    } else {
        showMessage(data.detail || "Login failed.", true);
    }
}

async function register() {
    const username = document.getElementById("registerUsername").value.trim();
    const email = document.getElementById("registerEmail").value.trim();
    const password = document.getElementById("registerPassword").value;

    if (!username || !email || !password) {
        showMessage("Please fill in all fields.", true);
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
        showMessage("Account created! You can now log in.", false);
        switchTab("login");
    } else {
        showMessage(data.detail || "Registration failed.", true);
    }
}

async function loadWatchlist() {
    const user_id = localStorage.getItem("user_id");

    const response = await fetch(`http://127.0.0.1:8000/user/${user_id}/anime`);
    const data = await response.json();

    const list = document.getElementById("watchlist");
    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `Anime ID: ${item.anime_id} | Status: ${item.watch_status}`;
        list.appendChild(li);
    });
}

async function loadUser() {
    const user_id = localStorage.getItem("user_id");

    const response = await fetch(`http://127.0.0.1:8000/user/${user_id}`);
    const data = await response.json();

    document.getElementById("username").textContent = data.username;
    document.getElementById("email").textContent = data.email;
}

function logout() {
    localStorage.removeItem("user_id");
    window.location.href = "login.html";
}

async function saveAnime(anime_id) {
    const user_id = localStorage.getItem("user_id");

    if (!user_id) {
        alert("Please login first");
        return;
    }

    const watch_status = document.getElementById("status").value;
    const rating = document.getElementById("rating").value;
    const episodes = document.getElementById("episodes").value;

    const response = await fetch("http://127.0.0.1:8000/user_anime", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: parseInt(user_id),
            anime_id: anime_id,
            watch_status: watch_status,
            rating: rating ? parseInt(rating) : null,
            episodes_watched: episodes ? parseInt(episodes) : 0
        })
    });

    const data = await response.json();

    if (response.ok) {
        alert("Saved successfully!");
    } else {
        alert(data.detail || "Error");
    }
}