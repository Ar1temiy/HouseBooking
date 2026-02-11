<template>
  <div class="social">
    <a class="social__btn" href="#" aria-label="VK">
      <img :src="vk" alt="" />
    </a>
    <a class="social__btn" href="#" aria-label="Telegram">
      <img :src="tg" alt="" />
    </a>
    <a class="social__btn" href="#" aria-label="Instagram">
      <img :src="ig" alt="" />
    </a>
  </div>
</template>

<script setup>
import vk from "../assets/icons/vk.svg";
import tg from "../assets/icons/telegram.svg";
import ig from "../assets/icons/instagram.svg";
</script>

<style scoped>
.social {
  display: flex;
  align-items: center;
  gap: 10px;
}

.social__btn {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid rgba(0, 0, 0, 0.06);
  text-decoration: none;
}

.social__btn:hover {
  background: rgba(255, 255, 255, 0.9);
}

.social__btn img {
  width: 16px;
  height: 16px;
  opacity: 0.75;
}
</style>
