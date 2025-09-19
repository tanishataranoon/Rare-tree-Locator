// Get URLs from template
const urls = document.getElementById("urls").dataset;

function navigate(page) {
  if (page === "home") window.location.href = urls.home;
  if (page === "trees") window.location.href = urls.trees;
  if (page === "blog") window.location.href = urls.blog;
  if (page === "login") window.location.href = urls.login;
  if (page === "signup") window.location.href = urls.signup;
}

// Highlight active nav on page load
window.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path === urls.home || path === "/") {
    document.getElementById("nav-home")?.classList.add("active");
    document.getElementById("m-nav-home")?.classList.add("active");
  } else if (path.startsWith(urls.trees)) {
    document.getElementById("nav-trees")?.classList.add("active");
    document.getElementById("m-nav-trees")?.classList.add("active");
  } else if (path.startsWith(urls.blog)) {
    document.getElementById("nav-blog")?.classList.add("active");
    document.getElementById("m-nav-blog")?.classList.add("active");
  }
});

// Toggle mobile menu
function toggleMenu() {
  const dropdown = document.getElementById("mobileDropdown");
  if (dropdown) {
    dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
  }
}
