document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================================
  // 1. Live Search & Filtering
  // ==========================================================
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  const cards = document.querySelectorAll(".tree-card");

  function filterTrees() {
    if (!searchInput) return;
    const query = searchInput.value.toLowerCase().trim();

    cards.forEach(card => {
      const streetName = card.querySelector("h3")?.textContent.toLowerCase() || "";
      const scientificName = card.querySelector(".scientific-name")?.textContent.toLowerCase() || "";
      const metaText = card.querySelector(".meta")?.textContent.toLowerCase() || "";

      const matches = streetName.includes(query) || 
                      scientificName.includes(query) || 
                      metaText.includes(query);

      card.style.display = matches ? "" : "none";
    });
  }

  if (searchBtn && searchInput) {
    searchBtn.addEventListener("click", filterTrees);
    searchInput.addEventListener("keyup", (e) => {
      if (e.key === "Enter") filterTrees();
    });
  }

  // ==========================================================
  // 2. Contributor Delete Action
  // ==========================================================
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const treeId = btn.dataset.id;
      if (!confirm("Are you sure you want to delete this tree record?")) return;

      fetch(`/trees/${treeId}/delete/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest"
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const card = btn.closest(".card");
          card.style.transition = "opacity 0.3s ease, transform 0.3s ease";
          card.style.opacity = "0";
          card.style.transform = "scale(0.9)";
          setTimeout(() => card.remove(), 300);
        } else {
          alert(data.error || "Failed to delete the tree record.");
        }
      })
      .catch(error => console.error("Error deleting tree:", error));
    });
  });

  // ==========================================================
  // 3. Edit Modal Management
  // ==========================================================
  const modal = document.getElementById("editTreeModal");
  const form = document.getElementById("editTreeForm");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const cancelModalBtn = document.getElementById("cancelModalBtn");

  const hideModal = () => modal?.classList.add("hidden");

  // Open & Populate Modal
  document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      // Read data straight from button data attributes
      document.getElementById("editTreeId").value = btn.dataset.id || "";
      document.getElementById("editStreetName").value = btn.dataset.street || "";
      document.getElementById("editScientificName").value = btn.dataset.scientific || "";
      document.getElementById("editHabitat").value = btn.dataset.habitat || "";
      document.getElementById("editDescription").value = btn.dataset.description || "";
      document.getElementById("editRarityStatus").value = btn.dataset.rarity || "";
      document.getElementById("editHeight").value = btn.dataset.height || "";
      document.getElementById("editAge").value = btn.dataset.age || "";
      document.getElementById("editLatitude").value = btn.dataset.lat || "";
      document.getElementById("editLongitude").value = btn.dataset.lng || "";

      modal?.classList.remove("hidden");
    });
  });

  // Close Modal Events
  closeModalBtn?.addEventListener("click", hideModal);
  cancelModalBtn?.addEventListener("click", hideModal);
  
  // Close modal when clicking dark overlay outside
  window.addEventListener("click", (e) => {
    if (e.target === modal) hideModal();
  });

  // Submit Modal Form (AJAX Update)
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const treeId = document.getElementById("editTreeId").value;
      const formData = new FormData(form);

      fetch(`/trees/${treeId}/update/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert("Tree updated successfully!");
          location.reload(); // Refresh page to display updated details
        } else {
          alert(data.error || "Error updating tree details.");
        }
      })
      .catch(error => console.error("Error submitting form:", error));
    });
  }

  // ==========================================================
  // Helper: Django CSRF Cookie Fetcher
  // ==========================================================
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

});