# Documentation AWS

## 1. Différence entre un ordinateur et un serveur

|               | Ordinateur           | Serveur                       |
| ------------- | -------------------- | ----------------------------- |
| Disponibilité | Sur le temps d'usage | Tourne 24/7                   |
| Usage         | Sert 1 utilisateur   | Sert plusieurs utilisateurs   |
| Stockage      | Limité au disque dur | Beaucoup plus large et fiable |
| Réseau        | Réseau local         | on-premise ou cloud           |

## 2. Pourquoi le cloud

- Données disponible partout à tout moment, passage à l'international
- Accées facile à différentes technologies
- réductions des coûts en payant que les services informatiques utilisé
- Plus de frais d'entretien des centres de données
- AWS est certifié RGPD et HIPAA, sécurité certifié
- Forte scalabilité du système en quelque clics

## 3. Créer un compte AWS

1. Aller sur **aws.amazon.com**
2. Cliquer sur **"Créer un compte AWS"**
3. Renseigner email, mot de passe, nom du compte
4. Choisir le type de compte (Personnel ou Professionnel)
5. Renseigner les informations de paiement (carte bancaire)
6. Vérification d'identité par téléphone
7. Choisir un plan de support (gratuit, développeur, business...)
8. Accès à la console AWS

### Free Tier

AWS propose un **niveau gratuit** pendant 12 mois incluant :

- 750h/mois d'instances EC2
- 5 Go de stockage S3
- 750h/mois de RDS (SGBDR)

# 4. Tarification AWS

### Modèles de tarification

- **Pay as you go** → tu paies à l'usage, à la seconde ou à l'heure
- **Save when you commit** → réductions si tu t'engages sur 1 ou 3 ans
- **Pay less by using more** → réductions par paliers selon le volume

### Services pertinents pour notre projet

| Service | Prix indicatif |
| Amazon ECS (conteneurs) | Gratuit, tu paies les ressources utilisées |
| Amazon DocumentDB | À partir de 0,277$/heure |
| Amazon RDS | À partir de 0,017$/heure |
| Amazon S3 (stockage) | 0,023$/Go/mois |
| Amazon ECR (images Docker) | 0,10$/Go/mois |

### Outils de calcul

- **AWS Pricing Calculator** → https://calculator.aws pour estimer les coûts

## 5. Amazon RDS pour MongoDB et Amazon DocumentDB

### Amazon DocumentDB

- Service **compatible MongoDB** géré par AWS
- Pas besoin de gérer l'infrastructure
- Haute disponibilité automatique
- Sauvegardes automatiques
- Compatible avec les drivers MongoDB existants
- **Limitation** : pas 100% compatible MongoDB — certaines fonctionnalités avancées manquent

### Amazon RDS

- Service de bases de données relationnelles géré
- Supporte MySQL, PostgreSQL, Oracle...
- **Ne supporte pas MongoDB nativement**
- À utiliser si tu migres vers une base SQL

### Lequel choisir pour notre projet ?

|                      | DocumentDB | RDS         |
| -------------------- | ---------- | ----------- |
| Compatible MongoDB   | ✅         | ❌          |
| Géré par AWS         | ✅         | ✅          |
| Notre driver pymongo | ✅         | ❌          |
| Prix                 | Plus élevé | Moins élevé |

**→ DocumentDB est le choix logique** pour notre projet car on utilise déjà MongoDB et pymongo.

## 6. Déploiement MongoDB sur Amazon ECS

### Qu'est-ce qu'Amazon ECS ?

Service géré de conteneurs Docker sur AWS — l'équivalent de docker-compose
mais dans le cloud avec haute disponibilité.

### Les composants clés

| Composant                            | Rôle                                             |
| ------------------------------------ | ------------------------------------------------ |
| **ECR** (Elastic Container Registry) | Stocke les images Docker (comme Docker Hub)      |
| **ECS** (Elastic Container Service)  | Orchestre les conteneurs                         |
| **Fargate**                          | Exécute les conteneurs sans gérer de serveurs    |
| **VPC**                              | Réseau privé isolé pour sécuriser les conteneurs |

### Étapes de déploiement

1. **Pousser l'image Docker sur ECR**

```bash
aws ecr create-repository --repository-name migration-script
docker tag migration-script:latest <account>.dkr.ecr.eu-west-1.amazonaws.com/migration-script
docker push <account>.dkr.ecr.eu-west-1.amazonaws.com/migration-script
```

2. **Créer un cluster ECS**
3. **Définir une Task Definition** → équivalent du docker-compose.yml
4. **Lancer le service**

### Lien avec notre projet

Notre `docker-compose.yml` peut être converti en Task Definition ECS —
les concepts sont similaires !

## 7. Sauvegardes et surveillance sur AWS

### Sauvegardes automatiques

#### DocumentDB

- Sauvegardes automatiques quotidiennes
- Rétention configurable de 1 à 35 jours
- Restauration à un point précis dans le temps (PITR)
- Snapshots manuels possibles à tout moment

#### Amazon S3

- Stocker les sauvegardes du CSV et des exports MongoDB
- Versioning activable → garde l'historique des fichiers
- Cycle de vie configurable → archive automatique après X jours

### Surveillance avec CloudWatch

AWS CloudWatch est le service de monitoring d'AWS :

| Métrique surveillée    | Utilité                         |
| ---------------------- | ------------------------------- |
| CPU/RAM des conteneurs | Détecter les surcharges         |
| Connexions MongoDB     | Détecter les pics d'utilisation |
| Erreurs applicatives   | Alertes en cas de problème      |
| Latence des requêtes   | Optimiser les performances      |

### Alertes

- Configurer des **alarmes CloudWatch** → notification par email/SMS si seuil dépassé
- Intégration avec **AWS SNS** (Simple Notification Service)
