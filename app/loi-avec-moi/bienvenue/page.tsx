import Link from "next/link";

// Page d'accueil multilingue (espace Belgique).
// Objectif : qu'une personne arrivant en Belgique, quelle que soit sa langue, comprenne
// immédiatement (1) ce qu'est ce site, (2) que c'est gratuit, (3) où trouver de l'aide
// en cas d'urgence, (4) comment accéder à ses droits.
// Honnête : les pages détaillées sont en français ; cette page oriente dans la langue de l'usager.
// Le 112 est le numéro d'urgence européen (valable en Belgique), gratuit, 24h/24.

const HUB = "/loi-avec-moi";

type Lang = {
  code: string;
  label: string;
  dir?: "rtl";
  greeting: string;
  intro: string;
  urgent: string;
  cta: string;
};

const LANGS: Lang[] = [
  { code: "FR", label: "Français", greeting: "Bienvenue", intro: "Ce site explique vos droits en mots simples et clairs — gratuitement.", urgent: "En danger immédiat ? Appelez le 112 (gratuit, 24h/24).", cta: "Découvrir mes droits" },
  { code: "NL", label: "Nederlands", greeting: "Welkom", intro: "Deze site legt uw rechten uit in eenvoudige, duidelijke taal — gratis.", urgent: "In direct gevaar? Bel 112 (gratis, 24/7).", cta: "Ontdek mijn rechten" },
  { code: "EN", label: "English", greeting: "Welcome", intro: "This site explains your rights in simple, clear language — for free.", urgent: "In immediate danger? Call 112 (free, 24/7).", cta: "Discover my rights" },
  { code: "AR", label: "العربية", dir: "rtl", greeting: "مرحبا", intro: "يشرح هذا الموقع حقوقك بلغة بسيطة وواضحة — مجانًا.", urgent: "في خطر فوري؟ اتصل بالرقم 112 (مجاني، على مدار الساعة).", cta: "اكتشف حقوقي" },
  { code: "FA", label: "فارسی", dir: "rtl", greeting: "خوش آمدید", intro: "این وب‌سایت حقوق شما را به زبان ساده و روشن توضیح می‌دهد — رایگان.", urgent: "در خطر فوری هستید؟ با ۱۱۲ تماس بگیرید (رایگان، شبانه‌روزی).", cta: "حقوق من را کشف کنید" },
  { code: "UK", label: "Українська", greeting: "Ласкаво просимо", intro: "Цей сайт пояснює ваші права простою та зрозумілою мовою — безкоштовно.", urgent: "Вам загрожує небезпека? Телефонуйте 112 (безкоштовно, цілодобово).", cta: "Дізнатися про мої права" },
  { code: "RU", label: "Русский", greeting: "Добро пожаловать", intro: "Этот сайт объясняет ваши права простым и понятным языком — бесплатно.", urgent: "Вам угрожает опасность? Звоните 112 (бесплатно, круглосуточно).", cta: "Узнать мои права" },
  { code: "TR", label: "Türkçe", greeting: "Hoş geldiniz", intro: "Bu site haklarınızı basit ve anlaşılır bir dille açıklar — ücretsiz.", urgent: "Acil tehlikede misiniz? 112'yi arayın (ücretsiz, 7/24).", cta: "Haklarımı keşfet" },
  { code: "ES", label: "Español", greeting: "Bienvenido", intro: "Este sitio explica sus derechos en un lenguaje sencillo y claro — gratis.", urgent: "¿En peligro inmediato? Llame al 112 (gratuito, 24/7).", cta: "Descubrir mis derechos" },
  { code: "PT", label: "Português", greeting: "Bem-vindo", intro: "Este site explica os seus direitos numa linguagem simples e clara — gratuitamente.", urgent: "Em perigo imediato? Ligue 112 (gratuito, 24/7).", cta: "Descobrir os meus direitos" },
  { code: "RO", label: "Română", greeting: "Bun venit", intro: "Acest site vă explică drepturile într-un limbaj simplu și clar — gratuit.", urgent: "În pericol imediat? Sunați la 112 (gratuit, 24/7).", cta: "Descoperă drepturile mele" },
  { code: "DE", label: "Deutsch", greeting: "Willkommen", intro: "Diese Website erklärt Ihre Rechte in einfacher, klarer Sprache — kostenlos.", urgent: "In unmittelbarer Gefahr? Rufen Sie 112 an (kostenlos, rund um die Uhr).", cta: "Meine Rechte entdecken" },
  { code: "IT", label: "Italiano", greeting: "Benvenuto", intro: "Questo sito spiega i tuoi diritti in un linguaggio semplice e chiaro — gratis.", urgent: "In pericolo immediato? Chiama il 112 (gratuito, 24/7).", cta: "Scopri i miei diritti" },
  { code: "PL", label: "Polski", greeting: "Witamy", intro: "Ta strona wyjaśnia Twoje prawa prostym i jasnym językiem — za darmo.", urgent: "W bezpośrednim niebezpieczeństwie? Zadzwoń pod 112 (bezpłatnie, 24/7).", cta: "Poznaj moje prawa" },
];

