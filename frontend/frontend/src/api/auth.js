import http from "./http";

export async function login(email, password) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);

  const res = await http.post("/auth/login", form);
  return res.data;
}

export async function register(payload) {
  const res = await http.post("/auth/register", payload);
  return res.data;
}
