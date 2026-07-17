// Eén enkele bron van waarheid voor alle Nederlandstalige fiches van « De wet met mij ».
// Zowel de themapagina's (/de-wet-met-mij/[thema]) als de zoekpagina (/de-wet-met-mij/zoeken)
// lezen uit dit bestand — zo is er GEEN duplicatie en blijft alles synchroon.
// Elke fiche citeert een reële wet/officiële bron (geen verzinsels). Gewestelijke materies
// (huur, energie) gebruiken de VLAAMSE regels, passend bij een Nederlandstalig publiek.

export type Fiche = {
  title: string;
  text: string;
  ref: string;
  url: string;
};

export type Thema = {
  slug: string;
  titel: string;
  emoji: string;
  beschrijving: string;
  fiches: Fiche[];
};

const wonen: Fiche[] = [
  {
    title: "De huurwaarborg bedraagt maximaal 3 maanden huur",
    text: "Voor een woninghuurcontract gesloten vanaf 1 januari 2019 mag de huurwaarborg niet meer bedragen dan 3 maanden huur, ongeacht de vorm. U kan kiezen voor een geïndividualiseerde rekening op uw naam, een zakelijke zekerheidstelling of een bankwaarborg via het OCMW.",
    ref: "Vlaams Woninghuurdecreet, art. 37 — huurwaarborg (max. 3 maanden)",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/huurprijs-en-huurwaarborg/huurwaarborg",
  },
  {
    title: "Een woninghuurcontract duurt in principe 9 jaar",
    text: "De standaardduur is 9 jaar. Wordt het niet tijdig opgezegd (minstens 6 maanden vóór de vervaldag), dan wordt het telkens met 3 jaar verlengd. Een kort contract (3 jaar of minder) is mogelijk, met eigen opzegregels.",
    ref: "Vlaams Woninghuurdecreet, art. 16 — duur van de overeenkomst",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/einde-en-opzegging-van-het-huurcontract",
  },
  {
    title: "Een omstandige plaatsbeschrijving beschermt u",
    text: "Een tegensprekelijke, gedetailleerde plaatsbeschrijving (bij intrede en uittrede) legt de staat van de woning vast. Ze moet samen met het huurcontract geregistreerd worden. Zonder plaatsbeschrijving is het voor de verhuurder zeer moeilijk om u schade aan te rekenen.",
    ref: "Vlaams Woninghuurdecreet — plaatsbeschrijving; registratie: FOD Financiën",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "U kan altijd opzeggen — let op de vergoeding de eerste 3 jaar",
    text: "Bij een 9-jarig contract kan de huurder op elk moment opzeggen met een opzegtermijn van 3 maanden. Beëindigt u tijdens de eerste 3 jaar, dan is een opzegvergoeding verschuldigd: 3 maanden huur (jaar 1), 2 maanden (jaar 2) of 1 maand (jaar 3). Vanaf het 4de jaar is er geen vergoeding meer.",
    ref: "Vlaams Woninghuurdecreet, art. 20 — opzegging door de huurder",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/huren-en-verhuren/einde-en-opzegging-van-het-huurcontract",
  },
  {
    title: "De huur wordt maar één keer per jaar geïndexeerd",
    text: "De verhuurder mag de huurprijs maximaal één keer per jaar indexeren, ten vroegste op de verjaardag van de inwerkingtreding van het contract, en alleen als het contract schriftelijk is. De indexering volgt de gezondheidsindex.",
    ref: "Vlaams Woninghuurdecreet — indexering van de huurprijs",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "Grote herstellingen zijn voor de verhuurder",
    text: "Het gewone onderhoud en de kleine herstellingen zijn voor de huurder; de grote herstellingen (dak, verwarmingsketel, slijtage door ouderdom of overmacht) zijn voor de verhuurder. Een officiële lijst verduidelijkt wie wat betaalt.",
    ref: "Vlaams Woninghuurdecreet + lijst van herstellingen (B.S. 19/12/2018)",
    url: "https://codex.vlaanderen.be/PrintDocument.ashx?id=1029963&geannoteerd=true",
  },
  {
    title: "Uw huurwoning moet aan kwaliteitsnormen voldoen",
    text: "Een gehuurde woning moet voldoen aan elementaire normen van veiligheid, gezondheid en woningkwaliteit (Vlaamse Codex Wonen). Voldoet de woning niet, dan kan u dit melden bij uw gemeente of Wonen in Vlaanderen.",
    ref: "Vlaamse Codex Wonen / Vlaams Woninghuurdecreet — woningkwaliteitsnormen",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/woningkwaliteit",
  },
  {
    title: "Bij verhuur is een EPC verplicht",
    text: "Wie een woning verhuurt, moet beschikken over een geldig energieprestatiecertificaat (EPC) en het energielabel vermelden in de advertentie. Zo weet u vooraf hoe energiezuinig de woning is.",
    ref: "Vlaams Energiedecreet / Energiebesluit (EPC) — Energiesparen (VEKA)",
    url: "https://www.energiesparen.be/epc-wonen",
  },
];

