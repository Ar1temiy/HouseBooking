import http from "./http";

export async function login(email, password) {
  // OAuth2PasswordRequestForm ждёт form-data, а не JSON
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);

  const res = await http.post("/auth/login", form);
  return res.data; // {access_token, token_type}
}
