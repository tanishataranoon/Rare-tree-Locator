document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;

    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const requestId = this.dataset.id;
            if (!confirm("Are you sure you want to delete this request?")) return;

            fetch(`/requests/${requestId}/delete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            }).then(response => {
                if (response.ok) {
                    document.getElementById(`request-card-${requestId}`).remove();
                } else {
                    alert("Error deleting request.");
                }
            });
        });
    });

    document.querySelectorAll(".edit-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const requestId = this.dataset.id;
            window.location.href = `/requests/${requestId}/edit/`;
        });
    });

    document.querySelectorAll(".view-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const requestId = this.dataset.id;
            window.location.href = `/requests/${requestId}/`;
        });
    });
});