export default function BienvenuePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-b from-indigo-950 to-slate-900 text-white">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            background:
              "radial-gradient(60% 60% at 50% 0%, rgba(99,102,241,0.25) 0%, rgba(15,23,42,0) 70%)",
          }}
        />
        <div className="relative max-w-3xl mx-auto px-6 py-16 text-center">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/15 text-indigo-100 text-sm font-medium mb-6">
            🌍 Welcome · مرحبا · Ласкаво просимо · Bienvenue
          </span>
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight">
            Le droit accessible pour tous
          </h1>
          <p className="mt-5 text-lg text-indigo-100 leading-relaxed">
            Trouvez votre langue ci-dessous. Vous comprendrez l&apos;essentiel tout de suite —
            et vous saurez où aller pour la suite.
          </p>
        </div>
      </section>

      {/* Note d'honnêteté */}
      <section className="px-6 py-10 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5 text-sm leading-relaxed text-amber-900">
          <p>
            <strong>En toute transparence&nbsp;:</strong> cette page d&apos;accueil vous oriente dans
            votre langue. Les fiches détaillées du site sont rédigées en <strong>français</strong> (et
            en néerlandais pour la Belgique). Pour les lire dans votre langue, utilisez la traduction
            automatique de votre navigateur — et en cas de doute important, demandez l&apos;aide
            d&apos;un service gratuit (nous vous indiquons lesquels).
          </p>
        </div>
      </section>

      {/* Cartes par langue */}
      <section className="px-6 pb-16 max-w-5xl mx-auto">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {LANGS.map((l) => (
            <div
              key={l.code}
              dir={l.dir ?? "ltr"}
              className="flex flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="flex items-center justify-between gap-2">
                <h2 className="text-xl font-bold tracking-tight text-slate-900">{l.greeting}</h2>
                <span className="flex-shrink-0 rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-semibold text-indigo-700">
                  {l.label}
                </span>
              </div>
              <p className="mt-2.5 text-sm text-slate-600 leading-relaxed">{l.intro}</p>
              <p className="mt-3 rounded-lg bg-rose-50 border border-rose-100 px-3 py-2 text-xs font-medium text-rose-800 leading-relaxed">
                ⚠️ {l.urgent}
              </p>
              <Link
                href={HUB}
                className="mt-4 inline-flex items-center justify-center gap-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 px-4 py-2.5 text-sm font-semibold text-white transition-colors"
              >
                {l.cta} <span aria-hidden="true">→</span>
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Aide humaine */}
      <section className="px-6 pb-20 max-w-3xl mx-auto">
        <div className="rounded-2xl border border-indigo-200 bg-indigo-50 p-6">
          <h2 className="font-semibold text-indigo-900 text-lg">Besoin d&apos;une aide humaine&nbsp;?</h2>
          <p className="text-indigo-800/90 mt-2 text-sm leading-relaxed">
            En Belgique, des services gratuits peuvent vous accompagner&nbsp;: les{" "}
            <strong>CPAS</strong> (aide sociale), les <strong>maisons de justice</strong>, l&apos;
            <strong>aide juridique de première ligne</strong> (consultation gratuite d&apos;un avocat),
            et de nombreuses associations. Beaucoup disposent d&apos;interprètes.
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              href="/loi-avec-moi/trouver-un-avocat"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white border border-indigo-200 px-4 py-2.5 text-sm font-semibold text-indigo-700 hover:bg-indigo-100 transition-colors"
            >
              Trouver un avocat (aide gratuite) →
            </Link>
            <Link
              href="/loi-avec-moi/nos-assistants"
              className="inline-flex items-center gap-1.5 rounded-xl bg-white border border-indigo-200 px-4 py-2.5 text-sm font-semibold text-indigo-700 hover:bg-indigo-100 transition-colors"
            >
              Qui sont nos assistants ? →
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-100 py-8 px-6 text-center text-sm text-slate-500">
        <Link href={HUB} className="hover:text-slate-900">
          ← La loi avec moi
        </Link>
      </footer>
    </main>
  );
}
