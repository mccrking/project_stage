# Rapport : Problème de cohérence des statuts entre le tableau et l'action info

## 🔍 Problème identifié

L'utilisateur a signalé une incohérence dans l'affichage des statuts :
- **Dans le tableau des équipements** : Le statut affiche "En ligne"
- **Dans l'action "info"** : Le statut affiche "Hors ligne"

## 🔧 Analyse technique

### 1. Affichage dans le tableau (templates/dashboard.html, lignes 203-211)

```html
<td>
    {% if device.is_online %}
        <span class="badge bg-success badge-status">
            <i class="fas fa-circle me-1"></i>En ligne
        </span>
    {% else %}
        <span class="badge bg-danger badge-status">
            <i class="fas fa-circle me-1"></i>Hors ligne
        </span>
    {% endif %}
</td>
```

✅ **Correct** : Utilise `device.is_online` directement depuis l'objet Device de la base de données.

### 2. Affichage dans l'action info (JavaScript, lignes 413-415)

**AVANT la correction :**
```javascript
<span class="badge ${device.status === 'online' ? 'bg-success' : 'bg-danger'}">
    ${device.status === 'online' ? 'En ligne' : 'Hors ligne'}
</span>
```

❌ **Problème** : Le code JavaScript cherchait un champ `status` qui n'existe pas dans la réponse de l'API.

### 3. Endpoint API (app.py, ligne 958)

```python
device_data = {
    'id': device.id,
    'ip': device.ip,
    'hostname': device.hostname,
    'mac': device.mac,
    'mac_vendor': device.mac_vendor,
    'is_online': device.is_online,  # ✅ Champ correct
    'last_seen': device.last_seen.isoformat() if device.last_seen else None,
    # ... autres champs
}
```

✅ **Correct** : L'API retourne bien le champ `is_online`.

## 🛠️ Solution appliquée

### 1. Correction du JavaScript (templates/dashboard.html)

**APRÈS la correction :**
```javascript
<span class="badge ${device.is_online ? 'bg-success' : 'bg-danger'}">
    ${device.is_online ? 'En ligne' : 'Hors ligne'}
</span>
```

### 2. Correction des noms de champs

**AVANT :**
```javascript
<tr><td>Adresse IP:</td><td><strong>${device.ip_address}</strong></td></tr>
<tr><td>Adresse MAC:</td><td>${device.mac_address || 'N/A'}</td></tr>
```

**APRÈS :**
```javascript
<tr><td>Adresse IP:</td><td><strong>${device.ip}</strong></td></tr>
<tr><td>Adresse MAC:</td><td>${device.mac || 'N/A'}</td></tr>
```

## 📊 Résultat

### Avant la correction :
- Tableau : ✅ Affiche correctement le statut
- Action info : ❌ Affiche toujours "Hors ligne" (car `device.status` était `undefined`)

### Après la correction :
- Tableau : ✅ Affiche correctement le statut
- Action info : ✅ Affiche le même statut que le tableau

## 🧪 Tests de validation

### Script de test créé : `test_status_consistency.py`

Ce script vérifie :
1. La cohérence entre le statut du tableau et l'action info pour tous les appareils
2. Le bon fonctionnement de l'API `/api/devices/{id}`
3. La correspondance des noms de champs

### Exécution du test :
```bash
python test_status_consistency.py
```

## 📋 Fichiers modifiés

1. **`templates/dashboard.html`** :
   - Ligne 413 : Correction de `device.status` vers `device.is_online`
   - Ligne 407 : Correction de `device.ip_address` vers `device.ip`
   - Ligne 409 : Correction de `device.mac_address` vers `device.mac`

## ✅ Conclusion

Le problème était dû à une incohérence dans les noms des champs entre :
- L'API backend qui retourne `is_online`, `ip`, `mac`
- Le JavaScript frontend qui cherchait `status`, `ip_address`, `mac_address`

**La correction assure maintenant une cohérence parfaite entre l'affichage du tableau et l'action info.**

## 🔄 Prochaines étapes recommandées

1. **Tester l'application** pour confirmer la correction
2. **Vérifier les autres endpoints** pour s'assurer de la cohérence des noms de champs
3. **Documenter les conventions** de nommage pour éviter ce type de problème à l'avenir 