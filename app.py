import sqlite3
import streamlit as st
import pandas as pd

# Connexion à la base
def connect_db():
    return sqlite3.connect("hotel.db")

st.title("Interface de gestion des réservations")

# Choix de la fonctionnalité
choix = st.sidebar.selectbox("Menu", [
    "Accueil",
    "Voir les réservations",
    "Voir les clients",
    "Voir les chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
])

conn = connect_db()
cursor = conn.cursor()

if choix == "Accueil":
    st.markdown("Bienvenue dans le système de gestion des réservations d'hôtel.")

elif choix == "Voir les réservations":
    requete = """
        SELECT Reservation.id_Reservation, Client.Nom_Complet, Reservation.Date_arrivee, Reservation.Date_depart
        FROM Reservation
        JOIN Client ON Reservation.id_Client = Client.id_Client
    """
    df = pd.read_sql_query(requete, conn)
    st.subheader("Réservations")
    st.dataframe(df)

elif choix == "Voir les clients":
    df = pd.read_sql_query("SELECT * FROM Client", conn)
    st.subheader("Clients")
    st.dataframe(df)

elif choix == "Voir les chambres disponibles":
    st.subheader("Rechercher des chambres disponibles")
    date_debut = st.date_input("Date d'arrivée")
    date_fin = st.date_input("Date de départ")

    if st.button("Chercher"):
        query = f"""
        SELECT * FROM Chambre
        WHERE id_Chambre NOT IN (
            SELECT id_Chambre FROM Concerner
            JOIN Reservation ON Concerner.id_Reservation = Reservation.id_Reservation
            WHERE NOT (
                Reservation.Date_depart < '{date_debut}' OR
                Reservation.Date_arrivee > '{date_fin}'
            )
        )
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)

elif choix == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")
    nom = st.text_input("Nom complet")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.text_input("Code postal")
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")

    if st.button("Ajouter"):
        cursor.execute("INSERT INTO Client (Adresse, Ville, Code_postal, Email, Telephone, Nom_Complet) VALUES (?, ?, ?, ?, ?, ?)",
            (adresse, ville, code_postal, email, telephone, nom))
        conn.commit()
        st.success("Client ajouté avec succès !")

elif choix == "Ajouter une réservation":
    st.subheader("Ajouter une réservation")
    clients = cursor.execute("SELECT id_Client, Nom_Complet FROM Client").fetchall()
    client_choisi = st.selectbox("Client", clients, format_func=lambda x: f"{x[1]} (ID {x[0]})")
    date_arrivee = st.date_input("Date d'arrivée")
    date_depart = st.date_input("Date de départ")

    if st.button("Enregistrer la réservation"):
        cursor.execute("INSERT INTO Reservation (Date_arrivee, Date_depart, id_Client) VALUES (?, ?, ?)",
            (str(date_arrivee), str(date_depart), client_choisi[0]))
        conn.commit()
        st.success("Réservation ajoutée avec succès !")

conn.close()
