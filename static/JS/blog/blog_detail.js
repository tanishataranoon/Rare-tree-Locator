
document.addEventListener("DOMContentLoaded", function() {
    const bookmarkBtn = document.getElementById("bookmark-btn");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    if (bookmarkBtn) {
        bookmarkBtn.addEventListener("click", function() {
            const postId = this.dataset.postId;

            fetch(`/post/${postId}/bookmark/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
            })
            .then(res => res.json())
            .then(data => {
                if (data.bookmarked) {
                    bookmarkBtn.textContent = "❤️ Bookmarked";
                } else {
                    bookmarkBtn.textContent = "🤍 Bookmark";
                }
            });
        });
    }
});
