<template>
  <header class="header">
    <div class="headerShell">
      <div class="header__inner">
        <div class="brand">
          <img class="brand__logo" :src="logoSrc" alt="logo" />
        </div>

        <button v-if="!isAuthenticated" class="cabinetBtn" type="button" @click="isAuthOpen = true">
          <img class="cabinetBtn__icon" :src="userIcon" alt="" />
          Вход в кабинет
        </button>

        <div v-else class="cabinetActions">
          <button class="logoutBtn" type="button" @click="logout">
            Выйти
          </button>

          <router-link class="cabinetBtn" to="/bookings">
            <img class="cabinetBtn__icon" :src="userIcon" alt="" />
            Личный кабинет
          </router-link>
        </div>
      </div>
    </div>
  </header>

  <AuthModal
    v-if="isAuthOpen"
    @close="isAuthOpen = false"
    @authenticated="onAuthenticated"
  />
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import logoSrc from "../assets/logo.svg";
import userIcon from "../assets/icons/user.svg";
import AuthModal from "./AuthModal.vue";

const router = useRouter();
const isAuthOpen = ref(false);
const isAuthenticated = ref(Boolean(localStorage.getItem("token")));

function onAuthenticated() {
  isAuthenticated.value = true;
  router.push("/");
}

function logout() {
  localStorage.removeItem("token");
  isAuthenticated.value = false;
  router.push("/");
}

window.addEventListener("storage", () => {
  isAuthenticated.value = Boolean(localStorage.getItem("token"));
});
</script>

<style scoped>
.header{
  padding: 18px 24px 0;
}

.headerShell{
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 18px;
  border-radius: 22px;

  background: rgba(255,255,255,0.85);
  border: 1px solid #e7eef5;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
  backdrop-filter: blur(8px);
}

.header__inner{
  display:flex;
  align-items:center;
  justify-content:space-between;
}

.brand__logo{
  height: 44px;
  width: auto;
  display:block;
}

.cabinetBtn{
  display:inline-flex;
  align-items:center;
  gap:10px;

  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.9);
  border: 1px solid #e7eef5;
  color: #1e2a33;
  text-decoration:none;
  font-size: 13px;
  cursor: pointer;
}

.cabinetBtn__icon{
  width: 18px;
  height: 18px;
  opacity: .75;
}

.cabinetActions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logoutBtn {
  border: none;
  background: transparent;
  color: #6f8296;
  font-size: 13px;
  cursor: pointer;
}
</style>