// ============================================================
// APP.JS — LE DATTIER
// Logique du site : rendu des produits, filtres, animations
// ============================================================

// ========================
// RENDU DES PRODUITS
// ========================
const grid = document.getElementById('productsGrid');

function renderProducts(cat) {
  const filtered = cat === 'all' ? products : products.filter(p => p.cat === cat);

  grid.innerHTML = filtered.map(p => `
    <div class="product-card reveal visible" data-id="${p.id}">
      <div class="product-image">
        <img src="${p.img}" alt="${p.name}" loading="lazy">
        ${p.badge ? `<span class="product-badge ${p.badge === 'new' ? 'badge-new' : 'badge-best'}">${p.badge === 'new' ? 'Nouveau' : 'Best-seller'}</span>` : ''}
      </div>
      <div class="product-info">
        <p class="product-origin">${p.origin}</p>
        <h3 class="product-name">${p.name}</h3>
        <p class="product-desc">${p.desc}</p>
        <div class="product-footer">
          <span class="product-price">${p.price.toFixed(2).replace('.',',')} € <small>/ ${p.unit}</small></span>
          <button
            class="add-to-cart snipcart-add-item"
            data-item-id="${p.id}"
            data-item-name="${p.name}"
            data-item-price="${p.price}"
            data-item-url="/"
            data-item-description="${p.desc}"
            data-item-image="${p.img}"
            data-item-weight="${p.weight}"
            data-item-categories="${p.cat}"
            title="Ajouter au panier"
            aria-label="Ajouter ${p.name} au panier">
            +
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

renderProducts('all');

// ========================
// FILTRES PAR CATÉGORIE
// ========================
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelector('.filter-btn.active').classList.remove('active');
    btn.classList.add('active');
    renderProducts(btn.dataset.cat);
  });
});

// ========================
// TOAST NOTIFICATION
// ========================
const toast = document.getElementById('toast');

function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2200);
}

document.addEventListener('snipcart.ready', () => {
  Snipcart.events.on('item.added', (item) => {
    showToast(`${item.name} ajouté au panier`);
  });

  // Flèche retour mobile : ferme le panier au clic
  document.getElementById('navBack').addEventListener('click', () => {
    Snipcart.api.theme.cart.close();
  });
});

// ========================
// NAVIGATION SCROLL
// ========================
window.addEventListener('scroll', () => {
  document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// ========================
// ANIMATIONS AU SCROLL
// ========================
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) e.target.classList.add('visible');
  });
}, { threshold: 0.1 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
