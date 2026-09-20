/* Parcours long : le jeu tient-il sur plusieurs semaines d'usage quotidien ?
   Simule 30 jours de séances au niveau du moteur (mêmes fonctions que l'interface).
   Lancer : node test/empire-chaima-linux.parcours.test.js */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const html = fs.readFileSync(path.join(__dirname, "..", "public", "empire-chaima-linux.html"), "utf8");
const m = html.match(/\/\* =+ CORE:START =+ \*\/([\s\S]*?)\/\* =+ CORE:END =+ \*\//);
const ctx = { console };
vm.createContext(ctx);
vm.runInContext(m[1], ctx);
const { EX, WORLDS, dailyQueue, dailyStock, nextBox, dueAt, isMastered, DAY,
        levelInfo, isWorldUnlocked, isExamOpen, examProgress, weakList, isBossOpen } = ctx;

let pass = 0, fail = 0; const errs = [];
const ok = (c, l) => { if (c) pass++; else { fail++; errs.push(l); } };

/* Une joueuse : N séries de 8 par jour, un taux de réussite donné,
   un jour manqué par semaine. Elle finit toujours par trouver la réponse. */
function jouer(jours, tauxReussite, seriesParJour) {
  let seed = 20260920;
  const rnd = () => { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; };
  const prog = {};
  let now = 1700000000000, xp = 0;
  const histoire = [];

  for (let j = 1; j <= jours; j++) {
    if (j % 7 === 0) { now += DAY; histoire.push({ j, saute: true, servies: 0, dus: dailyStock(prog, now).due.length }); continue; }
    let servies = 0, ratees = 0;
    for (let s = 0; s < seriesParJour; s++) {
      const q = dailyQueue(prog, now, 8, rnd);
      for (const ex of q) {
        const st = prog[ex.id] || (prog[ex.id] = { b: 0, due: 0, n: 0, ok: 0, ko: 0 });
        const juste = rnd() < tauxReussite;
        st.n++;
        st.ok++;                                   // elle finit par trouver, même après une erreur
        if (juste) { st.b = nextBox(st.b, true); xp += 12; }
        else { st.b = nextBox(st.b, false); st.ko++; xp += 5; }
        st.due = dueAt(st.b, now);
        st.last = now;
        servies++; if (!juste) ratees++;
      }
    }
    const stock = dailyStock(prog, now);
    histoire.push({ j, servies, ratees, dus: stock.due.length, neuves: stock.fresh.length,
      ancrees: Object.values(prog).filter(p => isMastered(p)).length,
      mondes: WORLDS.filter(w => isWorldUnlocked(w.n, prog)).length,
      niveau: levelInfo(xp).lvl, xp,
      examen: isExamOpen(prog), reussies: examProgress(prog),
      faibles: weakList(prog, 0).length });
    now += DAY;
  }
  return { prog, xp, histoire, now };
}

const r = jouer(30, 0.85, 2);
const h = r.histoire;
const joues = h.filter(x => !x.saute);

/* --- le jeu a toujours quelque chose à proposer --- */
ok(joues.every(x => x.servies > 0), "chaque jour joué propose des questions");
ok(joues.every(x => x.servies === 16), "deux séries de 8 questions par jour, tous les jours");

/* --- les rappels ne s'accumulent pas en arriéré --- */
const arriere = joues.map(x => x.dus);
ok(Math.max(...arriere) <= 45, `l'arriéré de rappels reste maîtrisé (max ${Math.max(...arriere)})`);
ok(arriere[arriere.length - 1] <= arriere[Math.floor(arriere.length / 2)] + 15,
   `l'arriéré ne s'emballe pas sur la seconde moitié du mois (${arriere[Math.floor(arriere.length / 2)]} puis ${arriere[arriere.length - 1]})`);

/* --- la progression avance vraiment --- */
const fin = joues[joues.length - 1];
ok(fin.ancrees >= 30, `l'ancrage progresse franchement en un mois (${fin.ancrees} ancrées)`);
ok(fin.reussies >= 80, `une part substantielle du contenu est vue en un mois (${fin.reussies}/${EX.length})`);
ok(fin.mondes >= 5, `les mondes s'ouvrent au fil du mois (${fin.mondes})`);
ok(fin.niveau >= 8, `le niveau progresse sans se bloquer (niveau ${fin.niveau})`);

/* --- les paliers arrivent, ni trop tôt ni trop tard --- */
const premierAncrage = joues.find(x => x.ancrees > 0);
ok(premierAncrage && premierAncrage.j <= 18, `première commande ancrée au jour ${premierAncrage ? premierAncrage.j : "jamais"}`);
const ouvertureExamen = joues.find(x => x.examen);
ok(ouvertureExamen && ouvertureExamen.j <= 20, `examen accessible au jour ${ouvertureExamen ? ouvertureExamen.j : "jamais"}`);
const deuxiemeMonde = joues.find(x => x.mondes >= 2);
ok(deuxiemeMonde && deuxiemeMonde.j <= 5, `deuxième monde ouvert au jour ${deuxiemeMonde ? deuxiemeMonde.j : "jamais"}`);

/* --- un boss devient accessible --- */
ok(isBossOpen(1, r.prog), "le boss du monde 1 est accessible après un mois de jeu");

/* --- le jour manqué ne casse rien --- */
const apresSaut = h.findIndex(x => x.saute);
ok(h[apresSaut + 1] && h[apresSaut + 1].servies === 16, "le lendemain d'un jour manqué propose une série complète");

/* --- la fiche de points faibles se remplit sans déborder --- */
ok(fin.faibles > 0 && fin.faibles < EX.length, `la fiche de points faibles reste ciblée (${fin.faibles} commandes)`);

/* --- rien n'est oublié : aucune commande vue ne disparaît de la circulation --- */
const jamaisRevues = Object.values(r.prog).filter(p => !isMastered(p) && p.due > r.now + 20 * DAY).length;
ok(jamaisRevues === 0, `aucune commande non ancrée n'est repoussée au-delà de trois semaines (${jamaisRevues})`);

/* --- une joueuse plus irrégulière ne se retrouve pas bloquée --- */
const r2 = jouer(21, 0.6, 1);
const j2 = r2.histoire.filter(x => !x.saute);
ok(j2.every(x => x.servies === 8), "une seule série par jour fonctionne aussi");
ok(j2[j2.length - 1].mondes >= 2, "même à 60 % de réussite, les mondes s'ouvrent");
const avancees = Object.values(r2.prog).filter(p => p.b >= 2).length;
ok(avancees >= 10, `même à 60 % de réussite, des commandes progressent dans les boîtes (${avancees})`);

console.log("Parcours 30 jours (2 séries/jour, 85 % de réussite) :");
[1, 3, 6, 13, 20, 29].forEach(j => {
  const x = h.find(y => y.j === j);
  if (x && !x.saute) console.log(`  J${String(j).padStart(2)} · niveau ${x.niveau} · ${x.xp} XP · ${x.reussies}/${EX.length} vues · ${x.ancrees} ancrées · ${x.mondes} mondes · ${x.dus} rappels en attente`);
});
console.log(`${pass} vérifications passées, ${fail} échec(s).`);
if (fail) { [...new Set(errs)].forEach(e => console.log("  ✕ " + e)); process.exit(1); }
