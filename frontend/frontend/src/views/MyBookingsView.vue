<template>
  <div class="cabinetPage">
    <aside class="sidebar">
      <img class="sidebar__logo" src="/src/assets/logo.svg" alt="logo" />

      <button class="sidebar__nav sidebar__nav_active" type="button">
        <span class="sidebar__dot">•</span>
        Бронирования
      </button>

      <button class="sidebar__logout" type="button" @click="logout">
        Выход
      </button>
    </aside>

    <main class="content">
      <div class="topBar">
        <div class="topBar__user">
          <img src="/src/assets/icons/user.svg" alt="" />
          {{ userName }}
        </div>
        <router-link class="topBar__cta" to="/">бронировать домик</router-link>
      </div>

      <section class="panel" v-if="loading">Загрузка...</section>
      <section class="panel" v-else-if="error">{{ error }}</section>
      <section class="panel" v-else-if="!bookings.length">У вас пока нет бронирований.</section>

      <section v-else class="panel panel_grid">
        <div class="mapCard">
          <div class="mapWrap">
            <img class="mapImg" :src="mapCabSrc" alt="карта бронирований" />

            <span
              v-for="h in houses"
              :key="`pin-${h.id}`"
              class="pin"
              :class="{ pin_active: currentBooking?.house_id === h.id }"
              :style="pinStyle(h.id)"
            >
              <img v-if="currentBooking?.house_id === h.id" :src="choosedPinSrc" alt="выбранный домик" />
              <span v-else>+</span>
            </span>


          </div>
        </div>

        <div class="requestCard">
          <h2 class="requestCard__title">Ваша заявка</h2>
          <div class="requestCard__house">{{ houseTitle(currentBooking?.house_id) }}</div>
          <hr />

          <h3>Дата бронирования</h3>
          <div class="chips">
            <div class="chip chip_green">
              <img :src="calendarIconSrc" alt="" />
              Дата заезда
            </div>
            <div class="chip">{{ formatDateRu(currentBooking?.date_from) }}</div>
            <div class="chip">срок: {{ bookingDays(currentBooking) }} {{ dayWord(bookingDays(currentBooking)) }}</div>
          </div>

          <hr />

          <div class="rowBetween">
            <h3>Количество гостей</h3>
            <div class="chip">{{ currentBooking?.guests }}</div>
          </div>

          <hr />

          <div class="price">{{ formatPrice(currentBooking?.total_price || 0) }} руб</div>
          <div class="priceSub">Сумма оплаты</div>

          <div class="statusRow">
            <h3>Статус</h3>
            <div class="statusLabel">
              {{ statusLabel(currentBooking?.status) }}
              <img :src="statusIcon(currentBooking?.status)" alt="" />
            </div>
          </div>

          <hr />

          <div class="pager" v-if="bookings.length > 1">
            <button type="button" @click="prevBooking">◀</button>
            <span>{{ currentIndex + 1 }}</span>
            <span>{{ bookings.length }}</span>
            <button type="button" @click="nextBooking">▶</button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchMyBookings } from "../api/bookings";
import { fetchHouses } from "../api/houses";

const router = useRouter();

const loading = ref(true);
const error = ref("");
const bookings = ref([]);
const houses = ref([]);
const currentIndex = ref(0);

const mapCabSrc = "/src/assets/booking/map_cab.svg";
const choosedPinSrc = "/src/assets/icons/choosed.svg";
const calendarIconSrc = "/src/assets/booking/calendar.svg";

const userName = localStorage.getItem("userName") || "Пользователь";

const currentBooking = computed(() => bookings.value[currentIndex.value] || null);

onMounted(async () => {
  try {
    const [bookingsRes, housesRes] = await Promise.all([fetchMyBookings(), fetchHouses()]);
    bookings.value = bookingsRes;
    houses.value = housesRes;
    currentIndex.value = 0;
  } catch (e) {
    error.value = e?.response?.data?.detail || "Не удалось загрузить бронирования";
  } finally {
    loading.value = false;
  }
});

function logout() {
  localStorage.removeItem("token");
  router.push("/");
}

function prevBooking() {
  currentIndex.value = (currentIndex.value - 1 + bookings.value.length) % bookings.value.length;
}

function nextBooking() {
  currentIndex.value = (currentIndex.value + 1) % bookings.value.length;
}

function houseTitle(houseId) {
  const house = houses.value.find((h) => h.id === houseId);
  return house?.title || `Домик №${houseId || "—"}`;
}

function bookingDays(booking) {
  if (!booking?.date_from || !booking?.date_to) return 0;
  const from = new Date(booking.date_from);
  const to = new Date(booking.date_to);
  return Math.max(1, Math.round((to - from) / (1000 * 60 * 60 * 24)));
}

