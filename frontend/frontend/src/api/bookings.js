import http from "./http";

export async function createBooking(payload) {
  const res = await http.post("/bookings", payload);
  return res.data;
}

export async function fetchMyBookings() {
  const res = await http.get("/bookings/me");
  return res.data;
}
