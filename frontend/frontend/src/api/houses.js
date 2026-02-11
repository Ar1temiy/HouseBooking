import http from "./http";

export async function fetchHouses() {
  const res = await http.get("/houses");
  return res.data;
}

export async function fetchAvailability(houseId, dateFrom, dateTo) {
  const res = await http.get(`/houses/${houseId}/availability`, {
    params: { date_from: dateFrom, date_to: dateTo },
  });
  return res.data;
}
