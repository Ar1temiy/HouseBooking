import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import HousesView from "../views/HousesView.vue";
import LoginView from "../views/LoginView.vue";
import MyBookingsView from "../views/MyBookingsView.vue";

const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/houses", name: "houses", component: HousesView },
  { path: "/bookings", name: "bookings", component: MyBookingsView },
  { path: "/login", name: "login", component: LoginView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
