"""
Futbol DB — 10 Büyük Lig, Gerçek Oyuncular, Otomatik Maç Sistemi
"""
import sqlite3
import random
from datetime import date, timedelta, datetime
from typing import Optional
import os

_DATA_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_DATA_DIR, "parti.db")

# ─── 10 Büyük Lig Tanımları ────────────────────────────────────────────────

LIGLER = {
    "premier_league":  {"ad": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League",  "ulke": "EN", "kisa": "PL"},
    "la_liga":         {"ad": "🇪🇸 La Liga",               "ulke": "ES", "kisa": "LL"},
    "bundesliga":      {"ad": "🇩🇪 Bundesliga",             "ulke": "DE", "kisa": "BL"},
    "serie_a":         {"ad": "🇮🇹 Serie A",                "ulke": "IT", "kisa": "SA"},
    "ligue_1":         {"ad": "🇫🇷 Ligue 1",               "ulke": "FR", "kisa": "L1"},
    "super_lig":       {"ad": "🇹🇷 Süper Lig",             "ulke": "TR", "kisa": "SL"},
    "eredivisie":      {"ad": "🇳🇱 Eredivisie",            "ulke": "NL", "kisa": "ED"},
    "primeira_liga":   {"ad": "🇵🇹 Primeira Liga",         "ulke": "PT", "kisa": "PRL"},
    "mls":             {"ad": "🇺🇸 MLS",                   "ulke": "US", "kisa": "MLS"},
    "brasileiro":      {"ad": "🇧🇷 Brasileirão",           "ulke": "BR", "kisa": "BRA"},
}

# ─── Gerçek Takımlar ve Kadroları ──────────────────────────────────────────

GERCEK_TAKIMLAR = {
    # ── Premier League ──
    "Manchester City": {
        "lig": "premier_league", "forma": "#6CABDD",
        "oyuncular": [
            ("Ederson", "Kaleci", 90, "BR"), ("Stefan Ortega", "Kaleci", 78, "DE"),
            ("Kyle Walker", "Defans", 84, "EN"), ("Manuel Akanji", "Defans", 84, "CH"),
            ("Rúben Dias", "Defans", 90, "PT"), ("Joško Gvardiol", "Defans", 86, "HR"),
            ("Rico Lewis", "Defans", 78, "EN"), ("Rodri", "Orta Saha", 93, "ES"),
            ("Kevin De Bruyne", "Orta Saha", 91, "BE"), ("Bernardo Silva", "Orta Saha", 89, "PT"),
            ("Phil Foden", "Orta Saha", 89, "EN"), ("İlkay Gündoğan", "Orta Saha", 85, "DE"),
            ("Matheus Nunes", "Orta Saha", 81, "PT"), ("Erling Haaland", "Forvet", 95, "NO"),
            ("Julián Álvarez", "Forvet", 86, "AR"), ("Jeremy Doku", "Forvet", 84, "BE"),
            ("Jack Grealish", "Forvet", 83, "EN"), ("Savinho", "Forvet", 79, "BR"),
        ]
    },
    "Arsenal": {
        "lig": "premier_league", "forma": "#EF0107",
        "oyuncular": [
            ("David Raya", "Kaleci", 87, "ES"), ("Karl Jakob Hein", "Kaleci", 72, "EE"),
            ("Ben White", "Defans", 85, "EN"), ("William Saliba", "Defans", 88, "FR"),
            ("Gabriel Magalhães", "Defans", 87, "BR"), ("Oleksandr Zinchenko", "Defans", 82, "UA"),
            ("Takehiro Tomiyasu", "Defans", 80, "JP"), ("Thomas Partey", "Orta Saha", 84, "GH"),
            ("Martin Ødegaard", "Orta Saha", 90, "NO"), ("Declan Rice", "Orta Saha", 88, "EN"),
            ("Jorginho", "Orta Saha", 80, "IT"), ("Bukayo Saka", "Forvet", 90, "EN"),
            ("Leandro Trossard", "Forvet", 84, "BE"), ("Gabriel Martinelli", "Forvet", 85, "BR"),
            ("Kai Havertz", "Forvet", 84, "DE"), ("Eddie Nketiah", "Forvet", 79, "EN"),
        ]
    },
    "Liverpool": {
        "lig": "premier_league", "forma": "#C8102E",
        "oyuncular": [
            ("Alisson Becker", "Kaleci", 91, "BR"), ("Caoimhín Kelleher", "Kaleci", 78, "IE"),
            ("Trent Alexander-Arnold", "Defans", 88, "EN"), ("Virgil van Dijk", "Defans", 91, "NL"),
            ("Ibrahima Konaté", "Defans", 85, "FR"), ("Andrew Robertson", "Defans", 85, "SC"),
            ("Joe Gomez", "Defans", 81, "EN"), ("Alexis Mac Allister", "Orta Saha", 87, "AR"),
            ("Dominik Szoboszlai", "Orta Saha", 85, "HU"), ("Ryan Gravenberch", "Orta Saha", 83, "NL"),
            ("Harvey Elliott", "Orta Saha", 79, "EN"), ("Curtis Jones", "Orta Saha", 80, "EN"),
            ("Mohamed Salah", "Forvet", 92, "EG"), ("Darwin Núñez", "Forvet", 84, "UY"),
            ("Diogo Jota", "Forvet", 84, "PT"), ("Luis Díaz", "Forvet", 86, "CO"),
            ("Cody Gakpo", "Forvet", 83, "NL"),
        ]
    },
    "Chelsea": {
        "lig": "premier_league", "forma": "#034694",
        "oyuncular": [
            ("Robert Sánchez", "Kaleci", 82, "ES"), ("Filip Jørgensen", "Kaleci", 78, "DK"),
            ("Reece James", "Defans", 86, "EN"), ("Levi Colwill", "Defans", 82, "EN"),
            ("Wesley Fofana", "Defans", 82, "FR"), ("Ben Chilwell", "Defans", 81, "EN"),
            ("Malo Gusto", "Defans", 80, "FR"), ("Enzo Fernández", "Orta Saha", 87, "AR"),
            ("Moisés Caicedo", "Orta Saha", 86, "EC"), ("Conor Gallagher", "Orta Saha", 82, "EN"),
            ("Cole Palmer", "Orta Saha", 88, "EN"), ("Romeo Lavia", "Orta Saha", 80, "BE"),
            ("Nicolas Jackson", "Forvet", 82, "SN"), ("Christopher Nkunku", "Forvet", 85, "FR"),
            ("Mykhailo Mudryk", "Forvet", 82, "UA"), ("João Félix", "Forvet", 83, "PT"),
            ("Noni Madueke", "Forvet", 81, "EN"),
        ]
    },
    "Manchester United": {
        "lig": "premier_league", "forma": "#DA291C",
        "oyuncular": [
            ("André Onana", "Kaleci", 85, "CM"), ("Altay Bayındır", "Kaleci", 77, "TR"),
            ("Aaron Wan-Bissaka", "Defans", 80, "EN"), ("Harry Maguire", "Defans", 79, "EN"),
            ("Lisandro Martínez", "Defans", 84, "AR"), ("Luke Shaw", "Defans", 82, "EN"),
            ("Diogo Dalot", "Defans", 82, "PT"), ("Casemiro", "Orta Saha", 84, "BR"),
            ("Bruno Fernandes", "Orta Saha", 88, "PT"), ("Mason Mount", "Orta Saha", 81, "EN"),
            ("Kobbie Mainoo", "Orta Saha", 80, "EN"), ("Scott McTominay", "Orta Saha", 81, "SC"),
            ("Marcus Rashford", "Forvet", 84, "EN"), ("Rasmus Højlund", "Forvet", 82, "DK"),
            ("Antony", "Forvet", 79, "BR"), ("Alejandro Garnacho", "Forvet", 81, "AR"),
        ]
    },
    "Tottenham": {
        "lig": "premier_league", "forma": "#132257",
        "oyuncular": [
            ("Guglielmo Vicario", "Kaleci", 84, "IT"), ("Fraser Forster", "Kaleci", 75, "SC"),
            ("Pedro Porro", "Defans", 83, "ES"), ("Cristian Romero", "Defans", 86, "AR"),
            ("Micky van de Ven", "Defans", 84, "NL"), ("Destiny Udogie", "Defans", 82, "IT"),
            ("Ben Davies", "Defans", 79, "WA"), ("Rodrigo Bentancur", "Orta Saha", 82, "UY"),
            ("James Maddison", "Orta Saha", 85, "EN"), ("Yves Bissouma", "Orta Saha", 81, "ML"),
            ("Pape Matar Sarr", "Orta Saha", 79, "SN"), ("Son Heung-min", "Forvet", 88, "KR"),
            ("Dejan Kulusevski", "Forvet", 84, "SE"), ("Richarlison", "Forvet", 82, "BR"),
            ("Brennan Johnson", "Forvet", 80, "WA"), ("Timo Werner", "Forvet", 79, "DE"),
        ]
    },
    # ── La Liga ──
    "Real Madrid": {
        "lig": "la_liga", "forma": "#FEBE10",
        "oyuncular": [
            ("Thibaut Courtois", "Kaleci", 91, "BE"), ("Andriy Lunin", "Kaleci", 82, "UA"),
            ("Dani Carvajal", "Defans", 87, "ES"), ("Éder Militão", "Defans", 86, "BR"),
            ("Antonio Rüdiger", "Defans", 87, "DE"), ("Ferland Mendy", "Defans", 85, "FR"),
            ("David Alaba", "Defans", 85, "AT"), ("Nacho", "Defans", 80, "ES"),
            ("Luka Modrić", "Orta Saha", 88, "HR"), ("Toni Kroos", "Orta Saha", 89, "DE"),
            ("Aurélien Tchouaméni", "Orta Saha", 86, "FR"), ("Federico Valverde", "Orta Saha", 88, "UY"),
            ("Eduardo Camavinga", "Orta Saha", 85, "FR"), ("Jude Bellingham", "Orta Saha", 91, "EN"),
            ("Vinícius Jr.", "Forvet", 93, "BR"), ("Rodrygo", "Forvet", 87, "BR"),
            ("Joselu", "Forvet", 80, "ES"), ("Brahim Díaz", "Forvet", 82, "ES"),
        ]
    },
    "Barcelona": {
        "lig": "la_liga", "forma": "#A50044",
        "oyuncular": [
            ("Marc-André ter Stegen", "Kaleci", 90, "DE"), ("Iñaki Peña", "Kaleci", 76, "ES"),
            ("Jules Koundé", "Defans", 86, "FR"), ("Ronald Araújo", "Defans", 87, "UY"),
            ("Pau Cubarsí", "Defans", 81, "ES"), ("Alejandro Balde", "Defans", 83, "ES"),
            ("Iñigo Martínez", "Defans", 82, "ES"), ("Pedri", "Orta Saha", 90, "ES"),
            ("Gavi", "Orta Saha", 88, "ES"), ("Frenkie de Jong", "Orta Saha", 87, "NL"),
            ("Fermín López", "Orta Saha", 78, "ES"), ("Marc Casadó", "Orta Saha", 75, "ES"),
            ("Robert Lewandowski", "Forvet", 90, "PL"), ("Lamine Yamal", "Forvet", 87, "ES"),
            ("Raphinha", "Forvet", 86, "BR"), ("Ferran Torres", "Forvet", 81, "ES"),
            ("Vitor Roque", "Forvet", 77, "BR"),
        ]
    },
    "Atletico Madrid": {
        "lig": "la_liga", "forma": "#CB3524",
        "oyuncular": [
            ("Jan Oblak", "Kaleci", 91, "SI"), ("Antonio Grbić", "Kaleci", 72, "RS"),
            ("Nahuel Molina", "Defans", 83, "AR"), ("José María Giménez", "Defans", 85, "UY"),
            ("César Azpilicueta", "Defans", 79, "ES"), ("Reinildo Mandava", "Defans", 80, "MZ"),
            ("Axel Witsel", "Defans", 80, "BE"), ("Rodrigo De Paul", "Orta Saha", 84, "AR"),
            ("Koke", "Orta Saha", 82, "ES"), ("Thomas Lemar", "Orta Saha", 80, "FR"),
            ("Saúl Ñíguez", "Orta Saha", 79, "ES"), ("Pablo Barrios", "Orta Saha", 77, "ES"),
            ("Antoine Griezmann", "Forvet", 89, "FR"), ("Álvaro Morata", "Forvet", 83, "ES"),
            ("Memphis Depay", "Forvet", 81, "NL"), ("Samuel Lino", "Forvet", 79, "PT"),
        ]
    },
    "Sevilla": {
        "lig": "la_liga", "forma": "#D4AC0D",
        "oyuncular": [
            ("Ørjan Nyland", "Kaleci", 80, "NO"), ("Álvaro Fernández", "Kaleci", 74, "ES"),
            ("Jesús Navas", "Defans", 78, "ES"), ("Loïc Badé", "Defans", 82, "FR"),
            ("Marko Dmitrović", "Defans", 79, "RS"), ("Marcos Acuña", "Defans", 80, "AR"),
            ("Fernando", "Orta Saha", 79, "BR"), ("Ivan Rakitić", "Orta Saha", 80, "HR"),
            ("Adnan Januzaj", "Orta Saha", 77, "BE"), ("Suso", "Orta Saha", 78, "ES"),
            ("Lukáš Hrošovský", "Orta Saha", 76, "SK"), ("Youssef En-Nesyri", "Forvet", 82, "MA"),
            ("Lucas Ocampos", "Forvet", 82, "AR"), ("Rafa Mir", "Forvet", 78, "ES"),
            ("Dodi Lukebakio", "Forvet", 79, "BE"),
        ]
    },
    # ── Bundesliga ──
    "Bayern München": {
        "lig": "bundesliga", "forma": "#DC052D",
        "oyuncular": [
            ("Manuel Neuer", "Kaleci", 90, "DE"), ("Sven Ulreich", "Kaleci", 77, "DE"),
            ("Joshua Kimmich", "Defans", 89, "DE"), ("Dayot Upamecano", "Defans", 86, "FR"),
            ("Kim Min-jae", "Defans", 87, "KR"), ("Alphonso Davies", "Defans", 86, "CA"),
            ("Matthijs de Ligt", "Defans", 84, "NL"), ("Leon Goretzka", "Orta Saha", 85, "DE"),
            ("Thomas Müller", "Orta Saha", 86, "DE"), ("Aleksandar Pavlović", "Orta Saha", 78, "DE"),
            ("Konrad Laimer", "Orta Saha", 81, "AT"), ("Raphaël Guerreiro", "Orta Saha", 82, "PT"),
            ("Harry Kane", "Forvet", 92, "EN"), ("Leroy Sané", "Forvet", 88, "DE"),
            ("Serge Gnabry", "Forvet", 85, "DE"), ("Kingsley Coman", "Forvet", 86, "FR"),
            ("Mathys Tel", "Forvet", 78, "FR"),
        ]
    },
    "Borussia Dortmund": {
        "lig": "bundesliga", "forma": "#FDE100",
        "oyuncular": [
            ("Gregor Kobel", "Kaleci", 86, "CH"), ("Alexander Meyer", "Kaleci", 75, "DE"),
            ("Mats Hummels", "Defans", 84, "DE"), ("Nico Schlotterbeck", "Defans", 82, "DE"),
            ("Niklas Süle", "Defans", 82, "DE"), ("Ian Maatsen", "Defans", 80, "NL"),
            ("Julian Ryerson", "Defans", 78, "NO"), ("Emre Can", "Orta Saha", 82, "DE"),
            ("Marcel Sabitzer", "Orta Saha", 82, "AT"), ("Julien Duranville", "Orta Saha", 77, "BE"),
            ("Giovanni Reyna", "Orta Saha", 78, "US"), ("Felix Nmecha", "Orta Saha", 78, "DE"),
            ("Niclas Füllkrug", "Forvet", 83, "DE"), ("Karim Adeyemi", "Forvet", 81, "DE"),
            ("Donyell Malen", "Forvet", 83, "NL"), ("Jamie Gittens", "Forvet", 78, "EN"),
        ]
    },
    "Bayer Leverkusen": {
        "lig": "bundesliga", "forma": "#E32221",
        "oyuncular": [
            ("Lukáš Hrádecký", "Kaleci", 84, "FI"), ("Matěj Kovář", "Kaleci", 80, "CZ"),
            ("Jeremie Frimpong", "Defans", 83, "NL"), ("Jonathan Tah", "Defans", 84, "DE"),
            ("Granit Xhaka", "Orta Saha", 85, "CH"), ("Florian Wirtz", "Orta Saha", 90, "DE"),
            ("Robert Andrich", "Orta Saha", 82, "DE"), ("Exequiel Palacios", "Orta Saha", 81, "AR"),
            ("Alex Grimaldo", "Defans", 83, "ES"), ("Piero Hincapié", "Defans", 81, "EC"),
            ("Odilon Kossounou", "Defans", 80, "CI"), ("Edmond Tapsoba", "Defans", 80, "BF"),
            ("Victor Boniface", "Forvet", 83, "NG"), ("Jonas Hofmann", "Forvet", 81, "DE"),
            ("Amine Adli", "Forvet", 79, "FR"), ("Patrik Schick", "Forvet", 82, "CZ"),
        ]
    },
    # ── Serie A ──
    "Inter Milan": {
        "lig": "serie_a", "forma": "#010E80",
        "oyuncular": [
            ("Yann Sommer", "Kaleci", 87, "CH"), ("Josep Martínez", "Kaleci", 78, "ES"),
            ("Benjamin Pavard", "Defans", 85, "FR"), ("Francesco Acerbi", "Defans", 83, "IT"),
            ("Alessandro Bastoni", "Defans", 87, "IT"), ("Federico Dimarco", "Defans", 84, "IT"),
            ("Denzel Dumfries", "Defans", 83, "NL"), ("Nicolò Barella", "Orta Saha", 89, "IT"),
            ("Hakan Çalhanoğlu", "Orta Saha", 87, "TR"), ("Henrikh Mkhitaryan", "Orta Saha", 81, "AM"),
            ("Davide Frattesi", "Orta Saha", 82, "IT"), ("Kristjan Asllani", "Orta Saha", 78, "AL"),
            ("Lautaro Martínez", "Forvet", 90, "AR"), ("Marcus Thuram", "Forvet", 86, "FR"),
            ("Mehdi Taremi", "Forvet", 83, "IR"), ("Alexis Sánchez", "Forvet", 79, "CL"),
        ]
    },
    "AC Milan": {
        "lig": "serie_a", "forma": "#FB090B",
        "oyuncular": [
            ("Mike Maignan", "Kaleci", 89, "FR"), ("Marco Sportiello", "Kaleci", 76, "IT"),
            ("Davide Calabria", "Defans", 80, "IT"), ("Fikayo Tomori", "Defans", 83, "EN"),
            ("Malick Thiaw", "Defans", 81, "DE"), ("Theo Hernández", "Defans", 86, "FR"),
            ("Strahinja Pavlović", "Defans", 80, "RS"), ("Youssouf Fofana", "Orta Saha", 83, "FR"),
            ("Tijjani Reijnders", "Orta Saha", 84, "NL"), ("Ruben Loftus-Cheek", "Orta Saha", 82, "EN"),
            ("Yunus Musah", "Orta Saha", 78, "US"), ("Ismael Bennacer", "Orta Saha", 82, "DZ"),
            ("Rafael Leão", "Forvet", 88, "PT"), ("Christian Pulisic", "Forvet", 84, "US"),
            ("Olivier Giroud", "Forvet", 82, "FR"), ("Noah Okafor", "Forvet", 79, "CH"),
            ("Samuel Chukwueze", "Forvet", 80, "NG"),
        ]
    },
    "Juventus": {
        "lig": "serie_a", "forma": "#000000",
        "oyuncular": [
            ("Wojciech Szczęsny", "Kaleci", 87, "PL"), ("Carlo Pinsoglio", "Kaleci", 68, "IT"),
            ("Andrea Cambiaso", "Defans", 82, "IT"), ("Gleison Bremer", "Defans", 85, "BR"),
            ("Danilo", "Defans", 81, "BR"), ("Alex Sandro", "Defans", 78, "BR"),
            ("Federico Gatti", "Defans", 80, "IT"), ("Manuel Locatelli", "Orta Saha", 83, "IT"),
            ("Adrien Rabiot", "Orta Saha", 83, "FR"), ("Weston McKennie", "Orta Saha", 80, "US"),
            ("Nicolás González", "Orta Saha", 80, "AR"), ("Fabio Miretti", "Orta Saha", 76, "IT"),
            ("Dušan Vlahović", "Forvet", 87, "RS"), ("Federico Chiesa", "Forvet", 84, "IT"),
            ("Moise Kean", "Forvet", 79, "IT"), ("Timothy Weah", "Forvet", 79, "US"),
        ]
    },
    "Napoli": {
        "lig": "serie_a", "forma": "#12A0C3",
        "oyuncular": [
            ("Alex Meret", "Kaleci", 84, "IT"), ("Pierluigi Gollini", "Kaleci", 78, "IT"),
            ("Giovanni Di Lorenzo", "Defans", 84, "IT"), ("Amir Rrahmani", "Defans", 82, "KO"),
            ("Min-jae Kim", "Defans", 87, "KR"), ("Mathías Olivera", "Defans", 80, "UY"),
            ("Natan", "Defans", 77, "BR"), ("Stanislav Lobotka", "Orta Saha", 84, "SK"),
            ("Piotr Zieliński", "Orta Saha", 85, "PL"), ("Eljif Elmas", "Orta Saha", 81, "MK"),
            ("André-Frank Zambo Anguissa", "Orta Saha", 84, "CM"), ("Diego Demme", "Orta Saha", 77, "IT"),
            ("Victor Osimhen", "Forvet", 90, "NG"), ("Khvicha Kvaratskhelia", "Forvet", 88, "GE"),
            ("Matteo Politano", "Forvet", 81, "IT"), ("Giacomo Raspadori", "Forvet", 80, "IT"),
        ]
    },
    # ── Ligue 1 ──
    "Paris Saint-Germain": {
        "lig": "ligue_1", "forma": "#004170",
        "oyuncular": [
            ("Gianluigi Donnarumma", "Kaleci", 90, "IT"), ("Keylor Navas", "Kaleci", 83, "CR"),
            ("Achraf Hakimi", "Defans", 87, "MA"), ("Marquinhos", "Defans", 88, "BR"),
            ("Lucas Hernández", "Defans", 83, "FR"), ("Presnel Kimpembe", "Defans", 82, "FR"),
            ("Nuno Mendes", "Defans", 83, "PT"), ("Marco Verratti", "Orta Saha", 87, "IT"),
            ("Fabian Ruiz", "Orta Saha", 83, "ES"), ("Warren Zaïre-Emery", "Orta Saha", 80, "FR"),
            ("Vitinha", "Orta Saha", 84, "PT"), ("Gonçalo Ramos", "Forvet", 84, "PT"),
            ("Ousmane Dembélé", "Forvet", 87, "FR"), ("Bradley Barcola", "Forvet", 82, "FR"),
            ("Randal Kolo Muani", "Forvet", 83, "FR"), ("Lee Kang-in", "Forvet", 82, "KR"),
            ("Desire Doue", "Forvet", 79, "FR"),
        ]
    },
    "Olympique Marseille": {
        "lig": "ligue_1", "forma": "#2CBFEB",
        "oyuncular": [
            ("Pau López", "Kaleci", 83, "ES"), ("Ruben Blanco", "Kaleci", 79, "ES"),
            ("Jonathan Clauss", "Defans", 82, "FR"), ("Samuel Gigot", "Defans", 79, "FR"),
            ("Chancel Mbemba", "Defans", 81, "CD"), ("Azzedine Ounahi", "Orta Saha", 80, "MA"),
            ("Geoffrey Kondogbia", "Orta Saha", 81, "CF"), ("Valentin Rongier", "Orta Saha", 79, "FR"),
            ("Jordan Veretout", "Orta Saha", 79, "FR"), ("Iliman Ndiaye", "Orta Saha", 78, "SN"),
            ("Pierre-Emerick Aubameyang", "Forvet", 83, "GA"), ("Vitinha", "Forvet", 78, "PT"),
            ("Ismaila Sarr", "Forvet", 80, "SN"), ("Alexis Sánchez", "Forvet", 80, "CL"),
        ]
    },
    "Monaco": {
        "lig": "ligue_1", "forma": "#CE1A26",
        "oyuncular": [
            ("Radosław Majecki", "Kaleci", 79, "PL"), ("Philipp Köhn", "Kaleci", 76, "DE"),
            ("Vanderson", "Defans", 79, "BR"), ("Axel Disasi", "Defans", 81, "FR"),
            ("Youssouf Fofana", "Orta Saha", 83, "FR"), ("Denis Zakaria", "Orta Saha", 81, "CH"),
            ("Aleksandr Golovin", "Orta Saha", 81, "RU"), ("Caio Henrique", "Defans", 79, "BR"),
            ("Mohamed Camara", "Orta Saha", 80, "GN"), ("Eliesse Ben Seghir", "Forvet", 78, "FR"),
            ("Wissam Ben Yedder", "Forvet", 82, "FR"), ("Takumi Minamino", "Forvet", 81, "JP"),
            ("Maghnes Akliouche", "Forvet", 77, "FR"), ("Folarin Balogun", "Forvet", 80, "US"),
        ]
    },
    # ── Süper Lig ──
    "Galatasaray": {
        "lig": "super_lig", "forma": "#F02D04",
        "oyuncular": [
            ("Fernando Muslera", "Kaleci", 83, "UY"), ("Inaki Peña", "Kaleci", 75, "ES"),
            ("Sacha Boey", "Defans", 79, "FR"), ("Davinson Sánchez", "Defans", 82, "CO"),
            ("Victor Nelsson", "Defans", 80, "DK"), ("Patrick van Aanholt", "Defans", 77, "NL"),
            ("Abdülkerim Bardakcı", "Defans", 78, "TR"), ("Dries Mertens", "Orta Saha", 82, "BE"),
            ("Lucas Torreira", "Orta Saha", 82, "UY"), ("Kerem Aktürkoğlu", "Forvet", 80, "TR"),
            ("Yunus Akgün", "Forvet", 76, "TR"), ("Bafétimbi Gomis", "Forvet", 77, "FR"),
            ("Mauro Icardi", "Forvet", 83, "AR"), ("Sérgio Oliveira", "Orta Saha", 79, "PT"),
            ("Milot Rashica", "Forvet", 78, "KO"), ("Hakim Ziyech", "Forvet", 83, "MA"),
            ("Wilfried Zaha", "Forvet", 81, "CI"), ("Barış Alper Yılmaz", "Forvet", 79, "TR"),
        ]
    },
    "Fenerbahçe": {
        "lig": "super_lig", "forma": "#002F5F",
        "oyuncular": [
            ("Altay Bayındır", "Kaleci", 77, "TR"), ("İrfan Can Eğribayat", "Kaleci", 75, "TR"),
            ("Bright Osayi-Samuel", "Defans", 78, "NG"), ("Attila Szalai", "Defans", 80, "HU"),
            ("Alexander Djiku", "Defans", 81, "GH"), ("Ferdi Kadıoğlu", "Defans", 81, "TR"),
            ("Enner Valencia", "Forvet", 79, "EC"), ("Miha Zajc", "Orta Saha", 78, "SI"),
            ("İsmail Yüksek", "Orta Saha", 76, "TR"), ("Sebastian Szymański", "Orta Saha", 81, "PL"),
            ("Fred", "Orta Saha", 81, "BR"), ("Dusan Tadic", "Forvet", 82, "RS"),
            ("Cengiz Ünder", "Forvet", 80, "TR"), ("Edin Džeko", "Forvet", 82, "BA"),
            ("Michy Batshuayi", "Forvet", 80, "BE"), ("Irfan Can Kahveci", "Orta Saha", 78, "TR"),
        ]
    },
    "Beşiktaş": {
        "lig": "super_lig", "forma": "#000000",
        "oyuncular": [
            ("Ersin Destanoğlu", "Kaleci", 79, "TR"), ("Mert Günok", "Kaleci", 77, "TR"),
            ("Valentin Rosier", "Defans", 78, "FR"), ("João Mário", "Defans", 78, "PT"),
            ("Domagoj Vida", "Defans", 79, "HR"), ("Josef de Souza", "Orta Saha", 79, "BR"),
            ("Salih Uçan", "Orta Saha", 75, "TR"), ("Ernest Muçi", "Forvet", 77, "AL"),
            ("Milot Rashica", "Forvet", 77, "KO"), ("Arthur Masuaku", "Defans", 77, "CD"),
            ("Can Bozdoğan", "Orta Saha", 74, "DE"), ("Dele Alli", "Orta Saha", 77, "EN"),
            ("Alex Oxlade-Chamberlain", "Orta Saha", 78, "EN"), ("Wout Weghorst", "Forvet", 81, "NL"),
            ("Rachid Ghezzal", "Forvet", 79, "DZ"), ("Umut Meraş", "Defans", 75, "TR"),
        ]
    },
    "Trabzonspor": {
        "lig": "super_lig", "forma": "#7A0035",
        "oyuncular": [
            ("Uğurcan Çakır", "Kaleci", 81, "TR"), ("Matthäus Jöst", "Kaleci", 71, "DE"),
            ("Ahmetcan Kaplan", "Defans", 77, "TR"), ("Marc Bartra", "Defans", 80, "ES"),
            ("Paulo Vinicius", "Defans", 78, "BR"), ("Dorukhan Toköz", "Orta Saha", 76, "TR"),
            ("Stefano Denswil", "Defans", 76, "NL"), ("Enis Destan", "Forvet", 74, "TR"),
            ("Fountas", "Forvet", 78, "GR"), ("Andreas Cornelius", "Forvet", 80, "DK"),
            ("Berat Özdemir", "Orta Saha", 74, "TR"), ("Erce Kardeşler", "Orta Saha", 73, "TR"),
            ("Edin Višća", "Forvet", 79, "BA"), ("Stefano Denswil", "Defans", 75, "NL"),
            ("Trezeguet", "Forvet", 79, "EG"),
        ]
    },
    # ── Eredivisie ──
    "Ajax": {
        "lig": "eredivisie", "forma": "#CC0000",
        "oyuncular": [
            ("Remko Pasveer", "Kaleci", 81, "NL"), ("Jay Gorter", "Kaleci", 74, "NL"),
            ("Devyne Rensch", "Defans", 79, "NL"), ("Jorrel Hato", "Defans", 79, "NL"),
            ("Ahmethan Kökcü", "Orta Saha", 78, "TR"), ("Steven Berghuis", "Forvet", 81, "NL"),
            ("Davy Klaassen", "Orta Saha", 79, "NL"), ("Jordan Henderson", "Orta Saha", 82, "EN"),
            ("Chuba Akpom", "Forvet", 79, "EN"), ("Sivert Mannsverk", "Orta Saha", 76, "NO"),
            ("Benjamin Tahirovic", "Orta Saha", 76, "SE"), ("Branco van den Boomen", "Orta Saha", 78, "NL"),
            ("Wout Weghorst", "Forvet", 81, "NL"), ("Bertrand Traoré", "Forvet", 78, "BF"),
            ("Carlos Forbs", "Forvet", 76, "PT"),
        ]
    },
    "PSV Eindhoven": {
        "lig": "eredivisie", "forma": "#CC0000",
        "oyuncular": [
            ("Walter Benítez", "Kaleci", 83, "AR"), ("Joël Drommel", "Kaleci", 76, "NL"),
            ("Jordan Teze", "Defans", 80, "NL"), ("Olivier Boscagli", "Defans", 81, "FR"),
            ("Armando Obispo", "Defans", 79, "NL"), ("Philipp Mwene", "Defans", 76, "AT"),
            ("Joey Veerman", "Orta Saha", 82, "NL"), ("Ibrahim Sangaré", "Orta Saha", 83, "CI"),
            ("Xavi Simons", "Orta Saha", 83, "NL"), ("Hirving Lozano", "Forvet", 83, "MX"),
            ("Cody Gakpo", "Forvet", 84, "NL"), ("Luuk de Jong", "Forvet", 80, "NL"),
            ("Noa Lang", "Forvet", 81, "NL"), ("Ricardo Pepi", "Forvet", 79, "US"),
        ]
    },
    # ── Primeira Liga ──
    "Benfica": {
        "lig": "primeira_liga", "forma": "#C41B17",
        "oyuncular": [
            ("Odysseas Vlachodimos", "Kaleci", 84, "GR"), ("Samuel Soares", "Kaleci", 72, "PT"),
            ("Gilberto", "Defans", 79, "BR"), ("António Silva", "Defans", 82, "PT"),
            ("Otamendi", "Defans", 84, "AR"), ("Grimaldo", "Defans", 83, "ES"),
            ("Fredrik Aursnes", "Orta Saha", 80, "NO"), ("Florentino Luís", "Orta Saha", 79, "PT"),
            ("Joăo Neves", "Orta Saha", 81, "PT"), ("Orkun Kökcü", "Orta Saha", 81, "TR"),
            ("Ángel Di María", "Forvet", 85, "AR"), ("Rafa Silva", "Forvet", 82, "PT"),
            ("Petar Musa", "Forvet", 80, "HR"), ("Arthur Cabral", "Forvet", 79, "BR"),
            ("Marcos Leonardo", "Forvet", 78, "BR"),
        ]
    },
    "FC Porto": {
        "lig": "primeira_liga", "forma": "#003087",
        "oyuncular": [
            ("Diogo Costa", "Kaleci", 85, "PT"), ("Claudio Ramos", "Kaleci", 75, "PT"),
            ("João Mário", "Defans", 78, "PT"), ("Chancel Mbemba", "Defans", 81, "CD"),
            ("Pepe", "Defans", 82, "PT"), ("Zaidu Sanusi", "Defans", 79, "NG"),
            ("Pepê", "Forvet", 80, "BR"), ("Otávio", "Orta Saha", 82, "PT"),
            ("Evanilson", "Forvet", 81, "BR"), ("Mehdi Taremi", "Forvet", 83, "IR"),
            ("Stephen Eustáquio", "Orta Saha", 80, "CA"), ("Wendell", "Defans", 78, "BR"),
            ("Iván Marcano", "Defans", 77, "ES"), ("Galeno", "Forvet", 80, "BR"),
            ("Toni Martínez", "Forvet", 78, "ES"),
        ]
    },
    # ── MLS ──
    "Inter Miami": {
        "lig": "mls", "forma": "#F7B5CD",
        "oyuncular": [
            ("Drake Callender", "Kaleci", 76, "US"), ("Nick Marsman", "Kaleci", 74, "NL"),
            ("DeAndre Yedlin", "Defans", 78, "US"), ("Sergio Busquets", "Orta Saha", 84, "ES"),
            ("Jordi Alba", "Defans", 82, "ES"), ("Gerard Piqué", "Defans", 80, "ES"),
            ("Lionel Messi", "Forvet", 94, "AR"), ("Gonzalo Higuain", "Forvet", 80, "AR"),
            ("Benjamin Cremaschi", "Orta Saha", 73, "US"), ("Robert Taylor", "Forvet", 72, "FI"),
            ("Leonardo Campana", "Forvet", 74, "EC"), ("Tomás Avilés", "Defans", 74, "AR"),
            ("Facundo Farías", "Forvet", 76, "AR"), ("David Ruiz", "Orta Saha", 73, "MX"),
            ("Luis Suárez", "Forvet", 83, "UY"), ("Riqui Puig", "Orta Saha", 79, "ES"),
        ]
    },
    "LA Galaxy": {
        "lig": "mls", "forma": "#00245D",
        "oyuncular": [
            ("John McCarthy", "Kaleci", 74, "US"), ("Jonathan Bond", "Kaleci", 73, "EN"),
            ("John Nelson", "Defans", 72, "US"), ("Raheem Edwards", "Defans", 71, "CA"),
            ("Emiro Garces", "Defans", 70, "CO"), ("Mark Delgado", "Orta Saha", 72, "US"),
            ("Riqui Puig", "Orta Saha", 79, "ES"), ("Dejan Joveljić", "Forvet", 74, "RS"),
            ("Gabriel Pec", "Forvet", 75, "BR"), ("Javier "Chicharito" Hernandez", "Forvet", 78, "MX"),
            ("Julian Araujo", "Defans", 75, "US"), ("Kellyn Acosta", "Orta Saha", 74, "US"),
            ("Marco Reus", "Orta Saha", 83, "DE"), ("Miki Yamane", "Defans", 73, "JP"),
            ("Gastón Brugman", "Orta Saha", 72, "UY"),
        ]
    },
    # ── Brasileirão ──
    "Flamengo": {
        "lig": "brasileiro", "forma": "#CC0000",
        "oyuncular": [
            ("Santos", "Kaleci", 80, "BR"), ("Agustín Rossi", "Kaleci", 79, "AR"),
            ("Rodrigo Caio", "Defans", 79, "BR"), ("Léo Pereira", "Defans", 81, "BR"),
            ("Filipe Luís", "Defans", 80, "BR"), ("Guillermo Varela", "Defans", 78, "UY"),
            ("Gerson", "Orta Saha", 82, "BR"), ("Thiago Maia", "Orta Saha", 79, "BR"),
            ("De Arrascaeta", "Orta Saha", 85, "UY"), ("Everton Ribeiro", "Orta Saha", 82, "BR"),
            ("Gabriel Barbosa (Gabigol)", "Forvet", 85, "BR"), ("Pedro", "Forvet", 83, "BR"),
            ("Michael", "Forvet", 79, "BR"), ("Everton Cebolinha", "Forvet", 80, "BR"),
            ("Bruno Henrique", "Forvet", 80, "BR"), ("Vidal", "Orta Saha", 80, "CL"),
        ]
    },
    "Palmeiras": {
        "lig": "brasileiro", "forma": "#006437",
        "oyuncular": [
            ("Weverton", "Kaleci", 84, "BR"), ("Marcelo Lomba", "Kaleci", 77, "BR"),
            ("Marcos Rocha", "Defans", 79, "BR"), ("Gustavo Gómez", "Defans", 83, "PY"),
            ("Murilo", "Defans", 81, "BR"), ("Piquerez", "Defans", 80, "UY"),
            ("Gabriel Menino", "Orta Saha", 80, "BR"), ("Danilo", "Orta Saha", 81, "BR"),
            ("Zé Rafael", "Orta Saha", 80, "BR"), ("Raphael Veiga", "Orta Saha", 83, "BR"),
            ("Endrick", "Forvet", 80, "BR"), ("Rony", "Forvet", 80, "BR"),
            ("Dudu", "Forvet", 82, "BR"), ("Luis Guilherme", "Forvet", 78, "BR"),
            ("Flaco López", "Forvet", 79, "AR"),
        ]
    },
}

TAKTIKLER = {
    "4-3-3":  (1.15, 0.90, "⚡ Agresif hücum"),
    "4-4-2":  (1.00, 1.00, "⚖️ Dengeli"),
    "5-3-2":  (0.88, 1.18, "🛡️ Güçlü defans"),
    "3-5-2":  (1.08, 1.05, "🎯 Orta saha hâkimiyeti"),
    "4-2-3-1":(1.05, 1.05, "🔄 Modern denge"),
}

BASARILAR = {
    "ilk_mac":       ("⚽ İlk Adım",        "İlk maçını oynadın!"),
    "5_galibiyet":   ("🏆 Çaylak Koç",      "5 galibiyet aldın!"),
    "10_galibiyet":  ("🔥 Deneyimli Koç",   "10 galibiyet aldın!"),
    "25_galibiyet":  ("👑 Efsane Koç",      "25 galibiyet aldın!"),
    "golcu_10":      ("⚡ Golcü Kral",       "Bir oyuncun 10 gol attı!"),
    "transfer_5":    ("🛒 Transfer Ustası",  "5 oyuncu transfer ettin!"),
    "sezon_sampiyon":("🥇 Şampiyon",        "Sezonu şampiyon bitirdin!"),
    "kupa_sampiyon": ("🏅 Kupa Şampiyonu",  "Kupayı kazandın!"),
    "spin_5":        ("🎰 Şans Çarkı",      "Çarkı 5 kez çevirdin!"),
    "altyapi":       ("🌱 Altyapı Yöneticisi","Altyapıdan ilk oyuncunu çıkardın!"),
}

SPIN_ODULLER = [
    ("💰 2.000₺",  "para",  2000,  30),
    ("💰 5.000₺",  "para",  5000,  25),
    ("💰 10.000₺", "para",  10000, 15),
    ("💰 20.000₺", "para",  20000, 8),
    ("⭐ 50 XP",   "xp",    50,    20),
    ("⭐ 100 XP",  "xp",    100,   12),
    ("🏋️ +3 Güç", "guc",   3,     8),
    ("🍀 500₺",   "para",  500,   40),
    ("💎 50.000₺", "para",  50000, 2),
]

BASLANGIC_PARASI = 500_000

POZ_ULKE = {
    "TR": "🇹🇷", "BR": "🇧🇷", "ES": "🇪🇸", "FR": "🇫🇷", "DE": "🇩🇪",
    "AR": "🇦🇷", "PT": "🇵🇹", "EN": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "IT": "🇮🇹", "NL": "🇳🇱",
    "BE": "🇧🇪", "CH": "🇨🇭", "HR": "🇭🇷", "UA": "🇺🇦", "NO": "🇳🇴",
    "KR": "🇰🇷", "CM": "🇨🇲", "SC": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "HU": "🇭🇺", "DK": "🇩🇰",
    "GH": "🇬🇭", "NG": "🇳🇬", "MA": "🇲🇦", "SN": "🇸🇳", "CO": "🇨🇴",
    "EG": "🇪🇬", "UY": "🇺🇾", "AT": "🇦🇹", "CA": "🇨🇦", "JP": "🇯🇵",
    "GE": "🇬🇪", "PL": "🇵🇱", "AM": "🇦🇲", "IR": "🇮🇷", "CL": "🇨🇱",
    "SI": "🇸🇮", "SK": "🇸🇰", "AL": "🇦🇱", "KO": "🇽🇰", "BA": "🇧🇦",
    "FI": "🇫🇮", "CZ": "🇨🇿", "EC": "🇪🇨", "RS": "🇷🇸", "CI": "🇨🇮",
    "US": "🇺🇸", "MX": "🇲🇽", "CD": "🇨🇩", "CF": "🇨🇫", "BF": "🇧🇫",
    "MZ": "🇲🇿", "GN": "🇬🇳", "PY": "🇵🇾", "MK": "🇲🇰", "ML": "🇲🇱",
    "DZ": "🇩🇿", "GA": "🇬🇦", "GR": "🇬🇷", "WA": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "SE": "🇸🇪",
    "IE": "🇮🇪", "EE": "🇪🇪", "RU": "🇷🇺", "MT": "🇲🇹", "CG": "🇨🇬",
}


class FutbolDB:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()
        self._gercek_ligler_yukle()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self):
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS futbol_para (
                    user_id INTEGER PRIMARY KEY,
                    para    INTEGER DEFAULT 500000
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS takimlar (
                    takim_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id          INTEGER,
                    isim             TEXT UNIQUE,
                    lig_kodu         TEXT DEFAULT 'premier_league',
                    puan             INTEGER DEFAULT 0,
                    galibiyet        INTEGER DEFAULT 0,
                    beraberlik       INTEGER DEFAULT 0,
                    maglubiyet       INTEGER DEFAULT 0,
                    atilan_gol       INTEGER DEFAULT 0,
                    yenilen_gol      INTEGER DEFAULT 0,
                    mac_sayisi       INTEGER DEFAULT 0,
                    son_mac          TEXT,
                    olusturma_tarihi TEXT,
                    taktik           TEXT DEFAULT '4-4-2',
                    sezon            INTEGER DEFAULT 1,
                    bot_takim        INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS oyuncular (
                    oyuncu_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    takim_id         INTEGER,
                    isim             TEXT,
                    pozisyon         TEXT,
                    guc              INTEGER,
                    deger            INTEGER,
                    ulke             TEXT DEFAULT 'TR',
                    antrenman_tarihi TEXT,
                    satista          INTEGER DEFAULT 0,
                    satis_fiyati     INTEGER DEFAULT 0,
                    gol              INTEGER DEFAULT 0,
                    asist            INTEGER DEFAULT 0,
                    sari_kart        INTEGER DEFAULT 0,
                    kirmizi_kart     INTEGER DEFAULT 0,
                    sakatlik_bitis   TEXT DEFAULT NULL,
                    genc             INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fikstur (
                    mac_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    ev_takim_id    INTEGER,
                    dep_takim_id   INTEGER,
                    hafta          INTEGER,
                    lig_kodu       TEXT DEFAULT 'premier_league',
                    oynanma_tarihi TEXT,
                    ev_gol         INTEGER,
                    dep_gol        INTEGER,
                    oynanmis       INTEGER DEFAULT 0,
                    sezon          INTEGER DEFAULT 1
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lig_durumu (
                    lig_kodu TEXT PRIMARY KEY,
                    aktif    INTEGER DEFAULT 0,
                    sezon    INTEGER DEFAULT 1,
                    baslangic_tarihi TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spin_kaydi (
                    user_id    INTEGER PRIMARY KEY,
                    son_spin   TEXT,
                    toplam     INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS basarilar (
                    user_id     INTEGER,
                    basari_kodu TEXT,
                    tarih       TEXT,
                    PRIMARY KEY (user_id, basari_kodu)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS grup_chatler (
                    chat_id INTEGER PRIMARY KEY
                )
            """)
            # ulke kolonu yoksa ekle
            try:
                conn.execute("ALTER TABLE oyuncular ADD COLUMN ulke TEXT DEFAULT 'TR'")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE oyuncular ADD COLUMN lig_kodu TEXT DEFAULT 'premier_league'")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE takimlar ADD COLUMN bot_takim INTEGER DEFAULT 0")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE takimlar ADD COLUMN lig_kodu TEXT DEFAULT 'premier_league'")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE fikstur ADD COLUMN lig_kodu TEXT DEFAULT 'premier_league'")
            except Exception:
                pass
            conn.commit()

    def _deger_hesapla(self, guc: int) -> int:
        if guc >= 90:
            return random.randint(5_000_000, 15_000_000)
        elif guc >= 85:
            return random.randint(2_000_000, 5_000_000)
        elif guc >= 80:
            return random.randint(800_000, 2_000_000)
        elif guc >= 75:
            return random.randint(300_000, 800_000)
        elif guc >= 70:
            return random.randint(100_000, 300_000)
        else:
            return random.randint(30_000, 100_000)

    def _gercek_ligler_yukle(self):
        """Her lig için gerçek takımları ve oyuncuları yükle (zaten varsa skip)"""
        with self._conn() as conn:
            for takim_adi, veri in GERCEK_TAKIMLAR.items():
                lig_kodu = veri["lig"]
                mevcut = conn.execute(
                    "SELECT takim_id FROM takimlar WHERE isim=?", (takim_adi,)
                ).fetchone()
                if mevcut:
                    continue
                conn.execute("""
                    INSERT INTO takimlar (isim, lig_kodu, bot_takim, olusturma_tarihi, taktik)
                    VALUES (?, ?, 1, ?, '4-4-2')
                """, (takim_adi, lig_kodu, date.today().isoformat()))
                conn.commit()
                takim_row = conn.execute(
                    "SELECT takim_id FROM takimlar WHERE isim=?", (takim_adi,)
                ).fetchone()
                takim_id = takim_row["takim_id"]
                for (isim, poz, guc, ulke) in veri["oyuncular"]:
                    deger = self._deger_hesapla(guc)
                    conn.execute("""
                        INSERT INTO oyuncular (takim_id, isim, pozisyon, guc, deger, ulke, satista, satis_fiyati)
                        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
                    """, (takim_id, isim, poz, guc, deger, ulke, deger))
                conn.commit()

    # ─── Para ────────────────────────────────────────────────────────────

    def para_getir(self, user_id: int) -> int:
        with self._conn() as conn:
            r = conn.execute("SELECT para FROM futbol_para WHERE user_id=?", (user_id,)).fetchone()
            if not r:
                conn.execute("INSERT INTO futbol_para VALUES (?,?)", (user_id, BASLANGIC_PARASI))
                conn.commit()
                return BASLANGIC_PARASI
            return r["para"]

    def para_guncelle(self, user_id: int, miktar: int):
        self.para_getir(user_id)
        with self._conn() as conn:
            conn.execute("UPDATE futbol_para SET para=para+? WHERE user_id=?", (miktar, user_id))
            conn.commit()

    # ─── Lig ─────────────────────────────────────────────────────────────

    def lig_listesi(self) -> list:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM lig_durumu ORDER BY lig_kodu").fetchall()
            return [dict(r) for r in rows]

    def lig_aktif_mi(self, lig_kodu: str) -> bool:
        with self._conn() as conn:
            r = conn.execute("SELECT aktif FROM lig_durumu WHERE lig_kodu=?", (lig_kodu,)).fetchone()
            return bool(r and r["aktif"])

    def lig_baslat(self, lig_kodu: str) -> tuple:
        """Admin bir ligi başlatır — fikstür oluşturulur, otomatik maçlar planlanır"""
        if lig_kodu not in LIGLER:
            return False, "Geçersiz lig kodu."
        if self.lig_aktif_mi(lig_kodu):
            return False, f"{LIGLER[lig_kodu]['ad']} zaten aktif!"
        with self._conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO lig_durumu (lig_kodu, aktif, sezon, baslangic_tarihi)
                VALUES (?, 1, 1, ?)
            """, (lig_kodu, date.today().isoformat()))
            conn.commit()
        ok = self._fikstur_olustur_lig(lig_kodu)
        if ok:
            lig_adi = LIGLER[lig_kodu]["ad"]
            takim_sayisi = len([t for t in GERCEK_TAKIMLAR.values() if t["lig"] == lig_kodu])
            return True, f"✅ {lig_adi} başlatıldı! {takim_sayisi} takım, fikstür hazır."
        return False, "Fikstür oluşturulamadı."

    def _fikstur_olustur_lig(self, lig_kodu: str, sezon: int = 1) -> bool:
        takimlar = self.lig_takimlari(lig_kodu)
        if len(takimlar) < 2:
            return False
        ids = [t["takim_id"] for t in takimlar]
        if len(ids) % 2 == 1:
            ids.append(None)
        n = len(ids)
        tum_maclar = []
        ids_rot = ids[1:]
        for tur in range(n - 1):
            hafta = tur + 1
            eslesmeler = [(ids[0], ids_rot[0])]
            for i in range(1, n // 2):
                eslesmeler.append((ids_rot[-i], ids_rot[i]))
            for ev, dep in eslesmeler:
                if ev and dep:
                    tum_maclar.append((ev, dep, hafta))
            ids_rot = [ids_rot[-1]] + ids_rot[:-1]
        toplam = n - 1
        for ev, dep, hafta in list(tum_maclar):
            tum_maclar.append((dep, ev, hafta + toplam))
        with self._conn() as conn:
            conn.execute("DELETE FROM fikstur WHERE lig_kodu=? AND sezon=?", (lig_kodu, sezon))
            for ev, dep, hafta in tum_maclar:
                conn.execute("""
                    INSERT INTO fikstur (ev_takim_id, dep_takim_id, hafta, lig_kodu, oynanmis, sezon)
                    VALUES (?, ?, ?, ?, 0, ?)
                """, (ev, dep, hafta, lig_kodu, sezon))
            conn.commit()
        return True

    def lig_takimlari(self, lig_kodu: str) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM takimlar WHERE lig_kodu=? ORDER BY puan DESC, (atilan_gol-yenilen_gol) DESC",
                (lig_kodu,)
            ).fetchall()
            return [dict(r) for r in rows]

    def tum_aktif_ligler(self) -> list:
        with self._conn() as conn:
            rows = conn.execute("SELECT lig_kodu FROM lig_durumu WHERE aktif=1").fetchall()
            return [r["lig_kodu"] for r in rows]

    # ─── Takım ───────────────────────────────────────────────────────────

    def takim_user(self, user_id: int) -> Optional[dict]:
        with self._conn() as conn:
            r = conn.execute("SELECT * FROM takimlar WHERE user_id=?", (user_id,)).fetchone()
            return dict(r) if r else None

    def takim_id(self, takim_id: int) -> Optional[dict]:
        with self._conn() as conn:
            r = conn.execute("SELECT * FROM takimlar WHERE takim_id=?", (takim_id,)).fetchone()
            return dict(r) if r else None

    def kullanici_takim_sec(self, user_id: int, takim_adi: str) -> tuple:
        """Kullanıcı mevcut bir gerçek takımı sahiplenebilir"""
        mevcut = self.takim_user(user_id)
        if mevcut:
            return False, f"Zaten '{mevcut['isim']}' takımına sahipsin."
        with self._conn() as conn:
            t = conn.execute(
                "SELECT * FROM takimlar WHERE isim=? AND (user_id IS NULL OR user_id=0)",
                (takim_adi,)
            ).fetchone()
            if not t:
                return False, "Bu takım bulunamadı veya zaten sahip var."
            conn.execute("UPDATE takimlar SET user_id=? WHERE takim_id=?", (user_id, t["takim_id"]))
            conn.commit()
        if not self.para_getir(user_id):
            self.para_guncelle(user_id, 0)
        return True, dict(t)

    def takim_oyunculari(self, takim_id: int) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM oyuncular WHERE takim_id=? ORDER BY guc DESC",
                (takim_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def takim_gucu(self, takim_id: int, taktik: str = "4-4-2") -> float:
        oyuncular = self.takim_oyunculari(takim_id)
        if not oyuncular:
            return 50.0
        bugun = date.today().isoformat()
        aktif = [o for o in oyuncular
                 if not o.get("sakatlik_bitis") or o["sakatlik_bitis"] <= bugun]
        if not aktif:
            aktif = oyuncular
        gucler = sorted([o["guc"] for o in aktif], reverse=True)
        en_iyi = gucler[:11]
        taban = sum(en_iyi) / len(en_iyi)
        h, d, _ = TAKTIKLER.get(taktik, (1.0, 1.0, ""))
        return taban * ((h + d) / 2)

    def taktik_sec(self, takim_id: int, taktik: str) -> bool:
        if taktik not in TAKTIKLER:
            return False
        with self._conn() as conn:
            conn.execute("UPDATE takimlar SET taktik=? WHERE takim_id=?", (taktik, takim_id))
            conn.commit()
        return True

    def sakatlanan_oyuncular(self, takim_id: int) -> list:
        bugun = date.today().isoformat()
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM oyuncular WHERE takim_id=? AND sakatlik_bitis > ?",
                (takim_id, bugun)
            ).fetchall()
            return [dict(r) for r in rows]

    # ─── Otomatik Maç Sistemi ─────────────────────────────────────────────

    def oynanacak_maclar(self, lig_kodu: str) -> list:
        """Ligdeki oynanmamış maçları döndür"""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM fikstur WHERE lig_kodu=? AND oynanmis=0 ORDER BY hafta ASC",
                (lig_kodu,)
            ).fetchall()
            return [dict(r) for r in rows]

    def bu_haftanin_maclari(self, lig_kodu: str) -> list:
        """Bu haftanın oynanmamış maçları"""
        with self._conn() as conn:
            min_hafta = conn.execute(
                "SELECT MIN(hafta) FROM fikstur WHERE lig_kodu=? AND oynanmis=0",
                (lig_kodu,)
            ).fetchone()[0]
            if not min_hafta:
                return []
            rows = conn.execute(
                "SELECT * FROM fikstur WHERE lig_kodu=? AND hafta=? AND oynanmis=0",
                (lig_kodu, min_hafta)
            ).fetchall()
            return [dict(r) for r in rows]

    def hafta_oyna(self, lig_kodu: str) -> list:
        """Bir haftanın tüm maçlarını otomatik oyna, sonuçları döndür"""
        maclar = self.bu_haftanin_maclari(lig_kodu)
        sonuclar = []
        for mac in maclar:
            sonuc, hata = self._mac_simule_et(mac["mac_id"])
            if sonuc:
                sonuclar.append(sonuc)
        return sonuclar

    def _mac_simule_et(self, mac_id: int):
        """Tek bir maçı simüle eder (bot vs bot dahil)"""
        with self._conn() as conn:
            r = conn.execute("SELECT * FROM fikstur WHERE mac_id=?", (mac_id,)).fetchone()
            if not r:
                return None, "Maç bulunamadı."
            mac = dict(r)
        if mac["oynanmis"]:
            return None, "Bu maç zaten oynandı."

        ev_t = self.takim_id(mac["ev_takim_id"])
        dep_t = self.takim_id(mac["dep_takim_id"])
        if not ev_t or not dep_t:
            return None, "Takım bulunamadı."

        ev_taktik = ev_t.get("taktik", "4-4-2")
        dep_taktik = dep_t.get("taktik", "4-4-2")

        # Bot takımlar için rastgele taktik
        if ev_t.get("bot_takim"):
            ev_taktik = random.choice(list(TAKTIKLER.keys()))
        if dep_t.get("bot_takim"):
            dep_taktik = random.choice(list(TAKTIKLER.keys()))

        ev_h, ev_d, _ = TAKTIKLER.get(ev_taktik, (1.0, 1.0, ""))
        dep_h, dep_d, _ = TAKTIKLER.get(dep_taktik, (1.0, 1.0, ""))
        ev_guc_ham = self.takim_gucu(mac["ev_takim_id"], ev_taktik)
        dep_guc_ham = self.takim_gucu(mac["dep_takim_id"], dep_taktik)
        ev_guc_adj = ev_guc_ham * 1.08 * ev_h / dep_d
        dep_guc_adj = dep_guc_ham * dep_h / ev_d
        toplam = ev_guc_adj + dep_guc_adj
        ev_oran = ev_guc_adj / toplam if toplam else 0.5
        ev_gol = max(0, min(9, round(random.gauss(ev_oran * 3.2, 1.1))))
        dep_gol = max(0, min(9, round(random.gauss((1 - ev_oran) * 3.2, 1.1))))

        ev_oyuncular = self.takim_oyunculari(mac["ev_takim_id"])
        dep_oyuncular = self.takim_oyunculari(mac["dep_takim_id"])
        olaylar = []

        def gol_atan(oyuncular, sayi):
            forvetler = [o for o in oyuncular if o["pozisyon"] in ("Forvet", "Orta Saha")]
            havuz = forvetler if forvetler else oyuncular
            atanlar = []
            with self._conn() as c:
                for _ in range(sayi):
                    if not havuz:
                        break
                    golcu = random.choice(havuz)
                    atanlar.append(golcu["isim"])
                    c.execute("UPDATE oyuncular SET gol=gol+1 WHERE oyuncu_id=?", (golcu["oyuncu_id"],))
                    diger = [o for o in havuz if o["oyuncu_id"] != golcu["oyuncu_id"]]
                    if diger:
                        asistci = random.choice(diger)
                        c.execute("UPDATE oyuncular SET asist=asist+1 WHERE oyuncu_id=?", (asistci["oyuncu_id"],))
                c.commit()
            return atanlar

        ev_gol_atanlar = gol_atan(ev_oyuncular, ev_gol)
        dep_gol_atanlar = gol_atan(dep_oyuncular, dep_gol)

        tum = [(o, "ev") for o in ev_oyuncular] + [(o, "dep") for o in dep_oyuncular]
        with self._conn() as c:
            for o, _t in tum:
                if random.random() < 0.15:
                    yeni_sari = (o.get("sari_kart") or 0) + 1
                    c.execute("UPDATE oyuncular SET sari_kart=? WHERE oyuncu_id=?", (yeni_sari, o["oyuncu_id"]))
                    olaylar.append(f"🟡 {o['isim']} sarı kart")
                elif random.random() < 0.03:
                    c.execute("UPDATE oyuncular SET kirmizi_kart=kirmizi_kart+1 WHERE oyuncu_id=?", (o["oyuncu_id"],))
                    olaylar.append(f"🔴 {o['isim']} direkt kırmızı!")
                if random.random() < 0.05:
                    gun = random.randint(2, 6)
                    bitis = (date.today() + timedelta(days=gun)).isoformat()
                    c.execute("UPDATE oyuncular SET sakatlik_bitis=? WHERE oyuncu_id=?", (bitis, o["oyuncu_id"]))
                    olaylar.append(f"🏥 {o['isim']} sakatlandı ({gun}g)")
            c.commit()

        bugun = date.today().isoformat()
        with self._conn() as conn:
            conn.execute("""
                UPDATE fikstur SET ev_gol=?,dep_gol=?,oynanmis=1,oynanma_tarihi=? WHERE mac_id=?
            """, (ev_gol, dep_gol, bugun, mac_id))

            def upd(tid, a, y):
                if a > y:
                    conn.execute("""
                        UPDATE takimlar SET puan=puan+3,galibiyet=galibiyet+1,
                        atilan_gol=atilan_gol+?,yenilen_gol=yenilen_gol+?,
                        mac_sayisi=mac_sayisi+1,son_mac=? WHERE takim_id=?
                    """, (a, y, bugun, tid))
                elif a < y:
                    conn.execute("""
                        UPDATE takimlar SET maglubiyet=maglubiyet+1,
                        atilan_gol=atilan_gol+?,yenilen_gol=yenilen_gol+?,
                        mac_sayisi=mac_sayisi+1,son_mac=? WHERE takim_id=?
                    """, (a, y, bugun, tid))
                else:
                    conn.execute("""
                        UPDATE takimlar SET puan=puan+1,beraberlik=beraberlik+1,
                        atilan_gol=atilan_gol+?,yenilen_gol=yenilen_gol+?,
                        mac_sayisi=mac_sayisi+1,son_mac=? WHERE takim_id=?
                    """, (a, y, bugun, tid))
            upd(mac["ev_takim_id"], ev_gol, dep_gol)
            upd(mac["dep_takim_id"], dep_gol, ev_gol)
            conn.commit()

        # Para ödülleri kullanıcı takımlarına
        for t_obj, a_gol, y_gol in [(ev_t, ev_gol, dep_gol), (dep_t, dep_gol, ev_gol)]:
            uid = t_obj.get("user_id")
            if uid and not t_obj.get("bot_takim"):
                if a_gol > y_gol:
                    self.para_guncelle(uid, 8_000)
                    self._mac_basari_kontrol(uid, True)
                elif a_gol == y_gol:
                    self.para_guncelle(uid, 3_000)
                    self._mac_basari_kontrol(uid, False)
                else:
                    self.para_guncelle(uid, 1_000)
                    self._mac_basari_kontrol(uid, False)

        self._golcu_basari_kontrol()

        return {
            "mac_id": mac_id,
            "hafta": mac["hafta"],
            "lig_kodu": mac["lig_kodu"],
            "ev_takim": ev_t["isim"],
            "dep_takim": dep_t["isim"],
            "ev_takim_id": mac["ev_takim_id"],
            "dep_takim_id": mac["dep_takim_id"],
            "ev_takim_user": ev_t.get("user_id"),
            "dep_takim_user": dep_t.get("user_id"),
            "ev_gol": ev_gol,
            "dep_gol": dep_gol,
            "ev_gol_atanlar": ev_gol_atanlar,
            "dep_gol_atanlar": dep_gol_atanlar,
            "ev_guc": round(ev_guc_ham, 1),
            "dep_guc": round(dep_guc_ham, 1),
            "ev_taktik": ev_taktik,
            "dep_taktik": dep_taktik,
            "olaylar": olaylar[:8],
        }, None

    # ─── Piyasa ──────────────────────────────────────────────────────────

    def piyasa(self, sayfa: int = 0, sayfa_boyut: int = 8):
        with self._conn() as conn:
            toplam = conn.execute(
                "SELECT COUNT(*) FROM oyuncular WHERE satista=1"
            ).fetchone()[0]
            rows = conn.execute(
                "SELECT * FROM oyuncular WHERE satista=1 ORDER BY guc DESC LIMIT ? OFFSET ?",
                (sayfa_boyut, sayfa * sayfa_boyut)
            ).fetchall()
            return [dict(r) for r in rows], toplam

    def oyuncu_getir(self, oyuncu_id: int) -> Optional[dict]:
        with self._conn() as conn:
            r = conn.execute("SELECT * FROM oyuncular WHERE oyuncu_id=?", (oyuncu_id,)).fetchone()
            return dict(r) if r else None

    def satin_al(self, user_id: int, takim_id: int, oyuncu_id: int):
        oyuncu = self.oyuncu_getir(oyuncu_id)
        if not oyuncu:
            return False, "❌ Oyuncu bulunamadı.", None
        if not oyuncu["satista"]:
            return False, "❌ Bu oyuncu satışta değil.", None
        fiyat = oyuncu["satis_fiyati"]
        para = self.para_getir(user_id)
        if para < fiyat:
            return False, f"❌ Yetersiz bütçe. Gerekli: {fiyat:,}₺, Mevcut: {para:,}₺", None
        with self._conn() as conn:
            kadro = conn.execute(
                "SELECT COUNT(*) FROM oyuncular WHERE takim_id=? AND satista=0", (takim_id,)
            ).fetchone()[0]
            if kadro >= 30:
                return False, "❌ Kadro dolu (max 30).", None
            satici_uid = None
            eski_takim = conn.execute(
                "SELECT user_id FROM takimlar WHERE takim_id=?", (oyuncu["takim_id"],)
            ).fetchone() if oyuncu["takim_id"] else None
            if eski_takim:
                satici_uid = eski_takim["user_id"]
                if satici_uid:
                    conn.execute(
                        "UPDATE futbol_para SET para=para+? WHERE user_id=?", (fiyat, satici_uid)
                    )
            conn.execute(
                "UPDATE oyuncular SET takim_id=?, satista=0, satis_fiyati=0 WHERE oyuncu_id=?",
                (takim_id, oyuncu_id)
            )
            conn.commit()
        self.para_guncelle(user_id, -fiyat)
        return True, f"✅ *{oyuncu['isim']}* transfer edildi! -{fiyat:,}₺", satici_uid

    def sat(self, user_id: int, oyuncu_id: int, fiyat: int) -> tuple:
        oyuncu = self.oyuncu_getir(oyuncu_id)
        if not oyuncu:
            return False, "❌ Oyuncu bulunamadı."
        with self._conn() as conn:
            t = conn.execute(
                "SELECT * FROM takimlar WHERE takim_id=? AND user_id=?",
                (oyuncu["takim_id"], user_id)
            ).fetchone()
        if not t:
            return False, "❌ Bu oyuncu senin takımında değil."
        min_fiyat = int(oyuncu["deger"] * 0.5)
        if fiyat < min_fiyat:
            return False, f"❌ Minimum satış fiyatı: {min_fiyat:,}₺"
        with self._conn() as conn:
            conn.execute(
                "UPDATE oyuncular SET satista=1, satis_fiyati=? WHERE oyuncu_id=?",
                (fiyat, oyuncu_id)
            )
            conn.commit()
        return True, f"✅ *{oyuncu['isim']}* {fiyat:,}₺'ye satışa çıkarıldı."

    def sat_iptal(self, user_id: int, oyuncu_id: int) -> tuple:
        oyuncu = self.oyuncu_getir(oyuncu_id)
        if not oyuncu:
            return False, "❌ Oyuncu bulunamadı."
        with self._conn() as conn:
            t = conn.execute(
                "SELECT * FROM takimlar WHERE takim_id=? AND user_id=?",
                (oyuncu["takim_id"], user_id)
            ).fetchone()
        if not t:
            return False, "❌ Bu oyuncu senin takımında değil."
        with self._conn() as conn:
            conn.execute(
                "UPDATE oyuncular SET satista=0, satis_fiyati=0 WHERE oyuncu_id=?", (oyuncu_id,)
            )
            conn.commit()
        return True, f"✅ {oyuncu['isim']} satıştan kaldırıldı."

    def antrenman_yap(self, user_id: int, takim_id: int, oyuncu_id: int) -> tuple:
        oyuncu = self.oyuncu_getir(oyuncu_id)
        if not oyuncu or oyuncu["takim_id"] != takim_id:
            return False, "❌ Geçersiz oyuncu."
        bugun = date.today().isoformat()
        if oyuncu.get("antrenman_tarihi") == bugun:
            return False, "⚠️ Bu oyuncu bugün zaten antrenman yaptı."
        maliyet = 2_000
        para = self.para_getir(user_id)
        if para < maliyet:
            return False, f"❌ Yetersiz bütçe (gerekli {maliyet:,}₺)."
        artis = random.randint(1, 3) if not oyuncu.get("genc") else random.randint(1, 4)
        with self._conn() as conn:
            conn.execute(
                "UPDATE oyuncular SET guc=MIN(99,guc+?), antrenman_tarihi=? WHERE oyuncu_id=?",
                (artis, bugun, oyuncu_id)
            )
            conn.commit()
        self.para_guncelle(user_id, -maliyet)
        return True, f"✅ *{oyuncu['isim']}* +{artis} güç! Yeni: {min(99, oyuncu['guc'] + artis)}"

    def altyapi_cikart(self, takim_id: int, user_id: int):
        para = self.para_getir(user_id)
        maliyet = 10_000
        if para < maliyet:
            return None, f"❌ Altyapı için {maliyet:,}₺ gerekli."
        kadro = self.takim_oyunculari(takim_id)
        if len(kadro) >= 30:
            return None, "❌ Kadro dolu (max 30)."
        isimler = list({o["isim"] for o in kadro})
        gen_isimler = [
            "Arda Güler", "Kenan Yıldız", "Yankı Yıldız", "Emirhan Toprak",
            "Alex İnce", "Tom Müller Jr", "Pablo Jr", "Lucas Filho",
            "André Silva", "Mateo García",
        ]
        random.shuffle(gen_isimler)
        isim = next((i for i in gen_isimler if i not in isimler), f"Genç #{random.randint(10,99)}")
        pozisyon = random.choice(["Kaleci", "Defans", "Defans", "Orta Saha", "Orta Saha", "Forvet"])
        guc = random.randint(60, 72)
        deger = self._deger_hesapla(guc)
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO oyuncular (takim_id,isim,pozisyon,guc,deger,ulke,satista,satis_fiyati,genc)
                VALUES (?,?,?,?,?,'TR',0,?,1)
            """, (takim_id, isim, pozisyon, guc, deger, deger))
            conn.commit()
        self.para_guncelle(user_id, -maliyet)
        self.basari_ver(user_id, "altyapi")
        return {"isim": isim, "pozisyon": pozisyon, "guc": guc, "deger": deger}, None

    # ─── Fikstür / Maç Geçmişi ───────────────────────────────────────────

    def son_maclar_lig(self, lig_kodu: str, limit: int = 10) -> list:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT f.*,
                    (SELECT isim FROM takimlar WHERE takim_id=f.ev_takim_id)  AS ev_isim,
                    (SELECT isim FROM takimlar WHERE takim_id=f.dep_takim_id) AS dep_isim
                FROM fikstur f
                WHERE f.lig_kodu=? AND f.oynanmis=1
                ORDER BY f.oynanma_tarihi DESC, f.mac_id DESC LIMIT ?
            """, (lig_kodu, limit)).fetchall()
            return [dict(r) for r in rows]

    def takim_son_maclar(self, takim_id: int, limit: int = 5) -> list:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT f.*,
                    (SELECT isim FROM takimlar WHERE takim_id=f.ev_takim_id)  AS ev_isim,
                    (SELECT isim FROM takimlar WHERE takim_id=f.dep_takim_id) AS dep_isim
                FROM fikstur f
                WHERE (f.ev_takim_id=? OR f.dep_takim_id=?) AND f.oynanmis=1
                ORDER BY f.oynanma_tarihi DESC, f.mac_id DESC LIMIT ?
            """, (takim_id, takim_id, limit)).fetchall()
            return [dict(r) for r in rows]

    def haftalik_fikstur(self, hafta: int, lig_kodu: str) -> list:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT f.*,
                    (SELECT isim FROM takimlar WHERE takim_id=f.ev_takim_id)  AS ev_isim,
                    (SELECT isim FROM takimlar WHERE takim_id=f.dep_takim_id) AS dep_isim
                FROM fikstur f WHERE f.hafta=? AND f.lig_kodu=? ORDER BY f.mac_id
            """, (hafta, lig_kodu)).fetchall()
            return [dict(r) for r in rows]

    def mevcut_hafta(self, lig_kodu: str) -> int:
        with self._conn() as conn:
            r = conn.execute(
                "SELECT MAX(hafta) FROM fikstur WHERE oynanmis=1 AND lig_kodu=?", (lig_kodu,)
            ).fetchone()[0]
            if r:
                return r
            r2 = conn.execute(
                "SELECT MIN(hafta) FROM fikstur WHERE oynanmis=0 AND lig_kodu=?", (lig_kodu,)
            ).fetchone()[0]
            return r2 or 1

    def sonraki_mac_user(self, user_id: int) -> Optional[dict]:
        takim = self.takim_user(user_id)
        if not takim:
            return None
        with self._conn() as conn:
            r = conn.execute("""
                SELECT * FROM fikstur
                WHERE (ev_takim_id=? OR dep_takim_id=?) AND oynanmis=0
                ORDER BY hafta ASC LIMIT 1
            """, (takim["takim_id"], takim["takim_id"])).fetchone()
            return dict(r) if r else None

    # ─── İstatistikler ───────────────────────────────────────────────────

    def sezon_golculeri(self, lig_kodu: str = None, limit: int = 20) -> list:
        with self._conn() as conn:
            if lig_kodu:
                rows = conn.execute("""
                    SELECT o.isim, o.gol, o.asist, t.isim AS takim_isim, t.lig_kodu
                    FROM oyuncular o JOIN takimlar t ON o.takim_id=t.takim_id
                    WHERE t.lig_kodu=? AND o.gol > 0
                    ORDER BY o.gol DESC, o.asist DESC LIMIT ?
                """, (lig_kodu, limit)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT o.isim, o.gol, o.asist, t.isim AS takim_isim, t.lig_kodu
                    FROM oyuncular o JOIN takimlar t ON o.takim_id=t.takim_id
                    WHERE o.gol > 0
                    ORDER BY o.gol DESC, o.asist DESC LIMIT ?
                """, (limit,)).fetchall()
            return [dict(r) for r in rows]

    def oyuncu_istatistikleri(self, takim_id: int) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM oyuncular WHERE takim_id=? ORDER BY gol DESC, asist DESC",
                (takim_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    # ─── Başarı ──────────────────────────────────────────────────────────

    def basari_ver(self, user_id: int, kod: str) -> bool:
        if kod not in BASARILAR:
            return False
        with self._conn() as conn:
            try:
                conn.execute(
                    "INSERT INTO basarilar (user_id,basari_kodu,tarih) VALUES (?,?,?)",
                    (user_id, kod, date.today().isoformat())
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def kullanici_basarilari(self, user_id: int) -> list:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT basari_kodu, tarih FROM basarilar WHERE user_id=? ORDER BY tarih DESC",
                (user_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def _mac_basari_kontrol(self, user_id: int, kazandi: bool):
        self.basari_ver(user_id, "ilk_mac")
        if not kazandi:
            return
        takim = self.takim_user(user_id)
        if not takim:
            return
        g = takim["galibiyet"]
        for esik, kod in [(5, "5_galibiyet"), (10, "10_galibiyet"), (25, "25_galibiyet")]:
            if g >= esik:
                self.basari_ver(user_id, kod)

    def _golcu_basari_kontrol(self):
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT t.user_id FROM oyuncular o
                JOIN takimlar t ON o.takim_id = t.takim_id
                WHERE o.gol >= 10 AND t.user_id IS NOT NULL
            """).fetchall()
            for r in rows:
                if r["user_id"]:
                    self.basari_ver(r["user_id"], "golcu_10")

    # ─── Spin ────────────────────────────────────────────────────────────

    def spin_cevir(self, user_id: int):
        bugun = date.today().isoformat()
        with self._conn() as conn:
            r = conn.execute("SELECT * FROM spin_kaydi WHERE user_id=?", (user_id,)).fetchone()
            if r and r["son_spin"] == bugun:
                return None, "Bugün zaten çevirdin! Yarın tekrar gel. 🎰"
            agirliklar = [o[3] for o in SPIN_ODULLER]
            odul = random.choices(SPIN_ODULLER, weights=agirliklar, k=1)[0]
            yeni_toplam = ((r["toplam"] if r else 0) + 1)
            if r:
                conn.execute("UPDATE spin_kaydi SET son_spin=?,toplam=? WHERE user_id=?",
                             (bugun, yeni_toplam, user_id))
            else:
                conn.execute("INSERT INTO spin_kaydi VALUES (?,?,?)", (user_id, bugun, yeni_toplam))
            conn.commit()
        if odul[1] == "para":
            self.para_guncelle(user_id, odul[2])
        if yeni_toplam >= 5:
            self.basari_ver(user_id, "spin_5")
        return odul, yeni_toplam

    # ─── Sezon Sıfırlama ─────────────────────────────────────────────────

    def sezon_sifirla(self, lig_kodu: str):
        takimlar = self.lig_takimlari(lig_kodu)
        if takimlar:
            sampiyon = takimlar[0]
            uid = sampiyon.get("user_id")
            if uid:
                self.basari_ver(uid, "sezon_sampiyon")
        with self._conn() as conn:
            for t in takimlar:
                conn.execute("""
                    UPDATE takimlar SET puan=0,galibiyet=0,beraberlik=0,maglubiyet=0,
                    atilan_gol=0,yenilen_gol=0,mac_sayisi=0,son_mac=NULL,sezon=sezon+1
                    WHERE takim_id=?
                """, (t["takim_id"],))
                conn.execute("""
                    UPDATE oyuncular SET gol=0,asist=0,sari_kart=0,kirmizi_kart=0
                    WHERE takim_id=?
                """, (t["takim_id"],))
            conn.execute("DELETE FROM fikstur WHERE lig_kodu=?", (lig_kodu,))
            conn.execute("UPDATE lig_durumu SET aktif=0 WHERE lig_kodu=?", (lig_kodu,))
            conn.commit()
        return len(takimlar)

    # ─── Grup ────────────────────────────────────────────────────────────

    def grup_kaydet(self, chat_id: int):
        with self._conn() as conn:
            conn.execute("INSERT OR IGNORE INTO grup_chatler VALUES (?)", (chat_id,))
            conn.commit()

    def gruplari_getir(self) -> list:
        with self._conn() as conn:
            rows = conn.execute("SELECT chat_id FROM grup_chatler").fetchall()
            return [r["chat_id"] for r in rows]