const werk: Fiche[] = [
  {
    title: "Een ontslag volgt strikte regels",
    text: "De werkgever moet het ontslag betekenen per aangetekende brief of via een deurwaarder. Een mondeling ontslag of een ontslag via een gewoon bericht respecteert de wettelijke vorm niet.",
    ref: "FOD Werkgelegenheid — einde van de arbeidsovereenkomst",
    url: "https://werk.belgie.be/nl/themas/arbeidsovereenkomsten/einde-van-de-arbeidsovereenkomst",
  },
  {
    title: "U heeft recht op een opzegtermijn (of een vergoeding)",
    text: "De duur van de opzegtermijn hangt af van uw anciënniteit. Respecteert de werkgever die niet, dan is hij u een overeenkomstige opzeggingsvergoeding verschuldigd.",
    ref: "FOD Werkgelegenheid — ontslag met opzegtermijn",
    url: "https://werk.belgie.be/nl/themas/arbeidsovereenkomsten/einde-van-de-arbeidsovereenkomst",
  },
  {
    title: "Het document C4 is u verschuldigd op het einde",
    text: "Op het einde van elke overeenkomst moet de werkgever u het C4 bezorgen. Dat dient om uw rechten op werkloosheidsuitkering bij de RVA te doen gelden.",
    ref: "RVA (officieel)",
    url: "https://www.rva.be/nl",
  },
  {
    title: "Een minimumloon is gegarandeerd",
    text: "In België bestaat een gewaarborgd gemiddeld minimum maandinkomen (GGMMI). Hogere minima kunnen gelden afhankelijk van uw sector (paritair comité).",
    ref: "FOD Werkgelegenheid — loon",
    url: "https://werk.belgie.be/nl/themas/loon",
  },
  {
    title: "U heeft recht op betaald verlof",
    text: "Een voltijdse werknemer (vijfdagenweek) heeft recht op minstens 20 wettelijke verlofdagen per jaar, als hij het voorgaande jaar gewerkt heeft.",
    ref: "FOD Werkgelegenheid — jaarlijkse vakantie",
    url: "https://werk.belgie.be/nl/themas/jaarlijkse-vakantie",
  },
  {
    title: "Het arbeidsreglement moet voor u toegankelijk zijn",
    text: "Uw onderneming moet een arbeidsreglement hebben en u een kopie bezorgen. Het legt de uurroosters, sancties en uw interne rechten vast.",
    ref: "FOD Werkgelegenheid — arbeidsreglement",
    url: "https://werk.belgie.be/nl/themas/arbeidsreglementering/arbeidsreglement",
  },
];

const juridischeHulp: Fiche[] = [
  {
    title: "Eerstelijnsbijstand is gratis voor iedereen",
    text: "Een eerste, kort juridisch advies is gratis en zonder inkomensvoorwaarde: men informeert u en oriënteert u. Beschikbaar via de Commissie voor Juridische Bijstand, justitiehuizen en wetswinkels.",
    ref: "Advocaat.be — juridische bijstand",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig/pro-deo-juridische-bijstand",
  },
  {
    title: "Tweedelijnsbijstand (« pro Deo ») volgens uw inkomen",
    text: "Om bijgestaan of vertegenwoordigd te worden door een advocaat, geheel of gedeeltelijk gratis, afhankelijk van uw inkomen. Het Bureau voor Juridische Bijstand (BJB) controleert uw voorwaarden en wijst een advocaat aan.",
    ref: "Advocaat.be — pro Deo",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig/pro-deo-juridische-bijstand",
  },
  {
    title: "Een ereloonovereenkomst beschermt u",
    text: "Vraag aan uw advocaat een duidelijke afspraak over de erelonen en kosten, liefst schriftelijk. Zo vermijdt u verrassingen en weet u vooraf waar u aan toe bent.",
    ref: "Advocaat.be — erelonen",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig",
  },
  {
    title: "Een rechtsbijstandsverzekering kan de kosten dekken",
    text: "Een rechtsbijstandsverzekering (soms gekoppeld aan uw familiale of autoverzekering) kan advocaat- en procedurekosten geheel of gedeeltelijk dekken. Controleer uw polissen.",
    ref: "Belgium.be — justitie",
    url: "https://www.belgium.be/nl/justitie",
  },
  {
    title: "Rechtsbijstand: vrijstelling van de gerechtskosten",
    text: "Naast een gratis advocaat bestaat de « rechtsbijstand »: een gehele of gedeeltelijke vrijstelling van de gerechtskosten (rolrechten, kosten van de gerechtsdeurwaarder, deskundige…). Ze wordt aangevraagd bij het bureau voor rechtsbijstand of bij de rechter die de zaak behandelt.",
    ref: "Gerechtelijk Wetboek, art. 664 en volgende — rechtsbijstand",
    url: "https://justitie.belgium.be/nl",
  },
  {
    title: "Welke documenten meebrengen?",
    text: "Voor het Bureau voor Juridische Bijstand brengt u uw identiteitskaart mee, een bewijs van uw inkomsten (loonfiche, uitkering, laatste aanslagbiljet) en, indien van toepassing, een attest van gezinssamenstelling. Bepaalde uitkeringsgerechtigden worden vermoed in aanmerking te komen.",
    ref: "Gerechtelijk Wetboek, art. 508/1 e.v. — juridische bijstand (toekenningsvoorwaarden)",
    url: "https://www.advocaat.be/nl/een-advocaat-nodig/pro-deo-juridische-bijstand",
  },
];

