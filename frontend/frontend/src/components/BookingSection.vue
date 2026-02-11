<template>
  <section class="booking">
    <h2>Забронировать домик</h2>

    <div v-if="!houses.length">Загрузка...</div>

    <div v-else class="card">
      <div class="tabs">
        <button
          v-for="h in houses"
          :key="h.id"
          :class="['tab', h.id === selectedHouseId ? 'active' : '']"
          @click="$emit('select-house', h.id)"
        >
          {{ h.title }}
        </button>
      </div>

      <div class="content">
        <div class="left">
          <h3>{{ currentHouse?.title }}</h3>
          <p>{{ currentHouse?.description }}</p>
        </div>

        <div class="right">
          <label>Дата заезда</label>
          <input v-model="startDate" type="date" />

          <label>Количество дней</label>
          <input v-model.number="days" type="number" min="1" />

          <label>Количество гостей</label>
          <input v-model.number="guests" type="number" min="1" />

          <div class="price">
            Сумма: <b>{{ totalPrice }} руб</b>
          </div>

          <button :disabled="loading" @click="submit">
            {{ loading ? "Отправляем..." : "Забронировать" }}
          </button>

          <p v-if="error" class="err">{{ error }}</p>
          <p v-if="success" class="ok">Заявка отправлена (pending)</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { createBooking } from "../api/bookings";

const props = defineProps({
  houses: { type: Array, default: () => [] },
  selectedHouseId: { type: Number, default: null },
});
defineEmits(["select-house"]);

const startDate = ref("");
const days = ref(1);
const guests = ref(1);

const loading = ref(false);
const error = ref("");
const success = ref(false);

const currentHouse = computed(() =>
  props.houses.find((h) => h.id === props.selectedHouseId)
);

const totalPrice = computed(() => {
  const price = currentHouse.value?.price ?? 0;
  return price * (days.value || 0);
});

watch(() => props.selectedHouseId, () => {
  // при смене домика сбрасываем сообщения
  error.value = "";
  success.value = false;
});

async function submit() {
  error.value = "";
  success.value = false;

  if (!startDate.value) {
    error.value = "Выберите дату заезда";
    return;
  }

  loading.value = true;
  try {
    await createBooking({
      house_id: props.selectedHouseId,
      start_date: startDate.value,
      days: days.value,
      guests: guests.value,
    });
    success.value = true;
  } catch (e) {
    const msg = e?.response?.data?.detail || "Ошибка бронирования";
    error.value = msg;
  } finally {
    loading.value = false;
  }
}
</script>
