document.addEventListener("DOMContentLoaded", () => {
    const replyButtons = document.querySelectorAll(".reply-btn");
    const parentInput = document.getElementById("parent_id");

    replyButtons.forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            parentInput.value = btn.dataset.id;
            document.querySelector(".comment-form textarea").focus();
        });
    });
});

