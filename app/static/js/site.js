// app/static/js/site.js
// Header, mobile nav, dropdowns and other small behavior

// set current year in footer
document.getElementById('year') && (document.getElementById('year').textContent = String(new Date().getFullYear()));

// MOBILE MENU: open / close
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobileNav');
const mobileClose = document.getElementById('mobileClose');

function openMobileNav() {
  mobileNav.classList.add('open');
  hamburger.setAttribute('aria-expanded', 'true');
  mobileNav.setAttribute('aria-hidden', 'false');
}
function closeMobileNav() {
  mobileNav.classList.remove('open');
  hamburger.setAttribute('aria-expanded', 'false');
  mobileNav.setAttribute('aria-hidden', 'true');
}

if (hamburger) hamburger.addEventListener('click', () => {
  if (mobileNav.classList.contains('open')) closeMobileNav();
  else openMobileNav();
});
if (mobileClose) mobileClose.addEventListener('click', closeMobileNav);

// MOBILE ACCORDION (Categories)
document.querySelectorAll('.accordion-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    btn.classList.toggle('open');
    const panel = btn.nextElementSibling;
    if (!expanded) {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } else {
      panel.style.maxHeight = null;
    }
  });
});

// DESKTOP DROPDOWN: keyboard + click
document.querySelectorAll('.nav-item.dropdown').forEach(drop => {
  const btn = drop.querySelector('.drop-btn');

  if (!btn) return;

  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    drop.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (!drop.contains(e.target)) {
      btn.setAttribute('aria-expanded', 'false');
      drop.classList.remove('open');
    }
  });

  btn.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      btn.setAttribute('aria-expanded', 'false');
      drop.classList.remove('open');
      btn.focus();
    }
  });
});
