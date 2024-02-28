import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="BEST LINEUP 🏟️ ️",
    page_icon="⚽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Ajouter un lien vers le fichier CSS dans la balise head
st.markdown(
    """
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    """,
    unsafe_allow_html=True
)

# connection (db) et exécution des requêtes SQL et récupération des résultats en DataFrame
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

# exécution des requêtes SQL sans récupération de résultats
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

# Calcul des performances des équipes avec chaque schéma tactique pendant la période sélectionnée
def calculate_team_performance(period_start, period_end, df_tactique):
    # Code pour calculer les performances des équipes avec chaque tactique
    pass

# Partie pour afficher le meilleur système/la meilleure période
def get_best_formation():
    st.subheader('Sélectionner une Période de Temps')
    date_debut = st.date_input('Date de Début')
    date_fin = st.date_input('Date de Fin')

    if st.button('Calculer le Système de Jeu Recommandé'):
        if date_debut > date_fin:
            st.error('La date de fin doit être postérieure à la date de début.')
        else:
            df_tactique = run_query_select('SELECT * FROM Tactique')
            # Calcul et affichage du système de jeu recommandé pour la période sélectionnée
            recommended_formation = calculate_team_performance(date_debut, date_fin, df_tactique)
            st.subheader('Système de Jeu Recommandé pour la Période Sélectionnée')
            st.write(recommended_formation)

            # Afficher un graphique radar pour visualiser les performances des tactiques
            fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))
            
            # Exemple de données fictives pour les performances de chaque tactique (à remplacer par vos données réelles)
            tactiques = ['Tactique 1', 'Tactique 2', 'Tactique 3', 'Tactique 4', 'Tactique 5']
            performances = [4, 3, 2, 5, 4]  # Score de performance arbitraire pour chaque tactique
            
            # Angle pour chaque tactique
            angles = np.linspace(0, 2 * np.pi, len(tactiques), endpoint=False).tolist()
            
            # Créer un graphique radar
            ax.fill(angles, performances, color='blue', alpha=0.25)
            ax.plot(angles, performances, color='blue', linewidth=2)
            
            # Définir les étiquettes des tactiques
            ax.set_xticks(angles)
            ax.set_xticklabels(tactiques)
            
            st.pyplot(fig)

##############################################################################################################################################################

# Partie pour afficher le système en fonction des joueurs
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
        # Insertion des données des joueurs dans la base de données
        for i in range(1, total_joueurs + 1):
            nom_joueur = st.text_input(f"Nom du Joueur {i}", key=f"nom_{i}")
            poste_joueur = st.selectbox(f"Poste du Joueur {i}", ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'], key=f"poste_{i}")
            equipe_id = st.selectbox(f'Équipe du Joueur {i}', [1, 2, 3], key=f"equipe_{i}")

            query_insert = f"INSERT INTO Joueur (nom, poste, equipe_id) VALUES ('{nom_joueur}', '{poste_joueur}', {equipe_id})"
            run_query(query_insert)
        
        st.success('Données des joueurs enregistrées avec succès.')

        # Bouton pour obtenir le système de jeu recommandé
        if st.button('Afficher le Système de Jeu Recommandé'):
            # Récupérer les données des joueurs enregistrées dans la base de données
            query_joueur = 'SELECT * FROM Joueur'
            df_joueur = run_query_select(query_joueur)
            # Calculer le système de jeu recommandé et l'afficher
            recommended_formation = calculate_team_performance(df_joueur)
            st.subheader('Système de Jeu Recommandé')
            st.write(recommended_formation)

    # Affichage des données des joueurs
    st.subheader('Données des Joueurs')
    query_joueur = 'SELECT * FROM Joueur'
    df_joueur = run_query_select(query_joueur)
    st.write(df_joueur)

    with st.expander('Affiner la recherche'):
        # Filtre des joueurs par équipes ou par positions
        team_filter = st.multiselect('Équipes', sorted([str(i) for i in set(df_joueur['equipe_id'])]))
        position_filter = st.multiselect('Positions', ['Attaquant', 'Milieu', 'Défenseur', 'Gardien'])

# Affichage du contenu en fonction de l'option sélectionnée par l'utilisateur
option = st.sidebar.radio('Choisir une option', ['Le Meilleur Système/Période', 'Le Système en fonction des joueurs'])
if option == 'Le Meilleur Système/Période':
    get_best_formation()
else:
    get_best_formation_for_team()

# Ajout d'une séparation
st.markdown("---")

# Pied de page avec les informations de contact
st.markdown(
    """
    ---\n
    Contactez-nous : marmoussa24@gmail.com\n
    Suivez-nous sur Twitter : [BesttLineUp](https://twitter.com/SystèmeFootball)
    """
)
