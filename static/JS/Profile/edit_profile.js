// Global Toast Helper (Accessible to Django inline <script> tags)
window.showToast = function (message) {
    if (!message) return;

    const toast = document.createElement("div");
    toast.className = "toast-message";
    toast.textContent = message; // Using textContent over innerText for better performance

    document.body.appendChild(toast);

    // Trigger CSS slide-in/fade-in
    requestAnimationFrame(() => {
        toast.classList.add("show");
    });

    // Auto-remove toast after 3.5s
    setTimeout(() => {
        toast.classList.remove("show");
        toast.addEventListener("transitionend", () => toast.remove(), { once: true });
    }, 3500);
};

document.addEventListener("DOMContentLoaded", () => {
    // ---------- Profile Picture Preview ----------
    const avatarInput = document.getElementById("id_profile_pic");
    const avatarPreview = document.getElementById("avatarPreview");

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (!file) return;

            // Revoke old object URL if present to free memory
            if (avatarPreview.dataset.objectUrl) {
                URL.revokeObjectURL(avatarPreview.dataset.objectUrl);
            }

            // Create temporary URL for immediate preview
            const objectUrl = URL.createObjectURL(file);
            avatarPreview.src = objectUrl;
            avatarPreview.dataset.objectUrl = objectUrl;
        });
    }
});