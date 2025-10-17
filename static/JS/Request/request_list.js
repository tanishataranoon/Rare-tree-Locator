document.addEventListener("DOMContentLoaded", () => {
    // ================= New Request Modal =================
    const newRequestBtn = document.getElementById("new-request-btn");
    const newRequestModal = document.getElementById("new-request-modal");
    const newRequestClose = document.getElementById("new-request-close");

    if (newRequestBtn) {
        newRequestBtn.addEventListener("click", () => {
            newRequestModal.style.display = "block";
        });
    }
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
            e.preventDefault();
            const formData = new FormData(newRequestForm);

            fetch(newRequestForm.action, {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert("Request created successfully!");
                    location.reload();
                } else if (data.errors) {
                    for (let field in data.errors) {
                        const errorDiv = document.getElementById(`${field}-error`);
                        if (errorDiv) errorDiv.textContent = data.errors[field].join(", ");
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

                // Populate modal details
                document.getElementById("modal-title").textContent = card.dataset.title;
                document.getElementById("modal-id").textContent = card.dataset.id;
                document.getElementById("modal-requester").textContent = card.dataset.requester;
                document.getElementById("modal-location").textContent = card.dataset.location;
                document.getElementById("modal-description").textContent = card.dataset.description;
                const img = document.getElementById("modal-image");
                const imageTag = card.querySelector("img");
                img.src = imageTag ? imageTag.src : "";

                // ================= View Answer Button =================
                const viewAnswerBtn = document.getElementById("view-answer-btn");
                if (viewAnswerBtn) {
                    if (card.dataset.hasAnswer === "true") {
                        viewAnswerBtn.style.display = "inline-block";
                        viewAnswerBtn.onclick = () => {
                            window.location.href = `/requests/${card.dataset.id}/answer/view/`;
                        };
                    } else {
                        viewAnswerBtn.style.display = "none";
                    }
                }

                // ================= Answer Button (for contributors/admins) =================
                const answerBtn = document.getElementById("answer-btn");
                if (answerBtn) {
                    const reqId = card.dataset.id;
                    answerBtn.href = `/requests/${reqId}/answer/`;
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

        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", () => {
                deleteRequestId = btn.dataset.id;
                deleteModal.style.display = "block";
            });
        });

        deleteClose.addEventListener("click", () => deleteModal.style.display = "none");
        cancelDelete.addEventListener("click", () => deleteModal.style.display = "none");
        window.addEventListener("click", (e) => { if (e.target === deleteModal) deleteModal.style.display = "none"; });

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
            .then(res => res.json())
            .then(data => {
                if (data.success) location.reload();
                else alert(data.error || "Delete failed!");
            })
            .catch(err => {
                console.error(err);
                alert("Delete failed due to server error.");
            });
        });
    }
});
$("#new-request-form").on("submit", function(e) {
    e.preventDefault();
    $.ajax({
        url: "{% url 'create_request' %}",
        type: "POST",
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success) {
                alert("Request created successfully!");
                location.reload(); // reload to show the new request
            } else {
                alert("Error: " + JSON.stringify(data.errors));
            }
        }
    });
});