const consumentenrecht: Fiche[] = [
  {
    title: "Afstandsverkoop: 14 dagen bedenktijd",
    text: "Bij een online aankoop of aankoop op afstand (telefoon, verkoop aan de deur) heeft u 14 dagen om zich te bedenken, zonder reden op te geven. De termijn loopt vanaf de ontvangst van het pakket.",
    ref: "FOD Economie — herroepingsrecht",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Wettelijke garantie van 2 jaar",
    text: "Voor elke aankoop door een consument bij een onderneming geldt een wettelijke garantie van 2 jaar op een nieuw product, vanaf de levering. Ze dekt gebreken aan overeenstemming en komt bovenop elke commerciële garantie van de winkel.",
    ref: "FOD Economie — de garantie",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Volledige terugbetaling binnen 14 dagen",
    text: "Nadat u uw herroeping heeft gemeld, moet de verkoper u binnen 14 dagen terugbetalen — inclusief de standaard leveringskosten. Hij mag wachten tot hij het goed (of het verzendbewijs) terug heeft.",
    ref: "Belgium.be — consumentenbescherming",
    url: "https://www.belgium.be/nl/economie",
  },
  {
    title: "Niet elke aankoop heeft een herroepingsrecht",
    text: "De termijn van 14 dagen geldt niet voor alles: producten op maat of gepersonaliseerd, bederfbare goederen, gedownloade digitale inhoud (met uw akkoord), kranten, gedateerde tickets (concerten, reizen)… Controleer steeds de uitzonderingen vóór u koopt.",
    ref: "FOD Economie — uitzonderingen",
    url: "https://economie.fgov.be/nl/themas/consumentenbescherming",
  },
  {
    title: "Geschil? De Consumentenombudsdienst helpt gratis",
    text: "Reageert de verkoper niet, dan kan deze federale openbare dienst gratis bemiddelen om een minnelijke oplossing te vinden, of u doorverwijzen. Klaag eerst schriftelijk (e-mail of aangetekend) en bewaar een kopie.",
    ref: "Consumentenombudsdienst",
    url: "https://consumentenombudsdienst.be/nl",
  },
  {
    title: "Een consumentenkrediet getekend? U heeft 14 dagen bedenktijd",
    text: "Heeft u een consumentenkrediet (lening op afbetaling, kredietopening…) afgesloten, dan kan u zich binnen 14 kalenderdagen bedenken en de overeenkomst herroepen, zonder boete. U betaalt enkel het opgenomen kapitaal terug, vermeerderd met de intrest voor de gebruikte periode.",
    ref: "Wetboek van economisch recht, boek VII, art. VII.83 — herroepingsrecht consumentenkrediet",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/krediet/consumentenkrediet",
  },
  {
    title: "Te dure lening? Er zijn wettelijke maximumrentevoeten",
    text: "Vergelijk altijd het JKP (jaarlijks kostenpercentage): dat omvat alle kosten van het krediet. Voor consumentenkrediet gelden bovendien wettelijk vastgelegde maximale JKP's; een aanbod erboven is verboden.",
    ref: "Wetboek van economisch recht, boek VII — JKP en maximale rentevoeten",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/krediet/consumentenkrediet",
  },
];

