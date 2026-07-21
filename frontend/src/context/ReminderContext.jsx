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
  function removeReminder(id) {
    setReminders((prev) => prev.filter((r) => r.id !== id));
  }

  function replaceReminder(updatedReminder) {
    setReminders((prev) =>
      prev.map((r) => (r.id === updatedReminder.id ? updatedReminder : r)),
    );
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
        removeReminder,
        replaceReminder,
      }}
    >
      {children}
    </ReminderContext.Provider>
  );
}
