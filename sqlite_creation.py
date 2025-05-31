import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Hotel (
    id_Hotel INTEGER PRIMARY KEY,
    Ville TEXT,
    Pays TEXT,
    Code_postal INTEGER
);

CREATE TABLE IF NOT EXISTS Client (
    id_Client INTEGER PRIMARY KEY,
    Adresse TEXT,
    Ville TEXT,
    Code_postal INTEGER,
    Email TEXT,
    Telephone TEXT,
    Nom_Complet TEXT
);

CREATE TABLE IF NOT EXISTS Prestation (
    id_Prestation INTEGER PRIMARY KEY,
    Prix REAL,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Type_Chambre (
    id_Type INTEGER PRIMARY KEY,
    Type TEXT,
    Tarif REAL
);

CREATE TABLE IF NOT EXISTS Chambre (
    id_Chambre INTEGER PRIMARY KEY,
    Numero INTEGER,
    Etage INTEGER,
    Fumeurs INTEGER,
    id_Type INTEGER,
    id_Hotel INTEGER,
    FOREIGN KEY (id_Type) REFERENCES Type_Chambre(id_Type),
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel)
);

CREATE TABLE IF NOT EXISTS Reservation (
    id_Reservation INTEGER PRIMARY KEY,
    Date_arrivee TEXT,
    Date_depart TEXT,
    id_Client INTEGER,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client)
);

CREATE TABLE IF NOT EXISTS Concerner (
    id_Reservation INTEGER,
    id_Chambre INTEGER,
    PRIMARY KEY (id_Reservation, id_Chambre),
    FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation),
    FOREIGN KEY (id_Chambre) REFERENCES Chambre(id_Chambre)
);

CREATE TABLE IF NOT EXISTS Evaluation (
    id_Evaluation INTEGER PRIMARY KEY,
    Date_arrivee TEXT,
    Note INTEGER,
    Texte TEXT,
    id_Client INTEGER,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client)
);

CREATE TABLE IF NOT EXISTS Offre (
    id_Hotel INTEGER,
    id_Prestation INTEGER,
    PRIMARY KEY (id_Hotel, id_Prestation),
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
    FOREIGN KEY (id_Prestation) REFERENCES Prestation(id_Prestation)
);
""")

conn.commit()
conn.close()

print("Tables créées avec succès.")