const familie: Fiche[] = [
  {
    title: "Huwelijk, wettelijke en feitelijke samenwoning: drie heel verschillende statuten",
    text: "Feitelijke samenwoning schept geen juridische band: bij overlijden erft de partner niets automatisch. Wettelijke samenwoning (aangifte bij de gemeente) geeft bescherming van de gezinswoning en vruchtgebruik daarvan. Het huwelijk biedt de breedste bescherming: solidariteit, gewaarborgd reservatair deel en vruchtgebruik op de hele nalatenschap.",
    ref: "Belgium.be — koppel en scheiding",
    url: "https://www.belgium.be/nl/familie",
  },
  {
    title: "Een overeenkomst bij de notaris beschermt uw koppel",
    text: "Zonder huwelijkscontract valt u automatisch onder het wettelijk stelsel. Een huwelijkscontract, of een samenlevingscontract bij notariële akte, laat toe inkomsten, gezinskosten, woning en bescherming bij scheiding te regelen. Het beste moment om te beslissen is vóór een conflict.",
    ref: "Notaris.be — relaties en samenleven",
    url: "https://www.notaris.be/",
  },
  {
    title: "Echtscheiding: twee wegen, naargelang u akkoord bent of niet",
    text: "De echtscheiding met onderlinge toestemming veronderstelt een volledig akkoord (goederen, woning, kinderen, onderhoudsgeld) dat bij de familierechtbank wordt neergelegd — dit is het snelst. Zonder akkoord geldt de echtscheiding wegens onherstelbare ontwrichting: gezamenlijk na 6 maanden scheiding, of eenzijdig na 1 jaar.",
    ref: "Justitie — echtscheiding",
    url: "https://justitie.belgium.be/nl",
  },
  {
    title: "Scheiding en kinderen: het ouderlijk gezag blijft gezamenlijk",
    text: "Of u nu samenwoont of niet, het wettelijk principe is dat beide ouders samen het ouderlijk gezag uitoefenen (belangrijke beslissingen: gezondheid, school, religie). Voor het verblijf onderzoekt de familierechtbank bij onenigheid bij voorrang de gelijkmatig verdeelde huisvesting. Bemiddeling wordt aangemoedigd vóór de procedure.",
    ref: "Belgium.be — ouderlijk gezag",
    url: "https://www.belgium.be/nl/familie",
  },
  {
    title: "Erfenis: uw naasten kunnen niet volledig onterfd worden",
    text: "De Belgische wet beschermt bepaalde erfgenamen via een « reservatair deel »: kinderen (en bij huwelijk de langstlevende echtgenoot) kunnen niet volledig uit de erfenis worden gesloten, zelfs niet bij testament. Over een ander deel beschikt u vrij. De notaris is de sleutelfiguur voor een geldig testament of schenking.",
    ref: "Notaris.be",
    url: "https://www.notaris.be/",
  },
  {
    title: "Onderhoudsbijdrage voor de kinderen: beide ouders dragen bij",
    text: "Beide ouders moeten bijdragen in de kosten van hun kinderen, in verhouding tot hun draagkracht — ook na een scheiding en ongeacht of ze gehuwd waren. Het bedrag wordt vastgelegd in een akkoord of door de familierechtbank en is doorgaans jaarlijks indexeerbaar.",
    ref: "Burgerlijk Wetboek — onderhoudsplicht van de ouders (onderhoudsbijdrage), met indexering",
    url: "https://www.belgium.be/nl/familie",
  },
  {
    title: "Onderhoudsgeld niet betaald? DAVO kan helpen",
    text: "De Dienst voor Alimentatievorderingen (DAVO) bij de FOD Financiën int niet-betaald onderhoudsgeld bij de onderhoudsplichtige en kan, onder voorwaarden, een voorschot betalen op het onderhoudsgeld voor de kinderen (momenteel maximaal € 175 per kind per maand). De aanvraag is gratis.",
    ref: "FOD Financiën — Dienst voor Alimentatievorderingen (DAVO)",
    url: "https://fin.belgium.be/nl/particulieren/meer-diensten/onderhoudsgeld-davo",
  },
  {
    title: "Een conflict oplossen zonder proces: familiale bemiddeling",
    text: "In plaats van (of vóór) een procedure kan u een beroep doen op een erkende bemiddelaar in familiezaken. Samen zoekt u een akkoord (kinderen, woning, onderhoudsgeld); een akkoord kan daarna door de familierechtbank worden bekrachtigd. Bij sommige geschillen wijst de rechter zelf op de mogelijkheid van bemiddeling.",
    ref: "Gerechtelijk Wetboek, art. 1723 en volgende — bemiddeling",
    url: "https://justitie.belgium.be/nl",
  },
  {
    title: "Uw privacy: u heeft GDPR-rechten",
    text: "U kan toegang vragen tot uw gegevens, ze laten verbeteren of wissen, en zich verzetten tegen bepaald gebruik. Een organisatie moet in principe binnen één maand antwoorden. Bij problemen kan u klacht indienen bij de Gegevensbeschermingsautoriteit (GBA).",
    ref: "Gegevensbeschermingsautoriteit (GBA)",
    url: "https://www.gegevensbeschermingsautoriteit.be/burger",
  },
];

