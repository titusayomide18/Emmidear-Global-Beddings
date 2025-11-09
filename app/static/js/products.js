// app/static/js/products.js
(async function () {
  const grid = document.getElementById('productsGrid');
  if (!grid) return;

// If server already rendered product cards, bail out.
if (grid.querySelectorAll('.product-card:not(.skeleton)').length > 0) {
  // already has product cards rendered server-side — skip client fetch
  console.log('products.js: server-rendered products detected — skipping client fetch.');
  return;
}

  function createFromHTML(html) {
    const div = document.createElement('div');
    div.innerHTML = html.trim();
    return div.firstChild;
  }

  function renderProductCard(p) {
    const imgSrc = (p.images && p.images.length) ? p.images[0] : '/static/uploads/Throw Pillows p.jpg';
    const html = `
      <article class="product-card">
        <img src="${imgSrc}" alt="${p.name}">
        <div class="product-info">
          <h3>${p.name}</h3>
          <p class="price">₦${Number(p.price).toLocaleString()}</p>
        </div>
      </article>
    `;
    const node = createFromHTML(html);
    node.addEventListener('click', () => {
      alert('Product: ' + p.name + '\n(Detail page not implemented yet)');
    });
    return node;
  }

  function showLoading() {
    grid.innerHTML = '';
    for (let i = 0; i < 6; i++) {
      const s = document.createElement('div');
      s.className = 'product-card skeleton';
      s.style.minHeight = '180px';
      s.textContent = 'Loading...';
      grid.appendChild(s);
    }
  }

  function showError(msg) {
    grid.innerHTML = `<div class="muted" style="padding:18px;">Error loading products: ${msg}</div>`;
  }

  showLoading();

  try {
    const res = await fetch('/api/products?featured=true');
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    const data = await res.json();

    grid.innerHTML = '';

    if (!data || data.length === 0) {
      grid.innerHTML = '<div class="muted">No featured products found. Seed the DB or unset featured flag.</div>';
      return;
    }

    data.forEach(p => {
      const card = renderProductCard(p);
      grid.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to load products', err);
    showError(err.message || 'Network error');
  }
})();
