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