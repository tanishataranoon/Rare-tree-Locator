document.addEventListener("DOMContentLoaded", () => {

    // ================= Cookie Helper Function =================
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


    // ================= New Request Modal =================
    const newRequestBtn = document.getElementById("new-request-btn");
    const newRequestModal = document.getElementById("new-request-modal");
    const newRequestClose = document.getElementById("new-request-close");

    if (newRequestBtn && newRequestModal) {
        newRequestBtn.addEventListener("click", () => {
            newRequestModal.style.display = "block";
        });
    }
    if (newRequestClose && newRequestModal) {
        newRequestClose.addEventListener("click", () => {
            newRequestModal.style.display = "none";
        });
    }
    window.addEventListener("click", (e) => {
        if (newRequestModal && e.target === newRequestModal) {
            newRequestModal.style.display = "none";
        }
    });


    // ================= Image Preview =================
    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("image-preview");
    if (imageInput && imagePreview) {
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


    // ================= Form Submission via Fetch API =================
    const newRequestForm = document.getElementById("new-request-form");
    if (newRequestForm) {
        newRequestForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const formData = new FormData(newRequestForm);

            // Clear previous errors
            document.querySelectorAll(".form-error").forEach(el => el.textContent = "");

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
    if (modalClose) {
        modalClose.addEventListener("click", () => requestModal.style.display = "none");
    }
    
    window.addEventListener("click", (e) => { 
        if (e.target === requestModal) requestModal.style.display = "none"; 
    });

    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", () => {
            const card = btn.closest(".request-card-modern");
            if (!card) return;

            const reqId = card.dataset.id;

            // Populate modal details
            const titleElem = document.getElementById("modal-title");
            const idElem = document.getElementById("modal-id");
            const requesterElem = document.getElementById("modal-requester");
            const locationElem = document.getElementById("modal-location");
            const statusElem = document.getElementById("modal-status"); // <-- ADDED
            const dateElem = document.getElementById("modal-date");     // <-- ADDED
            const descElem = document.getElementById("modal-description");

            if (titleElem) titleElem.textContent = card.dataset.title || "Request Details";
            if (idElem) idElem.textContent = reqId;
            if (requesterElem) requesterElem.textContent = card.dataset.requester || "Anonymous";
            if (locationElem) locationElem.textContent = card.dataset.location || "N/A";
            if (statusElem) statusElem.textContent = card.dataset.status || "Pending"; // Sets actual status
            if (dateElem) dateElem.textContent = card.dataset.date || "N/A";           // Sets actual date
            if (descElem) descElem.textContent = card.dataset.description || "";
            
            const img = document.getElementById("modal-image");
            if (img) {
                const imageTag = card.querySelector("img");
                img.src = imageTag ? imageTag.src : "";
            }

            // View Answer link update
            const viewAnswerElem = document.getElementById("view-answer-link") || document.getElementById("view-answer-btn");
            if (viewAnswerElem) {
                const targetUrl = `/dashboard/requests/${reqId}/answer/`;
                if (viewAnswerElem.tagName === "A") {
                    viewAnswerElem.href = targetUrl;
                } else {
                    viewAnswerElem.onclick = () => { window.location.href = targetUrl; };
                }
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
            btn.addEventListener("click", (e) => {
                e.stopPropagation(); // Prevents triggering card view click events
                deleteRequestId = btn.dataset.id;
                deleteModal.style.display = "block";
            });
        });

        if (deleteClose) deleteClose.addEventListener("click", () => deleteModal.style.display = "none");
        if (cancelDelete) cancelDelete.addEventListener("click", () => deleteModal.style.display = "none");
        window.addEventListener("click", (e) => { 
            if (e.target === deleteModal) deleteModal.style.display = "none"; 
        });

        if (confirmDelete) {
            confirmDelete.addEventListener("click", () => {
                if (!deleteRequestId) return;
                
                fetch(`/dashboard/requests/${deleteRequestId}/delete/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                })
                .then(res => res.json())
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
    }
});