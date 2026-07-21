import api from "./api";

export async function getReminders() {
  const response = await api.get("/reminders");
  return response.data;
}

export async function deleteReminder(id) {
  await api.delete(`/reminders/${id}`);
}

export async function updateReminder(id, scheduled_for) {
  const { data } = await api.patch(`/reminders/${id}`, {
    scheduled_for,
  });

  return data;
}
