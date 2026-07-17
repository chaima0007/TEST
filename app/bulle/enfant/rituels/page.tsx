import BulleHeader from "@/components/bulle/BulleHeader";
import RitualsScreen from "@/components/bulle/RitualsScreen";

export default function RituelsPage() {
  return (
    <main>
      <BulleHeader home="/bulle/enfant" />
      <h1 className="text-3xl font-extrabold">
        <span aria-hidden>🪄 </span>Nos rituels
      </h1>
      <p className="mt-2 text-[var(--b-muted)]">
        À faire <strong>ensemble</strong>&nbsp;: on se passe le téléphone quand c’est au tour de
        l’autre. Choisis un rituel.
      </p>
      <div className="mt-6">
        <RitualsScreen />
      </div>
    </main>
  );
}
