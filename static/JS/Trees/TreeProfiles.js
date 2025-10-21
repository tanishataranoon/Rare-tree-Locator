document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");

  // Subtle hover glow animation
  cards.forEach(card => {
    card.addEventListener("mouseenter", () => {
      card.style.boxShadow = "0 15px 40px rgba(0,0,0,0.2)";
    });
    card.addEventListener("mouseleave", () => {
      card.style.boxShadow = "0 6px 20px rgba(0,0,0,0.08)";
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const cards = document.querySelectorAll(".grid-container .card");

  function filterTrees() {
    const query = searchInput.value.toLowerCase().trim();

    cards.forEach(card => {
      const name = card.querySelector("h3")?.textContent.toLowerCase() || "";
      const scientific = card.querySelector("p")?.textContent.toLowerCase() || "";
      const location = card.querySelector(".meta span")?.textContent.toLowerCase() || "";

      if (name.includes(query) || scientific.includes(query) || location.includes(query)) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });
  }

  // Trigger on button click or Enter key
  searchBtn.addEventListener("click", filterTrees);
  searchInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") filterTrees();
  });
});