const administratie: Fiche[] = [
  {
    title: "Een beslissing van de administratie moet gemotiveerd zijn",
    text: "Sinds de wet van 29 juli 1991 moet elke individuele administratieve handeling « formeel gemotiveerd » worden: de beslissing moet de feitelijke en juridische redenen vermelden. Legt een beslissing niets uit, dan is dat al een argument in uw voordeel.",
    ref: "BOSA — wet van 29 juli 1991",
    url: "https://bosa.belgium.be/nl",
  },
  {
    title: "De brief moet zeggen hoe en binnen welke termijn u kan reageren",
    text: "Wanneer de administratie u een beslissing betekent waartegen beroep mogelijk is, moet ze de beroepsmogelijkheid, de termijn en de vorm vermelden. Lees steeds de onderkant van de brief: daar staan vaak uw beroepsmogelijkheden. Ontbreken die vermeldingen, dan is de termijn mogelijk niet tegenstelbaar.",
    ref: "Belgium.be — administratie",
    url: "https://www.belgium.be/nl",
  },
  {
    title: "De termijnen zijn kort: noteer de datum van kennisgeving",
    text: "In administratieve zaken lopen de termijnen meestal vanaf de dag na de kennisgeving. Voor een annulatieberoep bij de Raad van State bedraagt de termijn 60 dagen. Noteer onmiddellijk de ontvangstdatum en wacht niet: een overschreden termijn sluit de deur vaak definitief.",
    ref: "Raad van State — procedure",
    url: "https://www.raadvst-consetat.be/",
  },
  {
    title: "Het administratief beroep (gratis) vóór de rechter",
    text: "Vóór u naar een rechtbank stapt, kunnen veel beslissingen worden aangevochten via een administratief beroep: u vraagt de administratie (of een hogere instantie) haar beslissing te herzien. Dat is gratis, schriftelijk, en lost het probleem vaak op zonder proces. Respecteer de vorm en de termijn vermeld op de beslissing.",
    ref: "Belgium.be — administratie",
    url: "https://www.belgium.be/nl",
  },
  {
    title: "De federale Ombudsman: gratis, en hij « bevriest » uw termijn",
    text: "Bij een geschil met een federale administratie kan u zich gratis tot de federale Ombudsman wenden. Groot voordeel: zijn tussenkomst schorst de beroepstermijn bij de Raad van State voor maximaal 4 maanden. Mislukt de bemiddeling, dan rest u dus nog tijd. (Gewesten en gemeenten hebben ook hun ombudsmannen.)",
    ref: "Federale Ombudsman",
    url: "https://www.federaalombudsman.be/nl",
  },
];

const schulden: Fiche[] = [
  {
    title: "De collectieve schuldenregeling: een uitweg onder gerechtelijk toezicht",
    text: "Wie structureel niet meer in staat is zijn schulden te betalen, kan een collectieve schuldenregeling (CSR) aanvragen bij de arbeidsrechtbank. Alle schuldeisers worden samengebracht en dragen, onder toezicht van een rechter, bij tot een oplossing.",
    ref: "Wet van 5 juli 1998 betreffende de collectieve schuldenregeling; Gerechtelijk Wetboek, art. 1675/2 en volgende",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Voorwaarden om toegelaten te worden",
    text: "De CSR staat open voor een natuurlijke persoon die duurzaam niet in staat is zijn opeisbare schulden te betalen en die zijn onvermogen niet kennelijk zelf heeft georganiseerd. De aanvraag gebeurt via een verzoekschrift bij de arbeidsrechtbank.",
    ref: "Gerechtelijk Wetboek — toelaatbaarheidsvoorwaarden voor de CSR",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "De schuldbemiddelaar en uw leefgeld",
    text: "De rechtbank stelt een schuldbemiddelaar aan die uw inkomsten beheert en de schuldeisers terugbetaalt. U behoudt een leefgeld: een bedrag om menswaardig te leven (huisvesting, voeding, gezin).",
    ref: "Gerechtelijk Wetboek — schuldbemiddeling en leefgeld",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Gevolgen en duur",
    text: "Zodra de regeling toelaatbaar is, worden de invorderingen en beslagen in principe opgeschort. Op het einde van een aanzuiveringsregeling kan de rechter het saldo van bepaalde schulden kwijtschelden, zodat u opnieuw kunt starten.",
    ref: "Gerechtelijk Wetboek — gevolgen van de CSR en kwijtschelding van het saldo",
    url: "https://economie.fgov.be/nl/themas/financiele-diensten/schuldenlast/collectieve-schuldenregeling",
  },
  {
    title: "Niet heel uw loon kan in beslag worden genomen",
    text: "Een deel van uw loon is wettelijk beschermd en kan niet in beslag genomen worden. De voor beslag vatbare gedeelten en de drempels worden jaarlijks op 1 januari geïndexeerd en zijn hoger beschermd als u kinderen ten laste heeft.",
    ref: "Gerechtelijk Wetboek, art. 1409 en volgende (voor beslag vatbare gedeelten); jaarlijkse indexering op 1 januari",
    url: "https://werk.belgie.be/nl/themas/loon",
  },
  {
    title: "Eerst proberen: minnelijke schuldbemiddeling",
    text: "Vóór een gerechtelijke procedure kan een minnelijke schuldbemiddeling helpen om met de schuldeisers een afbetalingsplan af te spreken. De FOD Financiën voorziet bovendien eigen oplossingen (zoals een afbetalingsplan) voor schulden bij de fiscus.",
    ref: "FOD Financiën — wettelijke alternatieven bij betalingsmoeilijkheden",
    url: "https://fin.belgium.be/nl/particulieren/betalen-terugkrijgen/moeilijkheden-betalen/alternatieve-mogelijkheden",
  },
];

