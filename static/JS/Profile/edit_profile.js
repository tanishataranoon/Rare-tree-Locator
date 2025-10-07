document.addEventListener("DOMContentLoaded", function () {

    // ---------- Profile Picture Preview ----------
    const avatarInput = document.getElementById("id_profile_pic");
    const avatarPreview = document.getElementById("avatarPreview");

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    avatarPreview.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // ---------- Toast Messages from Django ----------
    // If you use Django messages framework, you can render them in template:
    // Example in edit_profile.html:
    // {% if messages %}
    //   {% for message in messages %}
    //     <script>showToast("{{ message }}");</script>
    //   {% endfor %}
    // {% endif %}
    function showToast(message) {
        let toast = document.createElement("div");
        toast.className = "toast-message";
        toast.innerText = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add("show"), 100);
        setTimeout(() => {
            toast.classList.remove("show");
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

});
