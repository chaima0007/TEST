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
const { WORLDS, EX, expandSol, accepted, acceptedStrings, tokenPool, isCorrect, diagnose,
        normalizeFree, freeTokens, checkFree, nextBox, dueAt, isMastered, levelInfo,
        xpTotalForLevel, worldStats, isWorldUnlocked, buildQueue, DAY, MASTER_BOX } = ctx;

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
for (const ex of EX) {
  const id = ex.id;
  ok(!ids.has(id), `id dupliqué : ${id}`); ids.add(id);
  ok(typeof ex.w === "number" && WORLDS.some(w => w.n === ex.w), `${id} : monde inconnu`);
  ok(ex.src === "cours" || ex.src === "general", `${id} : champ src invalide`);
  ok(typeof ex.sc === "string" && ex.sc.length > 25, `${id} : scénario trop court`);
  ok(typeof ex.ask === "string" && ex.ask.length > 10, `${id} : consigne trop courte`);
  ok(typeof ex.why === "string" && ex.why.length >= 60, `${id} : explication de concept absente ou trop courte`);
  ok(Array.isArray(ex.sol) && ex.sol.length > 0, `${id} : solution absente`);
  ok(ex.out !== undefined || ex.outCmd !== undefined, `${id} : aucune sortie terminal simulée`);
  ok(ex.traps && Object.keys(ex.traps).length > 0, `${id} : aucune explication de piège`);
}

/* ---------- 2. blocs / pièges cohérents ---------- */
for (const ex of EX) {
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
for (const ex of EX) {
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
for (const ex of EX) {
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
function variants(x) { return ctx.freeVariants(x); }
ok(variants("ls  -l   /home").includes("ls -l /home"), "espaces multiples normalisés");
ok(variants("ls tiret l").includes("ls -l"), "« tiret » recollé à l'option");
ok(variants("ls - l").includes("ls -l"), "tiret détaché recollé à l'option");
ok(variants("cat slash etc slash passwd").includes("cat /etc/passwd"), "« slash » converti et recollé");
ok(variants("cat / etc / passwd").includes("cat /etc/passwd"), "slashs espacés recollés");
ok(variants("cat notes point txt").includes("cat notes.txt"), "« point » converti et recollé");
ok(variants("cd point point").includes("cd .."), "« point point » = ..");
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
for (const ex of EX) {
  if (ex.quiz) continue;
  for (const s of acceptedStrings(ex)) {
    ok(checkFree(ex, s) === "ok", `${ex.id} : clavier libre refuse une réponse valable (${s})`);
    ok(checkFree(ex, " " + s.replace(/ /g, "   ") + " ") === "ok", `${ex.id} : clavier libre sensible aux espaces`);
    const dicte = s.replace(/\//g, " slash ").replace(/(\S)\.(\S)/g, "$1 point $2").replace(/ -/g, " tiret ");
    ok(checkFree(ex, dicte) === "ok", `${ex.id} : clavier libre refuse la dictée (${dicte})`);
  }
}
// et aucune réponse fausse ne doit passer à cause de la tolérance
for (const ex of EX) {
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
ok(nextBox(4, false) === 0, "erreur : retour en boîte 0");
ok(nextBox(MASTER_BOX, true) === MASTER_BOX, "la boîte finale ne dépasse pas le maximum");
const now = 1700000000000;
ok(dueAt(0, now) === now, "boîte 0 : à revoir tout de suite");
ok(dueAt(1, now) === now + DAY, "boîte 1 : demain");
ok(dueAt(5, now) === now + 16 * DAY, "boîte 5 : dans 16 jours");
ok(isMastered({ b: MASTER_BOX }) && !isMastered({ b: 5 }) && !isMastered(null), "détection des commandes ancrées");

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
ok(worldStats(9, p2).total === 0, "worldStats : monde vide toléré");

/* ---------- résultat ---------- */
const counts = {};
EX.forEach(e => counts[e.w] = (counts[e.w] || 0) + 1);
console.log("Exercices par monde :", JSON.stringify(counts), "— total", EX.length);
console.log(`${pass} assertions passées, ${fail} échec(s).`);
if (fail) {
  const uniq = [...new Set(errs)];
  uniq.slice(0, 40).forEach(e => console.log("  ✕ " + e));
  if (uniq.length > 40) console.log(`  … et ${uniq.length - 40} autres`);
  process.exit(1);
}
