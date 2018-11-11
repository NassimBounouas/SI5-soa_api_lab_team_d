# SI5-soa_api_lab_team_d 

## Révision ~2.1 - 11/11/2018

# Pré-requis

* Une installation fonctionnelle de `Docker`, avec l'utilisateur actuellement connecté appartenant au groupe docker.
* Le port `localhost:8080` doit être libre afin d'exposer notre `API-Gateway`.

# Remarques

- Nous avons rédigé une documentation de notre façade avec `Swagger`. Un fichier `swagger.yaml` est disponible à la racine du dépôt.
- Chaque `micro-service` inclut un readme interne.
  - ceux-ci sont hébergés sur `DockerHub` 
- Un fichier de documentation des échanges de messages a été tenu. Il est aussi disponible à la racine du projet sous le nom de `workflow.pdf`

# Construction

```bash
chmod +x install.sh
./install.sh
```

# Deploiement

```bash
docker-compose up -d
```

# Déroulement du scénario

```bash
chmod +x run.sh
./run.sh
```

# Déroulement du test de charge

```bash
chmod +x load.sh
./load.sh
```