const geweld: Fiche[] = [
  {
    title: "U ondervindt geweld: bel 1712 (gratis en anoniem)",
    text: "1712 is de hulplijn voor elke vraag over geweld, misbruik en kindermishandeling. Het nummer is gratis, verschijnt niet op de telefoonrekening en u hoeft niet te zeggen wie u bent. In een levensbedreigende situatie belt u de politie op 101 of de noodcentrale 112.",
    ref: "Hulplijn 1712 (officieel) — gratis en anoniem",
    url: "https://www.1712.be/nl",
  },
  {
    title: "De pleger kan tijdelijk uit de woning worden gezet",
    text: "Bij huiselijk geweld kan een tijdelijk huisverbod worden opgelegd: de persoon die een ernstige bedreiging vormt, mag de gezamenlijke woning gedurende een bepaalde periode niet betreden. Zo kan het slachtoffer in veiligheid blijven.",
    ref: "Wet van 15 mei 2012 betreffende het tijdelijk huisverbod in geval van huiselijk geweld",
    url: "https://www.vlaanderen.be/hulplijn-geweld-misbruik-en-kindermishandeling-1712",
  },
  {
    title: "Uzelf beschermen en een dossier opbouwen",
    text: "Opzettelijke slagen en verwondingen en bedreigingen zijn strafbaar. U kunt klacht indienen bij de politie. Bewaar bewijzen (medische attesten, foto's, berichten, getuigenissen): ze versterken uw dossier.",
    ref: "Strafwetboek — opzettelijke slagen en verwondingen, bedreigingen; klacht bij de politie",
    url: "https://www.1712.be/nl",
  },
  {
    title: "Gratis slachtofferhulp bestaat",
    text: "De Centra voor Algemeen Welzijnswerk (CAW) bieden gratis slachtofferhulp: een luisterend oor, psychosociale ondersteuning en hulp bij administratieve en juridische stappen. 1712 verwijst u door naar de dienst die het best bij u past.",
    ref: "Vlaanderen.be — hulplijn 1712 en slachtofferhulp (CAW)",
    url: "https://www.vlaanderen.be/hulplijn-geweld-misbruik-en-kindermishandeling-1712",
  },
];

