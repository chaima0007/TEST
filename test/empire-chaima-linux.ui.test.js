/* Test d'interface du jeu (navigateur réel, sans réseau).
   Lancer : NODE_PATH=$(npm root -g) node test/empire-chaima-linux.ui.test.js */
const path = require("path");
const { chromium } = require("playwright");

const FILE = "file://" + path.join(__dirname, "..", "public", "empire-chaima-linux.html");
let pass = 0, fail = 0;
const errs = [];
const ok = (c, l) => { if (c) pass++; else { fail++; errs.push(l); } };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 400, height: 820 } });
  const problems = [];
  page.on("pageerror", e => problems.push("pageerror: " + e.message));
  page.on("console", m => { if (m.type() === "error") problems.push("console: " + m.text()); });
  await page.goto(FILE);

  /* --- mise en page tablette --- */
  const noScrollX = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
  ok(noScrollX, "aucun défilement horizontal en 400px");
  ok(await page.locator("#btnPlay").isVisible(), "le bouton Jouer est visible dès l'ouverture");
  const small = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll("button").forEach(b => {
      const r = b.getBoundingClientRect();
      if (r.width > 0 && r.height > 0 && r.height < 44) bad.push((b.id || b.className) + ":" + Math.round(r.height));
    });
    return bad;
  });
  ok(small.length === 0, "toutes les zones cliquables font au moins 44px (" + small.join(", ") + ")");

  /* --- une session complète, en répondant juste --- */
  await page.click("#btnPlay");
  ok(await page.locator("#scPlay").isVisible(), "l'écran de jeu s'ouvre");
  const total = await page.evaluate(() => SES.queue.length);
  ok(total === 8, "la série compte 8 questions");

  let answered = 0, lastXp = 0;
  for (let step = 0; step < 30; step++) {
    if (await page.locator("#scRecap").isVisible()) break;
    const info = await page.evaluate(() => {
      const ex = SES.queue[SES.idx];
      return { id: ex.id, answer: accepted(ex)[0], pool: POOL, scenario: document.getElementById("scText").textContent };
    });
    ok(info.scenario.length > 20, info.id + " : le scénario est affiché");
    const xpBefore = await page.evaluate(() => S.xp);

    if (step === 1) { // une erreur volontaire : le feedback doit expliquer le piège
      const ex = await page.evaluate(() => { const e = SES.queue[SES.idx]; return { blocks: e.blocks, traps: e.traps }; });
      const trapTok = ex.blocks[0];
      await page.evaluate(t => addTok(POOL.indexOf(t)), trapTok);
      await page.click("#btnCheck");
      const fbText = await page.locator("#feedbackZone").innerText();
      ok(await page.locator(".feedback.ko").isVisible(), info.id + " : erreur signalée");
      ok(fbText.length > 60, info.id + " : le feedback d'erreur explique quelque chose");
      const trapMsg = ex.traps[trapTok].replace(/\s+/g, " ").slice(0, 40);
      ok(fbText.replace(/\s+/g, " ").includes(trapMsg), info.id + " : l'explication correspond au bloc fautif");
      ok(await page.evaluate(() => S.xp) === xpBefore, "une erreur ne donne pas d'XP");
      await page.click("#btnClear");
    }

    for (const tok of info.answer) {
      await page.evaluate(t => {
        for (let i = 0; i < POOL.length; i++) {
          if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); return; }
        }
      }, tok);
    }
    const built = await page.evaluate(() => BUILT.map(b => b.t));
    ok(built.join(" ") === info.answer.join(" "), info.id + " : la ligne de commande reflète les blocs cliqués");
    if (!(await page.locator("#feedbackZone .feedback.ok").isVisible())) await page.click("#btnCheck");
    ok(await page.locator(".feedback.ok").isVisible(), info.id + " : la bonne réponse est acceptée");
    ok(await page.locator(".term").isVisible(), info.id + " : la sortie terminal est simulée");
    const xpAfter = await page.evaluate(() => S.xp);
    ok(xpAfter > xpBefore, info.id + " : la bonne réponse rapporte des XP");
    lastXp = xpAfter;
    answered++;
    await page.waitForTimeout(400);
    if (await page.locator("#lvlOverlay.on").isVisible()) {   // palier : célébration bloquante
      ok(await page.locator("#ovTitle").innerText() !== "", "le palier est annoncé");
      await page.waitForTimeout(450);
      await page.click("#ovClose");
      await page.waitForTimeout(120);
    }
    await page.click("#btnNext");
    await page.waitForTimeout(60);
  }
  ok(answered >= 8, "toutes les questions de la série ont été traitées (" + answered + ")");
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  ok(await page.locator("#scRecap").isVisible(), "l'écran de récapitulatif s'affiche");
  const recap = await page.locator("#scRecap").innerText();
  ok(/\d+\/\d+/.test(recap), "le récapitulatif affiche un score");

  /* --- montée de niveau --- */
  ok(await page.evaluate(() => levelInfo(S.xp).lvl) >= 2, "le niveau 2 est atteint après une série réussie");
  ok(await page.evaluate(() => Number(document.getElementById("lvlNum").textContent)) >= 2, "le badge de niveau est à jour");

  /* --- persistance --- */
  await page.reload();
  const xpAfterReload = await page.evaluate(() => S.xp);
  ok(xpAfterReload === lastXp, "la progression survit au rechargement (" + xpAfterReload + " vs " + lastXp + ")");
  ok(await page.evaluate(() => Number(document.getElementById("xpNow").textContent)) >= 0, "le compteur d'XP est rendu");

  /* --- streak --- */
  ok(await page.evaluate(() => S.streak) === 1, "le streak quotidien démarre à 1");

  /* --- clavier libre + dictée --- */
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  await page.click("#btnSettings");
  await page.click("#btnMode");
  ok(await page.evaluate(() => S.mode) === "progressif", "le mode de saisie passe en progressif");
  await page.click("#btnMode");
  ok(await page.evaluate(() => S.mode) === "clavier", "puis en clavier libre");
  await page.click("#btnBack2");
  await page.click("#btnPlay");
  const isQuiz = await page.evaluate(() => !!SES.queue[SES.idx].quiz);
  ok(await page.locator(isQuiz ? "#buildZone" : "#freeZone").isVisible(),
     "le mode saisie correspond au type de question");
  if (!isQuiz) {
    const dictee = await page.evaluate(() => accepted(SES.queue[SES.idx])[0].join(" ")
      .replace(/\//g, " slash ").replace(/(\S)\.(\S)/g, "$1 point $2").replace(/ -/g, " tiret "));
    await page.fill("#freeInput", dictee);
    await page.click("#btnCheck");
    ok(await page.locator(".feedback.ok").isVisible(), "clavier libre : la dictée « " + dictee + " » est acceptée");
  }
  await page.click("#btnSettings"); await page.click("#btnMode"); await page.click("#btnBack2");
  ok(await page.evaluate(() => S.mode) === "blocs", "le mode revient sur les blocs");

  /* --- déblocage du monde 2 --- */
  await page.evaluate(() => {
    const l = EX.filter(e => e.w === 1);
    l.forEach((e, i) => { if (i < Math.ceil(l.length * 0.7)) S.prog[e.id] = { b: 2, due: 0, n: 1, ok: 1, ko: 0 }; });
    save(); renderHome();
  });
  const cards = await page.locator(".world").count();
  const attendus = await page.evaluate(() => WORLDS.filter(w => !w.soon).length);
  ok(cards === attendus,
     "tous les mondes ouverts à la lecture sont proposés (" + cards + " sur " + attendus + ")");
  const w2locked = await page.evaluate(() => document.querySelectorAll(".world")[1].className.includes("locked"));
  ok(!w2locked, "le monde 2 se débloque une fois le seuil du monde 1 atteint");
  await page.evaluate(() => document.querySelectorAll(".world")[1].click());
  ok(await page.evaluate(() => SES.world) === 2, "on peut lancer une série dans le monde 2");

  /* --- export --- */
  await page.click("#btnBack"); await page.click("#btnSettings");
  const dl = await Promise.all([page.waitForEvent("download", { timeout: 4000 }).catch(() => null), page.click("#btnExport")]);
  ok(dl[0] && /empire-chaima-progression-.*\.json/.test(dl[0].suggestedFilename()), "l'export produit un fichier JSON");
  if (dl[0]) {
    const fs = require("fs");
    const p = await dl[0].path();
    const data = JSON.parse(fs.readFileSync(p, "utf8"));
    ok(typeof data.xp === "number" && data.prog && typeof data.prog === "object", "le fichier exporté contient bien la progression");
  }

  /* --- boss de fin de monde --- */
  await page.click("#btnBack2");
  await page.evaluate(() => {
    EX.filter(e => e.w === 1).forEach(e => { S.prog[e.id] = { b: 2, due: 0, n: 1, ok: 1, ko: 0 }; });
    save(); renderHome();
  });
  ok(await page.locator(".bossbtn").first().isVisible(), "le bouton de boss apparaît sur le monde 1");
  const bossLabel = await page.locator(".bossbtn").first().innerText();
  ok(bossLabel.includes("Boss"), "le bouton annonce le boss : " + bossLabel.trim());
  await page.locator(".bossbtn").first().click();
  ok(await page.evaluate(() => !!(SES && SES.boss)), "le boss se lance");
  const bossSteps = await page.evaluate(() => SES.queue.length);
  ok(bossSteps >= 4, "le boss enchaîne au moins 4 étapes (" + bossSteps + ")");
  ok(await page.locator("#btnHint").isHidden(), "aucun indice pendant un boss");
  ok((await page.locator("#hintZone").innerText()).length > 40, "la mise en situation du boss est affichée");
  for (let k = 0; k < bossSteps + 2; k++) {
    if (await page.locator("#scRecap").isVisible()) break;
    await page.evaluate(() => {
      accepted(SES.queue[SES.idx])[0].forEach(t => {
        for (let i = 0; i < POOL.length; i++) if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); return; }
      });
    });
    if (!(await page.locator("#feedbackZone .feedback.ok").isVisible())) await page.click("#btnCheck");
    ok(await page.locator(".feedback.ok").isVisible(), "étape de boss validée");
    await page.waitForTimeout(400);
    if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
    await page.click("#btnNext");
    await page.waitForTimeout(80);
  }
  await page.waitForTimeout(500);
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  ok(await page.locator("#scRecap").isVisible(), "le boss se termine sur un récapitulatif");
  ok((await page.locator("#recapTitle").innerText()).includes("Boss"), "le récapitulatif annonce la victoire");
  ok(await page.evaluate(() => !!(S.boss && S.boss[1] && S.boss[1].done)), "la victoire sur le boss est enregistrée");
  await page.click("#btnHome");
  ok((await page.locator(".bossbtn").first().innerText()).includes("vaincu"), "le monde 1 affiche son boss vaincu");

  /* --- fiche des points faibles --- */
  await page.evaluate(() => {
    const e = EX.find(x => x.w === 1);
    S.prog[e.id] = { b: 0, due: 0, n: 6, ok: 1, ko: 5, last: Date.now() };
    S.log = [{ t: Date.now(), id: e.id, mode: "série" }];
    save();
  });
  await page.click("#btnWeak");
  ok(await page.locator("#scWeak").isVisible(), "la fiche des points faibles s'ouvre");
  const weakTxt = await page.locator("#weakList").innerText();
  ok(weakTxt.includes("5×"), "la fiche compte les erreurs par commande");
  const firstWeak = await page.evaluate(() => accepted(weakList(S.prog, 1)[0].ex)[0].join(" "));
  ok(weakTxt.includes(firstWeak), "la fiche cite la commande la plus ratée : " + firstWeak);
  ok((await page.locator("#weakWorlds").innerText()).includes("Monde 1"), "la fiche résume chaque monde");
  const dl2 = await Promise.all([page.waitForEvent("download", { timeout: 4000 }).catch(() => null), page.click("#btnWeakExport")]);
  ok(dl2[0] && /empire-chaima-points-faibles-.*\.txt/.test(dl2[0].suggestedFilename()), "la fiche s'exporte en .txt");
  if (dl2[0]) {
    const fs = require("fs");
    const txt = fs.readFileSync(await dl2[0].path(), "utf8");
    ok(txt.includes("COMMANDES À RETRAVAILLER") && txt.includes(firstWeak), "le fichier exporté contient la fiche complète");
  }
  await page.click("#btnWeakTrain");
  ok(await page.evaluate(() => !!(SES && SES.weak)), "l'entraînement ciblé démarre depuis la fiche");
  ok(await page.evaluate(() => accepted(SES.queue[0])[0].join(" ")) === firstWeak, "il commence par la commande la plus ratée");
  await page.click("#btnBack");

  /* --- mode examen --- */
  await page.evaluate(() => { EX.forEach(e => { S.prog[e.id] = { b: 1, due: 0, n: 1, ok: 1, ko: 0 }; }); save(); renderHome(); });
  await page.click("#btnExam");
  ok(await page.evaluate(() => !!(SES && SES.exam)), "l'examen démarre");
  ok(await page.locator("#examTimer").isVisible(), "le minuteur est affiché");
  ok(/^\d+:\d\d$/.test((await page.locator("#examTimer").innerText()).trim()), "le minuteur affiche un décompte");
  ok(await page.locator("#btnHint").isHidden(), "aucun indice pendant l'examen");
  const examN = await page.evaluate(() => SES.queue.length);
  ok(examN === 12, "l'examen compte 12 questions (" + examN + ")");
  // une réponse fausse : pas de seconde chance, la réponse attendue est montrée
  await page.evaluate(() => {
    const ex = SES.queue[SES.idx];
    const bad = (ex.blocks || [])[0];
    addTok(POOL.indexOf(bad));
  });
  if (await page.locator("#actionRow").isVisible()) await page.click("#btnCheck");
  await page.waitForTimeout(200);
  const examFb = await page.locator("#feedbackZone").innerText();
  ok(examFb.includes("Réponse attendue"), "en examen, la réponse attendue est révélée immédiatement");
  ok(await page.locator("#btnNext").isVisible(), "on passe directement à la question suivante");
  ok(await page.locator("#actionRow").isHidden(), "aucune seconde tentative en examen");
  await page.evaluate(() => { SES.deadline = Date.now() + 500; });
  await page.waitForTimeout(1600);
  ok(await page.locator("#scRecap").isVisible(), "l'examen s'arrête quand le temps est écoulé");
  ok((await page.locator("#recapTitle").innerText()).includes("Temps"), "le récapitulatif signale le temps écoulé");
  ok(await page.locator("#examTimer").isHidden(), "le minuteur s'arrête avec l'examen");
  await page.click("#btnHome");

  /* --- revenir le lendemain : les rappels dus doivent être servis --- */
  await page.evaluate(() => {
    localStorage.removeItem("empire-chaima-linux-v1");
  });
  await page.reload();
  await page.waitForTimeout(150);
  await page.click("#btnPlay");
  for (let k = 0; k < 12; k++) {
    if (await page.locator("#scRecap").isVisible()) break;
    await page.evaluate(() => {
      accepted(SES.queue[SES.idx])[0].forEach(t => {
        for (let i = 0; i < POOL.length; i++) if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); return; }
      });
    });
    await page.waitForTimeout(160);
    if (await page.locator("#actionRow").isVisible() && !(await page.locator("#feedbackZone .feedback").isVisible()))
      await page.click("#btnCheck");
    await page.waitForTimeout(140);
    if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
    if (await page.locator("#btnNext").isVisible()) await page.click("#btnNext");
    await page.waitForTimeout(80);
  }
  await page.waitForTimeout(300);
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  ok(await page.locator("#scRecap").isVisible(), "une première journée se termine sur un récapitulatif");
  await page.click("#btnHome");
  ok(await page.locator("#scHome").isVisible(), "le bouton du bas ramène toujours à l'accueil, quel que soit son libellé");
  const veille = await page.evaluate(() => S.xp);
  // on avance d'une journée, comme au réveil le lendemain
  await page.evaluate(() => {
    const raw = JSON.parse(localStorage.getItem("empire-chaima-linux-v1"));
    const D = 86400000;
    for (const k in raw.prog) { if (raw.prog[k].due) raw.prog[k].due -= D; if (raw.prog[k].last) raw.prog[k].last -= D; }
    const d = new Date(raw.last + "T12:00:00"); d.setDate(d.getDate() - 1);
    raw.last = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    raw.dayKey = null; raw.dayCount = 0;
    localStorage.setItem("empire-chaima-linux-v1", JSON.stringify(raw));
  });
  await page.reload();
  await page.waitForTimeout(200);
  const stock = await page.evaluate(() => dailyStock(S.prog, Date.now()).due.length);
  ok(stock > 0, `le lendemain, des rappels sont arrivés à échéance (${stock})`);
  ok((await page.locator("#resumeLine").innerText()).includes("à revoir"),
     "l'accueil annonce les rappels du jour");
  await page.click("#btnPlay");
  await page.waitForTimeout(200);
  const rappelsServis = await page.evaluate(() => SES.queue.filter(e => S.prog[e.id] && S.prog[e.id].n > 0).length);
  ok(rappelsServis > 0, `la série du lendemain contient bien des rappels (${rappelsServis}/8)`);
  await page.evaluate(() => {
    accepted(SES.queue[SES.idx])[0].forEach(t => {
      for (let i = 0; i < POOL.length; i++) if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); return; }
    });
  });
  await page.waitForTimeout(160);
  if (await page.locator("#actionRow").isVisible() && !(await page.locator("#feedbackZone .feedback").isVisible()))
    await page.click("#btnCheck");
  await page.waitForTimeout(200);
  ok(await page.evaluate(() => S.xp) > veille, "une bonne réponse le lendemain rapporte bien des XP");
  ok(await page.evaluate(() => S.streak) === 2, "la série quotidienne passe à deux jours");
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  await page.click("#btnBack");

  /* --- objectif du jour atteint : la séance peut se terminer --- */
  await page.evaluate(() => { localStorage.removeItem("empire-chaima-linux-v1"); });
  await page.reload();
  await page.waitForTimeout(150);
  await page.click("#btnPlay");
  await page.waitForTimeout(150);
  // on se place juste avant l'objectif, puis on termine la série
  await page.evaluate(() => { S.dayKey = dayKey(); S.dayCount = dayGoal() - 1; save(); });
  for (let k = 0; k < 12; k++) {
    if (await page.locator("#scRecap").isVisible()) break;
    await page.evaluate(() => {
      accepted(SES.queue[SES.idx])[0].forEach(t => {
        for (let i = 0; i < POOL.length; i++) if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); return; }
      });
    });
    await page.waitForTimeout(160);
    if (await page.locator("#actionRow").isVisible() && !(await page.locator("#feedbackZone .feedback").isVisible()))
      await page.click("#btnCheck");
    await page.waitForTimeout(140);
    if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
    if (await page.locator("#btnNext").isVisible()) await page.click("#btnNext");
    await page.waitForTimeout(80);
  }
  await page.waitForTimeout(300);
  if (await page.locator("#lvlOverlay.on").isVisible()) { await page.waitForTimeout(450); await page.click("#ovClose"); }
  ok(await page.evaluate(() => dayDone()), "l'objectif du jour est atteint");
  const fini = await page.evaluate(() => ({
    haut: document.getElementById("btnHome").textContent.trim(),
    hautCls: document.getElementById("btnHome").className,
    hautOrdre: document.getElementById("btnHome").style.order,
    basOrdre: document.getElementById("btnAgain").style.order,
    bas: document.getElementById("btnAgain").textContent.trim(),
    msg: document.getElementById("recapMsg").textContent
  }));
  ok(fini.haut.includes("Terminé pour aujourd'hui"), "le récapitulatif propose d'arrêter pour aujourd'hui");
  ok(fini.hautCls.includes("primary") && Number(fini.hautOrdre) < Number(fini.basOrdre),
     "cette proposition est l'action mise en avant");
  ok(fini.bas.includes("Une série de plus"), "continuer reste possible, en second");
  ok(/Demain : \d+ commande/.test(fini.msg), "le récapitulatif annonce ce qui revient demain : " + fini.msg.slice(-40));
  await page.click("#btnHome");
  ok(await page.locator("#scHome").isVisible(), "terminer la journée ramène à l'accueil");

  /* --- affichage large --- */
  await page.setViewportSize({ width: 900, height: 800 });
  ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "aucun défilement horizontal en 900px");
  await page.setViewportSize({ width: 320, height: 700 });
  ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "aucun défilement horizontal en 320px");

  ok(problems.length === 0, "aucune erreur JavaScript : " + problems.slice(0, 5).join(" | "));

  /* --- réimporter une progression : cache vidé, changement d'appareil --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    const soucis = [];
    q.on("pageerror", e => soucis.push(e.message));
    await q.goto(FILE);
    await q.waitForTimeout(200);
    const sauvegarde = await q.evaluate(() => {
      S.xp = 1450; S.streak = 6; S.best = 9;
      EX.filter(e => e.w <= 3).forEach((e, i) => {
        S.prog[e.id] = { b: i % 4, due: Date.now() + i * 3600000, n: 2, ok: 2, ko: i % 3 ? 0 : 2, last: Date.now() };
      });
      S.boss = { 1: { done: true, best: "4/4", first: 4 } };
      S.exams = [{ t: Date.now() - 3 * 86400000, first: 9, n: 12, secs: 400 }];
      S.mode = "progressif"; S.len = 12; S.examOn = false;
      save();
      return localStorage.getItem("empire-chaima-linux-v1");
    });
    await q.evaluate(() => localStorage.clear());
    await q.reload();
    await q.waitForTimeout(200);
    ok(await q.evaluate(() => S.xp) === 0, "cache vidé : la progression repart de zéro");
    await q.click("#btnSettings");
    await q.setInputFiles("#fileInput", { name: "empire-chaima-progression.json", mimeType: "application/json", buffer: Buffer.from(sauvegarde) });
    await q.waitForTimeout(400);
    const restaure = await q.evaluate(() => ({
      xp: S.xp, streak: S.streak, best: S.best, prog: Object.keys(S.prog).length,
      boss: !!(S.boss && S.boss[1] && S.boss[1].done), exams: (S.exams || []).length,
      mode: S.mode, len: S.len, examOn: S.examOn, toast: document.getElementById("toast").textContent
    }));
    ok(restaure.xp === 1450 && restaure.prog > 40, `la progression est restaurée (${restaure.xp} XP, ${restaure.prog} commandes)`);
    ok(restaure.streak === 6 && restaure.best === 9, "les séries quotidiennes sont restaurées");
    ok(restaure.boss && restaure.exams === 1, "boss vaincu et historique d'examen restaurés");
    ok(restaure.mode === "progressif" && restaure.len === 12 && restaure.examOn === false, "les réglages sont restaurés");
    ok(restaure.toast.includes("importée"), "un retour visible confirme l'import");
    await q.reload();
    await q.waitForTimeout(250);
    ok(await q.evaluate(() => S.xp) === 1450, "la progression réimportée survit au rechargement");
    await q.click("#btnPlay");
    await q.waitForTimeout(250);
    ok(await q.locator("#scPlay").isVisible(), "une série se lance sur la progression réimportée");
    await q.click("#btnBack");
    await q.click("#btnSettings");
    await q.setInputFiles("#fileInput", { name: "autre.json", mimeType: "application/json", buffer: Buffer.from("pas du tout du json") });
    await q.waitForTimeout(400);
    ok((await q.locator("#toast").innerText()).includes("illisible"), "un fichier invalide est refusé proprement");
    ok(await q.evaluate(() => S.xp) === 1450, "un fichier invalide n'écrase pas la progression en place");
    ok(soucis.length === 0, "aucune erreur JavaScript pendant l'import");
    await ctx.close();
  }

  /* --- export quand la page tourne en ligne ---
     Là-bas, un lien de téléchargement direct est bloqué : c'est la capacité
     « downloads » qui doit prendre le relais, et le repli local doit rester. */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    await q.addInitScript(() => {
      window.__appels = [];
      window.claude = { use: (nom) => Promise.resolve(nom === "downloads"
        ? { save: (o) => { window.__appels.push(o); return Promise.resolve(); } } : null) };
    });
    await q.goto(FILE);
    await q.waitForTimeout(200);
    await q.evaluate(() => { S.xp = 340; S.prog = { "w1-ls": { b: 1, due: 0, n: 2, ok: 1, ko: 1, last: Date.now() } }; save(); });
    await q.click("#btnSettings");
    await q.click("#btnExport");
    await q.waitForTimeout(300);
    const appels = await q.evaluate(() => window.__appels);
    ok(appels.length === 1, "en ligne, l'export passe par la capacité downloads");
    ok(appels[0] && /^empire-chaima-progression-\d{4}-\d{2}-\d{2}\.json$/.test(appels[0].filename),
       "le fichier exporté porte un nom daté : " + (appels[0] && appels[0].filename));
    let contenu = null;
    try { contenu = JSON.parse(appels[0].data); } catch (e) { /* laissé à null */ }
    ok(contenu && contenu.xp === 340 && contenu.prog["w1-ls"], "l'export contient la progression réelle");
    await q.click("#btnBack2");
    await q.click("#btnWeak");
    await q.click("#btnWeakExport");
    await q.waitForTimeout(300);
    const appels2 = await q.evaluate(() => window.__appels);
    ok(appels2.length === 2 && /points-faibles-.*\.txt$/.test(appels2[1].filename),
       "la fiche de points faibles emprunte le même chemin");
    ok(appels2[1] && appels2[1].data.includes("COMMANDES À RETRAVAILLER"), "la fiche exportée contient le rapport complet");
    await ctx.close();

    // repli : sans la capacité, le téléchargement classique doit marcher
    const ctx2 = await browser.newContext({ viewport: { width: 412, height: 820 }, acceptDownloads: true });
    const q2 = await ctx2.newPage();
    await q2.addInitScript(() => { window.claude = { use: () => Promise.resolve(null) }; });
    await q2.goto(FILE);
    await q2.waitForTimeout(200);
    await q2.click("#btnSettings");
    const dl3 = await Promise.all([q2.waitForEvent("download", { timeout: 5000 }).catch(() => null), q2.click("#btnExport")]);
    ok(!!dl3[0], "sans la capacité, le téléchargement classique prend le relais");
    await ctx2.close();

    // refus : la page doit le dire, sans casser
    const ctx3 = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q3 = await ctx3.newPage();
    const soucis3 = [];
    q3.on("pageerror", e => soucis3.push(e.message));
    await q3.addInitScript(() => { window.claude = { use: () => Promise.resolve({ save: () => Promise.reject(new Error("refus")) }) }; });
    await q3.goto(FILE);
    await q3.waitForTimeout(200);
    await q3.click("#btnSettings");
    await q3.click("#btnExport");
    await q3.waitForTimeout(400);
    ok((await q3.locator("#toast").innerText()).length > 0 && soucis3.length === 0,
       "un refus d'enregistrement est annoncé, sans erreur JavaScript");
    await ctx3.close();
  }

  /* --- stockage refusé : le jeu doit le dire au lieu de perdre la progression en silence.
     Cas réel : le fichier ouvert dans un onglet de navigation privée sur la tablette. --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    const soucis = [];
    q.on("pageerror", e => soucis.push(e.message));
    await q.addInitScript(() => {
      Object.defineProperty(window, "localStorage", {
        configurable: true, get() { throw new Error("stockage bloqu\u00e9"); }
      });
    });
    await q.goto(FILE);
    await q.waitForTimeout(200);
    ok(soucis.length === 0, "sans stockage, la page se charge sans erreur JavaScript : " + soucis.join(" | "));
    ok(await q.locator("#noStore").isVisible(), "sans stockage, l'avertissement est affich\u00e9 d\u00e8s l'accueil");
    const texte = await q.locator("#noStore").innerText();
    ok(/export/i.test(texte), "l'avertissement dit quoi faire (exporter)");
    await q.click("#btnPlay");
    ok(await q.locator("#scPlay").isVisible(), "sans stockage, on peut quand m\u00eame jouer");
    await q.click("#btnBack");
    ok(soucis.length === 0, "une s\u00e9rie sans stockage ne d\u00e9clenche aucune erreur : " + soucis.join(" | "));
    await ctx.close();
  }

  /* --- cas normal : pas d'avertissement intempestif --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    await q.goto(FILE);
    await q.waitForTimeout(150);
    ok(await q.locator("#noStore").isHidden(), "quand le stockage marche, aucun avertissement n'appara\u00eet");
    await ctx.close();
  }

  /* --- économie : le boss, l'examen et l'objectif du jour --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    const soucis = [];
    q.on("pageerror", e => soucis.push(e.message));
    await q.goto(FILE);
    await q.waitForTimeout(150);

    // Le boss paie plein tarif une fois, puis cesse d'être une machine à XP.
    const boss = await q.evaluate(() => {
      const jouer = (justes) => {
        const n = BOSS[0].steps.length;
        const avant = S.xp;
        SES = { queue: new Array(n), first: justes, done: n, world: 1, boss: BOSS[0], xp: justes * 12, marks: {} };
        endBoss();
        return S.xp - avant;
      };
      S.boss = {}; S.xp = 1000; S.seen = {};
      const premiere = jouer(BOSS[0].steps.length);
      const rejeu1 = jouer(BOSS[0].steps.length);
      const rejeu2 = jouer(BOSS[0].steps.length);
      S.boss = {}; S.xp = 1000;
      const imparfaite = jouer(BOSS[0].steps.length - 1);
      const sansFauteApres = jouer(BOSS[0].steps.length);
      return { premiere, rejeu1, rejeu2, imparfaite, sansFauteApres };
    });
    ok(boss.premiere === 200, "la première victoire sur un boss vaut son plein tarif (" + boss.premiere + " XP)");
    ok(boss.rejeu1 === 25 && boss.rejeu2 === 25, "un rejeu de boss ne rapporte plus une journée d'XP (" + boss.rejeu1 + " XP)");
    ok(boss.imparfaite < boss.premiere, "une victoire imparfaite rapporte moins (" + boss.imparfaite + " XP)");
    ok(boss.sansFauteApres === 80, "le premier sans-faute après une victoire imparfaite est récompensé (" + boss.sansFauteApres + " XP)");

    // La célébration s'affiche 120 ms plus tard : d'ici là, une autre partie
    // a pu commencer. Le titre du boss doit être figé, pas relu au dernier moment.
    await q.evaluate(() => {
      S.boss = {}; S.xp = 1000; S.seen = {};
      const n = BOSS[0].steps.length;
      SES = { queue: new Array(n), first: n, done: n, world: 1, boss: BOSS[0], xp: n * 12, marks: {} };
      endBoss();
      SES = { queue: [], first: 0, done: 0, xp: 0, marks: {} };  // elle est déjà repartie ailleurs
    });
    await q.waitForTimeout(300);
    ok(soucis.length === 0, "la célébration d'un boss survit au départ d'une autre partie : " + soucis.join(" | "));

    // L'examen n'enlève jamais d'XP déjà gagnés.
    const exam = await q.evaluate(() => {
      const passer = (justes) => {
        const avant = S.xp;
        SES = { queue: new Array(12), first: justes, done: 12, start: Date.now() - 300000,
                exam: true, xp: justes * 12, marks: {}, missed: [] };
        endExam();
        return { avant, apres: S.xp };
      };
      S.xp = 2000; S.exams = [];
      return { faible: passer(7), moyen: passer(8), fort: passer(10), parfait: passer(12) };
    });
    ok(exam.faible.apres >= exam.faible.avant, "un examen raté ne fait jamais reculer le compteur d'XP");
    ok(exam.moyen.apres - exam.moyen.avant === 60, "un examen entre 60 et 79 % ajoute le palier intermédiaire");
    ok(exam.fort.apres - exam.fort.avant === 180, "un examen à 80 % et plus ajoute le grand palier");
    ok(exam.parfait.apres - exam.parfait.avant === 180, "un examen parfait aussi, et rien n'est retiré");

    // Même vérification pour l'examen.
    await q.evaluate(() => {
      S.xp = 2000; S.exams = [];
      SES = { queue: new Array(12), first: 12, done: 12, start: Date.now() - 300000,
              exam: true, xp: 144, marks: {}, missed: [] };
      endExam();
      SES = null;
    });
    await q.waitForTimeout(300);
    ok(soucis.length === 0, "la célébration d'un examen survit à la fin de la session : " + soucis.join(" | "));

    // L'objectif du jour est figé au réveil : il ne bouge plus en cours de séance.
    const objectif = await q.evaluate(() => {
      S.prog = {}; S.dayKey = null; S.dayTarget = 0; S.dayCount = 0; S.len = 8;
      bumpDay();
      const auDebut = dayGoal();
      const faux = {};
      EX.slice(0, 40).forEach(e => { faux[e.id] = { b: 1, due: Date.now() - 1000, n: 1, ok: 1, ko: 0, last: Date.now() - 86400000 }; });
      S.prog = faux;
      return { auDebut, plusTard: dayGoal() };
    });
    ok(objectif.auDebut === objectif.plusTard,
       "l'objectif du jour ne change pas pendant la journée (" + objectif.auDebut + " puis " + objectif.plusTard + ")");
    ok(objectif.auDebut <= 20, "l'objectif du jour reste tenable sur une tablette (" + objectif.auDebut + " questions)");

    // L'accueil dit où elle en est, avant et après l'objectif.
    await q.evaluate(() => { S.prog = {}; S.dayKey = dayKey(); S.dayTarget = 16; S.dayCount = 7; renderHome(); });
    const enCours = await q.locator("#resumeLine").innerText();
    ok(/7\s*\/\s*16 aujourd'hui/.test(enCours), "l'accueil affiche l'avancement du jour : " + enCours.split("\n")[0]);
    ok((await q.locator("#btnPlay").innerText()).indexOf("Jouer") >= 0, "tant que l'objectif n'est pas atteint, le bouton reste « Jouer »");
    await q.evaluate(() => { S.dayCount = 16; renderHome(); });
    ok((await q.locator("#btnPlay").innerText()).indexOf("Objectif du jour atteint") >= 0,
       "objectif atteint : l'accueil ne pousse plus à rejouer");
    ok(await q.locator("#btnPlay").isEnabled(), "elle peut quand même rejouer si elle le veut");

    // Un boss disponible se voit depuis l'accueil.
    const bossVu = await q.evaluate(() => {
      S.prog = {}; S.boss = {}; S.dayCount = 0; S.dayTarget = 0; S.dayKey = null;
      EX.filter(e => e.w === 1).forEach(e => { S.prog[e.id] = { b: 2, due: Date.now() + 86400000, n: 2, ok: 2, ko: 0, last: Date.now() }; });
      renderHome();
      return document.getElementById("resumeLine").innerText;
    });
    ok(/Boss disponible/.test(bossVu), "un boss ouvert et non vaincu est annoncé sur l'accueil : " + bossVu.replace(/\n/g, " · "));

    // Les annonces ne se répètent pas à chaque réouverture du fichier.
    await q.evaluate(() => { S.seen = {}; markAnnounced("monde2"); save(); });
    await q.reload();
    await q.waitForTimeout(150);
    ok(await q.evaluate(() => announced(2)), "un monde déjà annoncé le reste après rechargement");
    ok(soucis.length === 0, "aucune erreur JavaScript pendant ces vérifications : " + soucis.join(" | "));
    await ctx.close();
  }

  /* --- la montée de niveau doit être lisible, pas cachée sous le pouce --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    await q.goto(FILE);
    await q.waitForTimeout(150);
    await q.click("#btnPlay");
    await q.waitForTimeout(200);
    const pos = await q.evaluate(() => {
      document.getElementById("btnNext").style.display = "";
      toast("⬆ Niveau 3 — Exploratrice de l'arborescence", 4000, "lvl");
      const t = document.getElementById("toast").getBoundingClientRect();
      const n = document.getElementById("btnNext").getBoundingClientRect();
      const st = getComputedStyle(document.getElementById("toast"));
      const a = document.getElementById("actionRow").getBoundingClientRect();
      const chev = (r) => t.bottom > r.top && t.top < r.bottom;
      return { chevauche: chev(n) || chev(a), taille: parseFloat(st.fontSize),
               dansEcran: t.top >= 0 && t.bottom <= window.innerHeight };
    });
    ok(!pos.chevauche, "le message de niveau ne recouvre aucun bouton sous le pouce");
    ok(pos.dansEcran, "le message de niveau tient entièrement dans l'écran");
    ok(pos.taille >= 16, "le message de niveau est lisible (" + pos.taille + "px)");
    await ctx.close();
  }

  /* --- effets utiles et accessibilité : anatomie, voix, vibration, taille du texte --- */
  {
    const ctx = await browser.newContext({ viewport: { width: 412, height: 820 } });
    const q = await ctx.newPage();
    const soucis = [];
    q.on("pageerror", e => soucis.push(e.message));
    await q.addInitScript(() => {
      // Chromium de bureau n'a ni vibreur ni voix : on les instrumente pour les observer.
      window.__vibr = [];
      Object.defineProperty(navigator, "vibrate", {
        configurable: true, value: (p) => { window.__vibr.push(p); return true; }
      });
      window.__dits = [];
      Object.defineProperty(window, "speechSynthesis", {
        configurable: true,
        value: { speak: (u) => window.__dits.push(u && u.text), cancel: () => {} }
      });
      window.SpeechSynthesisUtterance = function (t) { this.text = t; this.lang = ""; this.rate = 1; };
    });
    await q.goto(FILE);
    await q.waitForTimeout(200);
    // la toute première question du jeu explique d'abord comment poser les blocs
    await q.click("#btnPlay");
    await q.waitForTimeout(250);
    ok((await q.locator("#hintZone").innerText()).indexOf("blocs") >= 0,
       "la toute première question explique comment poser les blocs, avant toute autre aide");
    await q.click("#btnBack");
    await q.evaluate(() => { S.seenIntro = true; save(); });
    await q.click("#btnPlay");
    await q.waitForTimeout(250);

    // on se place sur une question à blocs (les quiz n'ont ni anatomie ni « montre-moi »)
    for (let i = 0; i < 6 && await q.evaluate(() => !!SES.queue[SES.idx].quiz); i++) {
      await q.evaluate(() => { SES.idx++; renderQuestion(); });
    }

    /* écoute de la consigne */
    ok(await q.locator("#btnSay").isVisible(), "le bouton d'écoute de la consigne est proposé");
    await q.click("#btnSay");
    const ditConsigne = await q.evaluate(() => window.__dits.slice());
    ok(ditConsigne.length === 1 && ditConsigne[0].length > 30,
       "la consigne est envoyée à la synthèse vocale : " + (ditConsigne[0] || "").slice(0, 50));

    /* « je ne l'ai jamais vue » */
    ok(await q.locator("#btnShow").isVisible(), "à la première rencontre, le jeu propose de montrer la commande");
    const attendue = await q.evaluate(() => accepted(SES.queue[SES.idx])[0].join(" "));
    await q.click("#btnShow");
    const aide = (await q.locator("#hintZone").innerText()).replace(/\s+/g, " ");
    ok(aide.includes(attendue), "la commande attendue est montrée : " + attendue);
    ok(/compose/i.test(aide), "et le jeu demande quand même de la composer");

    /* composer la réponse montrée : barème réduit, marque distincte, anatomie */
    const avant = await q.evaluate(() => S.xp);
    await q.evaluate(() => {
      const rep = accepted(SES.queue[SES.idx])[0];
      for (const t of rep) {
        for (let i = 0; i < POOL.length; i++) {
          if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); break; }
        }
      }
    });
    if (!(await q.locator("#feedbackZone .feedback.ok").isVisible())) await q.click("#btnCheck");
    await q.waitForTimeout(150);
    const gagne = await q.evaluate(() => S.xp) - avant;
    ok(gagne === 4, "une commande montrée puis recomposée rapporte un barème réduit (" + gagne + " XP)");
    ok(await q.locator("#dots .dot.vu").count() === 1, "elle est marquée « vue », ni réussite ni erreur");

    const parts = await q.evaluate(() => Array.prototype.map.call(
      document.querySelectorAll(".anat .apart"), d => d.querySelector("em").textContent));
    ok(parts.length === attendue.split(" ").length, "l'anatomie découpe toute la commande (" + parts.length + " morceaux)");
    ok(parts.indexOf("commande") >= 0, "le verbe de la commande est nommé : " + parts.join(" · "));
    ok((await q.evaluate(() => window.__vibr.slice())).length === 1, "une bonne réponse déclenche une vibration courte");

    /* écoute de l'explication */
    ok(await q.locator("#feedbackZone .saybtn").isVisible(), "l'explication peut être écoutée");
    await q.click("#feedbackZone .saybtn");
    ok((await q.evaluate(() => window.__dits.length)) === 2, "l'explication part bien à la synthèse vocale");

    /* taille du texte */
    const avantPx = await q.evaluate(() => parseFloat(getComputedStyle(document.getElementById("scenario")).fontSize));
    await q.click("#btnBack");
    await q.click("#btnSettings");
    await q.click("#btnZoom");
    ok(await q.evaluate(() => document.body.classList.contains("zoom1")), "la taille « Grand » s'applique");
    await q.click("#btnZoom");
    ok((await q.locator("#btnZoom").innerText()).indexOf("Très") >= 0, "la taille « Très grand » existe");
    await q.click("#btnBack2");
    await q.click("#btnPlay");
    await q.waitForTimeout(200);
    const apresPx = await q.evaluate(() => parseFloat(getComputedStyle(document.getElementById("scenario")).fontSize));
    ok(apresPx > avantPx, "le texte des consignes grandit réellement (" + avantPx + " → " + apresPx + " px)");

    /* et rien ne déborde de l'écran, même sur la plus petite tablette */
    await q.setViewportSize({ width: 320, height: 720 });
    await q.waitForTimeout(150);
    ok(await q.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1),
       "en très grand et en 320px, aucun défilement horizontal");
    await q.setViewportSize({ width: 412, height: 820 });

    /* les deux aides se coupent */
    await q.click("#btnBack");
    await q.click("#btnSettings");
    await q.click("#swTts");
    await q.click("#swVibro");
    await q.click("#btnBack2");
    await q.click("#btnPlay");
    await q.waitForTimeout(200);
    ok(await q.locator("#btnSay").isHidden(), "la lecture à voix haute se coupe depuis les réglages");
    const vibrAvant = await q.evaluate(() => window.__vibr.length);
    await q.evaluate(() => {
      const rep = accepted(SES.queue[SES.idx])[0];
      for (const t of rep) {
        for (let i = 0; i < POOL.length; i++) {
          if (POOL[i] === t && !BUILT.some(b => b.i === i)) { addTok(i); break; }
        }
      }
    });
    if (!(await q.locator("#feedbackZone .feedback.ok").isVisible())) await q.click("#btnCheck");
    await q.waitForTimeout(150);
    ok(await q.evaluate(() => window.__vibr.length) === vibrAvant, "le retour vibrant se coupe aussi");
    ok(await q.locator("#feedbackZone .saybtn").count() === 0, "et le bouton d'écoute disparaît du feedback");

    /* les réglages de confort survivent au rechargement */
    await q.reload();
    await q.waitForTimeout(200);
    ok(await q.evaluate(() => S.zoom === 2 && S.tts === false && S.vibro === false),
       "les réglages de confort sont enregistrés");
    ok(await q.evaluate(() => document.body.classList.contains("zoom2")),
       "et la taille du texte est appliquée dès l'ouverture");
    ok(soucis.length === 0, "aucune erreur JavaScript sur tout ce parcours : " + soucis.join(" | "));
    await ctx.close();
  }

  await browser.close();
  console.log(`${pass} vérifications passées, ${fail} échec(s).`);
  if (fail) { [...new Set(errs)].forEach(e => console.log("  ✕ " + e)); process.exit(1); }
})();
