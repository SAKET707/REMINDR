export default function BulletList({ children }) {
  return (
    <ul className="list-disc space-y-3 pl-6 marker:text-primary-light">
      {children}
    </ul>
  );
}