function formatDateRu(value) {
  if (!value) return "—";
  const date = new Date(value);
  return new Intl.DateTimeFormat("ru-RU", { day: "numeric", month: "long" }).format(date);
}

function formatPrice(value) {
  return new Intl.NumberFormat("ru-RU").format(value || 0);
}

function dayWord(value) {
  const n = Number(value) || 0;
  if (n % 10 === 1 && n % 100 !== 11) return "день";
  if ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100)) return "дня";
  return "дней";
}

function statusLabel(status) {
  if (status === "confirmed") return "Подтверждена";
  if (status === "cancelled") return "Отменена";
  return "На проверке";
}

function statusIcon(status) {
  if (status === "confirmed") return "/src/assets/icons/yeas.svg";
  if (status === "cancelled") return "/src/assets/icons/cancel.svg";
  return "/src/assets/icons/wait.svg";
}

const pins = {
  1: { left: "10%", top: "35%" },
  2: { left: "31%", top: "44%" },
  3: { left: "54%", top: "56%" },
  4: { left: "71%", top: "62%" },
  5: { left: "89%", top: "44%" },
};

function pinStyle(id) {
  return pins[id] || { left: "10%", top: "10%" };
}
</script>

<style scoped>
.cabinetPage {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 206px 1fr;
  background: #f4f6fa;
}

.sidebar {
  border-right: 1px solid #e3e8f2;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
}

.sidebar__logo {
  width: 105px;
  margin-left: 18px;
  margin-bottom: 44px;
}

.sidebar__nav {
  border: none;
  border-radius: 999px;
  min-height: 34px;
  padding: 0 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #31475f;
  background: #eef2fa;
  width: fit-content;
}

.sidebar__dot { color: #9aa7c3; }

.sidebar__logout {
  margin-top: auto;
  border: none;
  border-radius: 999px;
  min-height: 40px;
  background: #eef2fa;
  color: #31475f;
}

.content { padding: 14px 24px; }

.topBar {
  background: #fff;
  border: 1px solid #e3e8f2;
  border-radius: 18px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.topBar__user {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #2a4158;
}

.topBar__cta {
  padding: 9px 16px;
  border-radius: 999px;
  background: #f2f4fa;
  color: #a7b3cc;
}

.panel {
  margin-top: 16px;
  background: #fff;
  border: 1px solid #e3e8f2;
  border-radius: 22px;
  padding: 18px;
}

.panel_grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 18px;
}

.mapWrap {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
}

.mapImg {
  width: 100%;
  display: block;
}

.pin {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 30px;
  height: 30px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #e7eef5;
  display: grid;
  place-items: center;
  color: #8596ad;
  font-size: 16px;
}

.pin_active {
  width: 34px;
  height: 34px;
  background: transparent;
  border: none;
}

.pin_active img {
  width: 34px;
  height: 34px;
}

.mapHint {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 20px;
  width: 82%;
  min-height: 68px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #e4ebf4;
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  color: #30455d;
}

.mapHint img { width: 18px; }

.requestCard {
  border-radius: 20px;
  background: #f7f9fd;
  border: 1px solid #e3e8f2;
  padding: 26px;
}

.requestCard__title {
  margin: 0;
  font-size: 48px;
  color: #25394d;
  font-weight: 300;
}

.requestCard__house {
  margin-top: 8px;
  color: #acb7d0;
  font-size: 40px;
}

.requestCard h3 {
  margin: 14px 0 10px;
  font-size: 53px;
  color: #25394d;
  font-weight: 300;
}

.requestCard hr {
  border: none;
  border-top: 1px solid #dce4ef;
  margin: 12px 0;
}

.chips {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
}

.chip {
  min-height: 46px;
  border-radius: 999px;
  border: 1px solid #e4eaf4;
  background: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #4f6278;
  font-size: 31px;
  gap: 8px;
}

.chip_green {
  background: #edf2eb;
  color: #74926d;
}

.chip_green img { width: 16px; }

.rowBetween {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
}

.price {
  font-size: 56px;
  color: #24384d;
}

.priceSub {
  color: #acb8cf;
  font-size: 30px;
}

.statusRow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.statusLabel {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #a9b6cd;
  font-size: 30px;
}

.statusLabel img {
  width: 38px;
  height: 38px;
}

.pager {
  margin-top: 18px;
  display: flex;
  gap: 14px;
  align-items: center;
  justify-content: center;
  color: #4b6077;
}

.pager button {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 999px;
  background: #e5ebdf;
  color: #74926d;
  cursor: pointer;
}

@media (max-width: 1100px) {
  .cabinetPage { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .panel_grid { grid-template-columns: 1fr; }
}
</style>
