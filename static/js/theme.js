// ===== SYSTÈME DE GESTION DES THÈMES =====

class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        // Appliquer le thème au chargement
        this.applyTheme(this.currentTheme);
        
        // Écouter les changements de préférences système
        this.listenForSystemThemeChange();
        
        // Ajouter les classes d'animation
        this.addAnimationClasses();
        
        // Gérer la navigation active
        this.setActiveNavigation();
    }

    getStoredTheme() {
        return localStorage.getItem('danone-theme');
    }

    setStoredTheme(theme) {
        localStorage.setItem('danone-theme', theme);
    }

    setTheme(theme) {
        this.applyTheme(theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        this.setStoredTheme(theme);
        
        // Mettre à jour l'icône du switch
        this.updateThemeSwitchIcon(theme);
        
        // Déclencher un événement personnalisé
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        
        // Animation de transition
        this.addTransitionEffect();
    }

    updateThemeSwitchIcon(theme) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    addTransitionEffect() {
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    listenForSystemThemeChange() {
        // Écouter les changements de préférences système
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (!this.getStoredTheme()) {
                    this.applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }

    addAnimationClasses() {
        // Ajouter des classes d'animation aux éléments
        document.addEventListener('DOMContentLoaded', () => {
            // Animation des cartes
            const cards = document.querySelectorAll('.card');
            cards.forEach((card, index) => {
                card.style.animationDelay = `${index * 0.1}s`;
                card.classList.add('fade-in');
            });

            // Animation des boutons
            const buttons = document.querySelectorAll('.btn');
            buttons.forEach(button => {
                button.classList.add('pulse');
            });
        });
    }

    // Gestion de la navigation active
    setActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            // Vérifier si le lien correspond à la page actuelle
            const linkPath = link.getAttribute('href');
            if (linkPath === currentPath || 
                (currentPath === '/' && linkPath === '/') ||
                (currentPath !== '/' && linkPath !== '/' && currentPath.includes(linkPath))) {
                link.classList.add('active');
            }
        });
    }
}

// ===== GESTIONNAIRE RESPONSIVE =====

class ResponsiveManager {
    constructor() {
        this.init();
    }

    init() {
        this.handleResize();
        this.addMobileOptimizations();
        this.setupTouchGestures();
    }

    handleResize() {
        window.addEventListener('resize', () => {
            this.updateLayout();
        });
    }

    updateLayout() {
        const width = window.innerWidth;
        
        if (width < 768) {
            document.body.classList.add('mobile-view');
            this.optimizeForMobile();
        } else {
            document.body.classList.remove('mobile-view');
            this.optimizeForDesktop();
        }
    }

    optimizeForMobile() {
        // Optimisations pour mobile
        const tables = document.querySelectorAll('.table');
        tables.forEach(table => {
            if (!table.classList.contains('table-responsive')) {
                table.classList.add('table-responsive');
            }
        });

        // Réduire la taille des cartes
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.add('mobile-card');
        });
    }

    optimizeForDesktop() {
        // Optimisations pour desktop
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.classList.remove('mobile-card');
        });
    }

    addMobileOptimizations() {
        // Ajouter des optimisations spécifiques au mobile
        if ('ontouchstart' in window) {
            document.body.classList.add('touch-device');
        }
    }

    setupTouchGestures() {
        // Gestes tactiles pour mobile
        let startX = 0;
        let startY = 0;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;

            // Swipe gauche/droite pour naviguer
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe gauche
                    this.handleSwipeLeft();
                } else {
                    // Swipe droite
                    this.handleSwipeRight();
                }
            }
        });
    }

    handleSwipeLeft() {
        // Navigation vers la page suivante
        console.log('Swipe gauche détecté');
    }

    handleSwipeRight() {
        // Navigation vers la page précédente
        console.log('Swipe droite détecté');
    }
}

// ===== INITIALISATION =====

document.addEventListener('DOMContentLoaded', () => {
    // Initialiser les gestionnaires définis dans ce fichier
    window.themeManager = new ThemeManager();
    window.responsiveManager = new ResponsiveManager();
    
    // AnimationManager et NotificationManager sont initialisés par enhanced-global.js

    // Ajouter les styles CSS pour les notifications
    const style = document.createElement('style');
    style.textContent = `
        .notification-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        }

        .toast-notification {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: var(--shadow-lg);
            margin-bottom: 10px;
            overflow: hidden;
        }

        .toast-header {
            background: var(--bg-secondary);
            padding: 10px 15px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .toast-body {
            padding: 15px;
            color: var(--text-primary);
        }

        .mobile-card {
            margin-bottom: 1rem;
        }

        .mobile-view .table {
            font-size: 0.875rem;
        }

        .touch-device .btn {
            min-height: 44px;
        }

        .theme-switch-container {
            display: flex;
            align-items: center;
        }

        .theme-icon {
            font-size: 1.2rem;
            cursor: pointer;
        }
    `;
    document.head.appendChild(style);
});

// ===== EXPORT POUR UTILISATION GLOBALE =====

window.DanoneUI = {
    ThemeManager,
    ResponsiveManager
};

// ===== INITIALISATION AUTOMATIQUE =====

// Initialiser le thème manager au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Éviter les initialisations multiples
    if (window.themeManager) {
        console.log('🎨 Theme Manager déjà initialisé');
        return;
    }
    
    // Créer une instance globale du theme manager
    window.themeManager = new ThemeManager();
    
    // Attendre que la navbar soit créée puis initialiser le switch
    setTimeout(() => {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            // S'assurer qu'il n'y a qu'un seul event listener
            toggle.removeEventListener('change', window.themeManager.toggleTheme);
            toggle.checked = window.themeManager.currentTheme === 'dark';
            toggle.addEventListener('change', () => window.themeManager.toggleTheme());
            
            // Mettre à jour l'icône initiale
            window.themeManager.updateThemeSwitchIcon(window.themeManager.currentTheme);
            
            console.log('🎨 Switch de thème initialisé:', window.themeManager.currentTheme);
        } else {
            console.warn('❌ Switch de thème non trouvé dans le DOM');
        }
    }, 100);
    
    // Supprimer les switches de thème en double (garder seulement le premier)
    setTimeout(() => {
        const switches = document.querySelectorAll('.theme-switch-container');
        if (switches.length > 1) {
            for (let i = 1; i < switches.length; i++) {
                switches[i].remove();
                console.log('🧹 Switch de thème en double supprimé');
            }
        }
    }, 200);
    
    console.log('🎨 Theme Manager initialisé:', window.themeManager.currentTheme);
}); 