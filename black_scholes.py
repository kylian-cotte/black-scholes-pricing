"""
Black-Scholes (1973) — Pricing d'options européennes et Greeks.

Implémentation à partir du papier fondateur de Black, Scholes et Merton.
Le but : transformer la formule théorique en code fonctionnel pour
comprendre en profondeur le rôle de chaque variable.

Variables du modèle :
    S     : prix actuel du sous-jacent (l'action)
    K     : prix d'exercice (strike)
    T     : temps jusqu'à l'échéance, en années
    r     : taux sans risque (annualisé, ex : 0.03 = 3%)
    sigma : volatilité annualisée du sous-jacent (ex : 0.20 = 20%)
"""

import numpy as np
from scipy.stats import norm


def _d1_d2(S, K, T, r, sigma):
    """Calcule les termes intermédiaires d1 et d2 du modèle.

    d1 et d2 sont le coeur de la formule : ils mesurent, en unités
    d'écart-type, à quelle distance l'option est de la monnaie en
    tenant compte du temps, du taux et de la volatilité.
    """
    d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def call_price(S, K, T, r, sigma):
    """Prix d'une option d'achat (call) européenne.

    Intuition : c'est la valeur actuelle de ce qu'on espère gagner
    en achetant l'action au strike, pondérée par la probabilité que
    l'option finisse dans la monnaie.
    """
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def put_price(S, K, T, r, sigma):
    """Prix d'une option de vente (put) européenne."""
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


# ---------------------------------------------------------------------------
# Les Greeks : sensibilité du prix de l'option à chaque variable.
# C'est ici qu'on comprend VRAIMENT le modèle.
# ---------------------------------------------------------------------------

def delta(S, K, T, r, sigma, option="call"):
    """Sensibilité au prix du sous-jacent. Combien bouge l'option si
    l'action monte de 1€ ? (entre 0 et 1 pour un call)."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    if option == "call":
        return norm.cdf(d1)
    return norm.cdf(d1) - 1


def gamma(S, K, T, r, sigma):
    """Sensibilité du delta lui-même. Mesure la courbure."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def vega(S, K, T, r, sigma):
    """Sensibilité à la volatilité. Pour +1% de vol, combien gagne
    l'option ? (divisé par 100 pour exprimer par point de %)."""
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * np.sqrt(T) / 100


def theta(S, K, T, r, sigma, option="call"):
    """Sensibilité au temps qui passe. La perte de valeur par jour
    (time decay)."""
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    first = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    if option == "call":
        second = r * K * np.exp(-r * T) * norm.cdf(d2)
        return (first - second) / 365
    second = r * K * np.exp(-r * T) * norm.cdf(-d2)
    return (first + second) / 365


def rho(S, K, T, r, sigma, option="call"):
    """Sensibilité au taux sans risque (par point de %)."""
    _, d2 = _d1_d2(S, K, T, r, sigma)
    if option == "call":
        return K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    return -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100


def put_call_parity_check(S, K, T, r, sigma, tol=1e-9):
    """Vérifie la relation de parité call-put : C - P = S - K*e^(-rT).
    C'est une contrainte d'absence d'arbitrage : si elle n'est pas
    respectée, le code est faux."""
    c = call_price(S, K, T, r, sigma)
    p = put_price(S, K, T, r, sigma)
    gauche = c - p
    droite = S - K * np.exp(-r * T)
    return abs(gauche - droite) < tol


if __name__ == "__main__":
    # Exemple : action à 100€, strike 105€, 1 an, taux 3%, vol 20%
    S, K, T, r, sigma = 100, 105, 1, 0.03, 0.20

    print("=== Black-Scholes ===")
    print(f"Call : {call_price(S, K, T, r, sigma):.2f} €")
    print(f"Put  : {put_price(S, K, T, r, sigma):.2f} €")
    print()
    print("=== Greeks (call) ===")
    print(f"Delta : {delta(S, K, T, r, sigma):.4f}")
    print(f"Gamma : {gamma(S, K, T, r, sigma):.4f}")
    print(f"Vega  : {vega(S, K, T, r, sigma):.4f}")
    print(f"Theta : {theta(S, K, T, r, sigma):.4f}")
    print(f"Rho   : {rho(S, K, T, r, sigma):.4f}")
    print()
    ok = put_call_parity_check(S, K, T, r, sigma)
    print(f"Parité call-put respectée : {ok}")
