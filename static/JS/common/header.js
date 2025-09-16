function navigate(page) {
  console.log("Navigating to:", page);

  // Reset desktop nav
  document.querySelectorAll(".nav-links button").forEach(btn => {
    btn.classList.remove("active");
  });

  // Reset mobile nav
  document.querySelectorAll(".mobile-dropdown button").forEach(btn => {
    btn.classList.remove("active");
  });

  function navigate(page) {
  // Remove old active classes
  document.querySelectorAll(".nav-links button").forEach(btn => {
    btn.classList.remove("active");
  });

  // Redirect pages
  if (page === "home") {
    window.location.href = "/template/homepage.html"; // homepage
  }
  if (page === "trees") {
    window.location.href = "/template/Trees/TreeProfiles.html"; // trees page
  }
  if (page === "blog") {
    window.location.href = "/template/blog.html"; // blog page
  }

  // Set active state
  if (page === "home") {
    document.getElementById("nav-home")?.classList.add("active");
  }
  if (page === "trees") {
    document.getElementById("nav-trees")?.classList.add("active");
  }
  if (page === "blog") {
    document.getElementById("nav-blog")?.classList.add("active");
  }
}


  // Close menu on navigation (mobile)
  document.getElementById("mobileDropdown").style.display = "none";
}

function toggleMenu() {
  const dropdown = document.getElementById("mobileDropdown");
  dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
}
