document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('deleteModal');
    const modalText = document.getElementById('modal-text');
    const deleteForm = document.getElementById('deleteForm');

    // Prevent errors if modal element isn't on the current page
    if (!modal || !deleteForm || !modalText) return;

    const closeBtn = modal.querySelector('.close');
    const cancelBtn = modal.querySelector('.cancel-btn');

    // Function to open modal
    function openDeleteModal(postId, postTitle) {
        if (!postId) {
            console.error("Post ID missing!");
            return;
        }

        modalText.textContent = `Are you sure you want to delete "${postTitle || 'this post'}"?`;
        
        // Dynamically set Django delete action URL
        // Adjust '/blog/delete/' if your URL route is named differently in urls.py
        // deleteForm.action = `/blog/delete/${postId}/`;
        deleteForm.action = `/delete/${postId}/`;
        
        modal.style.display = 'block';
    }

    // Function to close modal
    function closeModal() {
        modal.style.display = 'none';
    }

    // Use Event Delegation so dynamically loaded posts (e.g. Load More) work seamlessly
    document.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.delete-btn');
        if (deleteBtn) {
            e.preventDefault();
            const postId = deleteBtn.getAttribute('data-post-id');
            const postTitle = deleteBtn.getAttribute('data-post-title');
            openDeleteModal(postId, postTitle);
        }
    });

    // Close button events
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

    // Close modal if user clicks outside modal window
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close modal on Escape key press
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'block') {
            closeModal();
        }
    });
});