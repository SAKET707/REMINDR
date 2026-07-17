export default function Section({ title, children }) {
  return (
    <section className="scroll-mt-24">
      <div className="mb-5 flex items-center gap-4">
        <div className="h-8 w-1 rounded-full bg-primary-light"></div>

        <h2 className="font-heading text-2xl font-semibold text-primary md:text-3xl">
          {title}
        </h2>
      </div>

      <div className="space-y-5 text-[16px] leading-8 text-text-secondary">
        {children}
      </div>
    </section>
  );
}
