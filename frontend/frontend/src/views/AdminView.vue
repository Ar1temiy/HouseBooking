<template>
  <div class="adminPage">
    <aside class="sidebar">
      <img class="sidebar__logo" src="/src/assets/logo.svg" alt="logo" />

      <button class="sidebar__nav sidebar__nav_active" type="button">
        <img class="sidebar__navIcon" src="/src/assets/icons/info.svg" alt="" />
        Заявки
      </button>

      <button class="sidebar__logout" type="button" @click="logout">Выход</button>
    </aside>

    <main class="content">
      <header class="topBar">
        <div class="topBar__user">
          <img src="/src/assets/icons/user.svg" alt="" />
          {{ userName }}
        </div>

        <button class="topBar__notify" type="button" aria-label="Уведомления">
          <img src="/src/assets/icons/wait.svg" alt="" />
          <span class="topBar__badge">3</span>
        </button>
      </header>

      <section class="board">
        <div class="toolbar">
          <button
            class="toolbar__tab"
            :class="{ toolbar__tab_active: activeTab === 'requests' }"
            type="button"
            @click="activeTab = 'requests'"
          >
            Заявки
          </button>
          <button
            class="toolbar__tab"
            :class="{ toolbar__tab_active: activeTab === 'history' }"
            type="button"
            @click="activeTab = 'history'"
          >
            История
          </button>

          <label class="toolbar__search">
            <img src="/src/assets/icons/user.svg" alt="" />
            <input v-model.trim="query" type="text" placeholder="Поиск" />
          </label>

          <button class="toolbar__sort" type="button" @click="newestFirst = !newestFirst">
            {{ newestFirst ? "сначала новые" : "сначала старые" }}
          </button>
        </div>

        <div v-if="loading" class="state">Загрузка заявок...</div>
        <div v-else-if="error" class="state state_error">{{ error }}</div>
        <div v-else-if="!filteredBookings.length" class="state">Ничего не найдено.</div>

        <div v-else class="rows">
          <article v-for="booking in pagedBookings" :key="booking.id" class="rowCard">
            <div class="houseCell">
              <img class="houseCell__img" src="/src/assets/booking/house-preview.svg" alt="домик" />
              <div>
                <div class="houseCell__title">{{ houseTitle(booking.house_id) }}</div>
                <div class="houseCell__date">{{ formatPeriod(booking.date_from, booking.date_to) }}</div>
              </div>
            </div>

            <div class="guestCell">
              <img src="/src/assets/icons/user.svg" alt="" />
              <div>
                <div class="guestCell__name">Клиент #{{ booking.user_id }}</div>
                <div class="guestCell__phone">+7 (9{{ booking.user_id }}) 000-00-00</div>
              </div>
            </div>

            <div class="priceCell">{{ formatPrice(booking.total_price) }} руб</div>

            <div class="actionsCell" v-if="booking.status === 'pending'">
              <button class="iconBtn iconBtn_cancel" type="button" @click="cancel(booking.id)">
                <img src="/src/assets/icons/cancel.svg" alt="отклонить" />
              </button>
              <button class="iconBtn iconBtn_confirm" type="button" @click="confirm(booking.id)">
                <img src="/src/assets/icons/yeas.svg" alt="подтвердить" />
              </button>
            </div>
            <div class="statusCell" v-else>
              <img :src="statusIcon(booking.status)" alt="" />
              {{ statusLabel(booking.status) }}
            </div>

            <div class="chatCell">
              <div>чат с клиентом</div>
              <small>0 сообщений</small>
            </div>
          </article>
        </div>

        <footer class="boardFooter" v-if="totalPages > 1">
          <button type="button" @click="prevPage" :disabled="currentPage === 1">◀</button>
          <span>{{ currentPage }}</span>
          <span>{{ totalPages }}</span>
          <button type="button" @click="nextPage" :disabled="currentPage === totalPages">▶</button>
        </footer>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { adminCancelBooking, confirmBooking, fetchAllBookings } from "../api/bookings";
import { fetchHouses } from "../api/houses";

const router = useRouter();

const userName = localStorage.getItem("userName") || "Администратор";
const loading = ref(true);
const error = ref("");
const bookings = ref([]);
const houses = ref([]);

const activeTab = ref("requests");
const newestFirst = ref(true);
const query = ref("");
const currentPage = ref(1);
const pageSize = 6;

onMounted(async () => {
  try {
    const [bookingsRes, housesRes] = await Promise.all([fetchAllBookings(), fetchHouses()]);
    bookings.value = bookingsRes;
    houses.value = housesRes;
  } catch (e) {
    error.value = e?.response?.data?.detail || "Не удалось загрузить заявки";
  } finally {
    loading.value = false;
  }
});

watch([activeTab, newestFirst, query], () => {
  currentPage.value = 1;
});

const filteredBookings = computed(() => {
  const targetStatus = activeTab.value === "requests" ? "pending" : null;

  const base = bookings.value.filter((item) => (targetStatus ? item.status === targetStatus : item.status !== "pending"));

  const q = query.value.toLowerCase();
  const searched = base.filter((item) => {
    const title = houseTitle(item.house_id).toLowerCase();
    return !q || title.includes(q) || String(item.user_id).includes(q);
  });

  searched.sort((a, b) => {
    if (newestFirst.value) return b.id - a.id;
    return a.id - b.id;
  });

  return searched;
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredBookings.value.length / pageSize)));

const pagedBookings = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredBookings.value.slice(start, start + pageSize);
});

