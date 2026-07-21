import { useState } from "react";
import Sidebar from "../components/dashboard/Sidebar";

export default function AppLayout({ children }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <main className="flex min-h-screen bg-background-soft">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

      <section className="min-w-0 flex-1">
        <div className="mx-auto w-full max-w-7xl p-5 sm:p-7 lg:p-10">
          {children}
        </div>
      </section>
    </main>
  );
}
