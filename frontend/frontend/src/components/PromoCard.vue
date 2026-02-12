<template>
  <section class="promo">
    <div class="promo__card">
      <div class="promo__imgWrap">
        <img class="promo__img" :src="promoImg" alt="promo" />
      </div>

      <div class="promo__content">
        <h3 class="promo__title">Пенная вечеринка</h3>

        <p class="promo__text">
          Порадуйте себя и близких вечеринкой, которая запомнится надолго!
          С нас — мастера, которые установят всё необходимое оборудование,
          а с вас — только хорошее настроение! Продолжительность мероприятия
          зависит только от вас.
        </p>
        <div class="promo__footer">
          <div class="promo__social">
            <a class="promo__socBtn" href="#" aria-label="VK">
              <img :src="vkIcon" alt="" />
            </a>
            <a class="promo__socBtn" href="#" aria-label="Instagram">
              <img :src="igIcon" alt="" />
            </a>
            <a class="promo__socBtn" href="#" aria-label="Facebook">
              <img :src="fbIcon" alt="" />
            </a>
          </div>

          <div class="promo__date">12.02.2026</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import promoImg from "../assets/promo.svg";

import vkIcon from "../assets/icons/vk.svg";
import igIcon from "../assets/icons/instagram.svg";
import fbIcon from "../assets/icons/facebook.svg"; // если нет — скажи, я уберу
</script>

<style scoped>
.promo {
  max-width: 1200px;
  margin: 18px auto 0;
  padding: 0 24px 18px;
}

.promo__card {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 18px;

  padding: 18px;
  border-radius: 24px;

  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(20, 35, 45, 0.08);
  box-shadow: 0 18px 60px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(14px);
}

.promo__imgWrap {
  border-radius: 18px;
  overflow: hidden;

  background: radial-gradient(700px 260px at 30% 30%, #f2f7fb 0%, #ffffff 60%);
  display: grid;
  place-items: center;
  min-height: 240px;
}

.promo__img {
  width: 92%;
  height: auto;
  display: block;
}

.promo__content {
  padding: 10px 6px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.promo__title {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #1e2a33;
}

.promo__text {
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  color: #51616f;
  max-width: 460px;
}

/* Кнопка как в макете: pill, мягкая, чуть “воздушная” */
.promo__btn {
  align-self: flex-start;
  border: none;
  border-radius: 999px;
  padding: 11px 22px;

  background: #7b9a74;
  color: white;
  font-size: 13px;
  font-weight: 500;

  cursor: pointer;
  box-shadow: 0 12px 30px rgba(123, 154, 116, 0.28);
}

.promo__btn:hover {
  filter: brightness(0.98);
  transform: translateY(-1px);
}

.promo__btn:active {
  transform: translateY(0);
}

.promo__footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.promo__social {
  display: flex;
  gap: 10px;
}

.promo__socBtn {
  width: 30px;
  height: 30px;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  border-radius: 999px;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(20, 35, 45, 0.10);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  text-decoration: none;
}

.promo__socBtn:hover {
  background: rgba(255, 255, 255, 0.92);
}

.promo__socBtn img {
  width: 16px;
  height: 16px;
  opacity: 0.75;
}

.promo__date {
  font-size: 12px;
  color: #8a98a6;
}

/* Мобилка */
@media (max-width: 900px) {
  .promo__card {
    grid-template-columns: 1fr;
  }
}
</style>
