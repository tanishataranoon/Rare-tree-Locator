// script.js - add this file in the same folder as index.html
document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.blog-card');

  if (!cards.length) {
    console.warn('No .blog-card elements found on the page.');
    return;
  }

  // Use IntersectionObserver if available (best perf)
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          obs.unobserve(entry.target); // animate once
        }
      });
    }, { threshold: 0.12 });

    cards.forEach(c => io.observe(c));
  } else {
    // fallback: on scroll
    const onScroll = () => {
      cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight - 60) {
          card.classList.add('visible');
        }
      });
    };
    onScroll();
    window.addEventListener('scroll', onScroll);
  }
});
