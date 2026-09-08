const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.primary-nav');
const navLinks = [...document.querySelectorAll('.primary-nav a')];
const footerNavLinks = [...document.querySelectorAll('.footer-nav a')];
const sectionNavLinks = [...navLinks, ...footerNavLinks];

if (menuToggle && nav) {
  menuToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  navLinks.forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open menu');
  }));
}

const sectionMap = navLinks
  .map(link => ({ link, id: link.getAttribute('href') }))
  .filter(item => item.id && item.id.startsWith('#'))
  .map(item => ({ ...item, section: document.querySelector(item.id) }))
  .filter(item => item.section);

const setActiveSection = (id) => {
  sectionNavLinks.forEach(link => {
    const isActive = link.getAttribute('href') === id;
    link.classList.toggle('active', isActive);
    if (isActive) {
      link.setAttribute('aria-current', 'location');
    } else {
      link.removeAttribute('aria-current');
    }
  });
};

const getHeaderOffset = () => {
  const header = document.querySelector('.site-header');
  return header ? header.getBoundingClientRect().height : 0;
};

const setActive = () => {
  if (!sectionMap.length) return;

  const viewportBottom = window.scrollY + window.innerHeight;
  const documentBottom = document.documentElement.scrollHeight;

  // The Contact section sits immediately above the footer, so the browser cannot
  // always scroll it high enough to satisfy a normal top-based scroll-spy test.
  // Treat the bottom of the page as Contact explicitly.
  if (documentBottom - viewportBottom <= 8) {
    setActiveSection('#contact');
    return;
  }

  const referenceY = window.scrollY + getHeaderOffset() + 24;
  let current = sectionMap[0];

  for (const item of sectionMap) {
    if (item.section.offsetTop <= referenceY) current = item;
  }

  if (current) setActiveSection(current.id);
};

// Set the selected state immediately when navigating from either the header or
// footer. The scroll-spy then keeps both navigation areas synchronized.
sectionNavLinks.forEach(link => {
  const href = link.getAttribute('href');
  if (!href || !href.startsWith('#')) return;

  link.addEventListener('click', (event) => {
    // #home points to the sticky header itself. Because a sticky element remains
    // visible while scrolling, browsers may decide there is nothing to scroll to.
    // Handle Home explicitly so it always returns to the top of the document.
    if (href === '#home') {
      event.preventDefault();

      // Home represents the document itself, not a hash target. Remove any
      // existing section hash (for example #contact or #about) so the address
      // bar returns to /index.html while we scroll to the top.
      const cleanUrl = `${window.location.pathname}${window.location.search}`;
      if (window.location.hash) {
        window.history.pushState(null, '', cleanUrl);
      }

      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
      setActiveSection('#home');
      return;
    }

    setActiveSection(href);
    // Re-evaluate once anchor scrolling has settled enough for the final section.
    window.setTimeout(setActive, 450);
  });
});

window.addEventListener('scroll', setActive, { passive: true });
window.addEventListener('resize', setActive);
setActive();

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

/*
 * PHONE CONFIGURATION
 * -------------------
 * The current number is a TEST number used during local validation.
 * Replace both arrays with the final BGP Data Works phone number before launch.
 * The number remains absent from index.html and is revealed only after user action.
 */
const PHONE_DISPLAY_PARTS = ['+40', '745', '123', '456'];
const PHONE_TEL_PARTS = ['+40', '745123456'];

const phoneRevealButtons = [...document.querySelectorAll('[data-phone-reveal]')];

phoneRevealButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const container = button.parentElement;
    const numberLink = container ? container.querySelector('[data-phone-number]') : null;

    if (!numberLink) return;

    if (!PHONE_DISPLAY_PARTS.length || !PHONE_TEL_PARTS.length) {
      button.textContent = 'Phone number not configured';
      button.disabled = true;
      return;
    }

    numberLink.textContent = PHONE_DISPLAY_PARTS.join(' ');
    numberLink.href = `tel:${PHONE_TEL_PARTS.join('')}`;
    numberLink.hidden = false;
    button.hidden = true;
    button.setAttribute('aria-expanded', 'true');
  });
});

// Back to top: shown only once the visitor has moved away from the top of the page.
const backToTop = document.querySelector('[data-back-to-top]');

if (backToTop) {
  const updateBackToTop = () => {
    backToTop.classList.toggle('is-visible', window.scrollY > 320);
  };

  backToTop.addEventListener('click', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });

  window.addEventListener('scroll', updateBackToTop, { passive: true });
  updateBackToTop();
}

