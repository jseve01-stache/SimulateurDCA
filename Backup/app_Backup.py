from Simulateur2 import lancer_simulation
import streamlit as st
import matplotlib.pyplot as plt


st.title("Simulateur DCA")

st.markdown(
"""
Simulateur Monte Carlo de patrimoine et de liberté financière.
"""
)

with st.expander("📁 Épargne", expanded=True):

    capital_depart = st.number_input(
    "Capital de départ (€)",
    value=0,
    step=1000
    )

    capacite = st.number_input(
    "Capacité mensuelle (€)",)

    augmentation_capacite = st.number_input(
    "Augmentation capacité (€)",
    value=100,
    step=50
)

    frequence_augmentation = st.number_input(
    "Tous les X ans",
    value=5,
    min_value=1
)

with st.expander("📁 Marchés"):
    
    rendement = st.slider(
    "Rendement moyen (%)",
    0.0,
    20.0,
    10.0
    )

    volatilité = st.slider(
    "Volatilité",
    0.0,
    0.40,
    0.15
    )

    régimes_actifs = st.checkbox(
    "Activer régimes de marché",
    value=True
    )

with st.expander("📁 Liberté financière"):

    cout_annuel_vie = st.number_input(
        "Coût annuel de vie (€)",
        value=20000,
        step=1000
    )

    taux_retrait = st.slider(
        "Taux de retrait (%)",
        2.0,
        8.0,
        4.0
    )

    patrimoine_fi = (
        cout_annuel_vie /
        (taux_retrait / 100)
    )

    st.info(
        f"Patrimoine cible FI : {patrimoine_fi:,.0f} €"
    )

with st.expander("📁 Salaire"):

    salaire_initial = st.number_input(
        "Salaire mensuel (€)",
        value=2000
    )

    augmentation_salaire = st.slider(
        "Augmentation salaire (%)",
        0.0,
        10.0,
        3.0
    )

with st.expander("📁 Dépenses exceptionnelles"):

    depenses_exceptionnelles = st.checkbox(
        "Activer",
        value=True
    )

    proba_depense = st.slider(
        "Probabilité (%)",
        0.0,
        20.0,
        5.0
    )

    depense_min = st.number_input(
        "Montant minimum (€)",
        value=2000
    )

    depense_max = st.number_input(
        "Montant maximum (€)",
        value=10000
    )

with st.expander("📁 Simulation"):
    horizon = st.slider(
    "Horizon (ans)",
    1,
    50,
    30
    )

    nb_simulations = st.number_input(
    "Nombre de simulations",
    value=10000,
    step=1000
    )

print("Valeur slider =", volatilité)

st.subheader("Résumé")

st.write(
    f"""
    Capital de départ : {capital_depart:,.0f} €

    Épargne : {capacite:,.0f} €/mois

    Horizon : {horizon} ans

    Rendement : {rendement:.1f} %

    Volatilité : {volatilité*100:.1f} %

    Patrimoine FI : {patrimoine_fi:,.0f} €
    """
)

if st.button("Lancer simulation"):

    resultats = lancer_simulation(
    
    rendement_moyen=rendement / 100,
    horizon=horizon,
    capacite_initiale=capacite,
    nb_simulations=nb_simulations,
    volatilité=volatilité,
    capital_depart=capital_depart,
    augmentation_capacite=augmentation_capacite,
    frequence_augmentation=frequence_augmentation,
    salaire_initial=salaire_initial,
    augmentation_salaire=augmentation_salaire / 100,
    cout_annuel_vie=cout_annuel_vie,
    taux_retrait=taux_retrait / 100,
    depenses_exceptionnelles=depenses_exceptionnelles,
    proba_depense=proba_depense / 100,
    depense_min=depense_min,
    depense_max=depense_max,
    régimes_actifs=régimes_actifs,
    )
  

    st.success("Simulation terminée")

    st.metric(
        "Capital médian",
        f"{resultats['capital_median']:,.0f} €"
    )

    st.metric(
        "Capital moyen",
        f"{resultats['capital_moyen']:,.0f} €"
    )

    st.metric(
        "Probabilité FI",
        f"{resultats['proba_fi']:.1f} %"
    )

    st.metric(
        "Probabilité 100k",
        f"{resultats['proba_100k']:.1f} %"
    )

    st.subheader("Capital final")

    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Min", f"{resultats['capital_min']:,.0f} €")
        st.metric("P10", f"{resultats['capital_p10']:,.0f} €")    
        st.metric("Q1", f"{resultats['capital_q1']:,.0f} €")
        st.metric("Médiane", f"{resultats['capital_median']:,.0f} €")
    
    with col2:
        st.metric("Q3", f"{resultats['capital_q3']:,.0f} €")
        st.metric("P90", f"{resultats['capital_p90']:,.0f} €")
        st.metric("Max", f"{resultats['capital_max']:,.0f} €")
        st.metric("Moyenne", f"{resultats['capital_moyen']:,.0f} €")

    "python -m streamlit run app.py"

    

    fig, ax = plt.subplots()

    ax.hist(
    resultats["capitaux_finaux"],
    bins=50)

    ax.axvline(
    resultats["capital_q1"],
    linestyle=":",
    linewidth=2,
    label="Q1")

    ax.axvline(
    resultats["capital_median"],
    linestyle="--",
    label="Médiane")

    ax.axvline(
    resultats["capital_q3"],
    linestyle=":",
    linewidth=2,
    label="Q3")

    ax.axvline(
    resultats["capital_moyen"],
    linestyle=":",
    label="Moyenne")

    ax.axvline(
    resultats["patrimoine_cible_fi"],
    color="red",
    linewidth=2,
    label="FI"
)

    ax.legend()

    st.metric(
    "Intervalle central 50 %",
    f"{resultats['capital_q1']:,.0f} € → {resultats['capital_q3']:,.0f} €")

    st.pyplot(fig)

print("Régimes actifs =", régimes_actifs)