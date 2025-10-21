document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".card");

  // Hover glow
  cards.forEach(card => {
    card.addEventListener("mouseenter", () => card.style.boxShadow = "0 15px 40px rgba(0,0,0,0.2)");
    card.addEventListener("mouseleave", () => card.style.boxShadow = "0 6px 20px rgba(0,0,0,0.08)");
  });

  // Search/filter
  const searchInput = document.getElementById("treeSearch");
  const searchBtn = document.getElementById("searchBtn");
  function filterTrees() {
    const q = searchInput.value.toLowerCase();
    cards.forEach(card => {
      const name = card.querySelector("h3")?.textContent.toLowerCase() || "";
      const sci = card.querySelector("p")?.textContent.toLowerCase() || "";
      const loc = card.querySelector(".meta span")?.textContent.toLowerCase() || "";
      card.style.display = (name.includes(q) || sci.includes(q) || loc.includes(q)) ? "" : "none";
    });
  }
  searchBtn.addEventListener("click", filterTrees);
  searchInput.addEventListener("keyup", e => { if(e.key==="Enter") filterTrees(); });

  // -----------------------
  // Contributor actions
  // -----------------------
  // Delete tree
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const treeId = btn.dataset.id;
      if(!confirm("Are you sure you want to delete this tree?")) return;

      fetch(`/trees/${treeId}/delete/`, {
        method:'POST',
        headers:{'X-CSRFToken': getCookie('csrftoken')}
      })
      .then(r=>r.json())
      .then(data => {
        if(data.success) btn.closest('.card').remove();
        else alert(data.error);
      });
    });
  });

  // Open modal
  const modal = document.getElementById("editTreeModal");
  const form = document.getElementById("editTreeForm");
  document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const card = btn.closest(".card");
      document.getElementById("editTreeId").value = btn.dataset.id;
      document.getElementById("editStreetName").value = card.querySelector("h3").innerText;
      document.getElementById("editScientificName").value = card.querySelector("p").innerText;
      document.getElementById("editLatitude").value = card.dataset.latitude;
      document.getElementById("editLongitude").value = card.dataset.longitude;
      modal.classList.remove("hidden");
    });
  });

  // Close modal
  document.getElementById("closeModalBtn").addEventListener("click", ()=>modal.classList.add("hidden"));

  // Submit form
  form.addEventListener("submit", e => {
    e.preventDefault();
    const treeId = document.getElementById("editTreeId").value;
    const formData = new FormData(form);

    fetch(`/trees/${treeId}/update/`, {
      method:'POST',
      headers:{'X-CSRFToken': getCookie('csrftoken')},
      body:formData
    })
    .then(r=>r.json())
    .then(data => {
      if(data.success){
        alert("Tree updated successfully!");
        location.reload(); // reload to see updated card
      } else alert(data.error);
    });
  });

  // CSRF helper
  function getCookie(name){
    let value = null;
    if(document.cookie && document.cookie!==''){
      document.cookie.split(';').forEach(c=>{
        c=c.trim();
        if(c.startsWith(name+'=')) value = decodeURIComponent(c.substring(name.length+1));
      });
    }
    return value;
  }

});
