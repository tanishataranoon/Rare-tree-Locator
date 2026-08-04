/**
 * Profile Page Interactivity
 * Path: static/JS/Profile/profile_view.js
 */

document.addEventListener("DOMContentLoaded", function () {
    // --------------------------------------------------------------------------
    // 1. Tab Switching Functionality
    // --------------------------------------------------------------------------
    window.showTab = function (tabId, event) {
        if (event) {
            event.preventDefault();
        }

        // Hide all tab content panes
        const tabContents = document.querySelectorAll(".tab-content");
        tabContents.forEach((content) => {
            content.classList.remove("active");
            content.style.display = "none";
        });

        // Deactivate all tab buttons
        const tabButtons = document.querySelectorAll(".tab-btn");
        tabButtons.forEach((btn) => {
            btn.classList.remove("active");
        });

        // Show selected tab content
        const targetTab = document.getElementById(tabId);
        if (targetTab) {
            targetTab.classList.add("active");
            targetTab.style.display = "block";
        }

        // Highlight the clicked button
        if (event && event.currentTarget) {
            event.currentTarget.classList.add("active");
        }
    };

    // Initialize display state for default active tab on page load
    const initialActiveTab = document.querySelector(".tab-content.active");
    if (initialActiveTab) {
        initialActiveTab.style.display = "block";
    }

    // --------------------------------------------------------------------------
    // 2. Toggle Extra Profile Details (Phone, Social Links)
    // --------------------------------------------------------------------------
    const toggleDetailsBtn = document.querySelector(".toggle-details-btn");
    const extraDetails = document.getElementById("extra-details");

    if (toggleDetailsBtn && extraDetails) {
        // Hide details by default
        extraDetails.style.display = "none";

        toggleDetailsBtn.addEventListener("click", function () {
            const isHidden = extraDetails.style.display === "none";

            if (isHidden) {
                extraDetails.style.display = "block";
                toggleDetailsBtn.textContent = "Hide Details";
            } else {
                extraDetails.style.display = "none";
                toggleDetailsBtn.textContent = "Show More Details";
            }
        });
    }

    // --------------------------------------------------------------------------
    // 3. "See More" Card Expansion Handler
    // --------------------------------------------------------------------------
    const seeMoreButtons = document.querySelectorAll(".see-more-btn");

    seeMoreButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Find parent tab content block
            const currentTab = this.closest(".tab-content");
            if (!currentTab) return;

            // Reveal all hidden cards inside this tab
            const hiddenCards = currentTab.querySelectorAll(".hidden-card");
            hiddenCards.forEach((card) => {
                card.classList.remove("hidden-card");
            });

            // Hide the "See More" button once expanded
            this.style.display = "none";
        });
    });

    // --------------------------------------------------------------------------
    // 4. Modal Handler (Prepared for comment-enabled delete modal)
    // --------------------------------------------------------------------------
    const deleteModal = document.getElementById("deleteModal");
    const closeModalBtn = document.querySelector("#deleteModal .close");
    const cancelModalBtn = document.querySelector("#deleteModal .cancel-btn");

    window.openDeleteModal = function (postTitle, deleteUrl) {
        if (!deleteModal) return;

        const modalText = document.getElementById("modal-text");
        const deleteForm = document.getElementById("deleteForm");

        if (modalText) {
            modalText.textContent = `Are you sure you want to delete "${postTitle}"?`;
        }
        if (deleteForm) {
            deleteForm.action = deleteUrl;
        }

        deleteModal.classList.add("show");
        deleteModal.style.display = "flex";
    };

    function closeDeleteModal() {
        if (!deleteModal) return;
        deleteModal.classList.remove("show");
        deleteModal.style.display = "none";
    }

    if (closeModalBtn) closeModalBtn.addEventListener("click", closeDeleteModal);
    if (cancelModalBtn) cancelModalBtn.addEventListener("click", closeDeleteModal);

    window.addEventListener("click", function (event) {
        if (event.target === deleteModal) {
            closeDeleteModal();
        }
    });
});