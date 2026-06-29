# Module Day Trading — Options

Stratégie de day trading sur **options**, alimentée par les données **Yahoo Finance**
et reliée à un **courtier** (Alpaca) pour l'exécution des ordres.

> ⚠️ **Avertissement.** Outil **éducatif**. Le trading d'options comporte un risque de
> perte **totale et rapide** du capital. Le module est en **paper / dry-run par défaut** :
> aucun ordre réel n'est envoyé tant que des clés API ne sont pas configurées **et** qu'une
> confirmation explicite n'est pas fournie. Aucune garantie de performance — backtestez
> toujours avant tout usage.

## La stratégie : Momentum VWAP / EMA

Signal calculé sur le **sous-jacent** (bougies 5 min par défaut), via la confluence de
quatre conditions :

| Brique | Rôle |
|---|---|
| **EMA 9 vs EMA 21** | Direction de la tendance (croisement = signal frais) |
| **VWAP** | Filtre : on n'achète qu'au-dessus, on ne vend qu'en dessous |
| **RSI 14** | Momentum dans une zone saine (ni surachat ni survente extrême) |
| **ATR 14** | Volatilité → niveaux de stop-loss et take-profit |

- **Signal LONG** → achat d'un **CALL** : EMA9 > EMA21, prix > VWAP, RSI ∈ [50 ; 72].
- **Signal SHORT** → achat d'un **PUT** : EMA9 < EMA21, prix < VWAP, RSI ≤ 48.
- Gestion du risque : stop = 1,5 × ATR, objectif = 2,5 × ATR. Pas de position overnight
  (clôture en fin de séance dans le backtest).

Le contrat d'option est choisi automatiquement dans la chaîne Yahoo : strike le plus
proche de la monnaie (ATM) par défaut, avec un décalage OTM configurable, en privilégiant
la liquidité. Le risque d'une option longue est borné à la prime payée, ce qui sert au
dimensionnement de position.

## Architecture

```
lib/trading/
  types.ts        Types partagés
  indicators.ts   SMA, EMA, RSI, ATR, VWAP
  yahoo.ts        Bougies OHLCV (API chart Yahoo Finance)
  options.ts      Chaîne d'options + sélection du contrat
  strategy.ts     Calcul des indicateurs, génération du signal, sizing
  backtest.ts     Moteur de backtest (stop/target/signal/EOD)
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
