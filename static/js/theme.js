// ===== SYSTÈME DE GESTION DES THÈMES =====

class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        // Appliquer le thème au chargement
        this.applyTheme(this.currentTheme);
        
        // Créer le switch de thème dans la navbar
        this.createThemeSwitch();
        
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

    createThemeSwitch() {
        // Chercher la navbar
        const navbar = document.querySelector('.navbar-nav');
        if (!navbar) return;

        // Créer le conteneur du switch
        const switchContainer = document.createElement('li');
        switchContainer.className = 'nav-item d-flex align-items-center ms-3';
        switchContainer.innerHTML = `
            <div class="theme-switch-container">
                <label class="theme-switch">
                    <input type="checkbox" id="theme-toggle">
                    <span class="slider"></span>
                </label>
                <span class="theme-icon ms-2" id="theme-icon">🌙</span>
            </div>
        `;

        // Ajouter au navbar
        navbar.appendChild(switchContainer);

        // Écouter les changements
        const toggle = document.getElementById('theme-toggle');
        toggle.checked = this.currentTheme === 'dark';
        toggle.addEventListener('change', () => this.toggleTheme());
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

// ===== NOTIFICATIONS PUSH EN TEMPS RÉEL =====

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.isSupported = 'Notification' in window;
        this.init();
    }

    init() {
        if (this.isSupported) {
            this.requestPermission();
            this.setupWebSocket();
        }
    }

    async requestPermission() {
        if (Notification.permission === 'default') {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                this.showNotification('Notifications activées', 'Vous recevrez maintenant les alertes en temps réel.');
            }
        }
    }

    setupWebSocket() {
        // Simulation WebSocket pour l'instant
        // Dans une vraie implémentation, on utiliserait une vraie connexion WebSocket
        this.simulateWebSocket();
    }

    simulateWebSocket() {
        // Simuler des notifications périodiques
        setInterval(() => {
            if (Math.random() > 0.8) { // 20% de chance
                this.showRandomNotification();
            }
        }, 30000); // Toutes les 30 secondes
    }

    showRandomNotification() {
        const notifications = [
            { title: 'Nouvel équipement détecté', message: 'Un nouvel équipement a été trouvé sur le réseau.' },
            { title: 'Alerte de performance', message: 'Temps de réponse élevé détecté sur le serveur principal.' },
            { title: 'Scan réseau terminé', message: 'Le scan automatique du réseau est terminé.' },
            { title: 'Mise à jour IA', message: 'Les modèles d\'IA ont été mis à jour avec de nouvelles données.' }
        ];

        const notification = notifications[Math.floor(Math.random() * notifications.length)];
        this.showNotification(notification.title, notification.message);
    }

    showNotification(title, message, options = {}) {
        if (!this.isSupported || Notification.permission !== 'granted') {
            this.showToastNotification(title, message);
            return;
        }

        const notification = new Notification(title, {
            body: message,
            icon: '/static/img/danone-logo.png',
            badge: '/static/img/danone-logo.png',
            tag: 'danone-dashboard',
            requireInteraction: false,
            ...options
        });

        notification.onclick = () => {
            window.focus();
            notification.close();
        };

        // Ajouter aussi une notification toast
        this.showToastNotification(title, message);
    }

    showToastNotification(title, message) {
        const toast = document.createElement('div');
        toast.className = 'toast-notification fade-in';
        toast.innerHTML = `
            <div class="toast-header">
                <strong>${title}</strong>
                <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        // Ajouter au conteneur de notifications
        let container = document.getElementById('notification-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'notification-container';
            document.body.appendChild(container);
        }

        container.appendChild(toast);

        // Supprimer automatiquement après 5 secondes
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 5000);
    }
}

// ===== GESTIONNAIRE D'ANIMATIONS =====

class AnimationManager {
    constructor() {
        this.init();
    }

    init() {
        this.addScrollAnimations();
        this.addHoverEffects();
        this.addLoadingAnimations();
    }

    addScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        // Observer tous les éléments avec la classe 'animate-on-scroll'
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    addHoverEffects() {
        // Effets de survol pour les cartes
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px) scale(1.02)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Effets de survol pour les boutons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });
    }

    addLoadingAnimations() {
        // Animation de chargement pour les données
        document.querySelectorAll('[data-loading]').forEach(element => {
            element.addEventListener('click', () => {
                this.showLoading(element);
            });
        });
    }

    showLoading(element) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Chargement...';
        element.disabled = true;

        // Simuler un chargement
        setTimeout(() => {
            element.innerHTML = originalContent;
            element.disabled = false;
        }, 2000);
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
    // Initialiser tous les gestionnaires
    window.themeManager = new ThemeManager();
    window.notificationManager = new NotificationManager();
    window.animationManager = new AnimationManager();
    window.responsiveManager = new ResponsiveManager();

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
    NotificationManager,
    AnimationManager,
    ResponsiveManager
}; 