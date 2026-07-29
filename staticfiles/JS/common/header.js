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
      e.stopPropagation();
      drop.classList.toggle("active");
      document.querySelectorAll(".dropdown").forEach(other => {
        if (other !== drop) other.classList.remove("active");
      });
    }
  });

  const menu = drop.querySelector(".dropdown-menu");
  if (menu) menu.addEventListener("click", e => e.stopPropagation());
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

// ===== Profile sidebar toggle =====
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
    const notifPopup = document.getElementById('notif-popup');
    if (notifPopup) notifPopup.style.display = 'none';
  });
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    profilePanel.classList.remove('active');
    overlay.classList.remove('active');
    document.body.classList.remove('no-scroll');
    const notifPopup = document.getElementById('notif-popup');
    if (notifPopup) notifPopup.style.display = 'none';
  }
});

// ===== Notifications =====
document.addEventListener('DOMContentLoaded', () => {
  const notifLink = document.getElementById('notif-link');
  const notifPopup = document.getElementById('notif-popup');
  const markReadBtn = document.getElementById('mark-read-btn');

  // Get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  if (notifPopup) notifPopup.style.display = 'none';

  // Toggle popup
  if (notifLink && notifPopup) {
    notifLink.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      notifPopup.style.display = (notifPopup.style.display === 'block') ? 'none' : 'block';
    });
  }

  // Mark all notifications as read
  if (markReadBtn) {
    markReadBtn.addEventListener('click', () => {
      fetch(markReadUrl, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const badge = document.querySelector('#notif-link .notif-count');
          if (badge) badge.style.display = 'none';
          notifPopup.querySelectorAll('li.unread').forEach(li => li.classList.remove('unread'));
        }
      })
      .catch(err => console.error('Error marking as read:', err));
    });
  }

  // Mark single notification as read
  if (notifPopup) {
    notifPopup.querySelectorAll('li.unread a').forEach(link => {
      link.addEventListener('click', (e) => {
        const li = link.closest('li');
        const notifId = li.dataset.id;

        fetch(`${markSingleUrlBase}/${notifId}/`, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrftoken },
        })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            li.classList.remove('unread');

            // Update badge count
            const badge = document.querySelector('#notif-link .notif-count');
            if (badge) {
              let count = parseInt(badge.textContent) - 1;
              if (count > 0) badge.textContent = count;
              else badge.style.display = 'none';
            }
          }
        });
      });
    });
  }

  // Close popup if clicked outside
  document.addEventListener('click', (e) => {
    if (notifPopup && notifLink && !notifPopup.contains(e.target) && !notifLink.contains(e.target)) {
      notifPopup.style.display = 'none';
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && notifPopup) notifPopup.style.display = 'none';
  });
});
