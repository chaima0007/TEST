import random, math
random.seed(20260705)  # reproductible
N = 100_000

def poisson(lam):
    # Knuth
    L = math.exp(-lam); k = 0; p = 1.0
    while True:
        p *= random.random()
        if p <= L: return k
        k += 1

def simule(l_bra, l_nor, rho=0.0, pen_bra=0.52):
    """rho: inflation du nul (Dixon-Coles simplifié). pen_bra: proba Brésil aux tirs au but."""
    w_bra = w_nul = w_nor = 0; qual_bra = 0
    for _ in range(N):
        b, n = poisson(l_bra), poisson(l_nor)
        # inflation du nul: on rejoue une part des écarts d'1 but vers le nul
        if rho > 0 and abs(b - n) == 1 and random.random() < rho:
            b = n = min(b, n)
        if b > n: w_bra += 1; qual_bra += 1
        elif n > b: w_nor += 1
        else:
            w_nul += 1
            # prolongation (lambdas /3)
            eb, en = poisson(l_bra/3), poisson(l_nor/3)
            if eb > en: qual_bra += 1
            elif eb == en and random.random() < pen_bra: qual_bra += 1
    return 100*w_bra/N, 100*w_nul/N, 100*w_nor/N, 100*qual_bra/N

modeles = [
  ("1. Base (agent: 2.05/1.10)",              2.05, 1.10, 0.00, 0.52),
  ("2. Nul infl. Dixon-Coles",                 2.05, 1.10, 0.12, 0.52),
  ("3. Scénario Norvège+ (Haaland fort, entame BRA ratée)", 1.75, 1.35, 0.00, 0.48),
  ("4. Scénario Brésil+ (Vinicius vs Pedersen exploité)",   2.35, 0.90, 0.00, 0.55),
  ("5. Ancré cotes marché (~55/25/20)",        1.85, 1.05, 0.10, 0.52),
  ("6. Leçon backtest (favori décoté vs bloc)",1.70, 1.00, 0.10, 0.50),
]
res = []
print(f"{'Modèle':<58}{'V.Brésil':>9}{'Nul':>7}{'V.Norv':>8}{'QUALIF BRA':>12}")
for nom, lb, ln, rho, pb in modeles:
    vb, nu, vn, q = simule(lb, ln, rho, pb)
    res.append(q)
    print(f"{nom:<58}{vb:>8.1f}%{nu:>6.1f}%{vn:>7.1f}%{q:>11.1f}%")
res_sorted = sorted(res)
print()
print(f"ENSEMBLE (moyenne des 6 modèles): qualification Brésil = {sum(res)/len(res):.1f}%")
print(f"Fourchette: {res_sorted[0]:.1f}% (pire cas) à {res_sorted[-1]:.1f}% (meilleur cas)")
print(f"Médiane: {(res_sorted[2]+res_sorted[3])/2:.1f}%")
