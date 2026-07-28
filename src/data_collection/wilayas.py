"""
HeatShield AI - Liste des 58 wilayas d'Algérie
Coordonnées GPS approximatives du chef-lieu de chaque wilaya.
"""

WILAYAS = [
    {"code": "01", "nom": "Adrar",               "lat": 27.8742, "lon": -0.2939},
    {"code": "02", "nom": "Chlef",               "lat": 36.1654, "lon": 1.3345},
    {"code": "03", "nom": "Laghouat",            "lat": 33.8000, "lon": 2.8650},
    {"code": "04", "nom": "Oum El Bouaghi",      "lat": 35.8750, "lon": 7.1136},
    {"code": "05", "nom": "Batna",               "lat": 35.5550, "lon": 6.1742},
    {"code": "06", "nom": "Béjaïa",              "lat": 36.7525, "lon": 5.0567},
    {"code": "07", "nom": "Biskra",              "lat": 34.8500, "lon": 5.7333},
    {"code": "08", "nom": "Béchar",              "lat": 31.6167, "lon": -2.2167},
    {"code": "09", "nom": "Blida",               "lat": 36.4700, "lon": 2.8300},
    {"code": "10", "nom": "Bouira",              "lat": 36.3800, "lon": 3.9000},
    {"code": "11", "nom": "Tamanrasset",         "lat": 22.7850, "lon": 5.5228},
    {"code": "12", "nom": "Tébessa",             "lat": 35.4000, "lon": 8.1167},
    {"code": "13", "nom": "Tlemcen",             "lat": 34.8828, "lon": -1.3167},
    {"code": "14", "nom": "Tiaret",              "lat": 35.3700, "lon": 1.3200},
    {"code": "15", "nom": "Tizi Ouzou",          "lat": 36.7167, "lon": 4.0500},
    {"code": "16", "nom": "Alger",               "lat": 36.7538, "lon": 3.0588},
    {"code": "17", "nom": "Djelfa",              "lat": 34.6700, "lon": 3.2500},
    {"code": "18", "nom": "Jijel",               "lat": 36.8200, "lon": 5.7667},
    {"code": "19", "nom": "Sétif",               "lat": 36.1900, "lon": 5.4100},
    {"code": "20", "nom": "Saïda",               "lat": 34.8400, "lon": 0.1500},
    {"code": "21", "nom": "Skikda",              "lat": 36.8667, "lon": 6.9000},
    {"code": "22", "nom": "Sidi Bel Abbès",      "lat": 35.2000, "lon": -0.6300},
    {"code": "23", "nom": "Annaba",              "lat": 36.9000, "lon": 7.7667},
    {"code": "24", "nom": "Guelma",              "lat": 36.4667, "lon": 7.4333},
    {"code": "25", "nom": "Constantine",         "lat": 36.3650, "lon": 6.6147},
    {"code": "26", "nom": "Médéa",               "lat": 36.2675, "lon": 2.7500},
    {"code": "27", "nom": "Mostaganem",          "lat": 35.9333, "lon": 0.0900},
    {"code": "28", "nom": "M'Sila",              "lat": 35.7000, "lon": 4.5500},
    {"code": "29", "nom": "Mascara",             "lat": 35.4000, "lon": 0.1400},
    {"code": "30", "nom": "Ouargla",             "lat": 31.9500, "lon": 5.3300},
    {"code": "31", "nom": "Oran",                "lat": 35.6969, "lon": -0.6331},
    {"code": "32", "nom": "El Bayadh",           "lat": 33.6800, "lon": 1.0200},
    {"code": "33", "nom": "Illizi",              "lat": 26.5000, "lon": 8.4800},
    {"code": "34", "nom": "Bordj Bou Arréridj",  "lat": 36.0700, "lon": 4.7600},
    {"code": "35", "nom": "Boumerdès",           "lat": 36.7600, "lon": 3.4700},
    {"code": "36", "nom": "El Tarf",             "lat": 36.7700, "lon": 8.3100},
    {"code": "37", "nom": "Tindouf",             "lat": 27.6700, "lon": -8.1500},
    {"code": "38", "nom": "Tissemsilt",          "lat": 35.6100, "lon": 1.8100},
    {"code": "39", "nom": "El Oued",             "lat": 33.3700, "lon": 6.8700},
    {"code": "40", "nom": "Khenchela",           "lat": 35.4300, "lon": 7.1400},
    {"code": "41", "nom": "Souk Ahras",          "lat": 36.2800, "lon": 7.9500},
    {"code": "42", "nom": "Tipaza",              "lat": 36.5900, "lon": 2.4500},
    {"code": "43", "nom": "Mila",                "lat": 36.4500, "lon": 6.2600},
    {"code": "44", "nom": "Aïn Defla",           "lat": 36.2600, "lon": 1.9700},
    {"code": "45", "nom": "Naâma",               "lat": 33.2700, "lon": -0.3100},
    {"code": "46", "nom": "Aïn Témouchent",      "lat": 35.3000, "lon": -1.1400},
    {"code": "47", "nom": "Ghardaïa",            "lat": 32.4900, "lon": 3.6700},
    {"code": "48", "nom": "Relizane",            "lat": 35.7400, "lon": 0.5500},
    {"code": "49", "nom": "Timimoun",            "lat": 29.2600, "lon": 0.2300},
    {"code": "50", "nom": "Bordj Badji Mokhtar", "lat": 21.3300, "lon": 0.9500},
    {"code": "51", "nom": "Ouled Djellal",       "lat": 34.4300, "lon": 5.0700},
    {"code": "52", "nom": "Béni Abbès",          "lat": 30.1300, "lon": -2.1700},
    {"code": "53", "nom": "In Salah",            "lat": 27.2000, "lon": 2.4700},
    {"code": "54", "nom": "In Guezzam",          "lat": 19.5700, "lon": 5.7700},
    {"code": "55", "nom": "Touggourt",           "lat": 33.1000, "lon": 6.0700},
    {"code": "56", "nom": "Djanet",              "lat": 24.5500, "lon": 9.4800},
    {"code": "57", "nom": "El M'Ghair",          "lat": 33.9500, "lon": 5.9200},
    {"code": "58", "nom": "El Meniaa",           "lat": 30.5800, "lon": 2.8800},
]


def get_all_wilayas():
    """Retourne la liste complète des 58 wilayas."""
    return WILAYAS


def get_wilaya_by_code(code):
    """Retourne une wilaya par son code (ex: '16')."""
    for w in WILAYAS:
        if w["code"] == code:
            return w
    return None


def get_wilaya_names():
    """Retourne la liste des noms uniquement."""
    return [w["nom"] for w in WILAYAS]


if __name__ == "__main__":
    print(f"Nombre de wilayas: {len(WILAYAS)}")
    print("Exemple:", WILAYAS[15])  # Alger