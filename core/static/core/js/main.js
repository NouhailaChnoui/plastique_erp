document.addEventListener("DOMContentLoaded", function () {
  // --- Toggle sidebar (mobile) ---
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("sidebarToggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => sidebar.classList.toggle("show"));
  }

  // --- Dark mode ---
  const root = document.documentElement;
  const darkBtn = document.getElementById("darkModeToggle");
  const stored = document.cookie.match(/theme=(dark|light)/);
  if (stored) {
    root.setAttribute("data-bs-theme", stored[1]);
  }
  updateDarkIcon();

  if (darkBtn) {
    darkBtn.addEventListener("click", () => {
      const current = root.getAttribute("data-bs-theme");
      const next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-bs-theme", next);
      document.cookie = `theme=${next};path=/;max-age=31536000`;
      updateDarkIcon();
    });
  }

  function updateDarkIcon() {
    if (!darkBtn) return;
    const icon = darkBtn.querySelector("i");
    const isDark = root.getAttribute("data-bs-theme") === "dark";
    icon.className = isDark ? "fa-solid fa-sun" : "fa-solid fa-moon";
  }

  // --- Calcul automatique montant (achats/ventes) ---
  const qte = document.getElementById("id_quantite");
  const prix = document.getElementById("id_prix_unitaire");
  const montant = document.getElementById("montant-calcule");
  function recalc() {
    if (!qte || !prix || !montant) return;
    const q = parseFloat(qte.value) || 0;
    const p = parseFloat(prix.value) || 0;
    montant.textContent = (q * p).toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " DH";
  }
  if (qte && prix) {
    qte.addEventListener("input", recalc);
    prix.addEventListener("input", recalc);
    recalc();
  }
});
