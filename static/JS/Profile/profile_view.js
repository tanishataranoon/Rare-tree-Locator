// Handle tab switching
function showTab(tabId, event) {
    document.querySelectorAll(".tab-content").forEach(div => div.classList.remove("active"));
    document.querySelectorAll(".tabs button").forEach(btn => btn.classList.remove("active"));

    document.getElementById(tabId).classList.add("active");
    if(event) event.target.classList.add("active");
}


// Show "trees" tab by default when page loads
document.addEventListener("DOMContentLoaded", () => {
    showTab("trees");
});
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const modal = document.getElementById("deleteModal");
    const closeBtn = modal.querySelector(".close");
    const cancelBtn = modal.querySelector(".cancel-btn");
    const deleteForm = document.getElementById("deleteForm");
    const modalText = document.getElementById("modal-text");

    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const postId = button.dataset.postId;
            const postTitle = button.dataset.postTitle;
            modalText.textContent = `Are you sure you want to delete "${postTitle}"?`;
            deleteForm.action = `/blog_delete/${postId}/`;
            modal.classList.add("show");
        });
    });
    
    closeBtn.onclick = cancelBtn.onclick = () => modal.classList.remove("show");
    window.onclick = (event) => {
        if (event.target === modal) modal.classList.remove("show");
    }
});
// =========================
// Toggle "Show More Details" dropdown
// =========================
function toggleDetails() {
    const details = document.getElementById("extra-details");
    const btn = document.querySelector(".toggle-details-btn");

    if (!details || !btn) return;

    // Smooth show/hide
    if (details.classList.contains("show")) {
        details.style.maxHeight = null;
        details.classList.remove("show");
        btn.textContent = "Show More Details";
    } else {
        details.classList.add("show");
        details.style.maxHeight = details.scrollHeight + "px";
        btn.textContent = "Hide Details";
    }
}
