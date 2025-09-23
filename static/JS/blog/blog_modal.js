document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('deleteModal');
    const modalText = document.getElementById('modal-text');
    const deleteForm = document.getElementById('deleteForm');
    const closeBtn = modal.querySelector('.close');
    const cancelBtn = modal.querySelector('.cancel-btn');

    // Select all Delete buttons (featured + posts)
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent page reload

            const postId = this.getAttribute('data-post-id');
            const postTitle = this.getAttribute('data-post-title');

            if (!postId) {
                console.error("Post ID missing!");
                return;
            }

            modalText.textContent = `Are you sure you want to delete "${postTitle}"?`;
            deleteForm.action = `/delete/${postId}/`; // Correctly set form action
            modal.style.display = 'block';
        });
    });

    // Close modal
    closeBtn.addEventListener('click', () => modal.style.display = 'none');
    cancelBtn.addEventListener('click', () => modal.style.display = 'none');

    // Close modal if clicked outside content
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});
