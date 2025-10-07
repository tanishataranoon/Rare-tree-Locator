document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const menuToggle = document.getElementById('mobile-menu');
  const navLinks = document.querySelector('.nav-links');
  const header = document.querySelector('header');

  // --- Mobile menu toggle ---
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // --- Active link highlighting ---
  const links = document.querySelectorAll('.nav-links a');
  links.forEach(link => {
    link.addEventListener('click', () => {
      links.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
    });
  });

  // --- Mobile dropdown toggle ---
  document.querySelectorAll(".dropdown").forEach(drop => {
    const toggle = drop.querySelector(".dropdown-toggle");
    if (!toggle) return;

    toggle.addEventListener("click", function(e) {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        e.stopPropagation();
        drop.classList.toggle("active");

        // Close other dropdowns
        document.querySelectorAll(".dropdown").forEach(other => {
          if (other !== drop) other.classList.remove("active");
        });
      }
    });

    // Prevent clicks inside dropdown-menu from closing
    const menu = drop.querySelector(".dropdown-menu");
    if (menu) {
      menu.addEventListener("click", e => e.stopPropagation());
    }
  });

  // --- Close dropdown if clicked outside ---
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown").forEach(drop => drop.classList.remove("active"));
  });

  // --- Hide header on scroll down, show on scroll up ---
  if (header) {
    // Add smooth transition
    header.style.transition = "top 0.3s";

    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (scrollTop > lastScrollTop && scrollTop > 50) {
        // Scroll down
        header.style.top = "-100px";
      } else {
        // Scroll up
        header.style.top = "0";
      }
      lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
  }
});
