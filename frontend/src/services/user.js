import api from "./api";

export async function getCurrentUser() {
  const response = await api.get("/user/me");
  return response.data;
}

export async function deleteAccount() {
  const response = await api.delete("/user/account");
  return response.data;
}
