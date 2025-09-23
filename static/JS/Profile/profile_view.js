// Handle tab switching
function showTab(tabId) {
    // Hide all tabs
    document.querySelectorAll(".tab-content").forEach(div => {
        div.classList.remove("active");
    });

    // Deactivate all buttons
    document.querySelectorAll(".tabs button").forEach(btn => {
        btn.classList.remove("active");
    });

    // Show selected tab
    document.getElementById(tabId).classList.add("active");

    // Activate selected button
    event.target.classList.add("active");
}

// Show "trees" tab by default when page loads
document.addEventListener("DOMContentLoaded", () => {
    showTab("trees");
});
