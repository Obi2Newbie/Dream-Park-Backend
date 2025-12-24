# Dream-Park-Backend

Ce projet constitue le moteur de gestion (Backend) du système DreamPark, incluant la gestion des entrées, des sorties, des abonnements et des services de maintenance/livraison.

## 📦 Installation

1. **Créer et activer un environnement virtuel (recommandé) :**
```bash
   python -m venv .venv
```
2. **Activer l'environnement virtuel :**
- Windows (PowerShell) :
```bash
.venv\Scripts\Activate.ps1
```
- Windows (CMD) :
```bash
.venv\Scripts\activate.bat
```
- Linux/macOS :
```bash
source .venv/bin/activate
```

3. **Installer les dépendances :**
```bash
pip install "fastapi[standard]" pydantic uvicorn
```

## 🚀 Lancement de FastAPI
Pour démarrer le serveur de développement avec rechargement automatique :
```bash
uvicorn main:app --reload
```
## 🧪 Tests Unitaires
Le projet utilise ```unittest``` pour garantir la fiabilité de la logique métier. Pour lancer l'ensemble des tests :
```bash
python -m unittest discover -s tests
```
## 🛠️ Logique métier & Algorithmes
**Partie 1 : Gestion des Entrées**
La logique principale de la première phase du projet (identification des véhicules, vérification des abonnements et attribution des places) est implémentée dans : ```controllers/partie1.py```

Vous pouvez tester cette logique spécifiquement en exécutant ce script ou via les tests unitaires associés dans le dossier ```/tests```.
