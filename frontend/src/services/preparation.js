import api from "./api";

export async function getPreparationTasks() {
  const { data } = await api.get("/preparation-tasks");
  return data;
}

export async function createPreparationTask(reminderId, title) {
  const { data } = await api.post(`/preparation-tasks/reminder/${reminderId}`, {
    title,
  });

  return data;
}

export async function updatePreparationTask(taskId, updates) {
  const { data } = await api.patch(`/preparation-tasks/${taskId}`, updates);

  return data;
}

export async function deletePreparationTask(taskId) {
  await api.delete(`/preparation-tasks/${taskId}`);
}

export async function generatePreparationSuggestions(reminderId) {
  const { data } = await api.post(
    `/preparation-ai/reminder/${reminderId}/generate`,
  );

  return data.suggestions;
}
