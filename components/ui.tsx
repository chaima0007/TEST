"use client";

// Petites primitives d'UI partagées.

export function PageHeader({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow?: string;
  title: string;
  subtitle?: string;
}) {
  return (
    <header className="px-5 pt-7 pb-3">
      {eyebrow ? <p className="eyebrow mb-1">{eyebrow}</p> : null}
      <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
      {subtitle ? <p className="text-muted text-sm mt-1">{subtitle}</p> : null}
    </header>
  );
}

export function Section({
  title,
  children,
  action,
}: {
  title?: string;
  children: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <section className="px-4 mt-4">
      {title ? (
        <div className="flex items-center justify-between px-1 mb-2">
          <h2 className="text-sm font-bold text-foreground/80">{title}</h2>
          {action}
        </div>
      ) : null}
      {children}
    </section>
  );
}

export function Loading() {
  return (
    <div className="px-4 pt-24 flex flex-col items-center text-muted">
      <span className="text-3xl mb-2" aria-hidden>
        🫀
      </span>
      <p className="text-sm">Un instant…</p>
    </div>
  );
}
