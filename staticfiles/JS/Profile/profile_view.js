// Tab switching
function showTab(tabId, event) {
    document.querySelectorAll(".tab-content").forEach(div => div.classList.remove("active"));
    document.querySelectorAll(".tabs button").forEach(btn => btn.classList.remove("active"));
    const tab = document.getElementById(tabId);
    if (tab) tab.classList.add("active");
    if (event) event.currentTarget.classList.add("active");
}

document.addEventListener("DOMContentLoaded", () => {
    // Default tab
    const defaultTab = document.querySelector(".tabs button.active");
    if (defaultTab) defaultTab.click();

    // Delete modal
    const deleteButtons = document.querySelectorAll(".delete-btn");
    const modal = document.getElementById("deleteModal");
    if (modal) {
        const closeBtn = modal.querySelector(".close");
        const cancelBtn = modal.querySelector(".cancel-btn");
        const deleteForm = document.getElementById("deleteForm");
        const modalText = document.getElementById("modal-text");
        const modalHeading = modal.querySelector("h2");

        deleteButtons.forEach(button => {
            button.addEventListener("click", () => {
                const type = button.dataset.type;
                const id = button.dataset.id;
                const title = button.dataset.title || (type === "post" ? "Post" : "Request");

                modalHeading.textContent = type === "post" ? "Delete Post" : "Delete Request";
                modalText.textContent = `Are you sure you want to delete "${title}"?`;
                deleteForm.action = type === "post" ? `/blog_delete/${id}/` : `/requests/${id}/delete/`;
                modal.classList.add("show");
            });
        });

        const closeModal = () => modal.classList.remove("show");
        closeBtn.addEventListener("click", closeModal);
        cancelBtn.addEventListener("click", closeModal);
        window.addEventListener("click", e => { if (e.target === modal) closeModal(); });
    }

    // Toggle Show More Details
    const toggleBtn = document.querySelector(".toggle-details-btn");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", () => {
            const details = document.getElementById("extra-details");
            if (!details) return;
            details.classList.toggle("show");
            toggleBtn.textContent = details.classList.contains("show") ? "Hide Details" : "Show More Details";
        });
    }

    // See More Cards
    const seeMoreBtns = document.querySelectorAll("#see-more-btn");
    seeMoreBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const tab = btn.closest(".tab-content");
            const hiddenCards = tab.querySelectorAll(".hidden-card");
            hiddenCards.forEach(c => c.classList.toggle("show-card"));
            btn.textContent = btn.textContent === "See More" ? "See Less" : "See More";
        });
    });
});
