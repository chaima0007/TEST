/* Tests de la logique du jeu Empire Chaima (public/empire-chaima-linux.html).
   Lancer : node test/empire-chaima-linux.test.js
   Le bloc CORE du fichier HTML est extrait puis évalué tel quel. */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const html = fs.readFileSync(path.join(__dirname, "..", "public", "empire-chaima-linux.html"), "utf8");
const m = html.match(/\/\* =+ CORE:START =+ \*\/([\s\S]*?)\/\* =+ CORE:END =+ \*\//);
if (!m) { console.error("Bloc CORE introuvable dans le fichier HTML"); process.exit(1); }
const ctx = { console };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const { WORLDS, EX, BOSS, dailyQueue, dailyStock, interleave, headVerb, shuffleList, freshWorlds,
        isExamOpen, examProgress, EXAM_MIN, expandSol, accepted, acceptedStrings, tokenPool, isCorrect, diagnose,
        normalizeFree, freeTokens, checkFree, nextBox, dueAt, isMastered, levelInfo,
        xpTotalForLevel, worldStats, isWorldUnlocked, buildQueue, DAY, MASTER_BOX,
        bossFor, isBossOpen, BOSS_UNLOCK, weakList, weakQueue, examQueue, examWorlds,
        buildReport, worldByN, ALLBY } = ctx;

/* exercices + étapes de boss : mêmes règles de qualité et de validation */
const STEPS = BOSS.reduce((a, b) => a.concat(b.steps), []);
const ITEMS = EX.concat(STEPS);

let pass = 0, fail = 0;
const errs = [];
function ok(cond, label) {
  if (cond) pass++;
  else { fail++; errs.push(label); }
}
function shuffle(a, seed) {
  const r = a.slice();
  for (let i = r.length - 1; i > 0; i--) {
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    const j = seed % (i + 1);
    [r[i], r[j]] = [r[j], r[i]];
  }
  return r;
}
function sameSet(a, b) {
  if (a.length !== b.length) return false;
  const x = a.slice().sort(), y = b.slice().sort();
  return x.every((v, i) => v === y[i]);
}

/* ---------- 1. intégrité du contenu ---------- */
const ids = new Set();
for (const ex of ITEMS) {
  const id = ex.id;
  ok(!ids.has(id), `id dupliqué : ${id}`); ids.add(id);
  ok(typeof ex.w === "number" && WORLDS.some(w => w.n === ex.w), `${id} : monde inconnu`);
  ok(["cours", "cours-ubuntu", "general"].includes(ex.src), `${id} : champ src invalide`);
  ok(typeof ex.sc === "string" && ex.sc.length > 25, `${id} : scénario trop court`);
  ok(typeof ex.ask === "string" && ex.ask.length > 10, `${id} : consigne trop courte`);
  ok(typeof ex.why === "string" && ex.why.length >= 60, `${id} : explication de concept absente ou trop courte`);
  ok(Array.isArray(ex.sol) && ex.sol.length > 0, `${id} : solution absente`);
  ok(ex.out !== undefined || ex.outCmd !== undefined, `${id} : aucune sortie terminal simulée`);
  ok(ex.traps && Object.keys(ex.traps).length > 0, `${id} : aucune explication de piège`);
}

/* ---------- 2. blocs / pièges cohérents ---------- */
for (const ex of ITEMS) {
  const accs = accepted(ex);
  const used = new Set();
  accs.forEach(s => s.forEach(t => used.add(t)));
  const blocks = ex.blocks || [];

  ok(blocks.length >= 2, `${ex.id} : moins de 2 blocs pièges`);
  ok(new Set(blocks).size === blocks.length, `${ex.id} : bloc piège en double`);
  for (const b of blocks) {
    ok(!used.has(b), `${ex.id} : le "piège" ${b} fait partie d'une réponse acceptée`);
    ok(ex.traps[b] !== undefined, `${ex.id} : pas d'explication pour le piège ${b}`);
    ok(typeof ex.traps[b] === "string" && ex.traps[b].length > 30, `${ex.id} : explication du piège ${b} trop vague`);
  }
  for (const k of Object.keys(ex.traps)) {
    ok(blocks.includes(k), `${ex.id} : le piège "${k}" n'est proposé dans aucun bloc (message inatteignable)`);
  }
  for (const k of Object.keys(ex.miss || {})) {
    ok(used.has(k), `${ex.id} : miss "${k}" ne fait partie d'aucune réponse`);
  }
  // le plateau contient bien de quoi composer la réponse
  const pool = tokenPool(ex);
  for (const t of accs[0]) {
    const c1 = accs[0].filter(x => x === t).length;
    const c2 = pool.filter(x => x === t).length;
    ok(c2 >= c1, `${ex.id} : bloc manquant sur le plateau (${t})`);
  }
}

/* ---------- 3. toute réponse correcte est reconnue ---------- */
for (const ex of ITEMS) {
  for (const seq of accepted(ex)) {
    ok(isCorrect(ex, seq), `${ex.id} : réponse valable refusée -> ${seq.join(" ")}`);
    // même séquence obtenue via le plateau mélangé
    const pool = shuffle(tokenPool(ex), 7);
    const built = [];
    const copy = pool.slice();
    for (const t of seq) {
      const i = copy.indexOf(t);
      ok(i >= 0, `${ex.id} : impossible de composer ${t} depuis le plateau`);
      copy.splice(i, 1); built.push(t);
    }
    ok(isCorrect(ex, built), `${ex.id} : composition depuis le plateau refusée`);
  }
}

/* ---------- 4. toute réponse fausse est refusée, avec un message ciblé ---------- */
for (const ex of ITEMS) {
  const accs = accepted(ex);
  const base = accs[0];

  // 4a. un bloc piège ajouté -> message du piège
  for (const b of (ex.blocks || [])) {
    const wrong = base.concat([b]);
    ok(!isCorrect(ex, wrong), `${ex.id} : réponse avec le piège ${b} acceptée à tort`);
    const d = diagnose(ex, wrong);
    ok(d.reason === ex.traps[b], `${ex.id} : le piège ${b} ne déclenche pas son explication`);
    ok(typeof d.why === "string" && d.why.length > 0, `${ex.id} : diagnostic sans concept`);
  }

  // 4b. un bloc retiré -> refusé, et message d'incomplétude
  if (base.length > 1) {
    for (let i = 0; i < base.length; i++) {
      const wrong = base.slice(0, i).concat(base.slice(i + 1));
      if (accs.some(a => a.join(" ") === wrong.join(" "))) continue;
      ok(!isCorrect(ex, wrong), `${ex.id} : commande incomplète acceptée -> ${wrong.join(" ")}`);
      const d = diagnose(ex, wrong);
      ok(d.reason && d.reason.length > 20, `${ex.id} : diagnostic vide pour une commande incomplète`);
    }
  }

  // 4c. mauvais ordre (mêmes blocs) -> refusé + message d'ordre
  if (base.length > 1) {
    const rev = base.slice().reverse();
    if (!accs.some(a => a.join(" ") === rev.join(" "))) {
      ok(!isCorrect(ex, rev), `${ex.id} : ordre inversé accepté -> ${rev.join(" ")}`);
      const d = diagnose(ex, rev);
      ok(d.order === true, `${ex.id} : l'inversion d'ordre n'est pas diagnostiquée comme telle`);
      ok(d.reason.indexOf("Forme attendue") > 0, `${ex.id} : le message d'ordre ne montre pas la forme attendue`);
    }
  }

  // 4d. réponse vide
  ok(!isCorrect(ex, []), `${ex.id} : réponse vide acceptée`);
  ok(diagnose(ex, []).reason.length > 10, `${ex.id} : pas de message pour une réponse vide`);

  // 4e. doublon d'un bloc
  const dup = base.concat([base[0]]);
  if (!accs.some(a => a.join(" ") === dup.join(" "))) {
    ok(!isCorrect(ex, dup), `${ex.id} : doublon accepté`);
    ok(diagnose(ex, dup).reason.length > 10, `${ex.id} : pas de message pour un doublon`);
  }
}

/* ---------- 5. permutations : uniquement celles déclarées ---------- */
const la = EX.find(e => e.id === "w1-ls-la");
ok(isCorrect(la, ["ls", "-l", "-a"]), "ls -l -a doit être accepté");
ok(isCorrect(la, ["ls", "-a", "-l"]), "ls -a -l doit être accepté");
ok(isCorrect(la, ["ls", "-la"]), "ls -la doit être accepté");
ok(isCorrect(la, ["ls", "-al"]), "ls -al doit être accepté");
ok(!isCorrect(la, ["-l", "-a", "ls"]), "la commande doit commencer par ls");
ok(!isCorrect(la, ["ls", "-l"]), "ls -l ne répond pas à la consigne fichiers cachés");
const cp = EX.find(e => e.id === "w1-cp");
ok(isCorrect(cp, ["cp", "config.txt", "config.txt.bak"]), "cp source destination");
ok(!isCorrect(cp, ["cp", "config.txt.bak", "config.txt"]), "source et destination inversées doivent être refusées");
ok(diagnose(cp, ["cp", "config.txt.bak", "config.txt"]).order === true, "inversion source/destination = problème d'ordre");
const home = EX.find(e => e.id === "w1-cd-home");
["cd"].forEach(x => ok(isCorrect(home, [x]), "cd seul accepté"));
ok(isCorrect(home, ["cd", "~"]), "cd ~ accepté");
ok(isCorrect(home, ["cd", "/home/chaima"]), "cd /home/chaima accepté");

/* ---------- 6. expandSol ---------- */
ok(expandSol(["a", { p: ["-x", "-y"] }]).length === 2, "expandSol : 2 permutations attendues");
ok(sameSet(expandSol(["a", { p: ["-x", "-y"] }]).map(s => s.join(" ")), ["a -x -y", "a -y -x"]), "expandSol : permutations correctes");
ok(sameSet(expandSol([{ any: ["a", "b"] }, "z"]).map(s => s.join(" ")), ["a z", "b z"]), "expandSol : any correct");
let threw = false; try { expandSol([{ zz: 1 }]); } catch (e) { threw = true; }
ok(threw, "expandSol : une partie invalide doit lever une erreur");

/* ---------- 7. clavier libre / dictée ---------- */
function variants(x) { return [ctx.freeGroups(x).join(" ")]; }
ok(variants("ls  -l   /home").includes("ls -l /home"), "espaces multiples normalisés");
ok(variants("ls tiret l").includes("ls -l"), "« tiret » recollé à l'option");
ok(variants("ls - l").includes("ls -l"), "tiret détaché recollé à l'option");
ok(variants("cat slash etc slash passwd").includes("cat /etc/passwd"), "« slash » converti et recollé");
ok(variants("cat / etc / passwd").includes("cat /etc/passwd"), "slashs espacés recollés");
ok(variants("cat notes point txt").includes("cat notes.txt"), "« point » converti et recollé");
ok(checkFree(EX.find(e => e.id === "w1-cd-parent"), "cd point point") === "ok", "« point point » dicté = cd ..");
ok(variants("su tiret paul").includes("su - paul"), "un tiret isolé peut rester séparé");
ok(variants("scp tiret P 2222 f").includes("scp -P 2222 f"), "casse préservée (-P)");
ok(variants("mv rapport-final.txt archives").includes("mv rapport-final.txt archives"), "tiret interne préservé");
const catEx = EX.find(e => e.id === "w1-cat");
ok(checkFree(catEx, "cat notes.txt") === "ok", "clavier libre : réponse exacte");
ok(checkFree(catEx, "cat notes point txt") === "ok", "clavier libre : dictée tolérée");
ok(checkFree(catEx, "CAT notes.txt") === "casse", "clavier libre : erreur de casse détectée");
ok(checkFree(catEx, "less notes.txt") === "non", "clavier libre : mauvaise commande refusée");
ok(checkFree(catEx, "cat notes txt") === "non", "clavier libre : token manquant refusé");
ok(checkFree(catEx, "   ") === "non", "clavier libre : saisie vide refusée");
const suEx = EX.find(e => e.id === "w3-su");
ok(checkFree(suEx, "su - paul") === "ok", "clavier libre : su - paul");
ok(checkFree(suEx, "su tiret paul") === "ok", "clavier libre : su dicté");
ok(checkFree(suEx, "su paul") === "non", "clavier libre : su sans tiret refusé");
ok(checkFree(suEx, "su -paul") === "non", "clavier libre : su -paul refusé");
const shEx = EX.find(e => e.id === "w3-shadow");
ok(checkFree(shEx, "sudo cat slash etc slash shadow") === "ok", "clavier libre : chemin dicté");
ok(checkFree(shEx, "cat /etc/shadow") === "non", "clavier libre : sudo manquant refusé");
// aucune réponse valable ne doit être refusée, quelle que soit la façon de la saisir
for (const ex of ITEMS) {
  if (ex.quiz) continue;
  for (const s of acceptedStrings(ex)) {
    ok(checkFree(ex, s) === "ok", `${ex.id} : clavier libre refuse une réponse valable (${s})`);
    ok(checkFree(ex, " " + s.replace(/ /g, "   ") + " ") === "ok", `${ex.id} : clavier libre sensible aux espaces`);
    const dicte = s.replace(/\//g, " slash ").replace(/(\S)\.(\S)/g, "$1 point $2").replace(/ -/g, " tiret ");
    ok(checkFree(ex, dicte) === "ok", `${ex.id} : clavier libre refuse la dictée (${dicte})`);
  }
}
// et aucune réponse fausse ne doit passer à cause de la tolérance
for (const ex of ITEMS) {
  if (ex.quiz) continue;
  const base = accepted(ex)[0];
  for (const b of (ex.blocks || [])) {
    ok(checkFree(ex, base.concat([b]).join(" ")) === "non", `${ex.id} : clavier libre accepte le piège ${b}`);
  }
  if (base.length > 1) {
    const short = base.slice(0, -1).join(" ");
    if (!acceptedStrings(ex).includes(short)) {
      ok(checkFree(ex, short) === "non", `${ex.id} : clavier libre accepte une commande incomplète`);
    }
  }
}

/* ---------- 8. révision espacée ---------- */
ok(nextBox(0, true) === 1 && nextBox(3, true) === 4, "bonne réponse : boîte suivante");
ok(nextBox(2, false) === 0, "erreur sur un item fragile : retour en boîte 0");
ok(nextBox(5, false) === 3, "erreur sur un item ancien : recul de deux boîtes, pas de remise à zéro");
ok(nextBox(3, false) === 1, "le recul ne descend jamais sous la boîte 1 depuis la boîte 3");
ok(nextBox(MASTER_BOX, true) === MASTER_BOX, "la boîte finale ne dépasse pas le maximum");
const now = 1700000000000;
ok(dueAt(0, now) === now, "boîte 0 : à revoir tout de suite");
ok(dueAt(1, now) === now + DAY, "boîte 1 : demain");
ok(dueAt(3, now) === now + 7 * DAY, "boîte 3 : dans une semaine");
ok(dueAt(MASTER_BOX, now) === now + 14 * DAY, "une commande ancrée revient en entretien deux semaines plus tard");
{ // une commande doit pouvoir s'ancrer avant l'examen
  let b = 0, jours = 0, rappels = 0;
  while (b < MASTER_BOX) { b = nextBox(b, true); jours = Math.round(dueAt(b, 0) / DAY); rappels++; }
  ok(rappels <= 4, `ancrage atteint en ${rappels} rappels`);
  ok(jours <= 14, `ancrage atteint au jour ${jours}, avant l'échéance d'examen`);
}
ok(isMastered({ b: MASTER_BOX }) && !isMastered({ b: MASTER_BOX - 1 }) && !isMastered(null), "détection des commandes ancrées");

const prog = {};
const w1 = EX.filter(e => e.w === 1);
w1.forEach(e => { prog[e.id] = { b: 0, due: 0, n: 0, ok: 0, ko: 0 }; });
let q = buildQueue(1, prog, now, 8);
ok(q.length === 8, "file : taille de session respectée");
prog[w1[0].id] = { b: 0, due: now - 10, n: 3, ok: 1, ko: 2 };
prog[w1[5].id] = { b: 4, due: now + 5 * DAY, n: 2, ok: 2, ko: 0 };
q = buildQueue(1, prog, now, 8);
ok(q[0].id === w1[0].id, "file : la commande ratée passe en premier");
ok(!q.slice(0, 6).some(e => e.id === w1[5].id), "file : une commande bien sue n'est pas répétée tout de suite");
w1.forEach(e => { prog[e.id] = { b: MASTER_BOX, due: now + 30 * DAY, n: 9, ok: 9, ko: 0 }; });
prog[w1[2].id] = { b: 0, due: now - 1, n: 4, ok: 1, ko: 3 };
q = buildQueue(1, prog, now, 8);
ok(q[0].id === w1[2].id, "file : seule la commande non ancrée revient en tête");

/* ---------- 8 bis. révision du jour, tous mondes confondus ---------- */
{
  const now2 = 1700000000000;
  const prog = {};
  const w1 = EX.filter(e => e.w === 1);
  const w4 = EX.filter(e => e.w === 4);
  // monde 1 entièrement en retard, mondes 2 et 3 sus, monde 4 débloqué et neuf
  EX.filter(e => e.w <= 3).forEach(e => { prog[e.id] = { b: 2, due: now2 + 9 * DAY, n: 2, ok: 2, ko: 0 }; });
  w1.forEach(e => { prog[e.id] = { b: 1, due: now2 - 5 * DAY, n: 2, ok: 2, ko: 0 }; });
  const q = dailyQueue(prog, now2, 8);
  ok(q.length === 8, "la série du jour fait la taille demandée");
  ok(q.some(e => e.w === 1), "elle sert les commandes en retard d'un monde déjà terminé");
  ok(q.some(e => e.w !== 1), "elle mélange plusieurs mondes dans la même série");
  const dus = q.filter(e => prog[e.id] && prog[e.id].due <= now2).length;
  ok(dus === 5, `au plus 5 rappels dus sur 8 questions (${dus})`);
  ok(new Set(q.map(e => e.id)).size === q.length, "aucun doublon dans la série du jour");
  // une commande ancrée n'est proposée qu'en entretien, une fois son échéance passée
  const prog2 = {};
  EX.filter(e => e.w === 1).forEach(e => { prog2[e.id] = { b: MASTER_BOX, due: now2 + 10 * DAY, n: 9, ok: 9, ko: 0 }; });
  ok(dailyQueue(prog2, now2, 8).every(e => !isMastered(prog2[e.id]) || prog2[e.id].due <= now2),
     "une commande ancrée non échue ne revient pas");
  const prog3 = {};
  EX.filter(e => e.w === 1).forEach(e => { prog3[e.id] = { b: MASTER_BOX, due: now2 - DAY, n: 9, ok: 9, ko: 0 }; });
  ok(dailyQueue(prog3, now2, 8).length > 0, "une commande ancrée échue revient en entretien");
  // elle ne pioche jamais dans un monde verrouillé
  ok(dailyQueue({}, now2, 8).every(e => e.w === 1), "sur une progression vierge, seul le monde 1 est servi");
  ok(dailyStock(prog, now2).due.length >= w1.length - 1, "le stock du jour compte les commandes en retard");
  ok(dailyStock(prog, now2).fresh.some(e => e.w === 4) === isWorldUnlocked(4, prog),
     "le stock de nouveautés suit les mondes débloqués");
}

/* ---------- 8 ter. entrelacement ---------- */
{
  const maxRun = (arr) => { let m = 1, r = 1; for (let i = 1; i < arr.length; i++) { r = arr[i] === arr[i - 1] ? r + 1 : 1; m = Math.max(m, r); } return m; };
  // monde 1 : les familles de commandes sont variées, la règle des deux d'affilée tient
  const w1x = EX.filter(e => e.w === 1);
  ok(maxRun(w1x.map(headVerb)) > 2, "le contenu déclaré est groupé par famille de commandes");
  ok(maxRun(interleave(w1x).map(headVerb)) <= 2,
     `après entrelacement, jamais plus de deux commandes de la même famille (${maxRun(interleave(w1x).map(headVerb))})`);
  // monde 12 : presque tout est firewall-cmd, l'entrelacement ne peut qu'améliorer
  const w12 = EX.filter(e => e.w === 12).slice(0, 10);
  ok(maxRun(interleave(w12).map(headVerb)) <= maxRun(w12.map(headVerb)),
     "sur un monde presque mono-commande, l'entrelacement ne dégrade jamais l'ordre");
  ok(interleave(w12).length === w12.length, "l'entrelacement ne perd aucun exercice");
  ok(new Set(interleave(w12).map(e => e.id)).size === w12.length, "l'entrelacement ne duplique aucun exercice");
  ok(headVerb(EX.find(e => e.id === "w12-add-service")) === "firewall-cmd", "le verbe de tête ignore sudo");
  const q = buildQueue(1, {}, Date.now(), 8);
  ok(maxRun(q.map(headVerb)) <= 2, "la première série d'un monde est entrelacée");
}

/* ---------- 8 quater. périmètre des nouveautés et accès à l'examen ---------- */
{
  const now3 = 1700000000000;
  const prog = {};
  EX.filter(e => e.w === 1).slice(0, 17).forEach(e => { prog[e.id] = { b: 1, due: now3 - DAY, n: 1, ok: 1, ko: 0 }; });
  const mondes = [...new Set(dailyQueue(prog, now3, 8).map(e => e.w))];
  ok(mondes.every(w => w <= 2), `la série du jour ne découvre pas un monde lointain (${mondes.join(",")})`);
  ok(freshWorlds(EX).length === 2, "au plus deux mondes de découverte à la fois");
  ok(worldByN(10).req === 7, "le monde console attend que find soit vu (monde 7)");
  ok(worldByN(11).req === 6, "le labo SSH attend systemctl, les paquets et le réseau");
  ok(worldByN(12).req === 4, "le pare-feu attend la gestion des services");
  ok(!isExamOpen({}), "l'examen est fermé au départ");
  const gros = {};
  EX.slice(0, EXAM_MIN).forEach(e => { gros[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(examProgress(gros) === EXAM_MIN, "le compteur d'accès à l'examen suit les commandes réussies");
  ok(isExamOpen(gros), `l'examen s'ouvre à ${EXAM_MIN} commandes réussies`);
  const rates = {};
  EX.slice(0, EXAM_MIN).forEach(e => { rates[e.id] = { b: 0, due: 0, n: 3, ok: 0, ko: 3 }; });
  ok(!isExamOpen(rates), "des tentatives sans réussite n'ouvrent pas l'examen");
}

/* ---------- 9. niveaux ---------- */
ok(levelInfo(0).lvl === 1, "0 XP -> niveau 1");
ok(xpTotalForLevel(2) === 60 && xpTotalForLevel(3) === 150, "seuils de niveaux attendus");
ok(levelInfo(59).lvl === 1 && levelInfo(60).lvl === 2, "passage de niveau au bon seuil");
let prev = 0;
for (let xp = 0; xp < 5000; xp += 7) {
  const li = levelInfo(xp);
  ok(li.lvl >= prev, "les niveaux ne redescendent jamais"); prev = li.lvl;
  ok(li.into >= 0 && li.into < li.span, `barre XP hors bornes à ${xp} XP`);
  ok(typeof li.title === "string" && li.title.length > 3, "titre de niveau manquant");
  if (xp === 4000) ok(li.title !== levelInfo(1620).title, "il reste des titres à gagner au-delà du niveau 10");
}

/* ---------- 10. déblocage des mondes ---------- */
const p2 = {};
ok(isWorldUnlocked(1, p2), "le monde 1 est toujours ouvert");
ok(!isWorldUnlocked(2, p2), "le monde 2 est fermé au départ");
ok(!isWorldUnlocked(4, p2), "un monde encore en préparation reste fermé");
const list1 = EX.filter(e => e.w === 1);
list1.slice(0, Math.ceil(list1.length * 0.5)).forEach(e => { p2[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
ok(!isWorldUnlocked(2, p2), "50% ne suffit pas à ouvrir le monde 2");
list1.slice(0, Math.ceil(list1.length * 0.6)).forEach(e => { p2[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
ok(isWorldUnlocked(2, p2), "60% ouvre le monde 2");
ok(worldStats(1, p2).total === list1.length, "worldStats : total correct");
ok(worldStats(99, p2).total === 0, "worldStats : monde inexistant toléré");

/* ---------- 11. boss de fin de monde ---------- */
for (const b of BOSS) {
  ok(worldByN(b.w) && !worldByN(b.w).soon, `boss du monde ${b.w} : monde inconnu`);
  ok(typeof b.name === "string" && b.name.length > 4, `boss ${b.w} : nom manquant`);
  ok(typeof b.intro === "string" && b.intro.length > 60, `boss ${b.w} : mise en situation trop courte`);
  ok(typeof b.xp === "number" && b.xp > 0, `boss ${b.w} : récompense manquante`);
  ok(b.steps.length >= 4, `boss ${b.w} : moins de 4 étapes (${b.steps.length})`);
  for (const st of b.steps) {
    ok(st.w === b.w, `étape ${st.id} : monde incohérent avec son boss`);
    ok(/^Étape \d/.test(st.sc), `étape ${st.id} : la narration ne situe pas l'étape`);
    ok(EX.every(e => e.id !== st.id), `étape ${st.id} : identifiant en conflit avec un exercice`);
  }
  // les commandes du boss doivent appartenir au vocabulaire du monde
  const vocab = new Set();
  EX.filter(e => e.w === b.w).forEach(e => accepted(e).forEach(sq => sq.forEach(t => vocab.add(t))));
  for (const st of b.steps) {
    const first = accepted(st)[0][0];
    ok(vocab.has(first), `étape ${st.id} : « ${first} » n'apparaît dans aucun exercice du monde ${b.w}`);
  }
}
{
  const remplis = WORLDS.filter(w => EX.some(e => e.w === w.n)).map(w => w.n);
  ok(remplis.every(n => bossFor(n)), "chaque monde rempli a son boss");
  ok(BOSS.length === remplis.length, `un boss par monde rempli attendu (${remplis.length}), ${BOSS.length} trouvés`);
}
{
  const p = {};
  ok(!isBossOpen(1, p), "le boss du monde 1 est fermé au départ");
  const l1 = EX.filter(e => e.w === 1);
  l1.slice(0, Math.ceil(l1.length * 0.6)).forEach(e => { p[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(!isBossOpen(1, p), "60% ne suffit pas à ouvrir le boss");
  l1.slice(0, Math.ceil(l1.length * BOSS_UNLOCK)).forEach(e => { p[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(isBossOpen(1, p), "70% ouvre le boss du monde 1");
  ok(!isBossOpen(2, p), "le boss d'un monde verrouillé reste fermé");
  ok(bossFor(99) === null, "aucun boss pour un monde inexistant");
}

/* ---------- 12. mondes hors chaîne principale ---------- */
{
  const p = {};
  ok(!isWorldUnlocked(10, p), "le monde bonus est fermé au départ");
  const l1 = EX.filter(e => e.w === 1);
  l1.slice(0, Math.ceil(l1.length * 0.6)).forEach(e => { p[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(!isWorldUnlocked(10, p), "le monde console attend son prérequis réel, pas seulement le monde 1");
  const l7 = EX.filter(e => e.w === 7);
  l7.slice(0, Math.ceil(l7.length * 0.6)).forEach(e => { p[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(isWorldUnlocked(10, p), "le monde console s'ouvre une fois find maîtrisé (monde 7)");
  ok(!isWorldUnlocked(9, p), "le monde 9 reste soumis à la chaîne principale");
  const p2 = {};
  const l6 = EX.filter(e => e.w === 6);
  l6.slice(0, Math.ceil(l6.length * 0.6)).forEach(e => { p2[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; });
  ok(isWorldUnlocked(11, p2), "le labo SSH s'ouvre après le monde réseau, sans attendre le monde 10");
}

/* ---------- 13. fiche des points faibles ---------- */
{
  const prog = {};
  const a = EX[0], b2 = EX[1], c = EX[2];
  prog[a.id] = { b: 0, due: 0, n: 5, ok: 1, ko: 4, last: 1700000000000 };
  prog[b2.id] = { b: 1, due: 0, n: 3, ok: 2, ko: 1, last: 1700000100000 };
  prog[c.id] = { b: 3, due: 0, n: 3, ok: 3, ko: 0, last: 1700000200000 };
  const w = weakList(prog, 0);
  ok(w.length === 2, "seules les commandes ratées entrent dans la fiche");
  ok(w[0].ex.id === a.id, "la commande la plus ratée arrive en tête");
  ok(w[0].cmd === accepted(a)[0].join(" "), "la fiche montre la commande attendue");
  ok(weakList(prog, 1).length === 1, "la fiche se limite au nombre demandé");
  const q = weakQueue(prog, Date.now(), 8);
  ok(q.length === 2 && q[0].id === a.id, "l'entraînement ciblé reprend les commandes ratées");
  prog[a.id].b = MASTER_BOX;
  ok(weakQueue(prog, Date.now(), 8).every(e => e.id !== a.id), "une commande ancrée sort de l'entraînement ciblé");
  ok(weakList(prog, 0).some(e => e.ex.id === a.id), "mais son historique d'erreurs reste dans la fiche");

  const state = { xp: 300, streak: 4, best: 6, prog: prog, boss: { 1: { done: true, best: "4/4" } },
                  log: [{ t: 1700000000000, id: a.id, mode: "série" }, { t: 1700000100000, id: "b1-1", mode: "boss" }] };
  const rep = buildReport(state, 1700000300000);
  ok(rep.indexOf("FICHE — MES POINTS FAIBLES") === 0, "la fiche exportée a un en-tête");
  ok(rep.includes("RÉSUMÉ PAR MONDE") && rep.includes("COMMANDES À RETRAVAILLER") && rep.includes("JOURNAL DES ERREURS"),
     "la fiche exportée contient ses trois sections");
  ok(rep.includes("boss vaincu (4/4)"), "la fiche exportée mentionne les boss vaincus");
  ok(rep.includes(accepted(a)[0].join(" ")), "la fiche exportée cite la commande ratée");
  ok(rep.includes(a.why.slice(0, 40)), "la fiche exportée rappelle le concept");
  ok(!rep.includes("undefined") && !rep.includes("NaN"), "la fiche exportée ne contient ni undefined ni NaN");
  ok(buildReport({ xp: 0, prog: {}, log: [] }, Date.now()).includes("Aucune erreur enregistrée"),
     "la fiche fonctionne sur une progression vierge");
}

/* ---------- 14. mode examen ---------- */
{
  const prog = {};
  EX.forEach(e => { prog[e.id] = { b: 2, due: 0, n: 2, ok: 2, ko: 0 }; });
  const worlds = examWorlds(prog);
  ok(worlds.length >= 12, `tous les mondes débloqués alimentent l'examen (${worlds.length})`);
  let seed = 42;
  const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
  const q = examQueue(prog, 12, rnd);
  ok(q.length === 12, `l'examen tire 12 questions (${q.length})`);
  ok(new Set(q.map(e => e.id)).size === q.length, "aucune question en double dans l'examen");
  const per = {};
  q.forEach(e => per[e.w] = (per[e.w] || 0) + 1);
  ok(Object.values(per).every(v => v <= 6), "pas plus de la moitié des questions dans un même monde");
  ok(Object.keys(per).length >= 3, "l'examen mélange plusieurs mondes");
  const vierge = examQueue({}, 12, rnd);
  ok(vierge.every(e => e.w === 1), "sur une progression vierge, l'examen ne pioche que dans le monde 1");
}

/* ---------- résultat ---------- */
const counts = {};
EX.forEach(e => counts[e.w] = (counts[e.w] || 0) + 1);
console.log("Exercices par monde :", JSON.stringify(counts), "— total", EX.length);
console.log("Boss :", BOSS.length, "— étapes de boss :", STEPS.length);
console.log(`${pass} assertions passées, ${fail} échec(s).`);
if (fail) {
  const uniq = [...new Set(errs)];
  uniq.slice(0, 40).forEach(e => console.log("  ✕ " + e));
  if (uniq.length > 40) console.log(`  … et ${uniq.length - 40} autres`);
  process.exit(1);
}
