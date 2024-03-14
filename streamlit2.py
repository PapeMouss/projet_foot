import streamlit as st
import pandas as pd
import psycopg2
import mplsoccer
import matplotlib.pyplot as plt

# Connexion à la base de données
conn = psycopg2.connect(
    dbname="football_db",
    user="moussamar",
    host="localhost"
)
cursor = conn.cursor()

# vérification de la connexion à la base de données
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

# Fonction pour charger les données du joueur sélectionné
def load_player_data(player_id):
    query = f"SELECT * FROM players WHERE player_id = {player_id};"
    df = pd.read_sql_query(query, conn)
    return df

# Titre de l'application
st.title("Football Data Visualization 🏟️")

# Sidebar pour sélectionner la problématique
problematic_choice = st.sidebar.selectbox(
    "Select a problematics",
    ("Goals Analysis", "Assists Analysis", "Shots Analysis", "Player Heatmap")
)

# Fonction pour charger les données en fonction de la problématique choisie
def load_data(problematic):
    if problematic == "Goals Analysis":
        query = "SELECT * FROM appearances WHERE goals > 0;"
    elif problematic == "Assists Analysis":
        query = "SELECT * FROM appearances WHERE assists > 0;"
    elif problematic == "Shots Analysis":
        query = "SELECT * FROM shots;"
    elif problematic == "Player Heatmap":
        query = "SELECT * FROM players;"
    df = pd.read_sql_query(query, conn)
    return df

# Chargement des données en fonction de la problématique choisie
data = load_data(problematic_choice)

# Affichage des données
st.write("## Data Overview")
st.write(data.head())

# Visualisations en fonction de la problématique choisie
if problematic_choice == "Goals Analysis":
    # Visualisation des buts marqués par joueur
    st.write("## Goals Analysis")
    goals_per_player = data.groupby("player_id")["goals"].sum()
    st.bar_chart(goals_per_player)

    # Top buteurs
    st.write("## Top Scorers")
    top_scorers = data.groupby('player_id')['goals'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_scorers)

    # Buts par match
    data['goals_per_match'] = data['goals'] / data['appearances']
    st.write("## Goals per Match")
    goals_per_match = data.groupby('player_id')['goals_per_match'].mean().sort_values(ascending=False)
    st.bar_chart(goals_per_match)

    # Répartition des buts par pied préféré
    st.write("## Goals Distribution by Preferred Foot")
    goals_by_foot = data.groupby('preferred_foot')['goals'].sum()
    st.bar_chart(goals_by_foot)

    # Histogramme des buts par minute de jeu
    st.write("## Goals Distribution by Minute")
    plt.hist(data['minute'], bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Minute')
    plt.ylabel('Number of Goals')
    st.pyplot()

elif problematic_choice == "Assists Analysis":
    # Visualisation des passes décisives par joueur
    st.write("## Assists Analysis")
    assists_per_player = data.groupby("player_id")["assists"].sum()
    st.bar_chart(assists_per_player)

elif problematic_choice == "Shots Analysis":
    # Visualisation des tirs
    st.write("## Shots Analysis")
    # Utiliser mplsoccer pour visualiser les tirs
    selected_player = st.sidebar.selectbox("Select a player", data['shooterID'].unique())
    filtered_data = data[data['shooterID'] == selected_player]
    pitch = mplsoccer.VerticalPitch(half=True)
    fig, ax = pitch.draw()
    for i, shot in filtered_data.iterrows():
        x = shot['position_x']
        y = shot['position_y']
        goal = shot['shotResult'] == 'Goal'
        pitch.scatter(x, y, ax=ax, color='red' if goal else 'blue')
    st.pyplot(fig)

elif problematic_choice == "Player Heatmap":
    # Visualisation du heatmap d'un joueur
    st.write("## Player Heatmap")
    all_players = data['player_id'].unique()
    selected_player = st.sidebar.selectbox("Select a player", all_players)
    player_data = load_player_data(selected_player)
    # Créer un heatmap pour les actions du joueur
    st.write(f"Heatmap for player: {selected_player}")

    # Créer le terrain de football
    pitch = mplsoccer.VerticalPitch(half=True)

    # Créer un nouveau graphique
    fig, ax = plt.subplots(figsize=(10, 7))

    # Afficher les tirs
    shots = player_data[player_data['shotResult'] == 'Goal']
    pitch.scatter(shots['positionX'], shots['positionY'], ax=ax, color='red', s=100, zorder=3)

    # Afficher le heatmap
    pitch.heatmap(player_data['positionX'], player_data['positionY'], ax=ax, bins=20, cmap='hot', edgecolors='none')

    # Afficher le terrain de football
    pitch.draw(ax=ax)

    # Afficher le graphique dans Streamlit
    st.pyplot(fig)

# Fermer la connexion à la base de données
cursor.close()
conn.close()
