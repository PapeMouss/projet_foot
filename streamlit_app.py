import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
import io


# Configuration de la page
st.set_page_config(
    page_title="BEST LINEUP",
    page_icon="⚽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour exécuter des requêtes SQL et récupérer les résultats sous forme de DataFrame
def run_query_select(query):
    conn = psycopg2.connect(
        dbname="foot_systeme_db",
        user="moussamar",
        host="localhost",
        port="5432"
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fonction pour exécuter des requêtes SQL sans récupération de résultats
def run_query(query):
    conn = psycopg2.connect(
        dbname="foot_systeme_db",
        user="moussamar",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

# Calculer les performances des équipes avec chaque schéma tactique pendant la période sélectionnée
def calculate_team_performance(period_start, period_end, df_tactique):
    # 1. Extraire les données des matchs pour la période sélectionnée à partir de la base de données
    query_match_period = f"SELECT * FROM Match WHERE date BETWEEN '{period_start}' AND '{period_end}'"
    df_match_period = run_query_select(query_match_period)


    ##
    query_match_period = f"SELECT * FROM Match WHERE match_date BETWEEN '{period_start}' AND '{period_end}'"


    # 2. Calculer les performances avec chaque schéma tactique
    performance_data = calculate_performance(df_match_period, df_tactique)

    # 3. Évaluer les performances relatives des schémas tactiques
    tactical_scores = evaluate_tactical_performance(performance_data)

    # 4. Recommander le système de jeu optimal
    recommended_formation = recommend_optimal_tactic(tactical_scores, df_tactique)

    # Retourner le système de jeu recommandé
    return recommended_formation

# Calculer les performances avec chaque schéma tactique
def calculate_performance(df_match_periode, df_tactique):
    # Fusionner les données des matchs avec les schémas tactiques utilisés par chaque équipe
    df_match_tactique = pd.merge(df_match_periode, df_tactique, how='inner', left_on='equipe_id', right_on='equipe_id')

    # Calculer les performances pour chaque équipe avec chaque schéma tactique
    # Exemple : nombre moyen de buts marqués
    performance_data = df_match_tactique.groupby(['equipe_id', 'tactique_id'])['but_equipe'].mean().reset_index()

    return performance_data

# Évaluer les performances relatives des schémas tactiques
def evaluate_tactical_performance(performance_data):
    # Calculer les scores pour chaque schéma tactique en fonction des performances
    # Exemple : attribuer un score basé sur le nombre moyen de buts marqués
    tactical_scores = performance_data.groupby('tactique_id')['but_equipe'].mean().reset_index()
    tactical_scores.rename(columns={'but_equipe': 'score'}, inplace=True)

    # Trier les schémas tactiques par score décroissant
    tactical_scores.sort_values(by='score', ascending=False, inplace=True)

    return tactical_scores

# Recommander le système de jeu optimal
def recommend_optimal_tactic(tactical_scores, df_tactique):
    # Sélectionner le schéma tactique avec le meilleur score global
    optimal_tactic_id = tactical_scores.iloc[0]['tactique_id']

    # Récupérer les détails du schéma tactique optimal
    optimal_tactic_details = df_tactique[df_tactique['tactique_id'] == optimal_tactic_id].iloc[0]

    return optimal_tactic_details

# Interface utilisateur pour sélectionner une période de temps et obtenir le meilleur système de jeu pour cette période
def get_best_formation():
    st.subheader('Sélectionner une Période de Temps')
    date_debut = st.date_input('Date de Début')
    date_fin = st.date_input('Date de Fin')

    if st.button('Calculer le Système de Jeu Recommandé'):
        if date_debut > date_fin:
            st.error('La date de fin doit être postérieure à la date de début.')
        else:
            df_tactique = run_query_select('SELECT * FROM Tactique')
            # Calculer et afficher le système de jeu recommandé pour la période sélectionnée
            recommended_formation = calculate_team_performance(date_debut, date_fin, df_tactique)
            st.subheader('Système de Jeu Recommandé pour la Période Sélectionnée')
            st.write(recommended_formation)



# Interface utilisateur pour saisir les données des joueurs et obtenir le meilleur système de jeu pour son équipe
def get_best_formation_for_team():
    st.title('Optimisation du Système de Jeu')
    st.subheader('Saisie des Données des Joueurs')
    nom_joueur = st.text_input('Nom du Joueur')
    poste_joueur = st.selectbox('Poste du Joueur', ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'])
    equipe_id = st.selectbox('Équipe', [1, 2, 3])  # Sélectionnez l'équipe à laquelle le joueur appartient

    if st.button('Enregistrer'):
        # Insertion des données du joueur dans la base de données
        query_insert = f"INSERT INTO Joueur (nom, poste, equipe_id) VALUES ('{nom_joueur}', '{poste_joueur}', {equipe_id})"
        run_query(query_insert)
        st.success('Données du joueur enregistrées avec succès.')

    # Affichage des données des joueurs
    st.subheader('Données des Joueurs')
    query_joueur = 'SELECT * FROM Joueur'
    df_joueur = run_query_select(query_joueur)
    st.write(df_joueur)

    # Affichage du système de jeu recommandé pour son équipe
    st.subheader('Système de Jeu Recommandé pour Votre Équipe')
    recommended_formation = '4-4-2'  # Remplacez cette chaîne par le système recommandé
    st.write(f'Système recommandé : {recommended_formation}')
    
    # Appel de la fonction pour afficher le terrain de football
    plot_football_field(recommended_formation)


def plot_football_field(recommended_formation):
    fig, ax = plt.subplots(figsize=(8, 5))

    # Dessiner le terrain
    plt.plot([0, 0, 100, 100, 0], [0, 50, 50, 0, 0], color='green')  # Bord extérieur
    plt.plot([20, 20, 80, 80, 20], [0, 20, 20, 0, 0], color='green')  # Surface de réparation gauche
    plt.plot([20, 20, 80, 80, 20], [50, 30, 30, 50, 50], color='green')  # Surface de réparation droite
    plt.plot([50], [0], 'o', color='blue')  # Cercle central
    plt.plot([20, 20], [25, 25], 'k-')  # Ligne médiane
    plt.plot([0, 100], [25, 25], 'k-')  # Ligne médiane

    # Afficher les positions des joueurs selon le système recommandé
    positions = {
        '4-4-2': [(30, 10), (30, 20), (30, 30), (30, 40), (50, 10), (50, 20), (50, 30), (50, 40), (70, 25), (70, 35)],
        '4-3-3': [(30, 10), (30, 25), (30, 40), (50, 10), (50, 25), (50, 40), (70, 10), (70, 25), (70, 40)],
        # Ajoutez d'autres formations ici
    }

    for position in positions[recommended_formation]:
        plt.plot(position[0], position[1], 'ro')  # Afficher la position des joueurs

    plt.title(f"Système de jeu recommandé : {recommended_formation}")
    plt.xlabel('Longueur du terrain')
    plt.ylabel('Largeur du terrain')
    plt.xlim(0, 100)
    plt.ylim(0, 50)
    plt.grid(True)

    # Convertir le graphique Matplotlib en image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    # Afficher l'image dans Streamlit
    st.image(buf)

# Interface utilisateur pour saisir les données des joueurs et obtenir le meilleur système de jeu pour son équipe
def get_best_formation_for_team():
    st.title('Optimisation du Système de Jeu')
    st.subheader('Saisie des Données des Joueurs')
    nom_joueur = st.text_input('Nom du Joueur')
    poste_joueur = st.selectbox('Poste du Joueur', ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'])
    equipe_id = st.selectbox('Équipe', [1, 2, 3])  # Sélectionnez l'équipe à laquelle le joueur appartient

    if st.button('Enregistrer'):
        # Insertion des données du joueur dans la base de données
        query_insert = f"INSERT INTO Joueur (nom, poste, equipe_id) VALUES ('{nom_joueur}', '{poste_joueur}', {equipe_id})"
        run_query(query_insert)
        st.success('Données du joueur enregistrées avec succès.')

    # Affichage des données des joueurs
    st.subheader('Données des Joueurs')
    query_joueur = 'SELECT * FROM Joueur'
    df_joueur = run_query_select(query_joueur)
    st.write(df_joueur)

    # Affichage du système de jeu recommandé pour son équipe
    st.subheader('Système de Jeu Recommandé pour Votre Équipe')
    st.write('À implémenter...')

# Ajouter un titre stylisé
st.title("BEST LINEUP")

# Ajouter une option de mode sombre
mode_sombre = st.sidebar.checkbox("Mode Sombre")

# Appliquer le mode sombre si activé
if mode_sombre:
    st.markdown(
        """
        <style>
        body {
            color: #000000;
            background-color: #121212;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Appeler les fonctions appropriées en fonction de l'option sélectionnée par l'utilisateur
option = st.radio('Choisir une option', ['Obtenir le Meilleur Système pour une Période de Temps', 'Optimiser le Système pour Votre Équipe'])
if option == 'Obtenir le Meilleur Système pour une Période de Temps':
    get_best_formation()
else:
    get_best_formation_for_team()

# Ajouter une séparation
st.markdown("---")

# Pied de page avec les informations de contact
st.markdown(
    """
    ---\n
    Contactez-nous : marmoussa24@gmail.com\n
    Suivez-nous sur Twitter : [BesttLineUp](https://twitter.com/SystèmeFootball)
    """
)
