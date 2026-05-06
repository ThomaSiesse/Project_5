# Project 5 - Migration MongoDB

## Description

Ce projet automatise la migration d'un dataset médical (CSV) vers MongoDB.
Le script `migrate.py` teste l'intégrité des données avant et après la migration.

## Prérequis

Ce projet utilise les versions indiqué dans le fichier requirements.txt
Il faut installer:

- Mongo DB en local ou utilisé Atlas
- Docker et Docker compose

## Configuration

Créer un fichier `.env` à la racine du projet :
MONGODB_URI=votre_connection_string_atlas

## Installation

Cloner le projet :

```bash
git clone https://github.com/ThomaSiesse/Project_5.git
cd Project_5
```

Créer et activer l'environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

### Sans Docker

```bash
python scripts/migrate.py
```

### Avec Docker

```bash
docker build -t migration-script .
docker run --env-file .env -v $(pwd)/data:/app/data migration-script
```

### Avec Docker Compose

```bash
docker-compose up
```

## Test d'intégrité:

Les tests suivants sont effectués avant et après la migration :

- **Age** : valeur entre O et 150
- **Gender** : valeur est Male ou Female
- **Blood** : valeur dans la liste ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
- **Dates** : Date of Admission < Discharge Date
- **Billing Amount** : valeur non nul
- **Room Number** : valeur > 0

## Note

Placer le fichier `healthcare_dataset.csv` dans le dossier `data/` avant de lancer le build Docker.

## Historique du développement

1. Mise en place de la structure du projet
2. Script de migration et tests d'intégrité
3. Dockerfile
4. Docker-compose avec volumes
5. Réseau nommé et finalisation

## Authentification

### Fonctionnement

auth.py permet de s'identifier et de définir les droit de base CRUD que l'on peut faire

1. Demande l'username
2. Si il existe alors demande le mot de passe
3. Si il n'existe pas demande de créer un mot de passe et de définir un rôle.
4. Valide l'authentification

### Rôles et permissions

admin: Create / Read / update
doctor: Create / Read / update
medical_staff: Read
developer: Create / Read / update / Delete

### Sécurité

Les mots de passe sont hachés avec **bcrypt** avant d'être stockés dans MongoDB — ils ne sont jamais stockés en clair.
