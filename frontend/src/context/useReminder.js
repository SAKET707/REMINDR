import { useContext } from "react";
import { ReminderContext } from "./ReminderContext";

export function useReminder() {
  return useContext(ReminderContext);
}