const gezondheid: Fiche[] = [
  {
    title: "U heeft zeven wettelijke patiëntenrechten",
    text: "Elke patiënt heeft recht op: kwaliteitsvolle zorg; vrije keuze van zorgverlener; informatie over zijn gezondheidstoestand; vrije en geïnformeerde toestemming; een zorgvuldig bijgehouden dossier (met inzage en afschrift); respect voor privacy; en het neerleggen van een klacht bij een ombudsfunctie.",
    ref: "Wet van 22 augustus 2002 betreffende de rechten van de patiënt (gewijzigd op 6 februari 2024)",
    url: "https://www.health.belgium.be/nl/professionals/gezondheidsprofessionals/menselijke-gezondheid/kwaliteit-veiligheid-gezondheidszorg/rechten-patient/rechten-patient",
  },
  {
    title: "Geen behandeling zonder uw toestemming",
    text: "Een zorgverlener mag in principe niet ingrijpen zonder uw vrije en geïnformeerde toestemming. U moet vooraf duidelijke informatie krijgen over het doel, de risico's en de alternatieven, en u mag een behandeling weigeren of stopzetten.",
    ref: "Wet van 22 augustus 2002 — vrije en geïnformeerde toestemming",
    url: "https://www.ejustice.just.fgov.be/eli/wet/2002/08/22/2002022737/justel",
  },
  {
    title: "U mag uw patiëntendossier inkijken",
    text: "U heeft recht op inzage in uw patiëntendossier en op een afschrift ervan. De zorgverlener moet hier binnen een redelijke termijn gevolg aan geven; bepaalde persoonlijke notities en gegevens over derden kunnen worden uitgesloten.",
    ref: "Wet van 22 augustus 2002 — inzage in en afschrift van het patiëntendossier",
    url: "https://www.ejustice.just.fgov.be/eli/wet/2002/08/22/2002022737/justel",
  },
  {
    title: "Een recht werd niet gerespecteerd? Er is een ombudsdienst",
    text: "Als een van uw patiëntenrechten niet werd nageleefd, kunt u een klacht neerleggen bij een ombudsfunctie. Voor zorg buiten het ziekenhuis bestaat de federale ombudsdienst « Rechten van de patiënt ». De bemiddeling is gratis.",
    ref: "Wet van 22 augustus 2002 — recht op klacht bij de ombudsfunctie",
    url: "https://www.health.belgium.be/nl/professionals/gezondheidsprofessionals/menselijke-gezondheid/kwaliteit-veiligheid-gezondheidszorg/rechten-patient",
  },
];

const energie: Fiche[] = [
  {
    title: "U kunt uw energiefactuur niet betalen: u wordt niet zomaar afgesloten",
    text: "Bij niet-betaling volgt een vaste procedure: eerst een betalingsherinnering (u heeft 15 dagen), dan een ingebrekestelling. Zegt de leverancier daarna uw contract op, dan moet hij nog minstens 45 kalenderdagen energie blijven leveren. Vindt u geen nieuwe leverancier, dan levert netbeheerder Fluvius verder als sociale leverancier.",
    ref: "Vlaanderen.be — wat als u uw factuur voor elektriciteit en aardgas niet betaalt",
    url: "https://www.vlaanderen.be/wat-als-u-uw-factuur-voor-elektriciteit-en-aardgas-niet-betaalt",
  },
  {
    title: "Beschermde afnemers en het sociaal tarief",
    text: "Wie bepaalde uitkeringen of tegemoetkomingen geniet, is « beschermde afnemer » en heeft recht op het sociaal tarief (sociale maximumprijs) — doorgaans zo'n 30 % goedkoper. Het wordt automatisch toegekend: de FOD Economie geeft de rechthebbenden door aan de leveranciers, u hoeft geen attest meer te bezorgen.",
    ref: "Vlaanderen.be — sociaal tarief voor energie (elektriciteit, aardgas, warmte)",
    url: "https://www.vlaanderen.be/sociaal-tarief-voor-energie-elektriciteit-aardgas-warmte",
  },
  {
    title: "Afsluiten kan enkel via de Lokale Adviescommissie (LAC)",
    text: "De netbeheerder mag u niet zomaar afsluiten: een afsluiting vereist in principe de toestemming van de Lokale Adviescommissie (LAC). Beschermde afnemers genieten bovendien extra waarborgen, zoals een gratis betalingsherinnering en ingebrekestelling.",
    ref: "Vlaamse Nutsregulator — sociaal energiebeleid",
    url: "https://www.vlaamsenutsregulator.be/elektriciteit-en-aardgas/energieprijzen-en-facturen/sociaal-energiebeleid",
  },
  {
    title: "Van energieleverancier veranderen is gratis",
    text: "U mag op elk moment van leverancier veranderen. U tekent gewoon een contract bij een nieuwe leverancier; die regelt de overstap en u hoeft uw oude contract niet zelf op te zeggen. Houd rekening met een opzegtermijn van minstens 3 weken. Met de V-test® van de Vlaamse Nutsregulator vergelijkt u de prijzen.",
    ref: "Vlaanderen.be — energieleveranciers en energiecontracten",
    url: "https://www.vlaanderen.be/bouwen-wonen-en-energie/elektriciteit-en-aardgas/energieleveranciers-en-energiecontracten",
  },
];

