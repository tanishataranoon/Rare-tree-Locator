const menuToggle = document.getElementById('mobile-menu');
const navLinks = document.querySelector('.nav-links');
const header = document.querySelector('header');

// ===== Mobile menu toggle =====
menuToggle.addEventListener('click', () => {
  navLinks.classList.toggle('active');
});

// ===== Active link highlighting =====
const links = document.querySelectorAll('.nav-links a');
links.forEach(link => {
  link.addEventListener('click', () => {
    links.forEach(l => l.classList.remove('active'));
    link.classList.add('active');
  });
});

// ===== Mobile dropdown toggle =====
document.querySelectorAll(".dropdown").forEach(drop => {
  const toggle = drop.querySelector(".dropdown-toggle");

  toggle.addEventListener("click", function(e) {
    if (window.innerWidth <= 768) {
      e.preventDefault();
      e.stopPropagation(); // Prevent document click from closing it
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

// ===== Close dropdown if clicked outside =====
document.addEventListener("click", () => {
  document.querySelectorAll(".dropdown").forEach(drop => drop.classList.remove("active"));
});

// ===== Hide header on scroll down, show on scroll up =====
let lastScrollTop = 0;
window.addEventListener('scroll', function () {
  let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  header.style.top = (scrollTop > lastScrollTop) ? "-100px" : "0";
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

const profilePic = document.querySelector('.profile-pic');
const profilePanel = document.querySelector('.profile-panel');
const overlay = document.getElementById('overlay');

if (profilePic && profilePanel && overlay) {
  profilePic.addEventListener('click', (e) => {
    e.preventDefault();
    profilePanel.classList.add('active');
    overlay.classList.add('active');
    document.body.classList.add('no-scroll');
  });

  overlay.addEventListener('click', () => {
    profilePanel.classList.remove('active');
    overlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
  });
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    profilePanel.classList.remove('active');
    overlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
  }
});
