/**
 * Enhanced Global Interactions & Utilities
 * Central Danone - Dashboard Enhancement
 * (ThemeManager est dans theme.js pour éviter les conflits)
 */

// Variables globales pour les fonctions nécessaires
let lastUpdateTime = new Date();

// Fonction updateLastUpdate globale pour les templates
function updateLastUpdate() {
    const now = new Date();
    lastUpdateTime = now;
    const timeStr = now.toLocaleTimeString('fr-FR');
    
    // Mettre à jour tous les éléments avec l'ID approprié
    const elements = [
        'nav-last-update',
        'dashboard-last-update', 
        'alerts-last-update',
        'last-update'
    ];
    
    elements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = timeStr;
        }
    });
}

class AnimationManager {
    constructor() {
        this.init();
    }

    init() {
        this.observeElements();
        this.bindScrollAnimations();
    }

    observeElements() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, {
            threshold: 0.1
        });

        // Observer les cartes et éléments à animer
        document.querySelectorAll('.card, .stat-card-enhanced').forEach(el => {
            observer.observe(el);
        });
    }

    bindScrollAnimations() {
        let ticking = false;

        function updateAnimations() {
            const scrolled = window.pageYOffset;
            const parallax = document.querySelectorAll('.parallax-element');
            
            parallax.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
            
            ticking = false;
        }

        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateAnimations);
                ticking = true;
            }
        }

        window.addEventListener('scroll', requestTick);
    }
}

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.init();
    }

    init() {
        this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(container);
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        const id = Date.now();
        
        notification.className = `alert alert-${type}-enhanced alert-dismissible fade show mb-2`;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas ${this.getIcon(type)} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" onclick="notificationManager.hide(${id})"></button>
            </div>
        `;
        notification.id = `notification-${id}`;
        
        document.getElementById('notification-container').appendChild(notification);
        
        // Animation d'entrée
        setTimeout(() => {
            notification.classList.add('slide-in-right');
        }, 100);
        
        // Auto-suppression
        if (duration > 0) {
            setTimeout(() => {
                this.hide(id);
            }, duration);
        }
        
        this.notifications.push(id);
        return id;
    }

    hide(id) {
        const notification = document.getElementById(`notification-${id}`);
        if (notification) {
            notification.style.animation = 'slideInRight 0.3s ease-in-out reverse';
            setTimeout(() => {
                notification.remove();
                this.notifications = this.notifications.filter(n => n !== id);
            }, 300);
        }
    }

    getIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            warning: 'fa-exclamation-triangle',
            danger: 'fa-times-circle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    // Méthodes de convenance
    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    error(message, duration) {
        return this.show(message, 'danger', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

class SearchManager {
    constructor() {
        this.searchIndex = [];
        this.init();
    }

    init() {
        this.createGlobalSearch();
        this.bindEvents();
    }

    createGlobalSearch() {
        // Création de la barre de recherche globale
        const searchContainer = document.createElement('div');
        searchContainer.className = 'global-search-container';
        searchContainer.innerHTML = `
            <div class="modal fade" id="globalSearchModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content modal-enhanced">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-search me-2"></i>Recherche globale
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <input type="text" class="form-control form-control-enhanced mb-3" 
                                   id="globalSearchInput" placeholder="Rechercher dans toute l'application...">
                            <div id="searchResults" class="search-results"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(searchContainer);
    }

    bindEvents() {
        // Raccourci clavier Ctrl/Cmd + K pour ouvrir la recherche
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.openSearch();
            }
            
            // Échapper pour fermer
            if (e.key === 'Escape') {
                const modal = bootstrap.Modal.getInstance(document.getElementById('globalSearchModal'));
                if (modal) {
                    modal.hide();
                }
            }
        });

        // Recherche en temps réel
        const searchInput = document.getElementById('globalSearchInput');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.performSearch(e.target.value);
            }, 300));
        }
    }

    openSearch() {
        const modal = new bootstrap.Modal(document.getElementById('globalSearchModal'));
        modal.show();
        setTimeout(() => {
            document.getElementById('globalSearchInput').focus();
        }, 500);
    }

    performSearch(query) {
        if (query.length < 2) {
            document.getElementById('searchResults').innerHTML = '';
            return;
        }

        // Simulation de recherche (à remplacer par une vraie recherche)
        const results = [
            { title: 'Dashboard Principal', url: '/', type: 'page' },
            { title: 'Alertes Réseau', url: '/alerts', type: 'page' },
            { title: 'Rapports', url: '/reports', type: 'page' },
            { title: 'Paramètres', url: '/settings', type: 'page' },
            { title: 'IA Dashboard', url: '/ai-dashboard', type: 'page' }
        ].filter(item => 
            item.title.toLowerCase().includes(query.toLowerCase())
        );

        this.displayResults(results);
    }

    displayResults(results) {
        const container = document.getElementById('searchResults');
        
        if (results.length === 0) {
            container.innerHTML = '<p class="text-muted">Aucun résultat trouvé</p>';
            return;
        }

        const html = results.map(result => `
            <div class="search-result-item p-2 mb-2 border rounded" onclick="window.location.href='${result.url}'">
                <div class="d-flex align-items-center">
                    <i class="fas ${this.getTypeIcon(result.type)} me-2 text-primary"></i>
                    <div>
                        <div class="fw-bold">${result.title}</div>
                        <small class="text-muted">${result.url}</small>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = html;
    }

    getTypeIcon(type) {
        const icons = {
            page: 'fa-file',
            device: 'fa-server',
            alert: 'fa-exclamation-triangle',
            report: 'fa-chart-bar'
        };
        return icons[type] || icons.page;
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

class PerformanceManager {
    constructor() {
        this.init();
    }

    init() {
        this.optimizeImages();
        this.implementLazyLoading();
    }

    optimizeImages() {
        // Observer pour le lazy loading des images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    implementLazyLoading() {
        // Lazy loading pour les composants lourds
        const componentObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const component = entry.target;
                    if (component.dataset.lazyComponent) {
                        this.loadComponent(component.dataset.lazyComponent, component);
                    }
                }
            });
        });

        document.querySelectorAll('[data-lazy-component]').forEach(el => {
            componentObserver.observe(el);
        });
    }

    loadComponent(componentName, container) {
        // Simulation du chargement de composant
        container.innerHTML = '<div class="loading-skeleton" style="height: 200px;"></div>';
        
        setTimeout(() => {
            container.innerHTML = `<p>Composant ${componentName} chargé !</p>`;
        }, 1000);
    }
}

// Initialisation globale
document.addEventListener('DOMContentLoaded', () => {
    // Initialiser les managers (ThemeManager sera initialisé par theme.js)
    window.animationManager = new AnimationManager();
    window.notificationManager = new NotificationManager();
    window.searchManager = new SearchManager();
    window.performanceManager = new PerformanceManager();
    
    // Ajouter les classes d'amélioration aux éléments existants
    document.querySelectorAll('.card').forEach(card => {
        if (!card.classList.contains('card-enhanced')) {
            card.classList.add('card-enhanced');
        }
    });
    
    document.querySelectorAll('.btn').forEach(btn => {
        if (!btn.classList.contains('btn-enhanced')) {
            btn.classList.add('btn-enhanced');
        }
    });
    
    document.querySelectorAll('.form-control').forEach(input => {
        if (!input.classList.contains('form-control-enhanced')) {
            input.classList.add('form-control-enhanced');
        }
    });
    
    // Message de bienvenue
    setTimeout(() => {
        if (window.notificationManager) {
            window.notificationManager.success('Interface améliorée chargée ! Utilisez Ctrl+K pour rechercher.', 3000);
        }
    }, 1000);
});

// Gestionnaire d'erreurs global
window.addEventListener('error', (e) => {
    console.error('Erreur globale:', e);
});

// Export pour utilisation dans d'autres scripts (ThemeManager est dans theme.js)
window.DanoneEnhanced = {
    NotificationManager,
    SearchManager, 
    AnimationManager,
    PerformanceManager,
    updateLastUpdate // Export de la fonction globale
};