function prevPage() {
  if (currentPage.value > 1) currentPage.value -= 1;
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value += 1;
}

async function confirm(id) {
  const updated = await confirmBooking(id);
  patchBooking(updated);
}

async function cancel(id) {
  const updated = await adminCancelBooking(id);
  patchBooking(updated);
}

function patchBooking(updated) {
  bookings.value = bookings.value.map((item) => (item.id === updated.id ? updated : item));
}

function houseTitle(houseId) {
  const house = houses.value.find((h) => h.id === houseId);
  return house?.title || `Домик №${houseId}`;
}

function formatPeriod(from, to) {
  if (!from || !to) return "—";
  const formatter = new Intl.DateTimeFormat("ru-RU", { day: "2-digit", month: "2-digit", year: "2-digit" });
  return `${formatter.format(new Date(from))} - ${formatter.format(new Date(to))}`;
}

function formatPrice(value) {
  return new Intl.NumberFormat("ru-RU").format(value || 0);
}

function statusLabel(status) {
  if (status === "confirmed") return "подтверждена";
  if (status === "cancelled") return "отменена";
  return "на проверке";
}

function statusIcon(status) {
  if (status === "confirmed") return "/src/assets/icons/yeas.svg";
  if (status === "cancelled") return "/src/assets/icons/cancel.svg";
  return "/src/assets/icons/wait.svg";
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("userRole");
  router.push("/");
}
</script>

<style scoped>
.adminPage {
  min-height: 100vh;
  background: #f4f6fa;
  display: grid;
  grid-template-columns: 176px 1fr;
}

.sidebar {
  border-right: 1px solid #e3e8f2;
  padding: 22px 16px;
  display: flex;
  flex-direction: column;
}

.sidebar__logo {
  width: 96px;
  margin: 0 0 26px 10px;
}

.sidebar__nav {
  border: none;
  border-radius: 999px;
  min-height: 36px;
  padding: 0 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #eef2fa;
  color: #2d4056;
  font-size: 20px;
}

.sidebar__navIcon { width: 16px; }

.sidebar__logout {
  margin-top: auto;
  border: none;
  border-radius: 999px;
  min-height: 40px;
  background: #eef2fa;
  color: #2d4056;
  font-size: 18px;
}

.content {
  padding: 14px 16px 18px;
}

.topBar {
  background: #fff;
  border: 1px solid #e3e8f2;
  border-radius: 16px;
  min-height: 56px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.topBar__user {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #2d4056;
}

.topBar__notify {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 12px;
  background: #f1f4fa;
  position: relative;
}

.topBar__notify img { width: 24px; }

.topBar__badge {
  position: absolute;
  right: 3px;
  bottom: 3px;
  width: 16px;
  height: 16px;
  border-radius: 999px;
  background: #e8617d;
  color: #fff;
  font-size: 11px;
  display: grid;
  place-items: center;
}

.board {
  margin-top: 12px;
  background: #fff;
  border-radius: 18px;
  padding: 14px;
  min-height: calc(100vh - 112px);
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
  gap: 10px;
  align-items: center;
  background: #f3f6fb;
  border-radius: 14px;
  padding: 8px;
}

.toolbar__tab,
.toolbar__sort {
  border: none;
  border-radius: 999px;
  min-height: 38px;
  padding: 0 16px;
  background: #eef2fa;
  color: #95a2bf;
}

.toolbar__tab_active {
  background: #fff;
  color: #2d4056;
}

.toolbar__search {
  min-height: 38px;
  background: #fff;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0 14px;
}

.toolbar__search img {
  width: 15px;
  opacity: 0.5;
}

.toolbar__search input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 16px;
  background: transparent;
}

.toolbar__sort {
  background: #eff5ea;
  color: #87a17b;
}

.rows {
  margin-top: 14px;
  display: grid;
  gap: 10px;
}

.rowCard {
  background: #f7f9fd;
  border-radius: 14px;
  padding: 10px 16px;
  display: grid;
  grid-template-columns: 280px 1fr auto auto 170px;
  gap: 12px;
  align-items: center;
}

.houseCell,
.guestCell,
.actionsCell,
.statusCell,
.chatCell {
  display: flex;
  align-items: center;
}

.houseCell,
.guestCell {
  gap: 12px;
}

.houseCell__img {
  width: 76px;
  height: 52px;
  object-fit: contain;
}

.houseCell__title {
  font-size: 20px;
  color: #30455d;
}

.houseCell__date {
  color: #a6b2cc;
}

.guestCell__name {
  color: #a6b2cc;
}

.guestCell__phone {
  color: #30455d;
}

.priceCell {
  font-size: 26px;
  color: #30455d;
  white-space: nowrap;
}

.actionsCell { gap: 8px; }

.iconBtn {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 999px;
  background: #fff;
  display: grid;
  place-items: center;
}

.iconBtn img { width: 28px; }

.statusCell {
  gap: 8px;
  color: #8fa48a;
  text-transform: lowercase;
}

.statusCell img { width: 26px; }

.chatCell {
  justify-content: space-between;
  gap: 8px;
  color: #30455d;
}

.chatCell small {
  color: #a6b2cc;
  display: block;
}

.state {
  margin-top: 16px;
  color: #7a8ba1;
}

.state_error { color: #c54e6d; }

.boardFooter {
  margin-top: auto;
  padding-top: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.boardFooter button {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 999px;
  background: #e8eee2;
  color: #7d9b72;
}

@media (max-width: 1200px) {
  .rowCard {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .chatCell { justify-content: flex-start; }
}
</style>
