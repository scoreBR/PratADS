function menuMobile() {
  document.addEventListener("DOMContentLoaded", function () {
    const mobileMenu = document.getElementById("mobile-menu");
    const navMenu = document.getElementById("nav-menu");
    const menuOverlay = document.getElementById("menu-overlay");

    function toggleMenu() {
      mobileMenu.classList.toggle("active");
      navMenu.classList.toggle("active");
      menuOverlay.classList.toggle("active");

      if (navMenu.classList.contains("active")) {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "auto";
      }
    }

    mobileMenu.addEventListener("click", toggleMenu);
    menuOverlay.addEventListener("click", toggleMenu);

    const navLinks = document.querySelectorAll("#nav-menu a");
    navLinks.forEach((link) => {
      link.addEventListener("click", toggleMenu);
    });
  });
}
