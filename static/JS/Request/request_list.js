document.addEventListener("DOMContentLoaded", () => {
    // ================= New Request Modal =================
    const newRequestBtn = document.getElementById("new-request-btn");
    const newRequestModal = document.getElementById("new-request-modal");
    const newRequestClose = document.getElementById("new-request-close");

    // Open modal
    if (newRequestBtn) {
        newRequestBtn.addEventListener("click", () => {
            newRequestModal.style.display = "block";
        });
    }

    // Close modal
    if (newRequestClose) {
        newRequestClose.addEventListener("click", () => {
            newRequestModal.style.display = "none";
        });
    }
    window.addEventListener("click", (e) => {
        if (e.target === newRequestModal) newRequestModal.style.display = "none";
    });

    // ================= Image Preview =================
    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("image-preview");
    if (imageInput) {
        imageInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview" class="preview-img">`;
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.innerHTML = "";
            }
        });
    }

    // ================= Form Submission via AJAX =================
    const newRequestForm = document.getElementById("new-request-form");
    if (newRequestForm) {
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

        newRequestForm.addEventListener("submit", (e) => {
            e.preventDefault(); // prevent page reload

            const formData = new FormData(newRequestForm);

            fetch(newRequestForm.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                body: formData
            })
            .then(res => {
                if (!res.ok) throw new Error("Server error");
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    alert("Request created successfully!");
                    location.reload();
                } else if (data.errors) {
                    // Display form errors
                    for (let field in data.errors) {
                        const errorDiv = document.getElementById(`${field}-error`);
                        if (errorDiv) {
                            errorDiv.textContent = data.errors[field].join(", ");
                        }
                    }
                } else {
                    alert(data.error || "Failed to create request.");
                }
            })
            .catch(err => {
                console.error(err);
                alert("Server error while creating request.");
            });
        });
    }



    // ================= Request Details Modal =================
    const requestModal = document.getElementById("request-modal");
    if (requestModal) {
        const modalClose = requestModal.querySelector(".close");
        modalClose.addEventListener("click", () => requestModal.style.display = "none");
        window.addEventListener("click", (e) => { if (e.target === requestModal) requestModal.style.display = "none"; });

        document.querySelectorAll(".btn-view").forEach(btn => {
            btn.addEventListener("click", () => {
                const card = btn.closest(".request-card-modern");
                document.getElementById("modal-title").textContent = card.dataset.title;
                document.getElementById("modal-id").textContent = card.dataset.id;
                document.getElementById("modal-requester").textContent = card.dataset.requester;
                document.getElementById("modal-location").textContent = card.dataset.location;
                document.getElementById("modal-description").textContent = card.dataset.description;
                const img = document.getElementById("modal-image");
                const imageTag = card.querySelector("img");
                img.src = imageTag ? imageTag.src : "";
                 // Show buttons dynamically
                const viewAnswerBtn = document.getElementById("view-answer-btn");
                const answerBtn = document.querySelector(".open-answer-modal");

                // If user is common
                if (viewAnswerBtn) {
                    if (card.dataset.hasAnswer === "true") {
                        viewAnswerBtn.style.display = "inline-block";
                } else {
                    viewAnswerBtn.style.display = "none";
                }
            }

            // If user is contributor/admin
            if (answerBtn) {
                answerBtn.dataset.requestId = card.dataset.id;
                answerBtn.style.display = "inline-block";
            }

            requestModal.style.display = "block";
            });
        });
    }

    // ================= Delete Modal =================
    const deleteModal = document.getElementById("delete-modal");
    if (deleteModal) {
        const deleteClose = deleteModal.querySelector(".close");
        const cancelDelete = document.getElementById("cancel-delete");
        const confirmDelete = document.getElementById("confirm-delete");
        let deleteRequestId = null;

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

        // Open Delete Modal
        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", () => {
                deleteRequestId = btn.dataset.id;
                deleteModal.style.display = "block";
            });
        });

        // Close modal
        deleteClose.addEventListener("click", () => deleteModal.style.display = "none");
        cancelDelete.addEventListener("click", () => deleteModal.style.display = "none");
        window.addEventListener("click", (e) => { if (e.target === deleteModal) deleteModal.style.display = "none"; });

        // Confirm Delete
        confirmDelete.addEventListener("click", () => {
            if (!deleteRequestId) return;

            fetch(`/requests/${deleteRequestId}/delete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            })
            .then(res => {
                if (!res.ok) throw new Error("Server error");
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.error || "Delete failed!");
                }
            })
            .catch(err => {
                console.error(err);
                alert("Delete failed due to server error.");
            });
        });
    }
});
// ================= Answer Modal =================
const answerModalContainer = document.getElementById("answerModalContainer");

// Only run if Answer buttons exist
if (document.querySelectorAll(".open-answer-modal").length > 0) {
    document.querySelectorAll(".open-answer-modal").forEach(btn => {
        btn.addEventListener("click", function () {
            const requestId = this.dataset.requestId;

            // Fetch the answer modal HTML
            fetch(`/answer-modal/${requestId}/`)
                .then(res => res.text())
                .then(html => {
                    // Inject modal HTML dynamically
                    if (answerModalContainer) {
                        answerModalContainer.innerHTML = html;
                    } else {
                        console.error("Missing #answerModalContainer in HTML!");
                        return;
                    }

                    // Initialize Bootstrap modal
                    const modalEl = document.getElementById("answerModal");
                    const modal = new bootstrap.Modal(modalEl);
                    modal.show();

                    // Attach form submission
                    const form = document.getElementById("answerForm");
                    if (form) {
                        form.addEventListener("submit", e => {
                            e.preventDefault();
                            const formData = new FormData(form);

                            fetch(`/submit-answer/${requestId}/`, {
                                method: "POST",
                                body: formData,
                            })
                                .then(res => res.json())
                                .then(data => {
                                    if (data.success) {
                                        modal.hide();
                                        // Reload to reflect updated status
                                        location.reload();
                                    } else {
                                        alert("Error: " + JSON.stringify(data.errors));
                                    }
                                })
                                .catch(err => {
                                    console.error("Error submitting answer:", err);
                                    alert("Failed to submit answer.");
                                });
                        });
                    }
                })
                .catch(err => console.error("Error loading answer modal:", err));
        });
    });
}
