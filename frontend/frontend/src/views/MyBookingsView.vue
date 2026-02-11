<template>
  <div class="page">
    <h1>Мои бронирования</h1>

    <div v-if="loading">Загрузка...</div>

    <div v-else-if="error" class="err">
      {{ error }}
    </div>

    <div v-else-if="!bookings.length">
      Пока нет бронирований.
    </div>

    <div v-else class="list">
      <div class="card" v-for="b in bookings" :key="b.id">
        <div><b>ID:</b> {{ b.id }}</div>
        <div><b>Домик:</b> {{ b.house_id }}</div>
        <div><b>Заезд:</b> {{ b.date_from }}</div>
        <div><b>Выезд:</b> {{ b.date_to }}</div>
        <div><b>Гости:</b> {{ b.guests }}</div>
        <div><b>Статус:</b> {{ b.status }}</div>
        <div><b>Сумма:</b> {{ b.total_price }} ₽</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchMyBookings } from "../api/bookings";

const bookings = ref([]);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    bookings.value = await fetchMyBookings();
  } catch (e) {
    // Если токена нет или он неверный — будет 401
    error.value = e?.response?.data?.detail || "Не удалось загрузить бронирования";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.page { padding: 24px; max-width: 900px; margin: 0 auto; }
.list { display: grid; gap: 12px; margin-top: 12px; }
.card { padding: 14px; border: 1px solid #eee; border-radius: 16px; }
.err { color: #b00020; }
</style>
