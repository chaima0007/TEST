import BulleHeader from "@/components/bulle/BulleHeader";
import CalmTools from "@/components/bulle/CalmTools";

export default function CalmePage() {
  return (
    <main>
      <BulleHeader home="/bulle/enfant" />
      <h1 className="text-3xl font-extrabold">
        <span aria-hidden>🎈 </span>Mon coin calme
      </h1>
      <p className="mt-2 text-[var(--b-muted)]">
        Quand c’est trop fort à l’intérieur, on ralentit. Le corps se calme d’abord, les mots
        viennent après.
      </p>
      <div className="mt-6">
        <CalmTools />
      </div>
    </main>
  );
}
