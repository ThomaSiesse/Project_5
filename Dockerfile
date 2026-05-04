#image de base - python 3.13 slim(pour une image légère)
FROM python:3.13-slim
#metadata de l'image (description, version, author)
LABEL description="Migration Scipts" version="1.0" author="Thomas S"
#Dossier de travail dans le conteneur
WORKDIR /app
#Copie les fichiers utilies pour la migration dans le conteneur
COPY scripts/migrate.py .
COPY requirements.txt .
COPY data/healthcare_dataset.csv /app/data/
#Installation des dépendances nécessaires pour la migration
RUN pip install -r requirements.txt
#commande au démarrage
CMD ["python", "migrate.py"]