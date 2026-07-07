import { createContext, useEffect, useState } from "react";
import { getReminders } from "../services/reminder";

export const ReminderContext = createContext();

export function ReminderProvider({ children }) {
  const [reminders, setReminders] = useState([]);
  const [loading, setLoading] = useState(true);

  async function refreshReminders() {
    setLoading(true);

    try {
      const data = await getReminders();
      setReminders(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  function clearReminders() {
    setReminders([]);
  }

  useEffect(() => {
    refreshReminders();
  }, []);

  return (
    <ReminderContext.Provider
      value={{
        reminders,
        loading,
        refreshReminders,
        clearReminders,
      }}
    >
      {children}
    </ReminderContext.Provider>
  );
}
