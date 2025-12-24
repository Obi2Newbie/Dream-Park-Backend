# Dream-Park-Backend

Ce projet constitue le moteur de gestion (Backend) du système DreamPark, incluant la gestion des entrées, des sorties, des abonnements et des services de maintenance/livraison.

## 🧪 Tests Unitaires
Le projet utilise ```unittest``` pour garantir la fiabilité de la logique métier. Pour lancer l'ensemble des tests :
```bash
python -m unittest discover -s tests
```
## 🛠️ Logique métier & Algorithmes
### Partie 1 : Gestion des Entrées
La logique principale de la première phase du projet (identification des véhicules, vérification des abonnements et attribution des places) est implémentée dans : ```controllers/partie1.py```

Vous pouvez tester cette logique spécifiquement en exécutant ce script ou via les tests unitaires associés dans le dossier ```/tests```.
### Partie 2 : Sortie et Services Flexibles
Implémentée dans `controllers/partie2.py`.
- **Récupération** : Activation du téléporteur et libération immédiate de la place pour le composant `Parking`.
- **Flexibilité** : Possibilité pour le client de modifier ses services (Livraison/Maintenance) par interaction système.
- **Livraison** : Coordination entre le `Client` et le `Voiturier` pour les remises de clés hors site.