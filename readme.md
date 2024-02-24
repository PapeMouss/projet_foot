# Projet d'Analyse Comparative des Équipes (systémes) de Football

## Structure de la Base de Données

Pour ce projet, nous avons défini une structure de base de données relationnelle pour stocker les informations sur les équipes de football, les joueurs, les matchs et les tactiques utilisées. Voici un aperçu de la structure :

### Tables :

1. **Equipe** : Cette table contient des informations sur chaque équipe de football, telles que le nom de l'équipe, le pays, l'entraîneur principal, etc.

2. **Joueur** : Cette table stocke les détails sur chaque joueur, y compris son nom, sa date de naissance, son poste, etc. Chaque joueur est lié à une équipe.

3. **Match** : Cette table enregistre les détails sur chaque match joué, y compris les équipes participantes et les scores.

4. **Tactique** : Cette table contient les schémas tactiques utilisés par les équipes.

### Relations :

- Il y a une relation "many-to-one" entre Joueur et Equipe.
- Il y a une relation "many-to-many" entre Match et Equipe.
- Il y a une relation "many-to-many" entre Tactique et Equipe.

Cette structure de base de données peut être étendue en fonction des besoins spécifiques du projet.

## Données

### Sources de Données :

Les données utilisées dans ce projet ont été obtenues à partir de différentes sources en ligne, notamment Kaggle et Infogol.

### Ensembles de Données Utilisés :

1. **Kaggle** : Nous avons utilisé des ensembles de données sur les équipes de football, les joueurs, les matchs et les performances des équipes et des joueurs.

   - Recherches :
     - Football team data
     - Soccer player data
     - Football match data
     - Soccer statistics dataset
     - Football league dataset

2. **Infogol** : Nous avons également utilisé un ensemble de données contenant des statistiques sur les meilleurs buteurs des principales ligues de football, ainsi que d'autres informations pertinentes.

   - Remarque : Les valeurs xG et xG Per Avg Match sont des valeurs statistiques supportées par le site web d'où les données ont été extraites (Infogol).

   - Source des données : Les données de cet ensemble ont été collectées à partir du site web Infogol à l'aide de la technologie Selenium.

### Fichiers CSV Utilisés :

- **results.csv** : Ce fichier comprend des informations sur les matchs de football, y compris les équipes participantes, les scores, les dates et les lieux des matchs.

- **shootouts.csv** : Ce fichier comprend des informations sur les séances de tirs au but, y compris les équipes participantes et les vainqueurs.

- **goalscorers.csv** : Ce fichier comprend des informations sur les buts marqués lors des matchs, y compris les équipes, les buteurs et d'autres détails.

## Tables de la Base de Données SQLite

Nous disposons également d'une base de données SQLite contenant des informations sur les pays, les ligues, les équipes, les joueurs, les matchs et les attributs des équipes et des joueurs.

1. **Country** : Cette table contient des informations sur les pays.
2. **League** : Cette table contient des informations sur les ligues.
3. **Team** : Cette table contient des informations sur les équipes de football.
4. **Player** : Cette table contient des informations sur les joueurs de football.
5. **Match** : Cette table contient des informations sur les matchs de football.
6. **Team_Attributes** : Cette table contient des attributs spécifiques aux équipes.
7. **Player_Attributes** : Cette table contient des attributs spécifiques aux joueurs.



Fonctionnalité dans votre application, vous pouvez ajouter un curseur dans l'interface Streamlit permettant à l'utilisateur de sélectionner une période de temps spécifique. Ensuite, vous pouvez utiliser cette période de temps pour filtrer les données des matchs dans votre requête SQL et calculer le système de jeu le plus efficace pour cette période.

# Algorithme de Recommandation du Système de Jeu

Cet algorithme permet de recommander un système de jeu optimal pour une équipe de football sur une période donnée, en se basant sur les performances des équipes avec différents schémas tactiques.

## Fonctionnement de l'Algorithme

L'algorithme suit les étapes suivantes :

1. **Sélection de la Période de Temps** : L'utilisateur sélectionne une période de temps spécifique pour laquelle il souhaite obtenir une recommandation de système de jeu.

2. **Extraction des Données des Matchs** : Les données des matchs pour la période sélectionnée sont extraites à partir de la base de données.

3. **Analyse des Performances des Équipes** : Les performances des équipes avec chaque schéma tactique sont analysées pendant la période sélectionnée. Des indicateurs de performance tels que le nombre moyen de buts marqués, le nombre moyen de buts encaissés, et le pourcentage de victoires sont utilisés pour évaluer les performances.

4. **Évaluation des Performances Relatives** : Les performances des équipes avec chaque schéma tactique sont comparées pour déterminer lequel est le plus efficace. Des scores sont attribués à chaque schéma tactique en fonction des performances.

5. **Recommandation du Système de Jeu Optimal** : Le système de jeu qui a obtenu le meilleur score global est recommandé comme système de jeu optimal pour la période sélectionnée.

## Utilisation de l'Algorithme

Pour utiliser l'algorithme, suivez les étapes suivantes :

1. **Sélectionnez une Période de Temps** : Utilisez l'interface Streamlit pour sélectionner une période de temps spécifique en entrant une date de début et une date de fin.

2. **Calculer le Système de Jeu Recommandé** : Cliquez sur le bouton pour calculer le système de jeu recommandé. L'algorithme analysera les performances des équipes avec différents schémas tactiques pendant la période sélectionnée et recommandera le système de jeu optimal.

3. **Afficher le Résultat** : Une fois le calcul terminé, le système de jeu recommandé pour la période sélectionnée sera affiché.

## Développement de l'Algorithme

L'algorithme est implémenté dans un script Python utilisant la bibliothèque Streamlit pour l'interface utilisateur et SQLite pour la gestion des données de la base de données. Les performances des équipes sont calculées en fonction des données extraites de la base de données et des critères d'évaluation définis.

Pour exécuter l'algorithme, assurez-vous d'avoir correctement configuré votre environnement Python avec toutes les dépendances nécessaires et une connexion à la base de données SQLite contenant les données des équipes de football.


revoir la connectivité de  la base de données et vérifier que toutes les tables sont bien liées entre elles

##conninfo:
connected to database "foot_systeme_db" as user "moussamar" via socket in "/tmp" at port "5432".