document.addEventListener("DOMContentLoaded", () => {
  // ===== Leaflet Map: Show tree lat & lng only =====
  const lat = parseFloat("{{ tree.latitude|default:0 }}");
  const lng = parseFloat("{{ tree.longitude|default:0 }}");

  const map = L.map('map').setView([lat, lng], 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const marker = L.marker([lat, lng]).addTo(map)
    .bindPopup(`<b>{{ tree.street_name }}</b><br>{{ tree.scientific_name|default:"N/A" }}`)
    .openPopup();

  // Glow effect for marker
  marker._icon.style.filter = "drop-shadow(0 0 8px #2e7d32)";

  // ===== Optional: Smooth hover effects for info & image handled via CSS =====
});
