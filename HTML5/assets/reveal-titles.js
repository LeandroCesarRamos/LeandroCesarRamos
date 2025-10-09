// Reveal animation for section titles and any element with .reveal
// Add the class 'reveal' or 'reveal-title' to any element you want to animate

document.addEventListener('DOMContentLoaded', function () {
  const revealElements = document.querySelectorAll('.reveal, .reveal-title');

  const observer = new window.IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
      } else {
        entry.target.classList.remove('active');
      }
    });
  }, { threshold: 0.2 });

  revealElements.forEach(el => {
    observer.observe(el);
  });
});
