import { createContext, useState } from "react";

export const SidebarContext = createContext();

export function SidebarProvider({ children }) {
  const [collapsed, setCollapsed] = useState(() => window.innerWidth < 1024);

  return (
    <SidebarContext.Provider
      value={{
        collapsed,
        setCollapsed,
      }}
    >
      {children}
    </SidebarContext.Provider>
  );
}
