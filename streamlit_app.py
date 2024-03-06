import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="BEST LINEUP 🏟️ ️",
    page_icon="⚽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    user='moussamar',
    database='football_db'
)

# Fonction pour vérifier la connexion à la base de données
def check_database_connection():
    try:
        conn.cursor().execute("SELECT 1")
        return True
    except psycopg2.Error as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
        return False

# Vérification de la connexion à la base de données
if check_database_connection():
    st.success("La connexion à la base de données a réussi.")
else:
    st.error("La connexion à la base de données a échoué.")

# Fonction pour exécuter une requête de sélection SQL et récupérer les résultats en DataFrame
def run_query_select(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    cursor.close()
    return df

# Exécution d'une requête SQL sans récupération de résultats
def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()

# Calcul des performances des équipes pendant la période sélectionnée
def calculate_team_performance(period_start, period_end):
    query = f"""
        SELECT
            homeTeam_id,
            awayTeam_id,
            homeGoals,
            awaysGoals
        FROM
            games
        WHERE
            date BETWEEN '{period_start}' AND '{period_end}'
    """
    df_games = run_query_select(query)

    # Calcul des performances pour chaque équipe
    performances = {}
    for index, row in df_games.iterrows():
        home_team_id = row['homeTeam_id']
        away_team_id = row['awayTeam_id']
        home_goals = row['homeGoals']
        away_goals = row['awaysGoals']

        # Victoire à domicile
        if home_goals > away_goals:
            performances[home_team_id] = performances.get(home_team_id, {'victoires': 0, 'matchs': 0})
            performances[home_team_id]['victoires'] += 1
            performances[home_team_id]['matchs'] += 1
        # Victoire à l'extérieur
        elif home_goals < away_goals:
            performances[away_team_id] = performances.get(away_team_id, {'victoires': 0, 'matchs': 0})
            performances[away_team_id]['victoires'] += 1
            performances[away_team_id]['matchs'] += 1
        # Match nul
        else:
            performances[home_team_id] = performances.get(home_team_id, {'matchs_nuls': 0, 'matchs': 0})
            performances[home_team_id]['matchs_nuls'] += 1
            performances[home_team_id]['matchs'] += 1
            performances[away_team_id] = performances.get(away_team_id, {'matchs_nuls': 0, 'matchs': 0})
            performances[away_team_id]['matchs_nuls'] += 1
            performances[away_team_id]['matchs'] += 1

    # Calcul des pourcentages de victoires et de matchs nuls pour chaque équipe
    for team_id, data in performances.items():
        total_matchs = data['matchs']
        if total_matchs > 0:
            performances[team_id]['pourcentage_victoires'] = (data.get('victoires', 0) / total_matchs) * 100
            performances[team_id]['pourcentage_matchs_nuls'] = (data.get('matchs_nuls', 0) / total_matchs) * 100
        else:
            performances[team_id]['pourcentage_victoires'] = 0
            performances[team_id]['pourcentage_matchs_nuls'] = 0

    return performances


# Partie affichage le meilleur système/période
def get_best_formation():
    st.subheader('Sélectionner une Période de Temps')
    date_debut = st.date_input('Date de Début')
    date_fin = st.date_input('Date de Fin')

    if st.button('Valider'):
        if date_debut > date_fin:
            st.error('La date de fin doit être postérieure à la date de début.')
        else:
            # Calcul et affichage du système de jeu recommandé pour la période sélectionnée
            recommended_formation = calculate_team_performance(date_debut, date_fin)
            st.subheader('Système de Jeu Recommandé pour la Période Sélectionnée')
            st.write(recommended_formation)

            # Affichage graphique radar pour visualiser les performances des équipes
            fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

            # Exemple de données fictives pour les performances des équipes (à remplacer par vos données réelles)
            equipe_ids = list(recommended_formation.keys())
            victoires = [data['pourcentage_victoires'] for data in recommended_formation.values()]
            matchs_nuls = [data['pourcentage_matchs_nuls'] for data in recommended_formation.values()]

            # Angle pour chaque équipe
            angles = np.linspace(0, 2 * np.pi, len(equipe_ids), endpoint=False).tolist()

            # Créer un graphique radar
            ax.fill(angles, victoires, color='blue', alpha=0.25, label='Pourcentage Victoires')
            ax.fill(angles, matchs_nuls, color='green', alpha=0.25, label='Pourcentage Matchs Nuls')
            ax.plot(angles, victoires, color='blue', linewidth=2)
            ax.plot(angles, matchs_nuls, color='green', linewidth=2)

            # Définir les étiquettes des équipes
            ax.set_xticks(angles)
            ax.set_xticklabels(equipe_ids)

            ax.legend()

            st.pyplot(fig)

##############################################################################################


# Partie affichage le système en fonction des joueurs
def get_best_formation_for_team():
    st.title('Optimisation du Système de Jeu')
    st.subheader('Saisie des Données des Joueurs')

    # Nombre total de joueurs à afficher
    total_joueurs = 11

    # Nombre de colonnes pour afficher les champs de saisie des joueurs
    num_colonnes = 3

    # Calcul du nombre total de lignes nécessaire pour afficher tous les joueurs
    num_lignes = total_joueurs // num_colonnes
    if total_joueurs % num_colonnes != 0:
        num_lignes += 1

    # Création de formulaires pour saisir les données de chaque joueur
    joueur_index = 0
    for ligne in range(num_lignes):
        columns = st.columns(num_colonnes)
        for colonne in columns:
            if joueur_index < total_joueurs:
                with colonne:
                    joueur_index += 1
                    st.write(f"Joueur {joueur_index}:")
                    nom_joueur = st.text_input(f"Nom du Joueur {joueur_index}", key=f"nom_{joueur_index}")  # Clé unique pour chaque texte d'entrée
                    poste_joueur = st.selectbox(f"Poste du Joueur {joueur_index}", ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'], key=f"poste_{joueur_index}")  # Clé unique pour chaque selectbox
                    equipe_id = st.selectbox(f'Équipe du Joueur {joueur_index}', [1, 2, 3], key=f"equipe_{joueur_index}")  # Clé unique pour chaque selectbox

    if st.button('Enregistrer'):
        # Insertion des données joueurs dans la base de données
        for i in range(1, total_joueurs + 1):
            nom_joueur = st.text_input(f"Nom du Joueur {i}", key=f"nom_{i}")
            poste_joueur = st.selectbox(f"Poste du Joueur {i}", ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'], key=f"poste_{i}")
            equipe_id = st.selectbox(f'Équipe du Joueur {i}', [1, 2, 3], key=f"equipe_{i}")

            query_insert = f"INSERT INTO players (name, position, team_id) VALUES ('{nom_joueur}', '{poste_joueur}', {equipe_id})"
            run_query(query_insert)
        
        st.success('Données des joueurs enregistrées avec succès.')

        # Bouton pour obtenir le système de jeu recommandé
        if st.button('Afficher le Système de Jeu Recommandé'):
            # Récupérer les données des joueurs enregistrées dans la base de données
            query_joueur = 'SELECT * FROM players'
            df_joueur = run_query_select(query_joueur)
            # Calculer le système de jeu recommandé et l'afficher
            recommended_formation = calculate_team_performance(df_joueur)
            st.subheader('Système de Jeu Recommandé')
            st.write(recommended_formation)

    # Affichage des données des joueurs
    st.subheader('Données des Joueurs')
    query_joueur = 'SELECT * FROM players'
    df_joueur = run_query_select(query_joueur)
    st.write(df_joueur)

    with st.expander('Affiner la recherche'):
        # Filtre des joueurs par équipes ou par positions
        team_filter = st.multiselect('Équipes', sorted([str(i) for i in set(df_joueur['team_id'])]))
        position_filter = st.multiselect('Positions', ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'])

# Affichage du contenu en fonction de l'option sélectionnée par l'utilisateur
option = st.sidebar.radio('Choisir une option', ['Le Meilleur Système/Période', 'Meilleur Système en fonction des joueurs'])
if option == 'Le Meilleur Système/Période':
    get_best_formation()
else:
    get_best_formation_for_team()

# Ajout séparation
st.markdown("---")

# Pied de page avec les informations de contact
st.markdown(
    """
    ---\n
    Contactez-nous : marmoussa24@gmail.com\n
    Suivez-nous sur Twitter : [BestLineUp](https://twitter.com/SystèmeFootball)
    """
)
