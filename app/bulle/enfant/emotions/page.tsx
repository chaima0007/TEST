import BulleHeader from "@/components/bulle/BulleHeader";
import EmotionExplorer from "@/components/bulle/EmotionExplorer";

export default function EmotionsPage() {
  return (
    <main>
      <BulleHeader home="/bulle/enfant" />
      <h1 className="text-3xl font-extrabold">
        <span aria-hidden>🃏 </span>Mes cartes émotions
      </h1>
      <p className="mt-2 text-[var(--b-muted)]">
        Chaque émotion a une raison d’être. On la nomme, puis on trouve ce qui aide.
      </p>
      <div className="mt-6">
        <EmotionExplorer />
      </div>
    </main>
  );
}
