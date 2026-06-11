import random
import statistics

# =====================================================
# PARAMETRES GENERAUX
# =====================================================

NB_SIMULATIONS = 10000
HORIZON = 30

SEED = None

# =====================================================
# REGIMES DE MARCHE
# =====================================================





PROBA_BULL = 0.40
PROBA_NORMAL = 0.40
PROBA_BEAR = 0.20

ECART_BULL = 0.08
ECART_BEAR = -0.20


BULL_VOLATILITE = 0.10
NORMAL_VOLATILITE = 0.15
BEAR_VOLATILITE = 0.20

# =====================================================
# MARCHE
# =====================================================


VOLATILITE = 0.20

KRACH_ACTIF = False
KRACH_AMPLITUDE = -0.40

# =====================================================
# EPARGNE
# =====================================================

CAPITAL_DEPART = 0

CAPACITE_INITIALE = 300



# =====================================================
# SALAIRE
# =====================================================


AUGMENTATION_SALAIRE = 0.03
AUGMENTATION_EPARGNE = 0

# =====================================================
# LIBERTE FINANCIERE
# =====================================================

COUT_ANNUEL_VIE = 20000
INFLATION_DEPENSES = 0.02


# =====================================================
# FISCALITE
# =====================================================

ACTIVER_FISCALITE = False
TAUX_FLAT_TAX = 0.30

# =====================================================
# INFLATION
# =====================================================

ACTIVER_INFLATION = True
INFLATION_ANNUELLE = 0.02

# =====================================================
# FRAIS ETF
# =====================================================

ACTIVER_FRAIS_ETF = False
FRAIS_ETF = 0.002

# =====================================================
#  Dépenses exceptionnelles
# =====================================================






# =====================================================
# SEED
# =====================================================

if SEED is not None:
    random.seed(SEED)

# =====================================================
# MONTE CARLO DCA
# =====================================================


def prochain_regime(regime):
    
    tirage = random.random()


    if regime == "BULL":

        if tirage < 0.85:
            return "BULL"
        elif tirage < 0.95:
            return "NORMAL"
        else:
            return "BEAR"

    elif regime == "NORMAL":

        if tirage < 0.20:
            return "BULL"
        elif tirage < 0.80:
            return "NORMAL"
        else:
            return "BEAR"

    else:  # BEAR

        if tirage < 0.05:
            return "BULL"
        elif tirage < 0.25:
            return "NORMAL"
        else:
            return "BEAR"
        
