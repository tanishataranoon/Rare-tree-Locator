document.addEventListener("DOMContentLoaded", function () {
    // ===== Modal Handling =====
    const createModal = document.getElementById("createModal");
    const openCreateBtn = document.getElementById("openCreateModal");
    const closeCreateBtn = document.getElementById("closeCreateModal");
  
    openCreateBtn.onclick = () => (createModal.style.display = "block");
    closeCreateBtn.onclick = () => (createModal.style.display = "none");
  
    const editModal = document.getElementById("editModal");
    const closeEditBtn = document.getElementById("closeEditModal");
  
    document.querySelectorAll(".edit-request-btn").forEach((btn) => {
      btn.onclick = () => {
        document.getElementById("edit_request_id").value = btn.dataset.id;
        document.getElementById("edit_title").value = btn.dataset.title;
        document.getElementById("edit_description").value =
          btn.dataset.description;
        document.getElementById("edit_location").value = btn.dataset.location;
        editModal.style.display = "block";
      };
    });
  
    closeEditBtn.onclick = () => (editModal.style.display = "none");
  
    const deleteModal = document.getElementById("deleteModal");
    const closeDeleteBtn = document.getElementById("closeDeleteModal");
    const cancelDeleteBtn = document.getElementById("cancelDelete");
  
    document.querySelectorAll(".delete-request-btn").forEach((btn) => {
      btn.onclick = () => {
        document.getElementById("delete_request_id").value = btn.dataset.id;
        deleteModal.style.display = "block";
      };
    });
  
    closeDeleteBtn.onclick = () => (deleteModal.style.display = "none");
    cancelDeleteBtn.onclick = () => (deleteModal.style.display = "none");
  
    window.onclick = (e) => {
      if (e.target === createModal) createModal.style.display = "none";
      if (e.target === editModal) editModal.style.display = "none";
      if (e.target === deleteModal) deleteModal.style.display = "none";
    };
  
    // ===== AJAX Create Request =====
    document.getElementById("createRequestForm").onsubmit = function (e) {
      e.preventDefault();
      const formData = new FormData(this);
  
      fetch(ajaxCreateUrl, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) location.reload();
          else alert("Error: " + JSON.stringify(data.errors));
        })
        .catch((err) => console.error("Create failed:", err));
    };
  
    // ===== AJAX Edit Request =====
    document.getElementById("editRequestForm").onsubmit = function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const requestId = document.getElementById("edit_request_id").value;
  
      fetch(`${ajaxUpdateUrl}${requestId}/`, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) location.reload();
          else alert("Error: " + JSON.stringify(data.errors));
        })
        .catch((err) => console.error("Update failed:", err));
    };
  
    // ===== AJAX Delete Request =====
    document.getElementById("deleteRequestForm").onsubmit = function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const requestId = document.getElementById("delete_request_id").value;
  
      fetch(`${ajaxDeleteUrl}${requestId}/`, {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) location.reload();
          else alert("Error deleting request.");
        })
        .catch((err) => console.error("Delete failed:", err));
    };
  });
  