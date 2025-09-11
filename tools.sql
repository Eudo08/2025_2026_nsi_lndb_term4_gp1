-- FROM interface IMPORT templates, inscription

CREATE DATABASE info_individu
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

INSERT INTO info_individu (nom, prenom, nom_utilisateur,mot_passe)
VALUES (Bonnière, Tristan, le caca, abc123)