import { Link } from "react-router-dom";

export default function PolicyLayout({ title, subtitle, children }) {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background-soft">
      {/* Background Blur Effects */}

      <div className="absolute -top-32 -right-32 h-96 w-96 rounded-full bg-primary-light/20 blur-3xl"></div>

      <div className="absolute bottom-0 -left-32 h-96 w-96 rounded-full bg-primary/10 blur-3xl"></div>

      {/* Hero Section */}

      <section className="relative bg-primary text-white">
        <div className="mx-auto max-w-5xl px-6 py-16 md:px-10 md:py-20">
          <Link
            to="/"
            className="inline-flex items-center gap-2 rounded-full border border-white/20 px-4 py-2 text-sm transition hover:bg-white hover:text-primary"
          >
            ← Back to Home
          </Link>

          <div className="mt-10 h-1 w-24 rounded-full bg-primary-light"></div>

          <h1 className="mt-6 font-heading text-4xl font-bold md:text-5xl">
            {title}
          </h1>

          <p className="mt-5 max-w-3xl text-base leading-8 text-secondary-light md:text-lg">
            {subtitle}
          </p>
        </div>
      </section>

      {/* Content Card */}

      <main className="relative mx-auto -mt-8 max-w-5xl px-6 pb-20 md:-mt-12 md:px-10">
        <div className="rounded-3xl border border-border bg-card p-8 shadow-2xl md:p-12">
          {children}

          {/* Footer */}

          <div className="mt-16 border-t border-border pt-8 text-center text-sm text-text-secondary">
            © {new Date().getFullYear()} REMINDR. All rights reserved.
          </div>
        </div>
      </main>
    </div>
  );
}
