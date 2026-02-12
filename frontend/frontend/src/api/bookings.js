import http from "./http";

export async function createBooking(payload) {
  const res = await http.post("/bookings", payload);
  return res.data;
}

export async function fetchMyBookings() {
  const res = await http.get("/bookings/me");
  return res.data;
}

export async function fetchAllBookings() {
  const res = await http.get("/bookings/all");
  return res.data;
}

export async function confirmBooking(bookingId) {
  const res = await http.patch(`/bookings/${bookingId}/confirm`);
  return res.data;
}

export async function adminCancelBooking(bookingId) {
  const res = await http.patch(`/bookings/${bookingId}/admin-cancel`);
  return res.data;
}
