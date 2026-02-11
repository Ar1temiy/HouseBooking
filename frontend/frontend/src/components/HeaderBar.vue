<template>
  <header class="header">
    <div class="headerShell">
      <div class="header__inner">
        <div class="brand">
          <img class="brand__logo" :src="logoSrc" alt="logo" />
        </div>

        <router-link class="cabinetBtn" to="/login">
          <img class="cabinetBtn__icon" :src="userIcon" alt="" />
          Вход в кабинет
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import logoSrc from "../assets/logo.svg";
import userIcon from "../assets/icons/user.svg";
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

  /* вот эта подложка как в макете */
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

/* кнопка справа */
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
}

.cabinetBtn__icon{
  width: 18px;
  height: 18px;
  opacity: .75;
}
</style>
