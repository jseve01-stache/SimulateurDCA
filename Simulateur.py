import random

resultats = []

for simulation in range(1000):

    capital = 0

    for annee in range(30):

        rendement = random.normalvariate(0.08, 0.08)

        capital = capital * (1 + rendement)

        capital += 300 * 12

    resultats.append(capital)

print("Pire scénario :", round(min(resultats),2))
print("Meilleur scénario :", round(max(resultats),2))
print("Moyenne :", round(sum(resultats)/len(resultats),2))
resultats.sort()

print("P10 :", round(resultats[100],2))
print("Médiane :", round(resultats[500],2))
print("P90 :", round(resultats[900],2))