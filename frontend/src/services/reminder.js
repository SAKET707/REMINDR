import api from "./api";

export async function getReminders() {
  const response = await api.get("/reminders");
  return response.data;
}
