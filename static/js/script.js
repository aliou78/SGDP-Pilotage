const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        menuToggle.setAttribute('aria-expanded', String(isOpen));
    });
}

document.querySelectorAll('.nav-links a').forEach((link) => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        menuToggle?.setAttribute('aria-expanded', 'false');
    });
});

const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.14 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const counter = entry.target;
        const target = Number(counter.dataset.value) || 0;
        const duration = 1200;
        const start = performance.now();

        const updateCounter = (now) => {
            const progress = Math.min((now - start) / duration, 1);
            counter.textContent = Math.floor(progress * target).toLocaleString('fr-FR');
            if (progress < 1) requestAnimationFrame(updateCounter);
        };

        requestAnimationFrame(updateCounter);
        observer.unobserve(counter);
    });
}, { threshold: 0.5 });

document.querySelectorAll('.counter').forEach((counter) => counterObserver.observe(counter));

const heroSlides = [...document.querySelectorAll('.hero-slide')];
const heroDots = [...document.querySelectorAll('.hero-dot')];
const heroPrevious = document.querySelector('.hero-prev');
const heroNext = document.querySelector('.hero-next');
const hero = document.querySelector('.hero');
let currentHeroSlide = 0;
let heroTimer;

const showHeroSlide = (index) => {
    currentHeroSlide = (index + heroSlides.length) % heroSlides.length;
    heroSlides.forEach((slide, slideIndex) => {
        slide.classList.toggle('is-active', slideIndex === currentHeroSlide);
    });
    heroDots.forEach((dot, dotIndex) => {
        const active = dotIndex === currentHeroSlide;
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-current', active ? 'true' : 'false');
    });
};

const restartHeroTimer = () => {
    window.clearInterval(heroTimer);
    heroTimer = window.setInterval(() => showHeroSlide(currentHeroSlide + 1), 5000);
};

heroNext?.addEventListener('click', () => {
    showHeroSlide(currentHeroSlide + 1);
    restartHeroTimer();
});

heroPrevious?.addEventListener('click', () => {
    showHeroSlide(currentHeroSlide - 1);
    restartHeroTimer();
});

heroDots.forEach((dot, index) => dot.addEventListener('click', () => {
    showHeroSlide(index);
    restartHeroTimer();
}));

hero?.addEventListener('mouseenter', () => window.clearInterval(heroTimer));
hero?.addEventListener('mouseleave', restartHeroTimer);

if (heroSlides.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    restartHeroTimer();
}