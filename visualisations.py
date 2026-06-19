"""
Visualisations Black-Scholes.

Génère trois graphiques qui montrent VISUELLEMENT pourquoi chaque
variable compte. C'est ce qui fait la différence avec une simple
lecture de la formule : on voit le comportement du modèle.

Lancement :  python visualisations.py
Produit :    prix_vs_sousjacent.png, prix_vs_volatilite.png, time_decay.png
"""

import numpy as np
import matplotlib.pyplot as plt

from black_scholes import call_price, put_price

# Style sobre, lisible
plt.rcParams.update({
    "figure.figsize": (9, 5.5),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
})

K, T, r, sigma = 100, 1.0, 0.03, 0.20


def graphe_prix_vs_sousjacent():
    """Prix de l'option en fonction du prix de l'action.
    On voit la 'cassure' autour du strike : la fameuse forme en
    hockey stick qui s'arrondit à cause de la valeur temps."""
    S = np.linspace(50, 150, 300)
    calls = [call_price(s, K, T, r, sigma) for s in S]
    puts = [put_price(s, K, T, r, sigma) for s in S]

    plt.figure()
    plt.plot(S, calls, label="Call", linewidth=2)
    plt.plot(S, puts, label="Put", linewidth=2)
    plt.axvline(K, color="grey", linestyle="--", alpha=0.6, label=f"Strike = {K}")
    plt.xlabel("Prix du sous-jacent (€)")
    plt.ylabel("Prix de l'option (€)")
    plt.title("Prix de l'option selon le prix de l'action")
    plt.legend()
    plt.tight_layout()
    plt.savefig("prix_vs_sousjacent.png", dpi=130)
    plt.close()


def graphe_prix_vs_volatilite():
    """Prix du call selon la volatilité.
    Relation quasi linéaire et croissante : plus c'est volatil,
    plus l'option vaut cher. C'est LE point clé du modèle."""
    vols = np.linspace(0.05, 0.80, 300)
    prix = [call_price(100, K, T, r, v) for v in vols]

    plt.figure()
    plt.plot(vols * 100, prix, color="darkorange", linewidth=2)
    plt.xlabel("Volatilité (%)")
    plt.ylabel("Prix du call (€)")
    plt.title("Plus la volatilité monte, plus l'option vaut cher")
    plt.tight_layout()
    plt.savefig("prix_vs_volatilite.png", dpi=130)
    plt.close()


def graphe_time_decay():
    """Valeur de l'option qui fond avec le temps (à la monnaie).
    L'accélération vers l'échéance illustre le theta."""
    temps = np.linspace(1.0, 0.01, 300)  # de 1 an à presque 0
    prix = [call_price(100, K, t, r, sigma) for t in temps]

    plt.figure()
    plt.plot((1 - temps) * 12, prix, color="crimson", linewidth=2)
    plt.xlabel("Mois écoulés (sur 1 an)")
    plt.ylabel("Prix du call à la monnaie (€)")
    plt.title("Time decay : l'option perd de la valeur en approchant l'échéance")
    plt.tight_layout()
    plt.savefig("time_decay.png", dpi=130)
    plt.close()


if __name__ == "__main__":
    graphe_prix_vs_sousjacent()
    graphe_prix_vs_volatilite()
    graphe_time_decay()
    print("3 graphiques générés : prix_vs_sousjacent.png, "
          "prix_vs_volatilite.png, time_decay.png")
