/**
 * Rhodesian Ridgeback Breeder Finder - Main JavaScript
 */

// Mobile menu toggle (if needed)
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Auto-submit filters on change (optional)
    const autoSubmitFilters = document.querySelectorAll('.auto-submit');
    autoSubmitFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            this.closest('form').submit();
        });
    });

    // Image lazy loading fallback for older browsers
    if ('loading' in HTMLImageElement.prototype) {
        // Native lazy loading supported
    } else {
        // Fallback for older browsers
        const images = document.querySelectorAll('img[loading="lazy"]');
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
        document.body.appendChild(script);
        images.forEach(img => {
            img.classList.add('lazyload');
            img.setAttribute('data-src', img.src);
        });
    }
});

// API helper functions
const API = {
    async getBreeders(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`/api/breeders?${queryString}`);
        return response.json();
    },

    async getBreeder(breederId) {
        const response = await fetch(`/api/breeder/${breederId}`);
        return response.json();
    },

    async getBreederImages(breederId) {
        const response = await fetch(`/api/breeder/${breederId}/images`);
        return response.json();
    },

    async getRecentImages(limit = 20) {
        const response = await fetch(`/api/gallery/recent?limit=${limit}`);
        return response.json();
    },

    async getStats() {
        const response = await fetch('/api/stats');
        return response.json();
    }
};

// Export for use in other scripts
window.RidgebackFinder = { API };
