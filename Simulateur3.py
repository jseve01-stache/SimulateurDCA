import random
import statistics

# =====================================================
# PARAMETRES GENERAUX
# =====================================================

NB_SIMULATIONS = 1000
HORIZON = 40

SEED = None

# =====================================================
# MARCHE
# =====================================================

RENDEMENT_MOYEN = 0.08
VOLATILITE = 0.15

KRACH_ACTIF = True
KRACH_AMPLITUDE = -0.40

# =====================================================
# EPARGNE
# =====================================================

CAPACITE_INITIALE = 300

AUGMENTATION_CAPACITE = 50
FREQUENCE_AUGMENTATION = 5

AUGMENTATION_SALAIRE = 0.00

# =====================================================
# CREDIT
# =====================================================

TAUX_CREDIT = 0.03

PORTEFEUILLE_PAYE_DEFICIT = True

# =====================================================
# FISCALITE
# =====================================================

ACTIVER_FISCALITE = True
TAUX_FLAT_TAX = 0.30

# =====================================================
# INFLATION
# =====================================================

ACTIVER_INFLATION = False
INFLATION_ANNUELLE = 0.02

# =====================================================
# FRAIS ETF
# =====================================================

ACTIVER_FRAIS_ETF = False
FRAIS_ETF = 0.002

# =====================================================
# SCENARIO EMPRUNTS
# =====================================================

EMPRUNTS = [

    {
        "annee": 0,
        "montant": 20000,
        "duree": 10
    },

    {
        "annee": 5,
        "montant": 0000,
        "duree": 10
    },

    {
        "annee": 10,
        "montant": 50000,
        "duree": 15
    },

    {
        "annee": 15,
        "montant": 0000,
        "duree": 10
    },

    {
        "annee": 20,
        "montant": 0000,
        "duree": 10
    },

    {
        "annee": 25,
        "montant": 100000,
        "duree": 20
    }

]

# =====================================================
# FONCTIONS
# =====================================================

def calcul_mensualite(montant, taux, duree):

    taux_mensuel = taux / 12

    nb_mois = duree * 12

    mensualite = (
        montant
        * taux_mensuel
        / (1 - (1 + taux_mensuel) ** (-nb_mois))
    )

    return mensualite


def appliquer_fiscalite(gain):

    if ACTIVER_FISCALITE:

        if gain > 0:
            gain *= (1 - TAUX_FLAT_TAX)

    return gain


# =====================================================
# SEED
# =====================================================

if SEED is not None:
    random.seed(SEED)

# =====================================================
# MONTE CARLO
# =====================================================

victoires = 0
ecarts = []

for simulation in range(NB_SIMULATIONS):

    if KRACH_ACTIF:
        annee_krach = random.randint(0, HORIZON - 1)

    capital_dca = 0
    capital_levier = 0

    capacite = CAPACITE_INITIALE

    for annee in range(HORIZON):

        # ==========================================
        # Nouveaux emprunts
        # ==========================================

        for emprunt in EMPRUNTS:

            if annee == emprunt["annee"]:
                capital_levier += emprunt["montant"]

        # ==========================================
        # Evolution capacité d'épargne
        # ==========================================

        if annee > 0:

            if annee % FREQUENCE_AUGMENTATION == 0:
                capacite += AUGMENTATION_CAPACITE

            capacite *= (1 + AUGMENTATION_SALAIRE)

        # ==========================================
        # Rendement annuel
        # ==========================================

        if KRACH_ACTIF and annee == annee_krach:

            rendement = KRACH_AMPLITUDE

        else:

            rendement = random.normalvariate(
                RENDEMENT_MOYEN,
                VOLATILITE
            )

        # ==========================================
        # Frais ETF
        # ==========================================

        if ACTIVER_FRAIS_ETF:
            rendement -= FRAIS_ETF

        # ==========================================
        # Inflation
        # ==========================================

        if ACTIVER_INFLATION:
            rendement -= INFLATION_ANNUELLE

        # ==========================================
        # DCA
        # ==========================================

        capital_dca *= (1 + rendement)

        capital_dca += capacite * 12

        # ==========================================
        # Levier
        # ==========================================

        capital_levier *= (1 + rendement)

        mensualite_totale = 0

        for emprunt in EMPRUNTS:

            debut = emprunt["annee"]
            fin = debut + emprunt["duree"]

            if debut <= annee < fin:

                mensualite_totale += calcul_mensualite(
                    emprunt["montant"],
                    TAUX_CREDIT,
                    emprunt["duree"]
                )

        difference = capacite - mensualite_totale

        if difference >= 0:

            capital_levier += difference * 12

        else:

            if PORTEFEUILLE_PAYE_DEFICIT:

                capital_levier -= abs(difference) * 12

        # Empêche les valeurs absurdes
        capital_levier = max(0, capital_levier)

    # ==========================================
    # Fiscalité
    # ==========================================

    gain = capital_levier - capital_dca

    gain = appliquer_fiscalite(gain)

    if gain > 0:
        victoires += 1

    ecarts.append(gain)

