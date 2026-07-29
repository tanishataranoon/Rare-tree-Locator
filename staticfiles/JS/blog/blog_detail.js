document.addEventListener("DOMContentLoaded", function () {
    // ==========================================
    // 1. Reply Button & Smooth Scroll Fix
    // ==========================================
    const replyButtons = document.querySelectorAll(".reply-btn");
    const parentIdInput = document.getElementById("parent_id");
    const commentForm = document.querySelector(".comment-form");
    const commentTextarea = commentForm ? commentForm.querySelector("textarea") : null;

    replyButtons.forEach((button) => {
        button.addEventListener("click", function (e) {
            e.preventDefault(); // Prevents page jumping to top!

            const commentId = this.getAttribute("data-id");
            if (parentIdInput) {
                parentIdInput.value = commentId;
            }

            // Smoothly scroll down to the comment form and focus textarea
            if (commentTextarea) {
                commentTextarea.focus();
                commentTextarea.placeholder = "Replying to comment... Type your response here.";
                commentTextarea.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        });
    });

    // ==========================================
    // 2. Updated Bookmark Toggle Logic
    // ==========================================
    const bookmarkBtn = document.getElementById("bookmark-btn");
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfMeta ? csrfMeta.getAttribute("content") : "";

    if (bookmarkBtn) {
        bookmarkBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const postId = this.dataset.postId;

            fetch(`/post/${postId}/bookmark/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((res) => res.json())
                .then((data) => {
                    const spanTag = bookmarkBtn.querySelector("span");

                    if (data.bookmarked) {
                        bookmarkBtn.classList.add("is-bookmarked");
                        if (spanTag) spanTag.textContent = "Bookmarked";
                        bookmarkBtn.innerHTML = `<i data-feather="bookmark" class="filled"></i> <span>Bookmarked</span>`;
                    } else {
                        bookmarkBtn.classList.remove("is-bookmarked");
                        if (spanTag) spanTag.textContent = "Bookmark";
                        bookmarkBtn.innerHTML = `<i data-feather="bookmark"></i> <span>Bookmark</span>`;
                    }

                    // Refresh Feather Icons inside the button
                    if (typeof feather !== "undefined") {
                        feather.replace();
                    }
                })
                .catch((err) => console.error("Error toggling bookmark:", err));
        });
    }
});