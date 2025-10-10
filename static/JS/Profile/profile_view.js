// Handle tab switching
function showTab(tabId, event) {
    document.querySelectorAll(".tab-content").forEach(div => div.classList.remove("active"));
    document.querySelectorAll(".tabs button").forEach(btn => btn.classList.remove("active"));

    document.getElementById(tabId).classList.add("active");
    if (event) event.currentTarget.classList.add("active");
}

// Show "trees" tab by default when page loads
document.addEventListener("DOMContentLoaded", () => {
    showTab("trees");

    // Delete modal for posts and requests
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const modal = document.getElementById("deleteModal");
    const closeBtn = modal.querySelector(".close");
    const cancelBtn = modal.querySelector(".cancel-btn");
    const deleteForm = document.getElementById("deleteForm");
    const modalText = document.getElementById("modal-text");
    const modalHeading = modal.querySelector("h2");

    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const type = button.dataset.type; // "post" or "request"
            const id = button.dataset.id;
            const title = button.dataset.title || (type === "post" ? "Post" : "Request");

            // Set modal heading
            modalHeading.textContent = type === "post" ? "Delete Post" : "Delete Request";

            // Set modal text
            modalText.textContent = `Are you sure you want to delete "${title}"?`;

            // Set form action dynamically
            deleteForm.action = type === "post" ? `/blog_delete/${id}/` : `/requests/${id}/delete/`;

            // Show modal
            modal.classList.add("show");
        });
    });

    // Close modal handlers
    const closeModal = () => modal.classList.remove("show");
    closeBtn.addEventListener("click", closeModal);
    cancelBtn.addEventListener("click", closeModal);
    window.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    // Toggle "Show More Details" dropdown
    const toggleBtn = document.querySelector(".toggle-details-btn");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            const details = document.getElementById("extra-details");
            if (!details) return;
            details.classList.toggle("show");
            toggleBtn.textContent = details.classList.contains("show") ? "Hide Details" : "Show More Details";
        });
    }
});
