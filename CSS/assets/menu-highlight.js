// Menu highlight fix: highlights the nav link for the section mais próxima do topo
// Considera 'Contact' ativa ao chegar no final da página

document.addEventListener('DOMContentLoaded', function () {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.sidebar ul li a');

  const sectionIdToNav = {};
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      sectionIdToNav[href.substring(1)] = link;
    }
  });

  function clearActive() {
    navLinks.forEach(link => link.classList.remove('active'));
  }

  function onScroll() {
    let closestSection = null;
    let minDistance = Infinity;
    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      if (rect.top >= -100 && rect.top < minDistance) {
        minDistance = rect.top;
        closestSection = section;
      }
    });
    // Se chegou ao final da página, ativa Contact
    const scrollBottom = window.innerHeight + window.scrollY;
    const docHeight = document.body.offsetHeight;
    if (docHeight - scrollBottom < 10) {
      closestSection = sections[sections.length - 1];
    }
    if (closestSection) {
      clearActive();
      const id = closestSection.getAttribute('id');
      if (sectionIdToNav[id]) {
        sectionIdToNav[id].classList.add('active');
      }
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // Run on load
});
