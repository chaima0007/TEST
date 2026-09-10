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
  ok(cards === 3, "les 3 mondes remplis sont proposés, les autres non (" + cards + ")");
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
