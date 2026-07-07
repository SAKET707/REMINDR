import api from "./api";

export async function connectTelegram() {
  const response = await api.post("/telegram/connect");
  return response.data;
}
