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

// ===== Hide header on scroll down, show on scroll up =====
let lastScrollTop = 0;

window.addEventListener('scroll', function () {
  let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollTop > lastScrollTop) {
    // scrolling down → hide header
    header.style.top = "-100px"; // adjust if header height differs
  } else {
    // scrolling up → show header
    header.style.top = "0";
  }

  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // prevent negative scroll
});
