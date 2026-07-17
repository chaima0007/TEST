import BulleHeader from "@/components/bulle/BulleHeader";
import ParentalGate from "@/components/bulle/ParentalGate";
import ParentSpace from "@/components/bulle/ParentSpace";

export default function ParentPage() {
  return (
    <main>
      <BulleHeader />
      <ParentalGate>
        <ParentSpace />
      </ParentalGate>
    </main>
  );
}