const ouderen: Fiche[] = [
  {
    title: "Wat is ouderenmis(be)handeling?",
    text: "Het gaat om elke vorm van geweld of verwaarlozing tegenover een oudere persoon: lichamelijk, psychisch, seksueel, maar ook financieel geweld of verwaarlozing (verkeerde medicatie, geen schone kleren, onvoldoende verzorging). Misbruik van iemands kwetsbare toestand is strafbaar.",
    ref: "Strafwetboek — misbruik van de zwakke toestand (art. 442quater) en geweldsmisdrijven",
    url: "https://www.vlaanderen.be/gezondheid-en-welzijn/conflicten-en-misdrijven/hulp-en-melding/geweld-en-misbruik-bij-ouderen",
  },
  {
    title: "U bent (of ziet) een mishandelde oudere: wie bellen?",
    text: "Bij mishandeling thuis kunt u — net als familie of vrienden — gratis bellen naar 1712, de hulplijn voor geweld, misbruik en kindermishandeling. Gaat het om mishandeling in een woonzorgcentrum, dan kunt u terecht bij de Woonzorglijn. De hulp is gratis en anoniem.",
    ref: "Vlaanderen.be — geweld en misbruik bij ouderen (hulplijn 1712, Woonzorglijn)",
    url: "https://www.vlaanderen.be/gezondheid-en-welzijn/conflicten-en-misdrijven/hulp-en-melding/geweld-en-misbruik-bij-ouderen",
  },
  {
    title: "Financieel misbruik telt ook mee",
    text: "Een veelvoorkomende vorm bij ouderen is financieel misbruik: geld of bezittingen afnemen, misbruik van een volmacht of bankkaart, druk uitoefenen om documenten te tekenen. Ook daarvoor kunt u terecht bij 1712 om uw situatie te bespreken.",
    ref: "Hulplijn 1712 — ouderenmis(be)handeling (incl. financieel geweld)",
    url: "https://www.1712.be/nl/soorten-geweld/ouderenmisbehandeling",
  },
  {
    title: "Professionals: contacteer VLOCO",
    text: "Komt u beroepsmatig in contact met ouderen en vermoedt u mis(be)handeling, dan kunt u terecht bij het Vlaams Ondersteuningscentrum Ouderenmis(be)handeling (VLOCO), het aanspreekpunt voor professionals. Iedereen — buur, familie, zorgverlener — kan een verschil maken door het gesprek aan te durven gaan.",
    ref: "Hulplijn 1712 — doorverwijzing naar VLOCO (vloco.be)",
    url: "https://www.1712.be/nl/soorten-geweld/ouderenmisbehandeling",
  },
];

// Per-slug toegang (gebruikt door de themapagina's).
export const NL_FICHES: Record<string, Fiche[]> = {
  wonen,
  werk,
  "juridische-hulp": juridischeHulp,
  consumentenrecht,
  familie,
  administratie,
  schulden,
  geweld,
  gezondheid,
  energie,
  ouderen,
};

// Volledige themalijst met metadata (gebruikt door de hub en de zoekpagina).
export const NL_THEMES: Thema[] = [
  { slug: "wonen", titel: "Wonen & huur", emoji: "🏠", beschrijving: "Huurwaarborg, plaatsbeschrijving, opzeg, herstellingen.", fiches: wonen },
  { slug: "werk", titel: "Werk", emoji: "💼", beschrijving: "Opzeg, ontslag, C4, minimumloon, verlof.", fiches: werk },
  { slug: "juridische-hulp", titel: "Juridische hulp", emoji: "⚖️", beschrijving: "Gratis eerste advies en pro-Deo-advocaat volgens inkomen.", fiches: juridischeHulp },
  { slug: "consumentenrecht", titel: "Consumentenrecht", emoji: "🛒", beschrijving: "Herroepingsrecht, garantie, aankopen.", fiches: consumentenrecht },
  { slug: "familie", titel: "Familie & privacy", emoji: "👪", beschrijving: "Samenwonen, scheiding, GDPR-rechten.", fiches: familie },
  { slug: "administratie", titel: "Administratieve stappen", emoji: "📄", beschrijving: "Beroep, termijnen, ombudsman.", fiches: administratie },
  { slug: "schulden", titel: "Schulden", emoji: "💶", beschrijving: "Collectieve schuldenregeling, schuldbemiddelaar, bescherming van uw loon.", fiches: schulden },
  { slug: "geweld", titel: "Geweld & slachtofferhulp", emoji: "🆘", beschrijving: "1712, tijdelijk huisverbod, klacht, gratis slachtofferhulp.", fiches: geweld },
  { slug: "gezondheid", titel: "Gezondheid & patiëntenrechten", emoji: "🩺", beschrijving: "Toestemming, inzage in uw dossier, klachtrecht en ombudsfunctie.", fiches: gezondheid },
  { slug: "energie", titel: "Energie", emoji: "⚡", beschrijving: "Betalingsmoeilijkheden, sociaal tarief, afsluiting, van leverancier veranderen.", fiches: energie },
  { slug: "ouderen", titel: "Bescherming van ouderen", emoji: "🧓", beschrijving: "Ouderenmis(be)handeling herkennen, 1712, Woonzorglijn, VLOCO.", fiches: ouderen },
];
