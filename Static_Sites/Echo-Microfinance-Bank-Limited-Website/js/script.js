/**
 * Echo Microfinance Bank Limited
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', () => {

    /* =========================================
       1. NAVBAR SCROLL EFFECT
       ========================================= */
    const navbar = document.getElementById('navbar');

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // Initial check
    handleScroll();

    // Listen for scroll
    window.addEventListener('scroll', handleScroll);


    /* =========================================
       2. MOBILE MENU TOGGLE
       ========================================= */
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const currentIcon = menuToggle.querySelector('i');

    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('mobile-active');

        if (navLinks.classList.contains('mobile-active')) {
            currentIcon.classList.remove('fa-bars');
            currentIcon.classList.add('fa-times');
        } else {
            currentIcon.classList.remove('fa-times');
            currentIcon.classList.add('fa-bars');
        }
    });

    // Close menu when a link is clicked
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks.classList.contains('mobile-active')) {
                navLinks.classList.remove('mobile-active');
                currentIcon.classList.remove('fa-times');
                currentIcon.classList.add('fa-bars');
            }
        });
    });


    /* =========================================
       3. SCROLL ANIMATIONS (INTERSECTION OBSERVER)
       ========================================= */
    const revealElements = document.querySelectorAll('.reveal, .fade-in-up');

    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                // Add active class to trigger CSS transitions
                entry.target.classList.add('active');
                // Stop observing once animated
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });

});
