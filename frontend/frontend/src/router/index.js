import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import HousesView from "../views/HousesView.vue";
import LoginView from "../views/LoginView.vue";
import MyBookingsView from "../views/MyBookingsView.vue";
import AdminView from "../views/AdminView.vue";
import { fetchMe } from "../api/auth";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/houses", name: "houses", component: HousesView },
  { path: "/bookings", name: "bookings", component: MyBookingsView },
  { path: "/admin", name: "admin", component: AdminView },
  { path: "/login", name: "login", component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

let mePromise = null;

async function resolveRole() {
  const token = localStorage.getItem("token");
  if (!token) return null;

  const cachedRole = localStorage.getItem("userRole");
  if (cachedRole) return cachedRole;

  if (!mePromise) {
    mePromise = fetchMe()
      .then((me) => {
        if (me?.name) localStorage.setItem("userName", me.name);
        if (me?.role) localStorage.setItem("userRole", me.role);
        return me?.role || null;
      })
      .catch(() => {
        localStorage.removeItem("userRole");
        return null;
      })
      .finally(() => {
        mePromise = null;
      });
  }

  return mePromise;
}

router.beforeEach(async (to) => {
  if (to.path === "/login") return true;

  const role = await resolveRole();

  if (to.path === "/bookings" && role === "admin") {
    return "/admin";
  }

  if (to.path === "/admin" && role !== "admin") {
    return "/bookings";
  }

  return true;
});

export default router;