def lancer_simulation(
    

    rendement_moyen=0.10,
    volatilité=0.15,

    horizon=30,
    nb_simulations=10000,

    capital_depart=0,
    capacite_initiale=300,
    augmentation_capacite=100,
    frequence_augmentation=5,

    salaire_initial=2000,
    augmentation_salaire=0.03,

    cout_annuel_vie=20000,
    taux_retrait=0.04,

    depenses_exceptionnelles=True,
    proba_depense=0.05,
    depense_min=2000,
    depense_max=10000,
    régimes_actifs=True,
):

    VOLATILITE = volatilité

    BULL_VOLATILITE = VOLATILITE * 0.7
    NORMAL_VOLATILITE = VOLATILITE
    BEAR_VOLATILITE = VOLATILITE * 1.3

    print("VOLATILITE PARAM =", VOLATILITE)


    print("Bull vol local =", BULL_VOLATILITE)
    print("Normal vol local =", NORMAL_VOLATILITE)
    print("Bear vol local =", BEAR_VOLATILITE)


    RENDEMENT_MOYEN = rendement_moyen
    HORIZON = horizon
    CAPACITE_INITIALE = capacite_initiale
    NB_SIMULATIONS = nb_simulations
    BULL_RENDEMENT = (
    RENDEMENT_MOYEN
    + ECART_BULL
)

    NORMAL_RENDEMENT = (
    RENDEMENT_MOYEN
)

    BEAR_RENDEMENT = (
    RENDEMENT_MOYEN
    + ECART_BEAR
)

    capitaux_finaux = []
    gains_nets = []
    annees_liberte = []
    annees_100k = []

    nb_bull = 0
    nb_normal = 0
    nb_bear = 0

    for simulation in range(NB_SIMULATIONS):


        capital = capital_depart

        etat_marche = "NORMAL"

        etat_marche = random.choice(
        ["BULL", "NORMAL", "BEAR"]
        )

        capacite = CAPACITE_INITIALE

        total_verse = 0
        salaire_mensuel = salaire_initial   

        annee_liberte = None
        annee_100k = None
        cout_annuel = cout_annuel_vie


        
        if KRACH_ACTIF:
            annee_krach = random.randint(0, HORIZON - 1)

        for annee in range(HORIZON):

            salaire_annuel = salaire_mensuel * 12

            # =====================================
            # Evolution capacité
            # =====================================

            if annee > 0:

                if (
                annee > 0
                and annee % frequence_augmentation == 0):
                    capacite += augmentation_capacite


                capacite *= (1 + AUGMENTATION_EPARGNE)
                salaire_mensuel *= (1 + augmentation_salaire)

            if régimes_actifs:
                etat_marche = prochain_regime(etat_marche)
            else:
                etat_marche = "NORMAL"

            if etat_marche == "BULL":
                nb_bull += 1

            elif etat_marche == "NORMAL":
                nb_normal += 1

            else:
                nb_bear += 1

            if etat_marche == "BULL":

                rendement = random.normalvariate(
                BULL_RENDEMENT,
                BULL_VOLATILITE
                )

            elif etat_marche == "NORMAL":

                rendement = random.normalvariate(
                NORMAL_RENDEMENT,
                NORMAL_VOLATILITE
                )

            else:

                rendement = random.normalvariate(
                BEAR_RENDEMENT,
                BEAR_VOLATILITE
                )

            # =====================================
            # Rendement
            # =====================================

            if KRACH_ACTIF and annee == annee_krach:

                rendement = KRACH_AMPLITUDE

            else:
        
                

            # =====================================
            # Frais ETF
            # =====================================

                if ACTIVER_FRAIS_ETF:
                    rendement -= FRAIS_ETF

            # =====================================
            # Inflation
            # =====================================

            if ACTIVER_INFLATION:
                rendement -= INFLATION_ANNUELLE

            # =====================================
            # Croissance portefeuille
            # =====================================

            capital *= (1 + rendement)

            # =====================================
            # Versement annuel
            # =====================================

            versement = capacite * 12

            capital += versement

            if depenses_exceptionnelles:

                if random.random() < proba_depense:

                    depense = random.uniform(
                    depense_min,
                    depense_max
                    )

                    capital -= depense

                    capital = max(0, capital)

            if annee_100k is None:

                if capital >= 100000:

                    annee_100k = annee + 1

            total_verse += versement

            revenu_passif = capital * taux_retrait  

            if annee_liberte is None:

                if revenu_passif >= cout_annuel:

                    annee_liberte = annee + 1

            cout_annuel *= (1 + INFLATION_DEPENSES)

        # =====================================
        # Fiscalité
        # =====================================

        gain_net = capital - total_verse

        if ACTIVER_FISCALITE and gain_net > 0:
            gain_net *= (1 - TAUX_FLAT_TAX)

            capital = total_verse + gain_net

        capitaux_finaux.append(capital)
        gains_nets.append(capital - total_verse)

        if annee_liberte is not None:
            annees_liberte.append(annee_liberte)

        if annee_100k is not None:
            annees_100k.append(annee_100k)

        if simulation == 0:
            total_verse_reference = total_verse

    # =====================================================
    # TRI
    # =====================================================

    capitaux_finaux.sort()
    gains_nets.sort()

    # =====================================================
    # STATISTIQUES CAPITAL FINAL
    # =====================================================

    capital_moyen = statistics.mean(capitaux_finaux)
    capital_median = statistics.median(capitaux_finaux)

    # =====================================================
    # STATISTIQUES GAIN NET
    # =====================================================

    gain_moyen = statistics.mean(gains_nets)
    gain_median = statistics.median(gains_nets)

    # =====================================================
    # AFFICHAGE
    # =====================================================

    resultats = {}

    print("===================================================")
    print("DCA MONTE CARLO")
    print("===================================================")


    print("PARAMETRES")

    print("Simulations :", NB_SIMULATIONS)
    print("Horizon :", HORIZON, "ans")



    print(
        "Bull :",
        round(BULL_RENDEMENT * 100, 2),
        "%"
    )

    print(
        "Normal :",
        round(NORMAL_RENDEMENT * 100, 2),
        "%"
    )

    print(
        "Bear :",
        round(BEAR_RENDEMENT * 100, 2),
        "%"
    )



    print("Krach activé :", KRACH_ACTIF)

    if KRACH_ACTIF:
        print("Amplitude krach :", round(KRACH_AMPLITUDE * 100, 2), "%")



    print("Capacité initiale :", CAPACITE_INITIALE, "€/mois")
    print("Augmentation capacité :", augmentation_capacite, "€/mois")
    print("Fréquence augmentation :", frequence_augmentation, "ans")


    print("Total investi :", round(total_verse_reference, 2), "€")


    print("===================================================")
    print("CAPITAL FINAL")
    print("===================================================")

    print("Min :", round(capitaux_finaux[0], 2))
    print("P10 :", round(capitaux_finaux[int(NB_SIMULATIONS * 0.10)], 2))
    print("Médiane :", round(capital_median, 2))
    print("P90 :", round(capitaux_finaux[int(NB_SIMULATIONS * 0.90)], 2))
    print("Max :", round(capitaux_finaux[-1], 2))
    print("Moyenne :", round(capital_moyen, 2))


    print("Multiple médian :",
        round(capital_median / total_verse_reference, 2), "x")

    print("Multiple moyen :",
        round(capital_moyen / total_verse_reference, 2), "x")


    print("===================================================")
    print("GAIN NET")
    print("===================================================")

    print("Min :", round(gains_nets[0], 2))
    print("P10 :", round(gains_nets[int(NB_SIMULATIONS * 0.10)], 2))
    print("Médiane :", round(gain_median, 2))
    print("P90 :", round(gains_nets[int(NB_SIMULATIONS * 0.90)], 2))
    print("Max :", round(gains_nets[-1], 2))
    print("Moyenne :", round(gain_moyen, 2))


    print("===================================================")
    print("LIBERTE FINANCIERE")
    print("===================================================")

    if len(annees_liberte) > 0:

        print(
            "Probabilité d'atteinte :",
            round(
                len(annees_liberte)
                / NB_SIMULATIONS
                * 100,
                2
            ),
            "%"
        )

        print(
            "Année moyenne :",
            round(statistics.mean(annees_liberte), 1)
        )

        print(
            "Année médiane :",
            round(statistics.median(annees_liberte), 1)
        )

        print(
            "Plus rapide :",
            min(annees_liberte)
        )

        print(
            "Plus lente :",
            max(annees_liberte)
        )

    else:

        print(
            "Aucune simulation n'atteint la liberté financière."
        )

    cout_annuel_final = (
        COUT_ANNUEL_VIE
        * (1 + INFLATION_DEPENSES) ** HORIZON
    )

    patrimoine_cible_final = (
        cout_annuel_final
        / taux_retrait
    )

    print(
        "Patrimoine cible FI (fin horizon) :",
        round(patrimoine_cible_final, 0),
        "€"
    )


    print("===================================================")
    print("OBJECTIF 100K")
    print("===================================================")

    if len(annees_100k) > 0:

        print(
            "Probabilité d'atteinte :",
            round(
                len(annees_100k)
                / NB_SIMULATIONS
                * 100,
                2
            ),
            "%"
        )

        print(
            "Année moyenne :",
            round(statistics.mean(annees_100k), 1)
        )

        print(
            "Année médiane :",
            round(statistics.median(annees_100k), 1)
        )

        print(
            "Plus rapide :",
            min(annees_100k)
        )

        print(
            "Plus lente :",
            max(annees_100k)
        )

    else:

        print(
            "Objectif jamais atteint."
        )

    print("===================================================")
    print("RÉGIME MARCHÉS")
    print("===================================================")

    print("Régimes actifs :", régimes_actifs)

    if régimes_actifs:

        print("Bull :", round(PROBA_BULL * 100, 1), "%")
        print("Normal :", round(PROBA_NORMAL * 100, 1), "%")
        print("Bear :", round(PROBA_BEAR * 100, 1), "%")

    print("Bull :", nb_bull)
    print("Normal :", nb_normal)
    print("Bear :", nb_bear)

    print(len(annees_100k))
    print(NB_SIMULATIONS)

    return {

    "capitaux_finaux": capitaux_finaux,   
    "capital_min": capitaux_finaux[0],
    "capital_p10": capitaux_finaux[int(NB_SIMULATIONS * 0.10)],
    "capital_q1": capitaux_finaux[int(NB_SIMULATIONS * 0.25)],
    "capital_median": capital_median,
    "capital_q3": capitaux_finaux[int(NB_SIMULATIONS * 0.75)],
    "capital_p90": capitaux_finaux[int(NB_SIMULATIONS * 0.90)],
    "capital_max": capitaux_finaux[-1],
    "capital_moyen": capital_moyen,

    "gain_min": gains_nets[0],
    "gain_p10": gains_nets[int(NB_SIMULATIONS * 0.10)],
    "gain_median": gain_median,
    "gain_p90": gains_nets[int(NB_SIMULATIONS * 0.90)],
    "gain_max": gains_nets[-1],
    "gain_moyen": gain_moyen,

    "proba_fi": (
        len(annees_liberte)
        / NB_SIMULATIONS
        * 100
    ),

    "proba_100k": (
        len(annees_100k)
        / NB_SIMULATIONS
        * 100
    ),

    "patrimoine_cible_fi": patrimoine_cible_final
    

    }
    
if __name__ == "__main__":
        resultats = lancer_simulation()
        print(resultats["capital_median"])