# =====================================================
# STATISTIQUES
# =====================================================

ecarts.sort()


print("====================================")
print("CONFIGURATION UTILISEE")
print("====================================")


print("Simulations :", NB_SIMULATIONS)
print("Horizon :", HORIZON, "ans")



print("Rendement moyen :", round(RENDEMENT_MOYEN * 100, 2), "%")
print("Volatilité :", round(VOLATILITE * 100, 2), "%")



print("Krach activé :", KRACH_ACTIF)

if KRACH_ACTIF:
    print("Amplitude krach :", round(KRACH_AMPLITUDE * 100, 2), "%")



print("Capacité initiale :", round(CAPACITE_INITIALE, 2), "€/mois")
print("Augmentation capacité :", round(AUGMENTATION_CAPACITE, 2), "€/mois")
print("Fréquence augmentation :", FREQUENCE_AUGMENTATION, "ans")
print("Augmentation salaire :", round(AUGMENTATION_SALAIRE * 100, 2), "%")



print("Taux crédit :", round(TAUX_CREDIT * 100, 2), "%")



print("Fiscalité activée :", ACTIVER_FISCALITE)

if ACTIVER_FISCALITE:
    print("Flat tax :", round(TAUX_FLAT_TAX * 100, 2), "%")



print("Inflation activée :", ACTIVER_INFLATION)

if ACTIVER_INFLATION:
    print("Inflation :", round(INFLATION_ANNUELLE * 100, 2), "%")



print("Frais ETF activés :", ACTIVER_FRAIS_ETF)

if ACTIVER_FRAIS_ETF:
    print("Frais ETF :", round(FRAIS_ETF * 100, 2), "%")



print("EMPRUNTS")

for i, emprunt in enumerate(EMPRUNTS, start=1):

    mensualite = calcul_mensualite(
        emprunt["montant"],
        TAUX_CREDIT,
        emprunt["duree"]
    )

    print(
        f"#{i} | Année {emprunt['annee']} | "
        f"{emprunt['montant']:,.0f}€ | "
        f"{emprunt['duree']} ans | "
        f"Mensualité ≈ {mensualite:.2f}€"
    )


print("====================================")
print("RESULTATS")
print("====================================")


print("Levier gagnant :", round(victoires / NB_SIMULATIONS * 100, 2), "%")
print("Gain moyen :", round(statistics.mean(ecarts), 2))
print("Pire écart :", round(ecarts[0], 2))
print("P10 écart :", round(ecarts[int(NB_SIMULATIONS * 0.10)], 2))
print("Médiane écart :", round(statistics.median(ecarts), 2))
print("P90 écart :", round(ecarts[int(NB_SIMULATIONS * 0.90)], 2))
print("Meilleur écart :", round(ecarts[-1], 2))