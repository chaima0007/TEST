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
      ok(await page.locator("#ovTitle").innerText() !== "", "la montée de niveau est annoncée");
      await page.click("#ovClose");
      await page.waitForTimeout(120);
    }
    await page.click("#btnNext");
    await page.waitForTimeout(60);
  }
  ok(answered >= 8, "toutes les questions de la série ont été traitées (" + answered + ")");
  if (await page.locator("#lvlOverlay.on").isVisible()) await page.click("#ovClose");
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
  if (await page.locator("#lvlOverlay.on").isVisible()) await page.click("#ovClose");
  await page.click("#btnSettings");
  await page.click("#swFree");
  ok(await page.evaluate(() => S.free) === true, "le clavier libre s'active dans les réglages");
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
  await page.click("#btnSettings"); await page.click("#swFree"); await page.click("#btnBack2");

  /* --- déblocage du monde 2 --- */
  await page.evaluate(() => {
    const l = EX.filter(e => e.w === 1);
    l.forEach((e, i) => { if (i < Math.ceil(l.length * 0.7)) S.prog[e.id] = { b: 2, due: 0, n: 1, ok: 1, ko: 0 }; });
    save(); renderHome();
  });
  const cards = await page.locator(".world").count();
  ok(cards === 12, "les 12 mondes (dont bonus et labos) sont proposés (" + cards + ")");
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
    if (await page.locator("#lvlOverlay.on").isVisible()) await page.click("#ovClose");
    await page.click("#btnNext");
    await page.waitForTimeout(80);
  }
  await page.waitForTimeout(500);
  if (await page.locator("#lvlOverlay.on").isVisible()) await page.click("#ovClose");
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

  /* --- affichage large --- */
  await page.setViewportSize({ width: 900, height: 800 });
  ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "aucun défilement horizontal en 900px");
  await page.setViewportSize({ width: 320, height: 700 });
  ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), "aucun défilement horizontal en 320px");

  ok(problems.length === 0, "aucune erreur JavaScript : " + problems.slice(0, 5).join(" | "));

  await browser.close();
  console.log(`${pass} vérifications passées, ${fail} échec(s).`);
  if (fail) { [...new Set(errs)].forEach(e => console.log("  ✕ " + e)); process.exit(1); }
})();
