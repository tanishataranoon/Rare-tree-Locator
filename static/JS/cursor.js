document.addEventListener("DOMContentLoaded", () => {
  // Cursor glow follow
  const cursorGlow = document.createElement("div");
  cursorGlow.classList.add("cursor-glow");
  document.body.appendChild(cursorGlow);

  document.addEventListener("mousemove", (e) => {
    cursorGlow.style.top = e.clientY + "px";
    cursorGlow.style.left = e.clientX + "px";
  });

  // Enlarge glow briefly when clicking
  document.addEventListener("mousedown", (e) => {
    cursorGlow.classList.add("active");

    const pulse = document.createElement("div");
    pulse.classList.add("cursor-pulse");
    pulse.style.left = e.clientX + "px";
    pulse.style.top = e.clientY + "px";
    document.body.appendChild(pulse);

    setTimeout(() => pulse.remove(), 600);
    setTimeout(() => cursorGlow.classList.remove("active"), 200);
  });
});