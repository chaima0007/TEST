# Module Day Trading — Options

Stratégie de day trading sur **options**, alimentée par les données **Yahoo Finance**
et reliée à un **courtier** (Alpaca) pour l'exécution des ordres.

> ⚠️ **Avertissement.** Outil **éducatif**. Le trading d'options comporte un risque de
> perte **totale et rapide** du capital. Le module est en **paper / dry-run par défaut** :
> aucun ordre réel n'est envoyé tant que des clés API ne sont pas configurées **et** qu'une
> confirmation explicite n'est pas fournie. Aucune garantie de performance — backtestez
> toujours avant tout usage.

## La stratégie : Momentum multi-confluences

Signal calculé sur le **sous-jacent** (bougies 5 min par défaut). On n'entre que lorsque
plusieurs signaux indépendants s'alignent, et **uniquement quand le marché a une vraie
tendance** (filtre ADX, pour éviter les marchés en range où le momentum échoue).

**Filtres durs (obligatoires) :**

| Brique | Rôle |
|---|---|
| **ADX 14 ≥ 20** | Force de tendance — sous le seuil, marché sans tendance → on s'abstient |
| **EMA 50** | Direction de fond : prix du bon côté de l'EMA de tendance |
| **EMA 9 vs EMA 21** | Tendance court terme |
| **VWAP** | Prix du bon côté du VWAP de la séance |

**Confirmations (score de confluence, ≥ 3 sur 5 requises) :**

| Brique | Rôle |
|---|---|
| **MACD (12/26/9)** | Histogramme du bon signe / en accélération |
| **RSI 14** | Momentum dans une zone saine |
| **+DI / -DI** | Dominance directionnelle cohérente |
| **Volume relatif** | Participation ≥ moyenne (volume / SMA volume) |
| **Stochastique 14** | Pas en zone extrême opposée |
| **Bandes de Bollinger** | Contexte de volatilité (exposé dans le signal) |
| **ATR 14** | Volatilité → stops et objectifs |

- **Signal LONG** → achat d'un **CALL** ; **Signal SHORT** → achat d'un **PUT**.
- La confiance du signal reflète le nombre de confirmations validées et la force de la tendance.

Le contrat d'option est choisi automatiquement dans la chaîne Yahoo : strike le plus
proche de la monnaie (ATM) par défaut, avec un décalage OTM configurable, en privilégiant
la liquidité. Le risque d'une option longue est borné à la prime payée, ce qui sert au
dimensionnement de position.

## Gestion de position (money & risk management)

Simulée bougie par bougie dans le backtest, paramétrable via `RiskParams` :

- **Stop initial** à 1,5 × ATR (= 1 R, l'unité de risque).
- **Prise partielle au TP1** (1 R) : on encaisse 50 % de la position…
- **…puis break-even** : le stop du reliquat remonte au prix d'entrée (trade « sans risque »).
- **Stop suiveur « chandelier »** (2,5 × ATR) activé après 1,5 R de profit, pour laisser
  courir les gains.
- **Objectif final TP2** à 3 × ATR.
- **Sortie sur signal inverse** et **clôture forcée en fin de séance** (aucune position overnight).
- **Garde-fous journaliers** : max 4 trades/jour, arrêt après −2 R cumulés sur la journée,
  pas de nouvelle entrée dans les 3 dernières bougies de la séance.

## Architecture

```
lib/trading/
  types.ts        Types partagés
  indicators.ts   SMA, EMA, RSI, ATR, VWAP, MACD, Bollinger, ADX, Stochastique, volume relatif
  yahoo.ts        Bougies OHLCV (API chart Yahoo Finance)
  options.ts      Chaîne d'options + sélection du contrat
  strategy.ts     Indicateurs, signal multi-confluences, sizing, params de risque
  backtest.ts     Backtest avec gestion de position (TP1 partiel, break-even, trailing, garde-fous)
  broker.ts       Client courtier Alpaca (paper/live, dry-run, garde-fous)
  bot.ts          Orchestrateur : données → signal → contrat → ordre

app/api/trading/
  signal/         GET  signal courant
  candles/        GET  bougies + indicateurs
  options/        GET  chaîne d'options + contrat sélectionné
  backtest/       GET  backtest de la stratégie
  account/        GET  état du compte courtier
  order/          POST exécute le pipeline complet (bot)

app/trading/      Tableau de bord (UI)
scripts/trade-bot.ts   Bot exécutable en CLI (cron-friendly)
```

## Utilisation

### Interface web

```bash
npm run dev
```
Ouvrir http://localhost:3000/trading

### API

```bash
# Signal courant
curl "http://localhost:3000/api/trading/signal?symbol=AAPL&interval=5m&range=5d"

# Backtest (1 mois de bougies 5m)
curl "http://localhost:3000/api/trading/backtest?symbol=AAPL&interval=5m&range=1mo"

# Pipeline complet (analyse seule, aucun ordre)
curl -X POST http://localhost:3000/api/trading/order \
  -H 'Content-Type: application/json' \
  -d '{"symbol":"AAPL","analyzeOnly":true}'
```

### CLI / cron

```bash
# Analyse seule (aucun ordre)
npx tsx scripts/trade-bot.ts AAPL --analyze

# Paper trading (clés requises) — risque 1 % d'un capital de 20 000
ALPACA_KEY_ID=... ALPACA_SECRET_KEY=... ALPACA_ENV=paper \
  npx tsx scripts/trade-bot.ts AAPL --capital 20000 --risk 1 --min-conf 0.65
```

Exemple de cron (toutes les 5 min en séance US, lun-ven) :
```cron
*/5 13-20 * * 1-5  cd /chemin/projet && npx tsx scripts/trade-bot.ts AAPL >> trade.log 2>&1
```

## Brancher le courtier (Alpaca)

1. Créez un compte sur https://alpaca.markets et activez le **trading d'options** (paper d'abord).
2. Générez une paire de clés API.
3. Copiez `.env.example` → `.env.local` et renseignez `ALPACA_KEY_ID`, `ALPACA_SECRET_KEY`.
4. Gardez `ALPACA_ENV=paper`. Le passage en `live` (argent réel) exige en plus que le code
   transmette la confirmation `"LIVE"` (`--live` en CLI), garde-fou contre les envois accidentels.

Sans clés, tout fonctionne en **dry-run** : le signal et le contrat sont calculés, l'ordre
est simulé mais jamais envoyé.

## Limites connues

- **Réseau** : l'accès à `query1.finance.yahoo.com` doit être autorisé par votre
  environnement. Certains réseaux (proxys d'entreprise, CI) le bloquent.
- Le backtest est réalisé sur le **sous-jacent**. Le P&L réel d'une option dépend du delta,
  de la volatilité implicite et du theta, non modélisés ici — les résultats du backtest ne
  reflètent donc pas exactement le rendement d'une position en options.
- Données Yahoo Finance non officielles, fournies sans garantie ; à usage personnel.
