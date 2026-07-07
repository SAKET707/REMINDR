import { useState } from "react";
import Sidebar from "../components/dashboard/Sidebar";

export default function AppLayout({ children }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <main className="flex min-h-screen bg-background-soft">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

      <section className="flex-1 p-10">{children}</section>
    </main>
  );
}
