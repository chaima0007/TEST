import random, math
random.seed(42)

# Probabilités de qualification de nos 7 pronostics
picks = [("Brésil", .68), ("Angleterre", .55), ("Espagne", .61),
         ("USA", .53), ("Argentine", .78), ("Colombie", .54), ("France", .69)]

# ---- A. DISTRIBUTION: combien de pronostics justes sur 7? (Poisson-binomiale)
dp = [1.0]
for _, p in picks:
    ndp = [0.0]*(len(dp)+1)
    for k, v in enumerate(dp):
        ndp[k] += v*(1-p); ndp[k+1] += v*p
    dp = ndp
print("A. Combien de mes 7 pronostics seront justes?")
for k, v in enumerate(dp):
    bar = '#'*int(v*60)
    print(f"   {k}/7 justes: {v*100:5.1f}%  {bar}")
print(f"   -> Espérance: {sum(k*v for k,v in enumerate(dp)):.1f} pronostics justes sur 7")
print(f"   -> P(les 7 justes) = {dp[7]*100:.1f}%  |  P(au moins 5 justes) = {sum(dp[5:])*100:.1f}%")
print(f"   -> P(au moins 1 surprise) = {(1-dp[7])*100:.1f}%  <- il y aura PRESQUE SUREMENT un upset")
print()

# ---- B. LE MEILLEUR SOUS-ENSEMBLE: quel combiné maximise la proba de tout avoir juste?
from itertools import combinations
print("B. Le meilleur paquet de pronostics (proba que TOUT le paquet soit juste):")
for taille in (2,3,4):
    best = max(combinations(picks, taille), key=lambda c: math.prod(p for _,p in c))
    prob = math.prod(p for _,p in best)
    noms = ' + '.join(n for n,_ in best)
    print(f"   Meilleur {taille} matchs: {noms} = {prob*100:.0f}%")
print("   -> au-delà de 3 matchs, même les meilleurs choix passent sous 50%: le combiné 'sûr' n'existe pas")
print()

# ---- C. TABLE BAYESIENNE EN DIRECT (Brésil-Norvège): la proba PENDANT le match
def quali_live(minute, diff, l_bra=2.05, l_nor=1.10, N=40000):
    """diff = buts Brésil - buts Norvège au moment 'minute'."""
    reste = (90-minute)/90
    q = 0
    for _ in range(N):
        b = diff
        # buts restants
        lb, ln = l_bra*reste, l_nor*reste
        # tirage Poisson
        def pois(lam):
            L=math.exp(-lam); k=0; pr=1.0
            while True:
                pr*=random.random()
                if pr<=L: return k
                k+=1
        b += pois(lb) - pois(ln)
        if b>0: q+=1
        elif b==0:
            eb, en = pois(l_bra/3), pois(l_nor/3)
            if eb>en or (eb==en and random.random()<0.56): q+=1  # 56% TAB (agents)
    return 100*q/N

print("C. Table LIVE Brésil: probabilité de qualification selon le score en cours")
print("   (à garder pendant le match — c'est là que les paris live ont de la valeur)")
for minute in (30, 60, 75):
    ligne = f"   {minute}e minute:  "
    for diff, label in ((1,'Brésil mène +1'), (0,'égalité'), (-1,'Norvège mène +1')):
        ligne += f"{label}: {quali_live(minute, diff):.0f}%   "
    print(ligne)
print()

# ---- D. LA VALEUR DE L'INFO 'CASEMIRO FORFAIT' (sensibilité aux compos)
print("D. Sensibilité aux compos de ce soir (recalcul complet):")
def quali(l_bra, l_nor, pen=0.56, N=60000):
    q=0
    for _ in range(N):
        def pois(lam):
            L=math.exp(-lam); k=0; pr=1.0
            while True:
                pr*=random.random()
                if pr<=L: return k
                k+=1
        b,n = pois(l_bra), pois(l_nor)
        if b>n: q+=1
        elif b==n:
            eb,en = pois(l_bra/3), pois(l_nor/3)
            if eb>en or (eb==en and random.random()<pen): q+=1
    return 100*q/N
print(f"   Compo normale:                 {quali(2.05,1.10):.0f}%")
print(f"   Casemiro forfait (milieu ouvert): {quali(1.95,1.30):.0f}%  <- si annoncé, on retire 6-7 points")
print(f"   Raphinha finalement titulaire:   {quali(2.20,1.10):.0f}%  <- si surprise, on ajoute 3-4 points")
