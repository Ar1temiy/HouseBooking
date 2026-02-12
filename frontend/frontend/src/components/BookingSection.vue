<template>
  <section class="booking">
    <div class="booking__top">
      <h2 class="booking__title">Забронировать домик</h2>

      <div class="booking__hint">
        <div class="booking__hintIcon">i</div>
        <div class="booking__hintText">
          <div>
            Стоимость посуточной аренды —
            {{ formatPrice(currentHouse?.price || 0) }} руб.
          </div>
          <div>
            В домике {{ currentHouse?.bedrooms ?? "—" }} спальных мест. Он
            рассчитан на {{ suggestedGuests }} человек.
          </div>
        </div>
      </div>
    </div>

    <div class="booking__card">
      <div class="booking__layout">
        <div class="booking__left">
          <div class="booking__tabs" role="tablist" aria-label="Выбор домика">
            <button
              v-for="h in houses"
              :key="h.id"
              :class="[
                'booking__tab',
                h.id === selectedHouseId ? 'booking__tab_active' : '',
              ]"
              type="button"
              @click="$emit('select-house', h.id)"
            >
              {{ h.title }}
            </button>
          </div>

          <h3 class="booking__houseTitle">
            {{ currentHouse?.title || "Домик" }}
          </h3>
          <p class="booking__houseDesc">
            {{
              currentHouse?.description || "Описание появится после загрузки."
            }}
          </p>

          <img
            class="booking__houseImage"
            :src="houseImage"
            alt="Иллюстрация домика"
          />
        </div>

        <div class="booking__right">
          <h3 class="booking__panelTitle">Дата бронирования</h3>

          <div class="booking__dateRow">
            <label class="booking__pill booking__pill_datePicker">
              <img
                class="booking__pillCalendarIcon"
                :src="calendarIcon"
                alt=""
              />
              <span>Выберите</span>
              <input v-model="startDate" type="date" />
            </label>

            <div class="booking__pill">
              <span class="booking__pillText">{{ startDateLabel }}</span>
            </div>

            <label class="booking__pill booking__pill_term">
              <span class="booking__termPrefix">срок:</span>
              <select v-model.number="days">
                <option v-for="n in 14" :key="n" :value="n">
                  {{ n }} {{ dayWord(n) }}
                </option>
              </select>
            </label>
          </div>

          <hr class="booking__separator" />

          <h3 class="booking__panelTitle">Количество гостей</h3>
          <p class="booking__text">
            Укажите, сколько гостей будет проживать в домике. Это нужно, чтобы
            проверить вместимость и подготовить дом к вашему приезду. Если вы
            ещё не уверены — выберите примерное число.
          </p>

          <input
            v-model.number="guests"
            class="booking__input"
            type="number"
            min="1"
            :max="suggestedGuests"
            placeholder="Количество гостей"
          />

          <hr class="booking__separator" />

          <div class="booking__totalLabel">Сумма за все дни</div>
          <div class="booking__totalValue">
            {{ formatPrice(totalPrice) }} руб
          </div>

          <p class="booking__text booking__text_bottom">
            Нажимая «Забронировать», вы соглашаетесь с правилами проживания,
            политикой отмены и обработкой персональных данных.
          </p>

          <button
            class="booking__submit"
            :disabled="loading || !selectedHouseId"
            type="button"
            @click="submit"
          >
            {{ loading ? "Отправляем..." : "Забронировать" }}
          </button>

          <p v-if="error" class="booking__error">{{ error }}</p>
          <p v-if="success" class="booking__success">
            Заявка отправлена (pending)
          </p>
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

const houseImage = "/src/assets/booking/house-preview.svg";
const calendarIcon = "/src/assets/booking/calendar.svg";

const startDate = ref("");
const days = ref(1);
const guests = ref(1);
const loading = ref(false);
const error = ref("");
const success = ref(false);

const currentHouse = computed(() =>
  props.houses.find((h) => h.id === props.selectedHouseId),
);

const suggestedGuests = computed(() => {
  const bedrooms = currentHouse.value?.bedrooms ?? 1;
  return bedrooms * 2 + 2;
});

const totalPrice = computed(() => {
  const price = currentHouse.value?.price ?? 0;
  return price * (days.value || 0);
});

const startDateLabel = computed(() => {
  if (!startDate.value) return "дату";
  const date = new Date(startDate.value);
  if (Number.isNaN(date.getTime())) return "дату";

  return new Intl.DateTimeFormat("ru-RU", {
    day: "numeric",
    month: "long",
  }).format(date);
});

watch(
  () => props.selectedHouseId,
  () => {
    error.value = "";
    success.value = false;
    guests.value = 1;
    days.value = 1;
  },
);

function dayWord(value) {
  const n = Number(value) || 0;
  if (n % 10 === 1 && n % 100 !== 11) return "день";
  if ([2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100))
    return "дня";
  return "дней";
}

function formatPrice(value) {
  return new Intl.NumberFormat("ru-RU").format(value || 0);
}

async function submit() {
  error.value = "";
  success.value = false;

  if (!props.selectedHouseId) {
    error.value = "Выберите домик";
    return;
  }

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
    error.value = e?.response?.data?.detail || "Ошибка бронирования";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.booking {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 18px;
}

.booking__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 18px;
}

.booking__title {
  margin: 0;
  font-size: 54px;
  font-weight: 400;
  letter-spacing: -0.02em;
}

.booking__hint {
  margin-top: 8px;
  max-width: 500px;
  display: flex;
  gap: 10px;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #e7eef5;
  background: rgba(255, 255, 255, 0.7);
}

.booking__hintIcon {
  width: 18px;
  height: 18px;
  flex: 0 0 18px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  background: #7b9a74;
  margin-top: 2px;
}

.booking__hintText {
  color: #344758;
  font-size: 13px;
  line-height: 1.35;
}

.booking__card {
  border: 1px solid #e7eef5;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.66);
  padding: 16px;
}

.booking__layout {
  border-radius: 16px;
  padding: 30px;
  background: #f5f8fc;
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 26px;
}

.booking__left {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.booking__tabs {
  display: flex;
  gap: 10px;
  row-gap: 10px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

.booking__tab {
  border: none;
  border-radius: 999px;
  background: #fff;
  color: #3e4f61;
  min-width: 124px;
  padding: 11px 12px;
  font-size: 16px;
  white-space: nowrap;
  cursor: pointer;
}

.booking__tab_active {
  background: #e9efe6;
  color: #75956f;
}

.booking__houseTitle {
  margin: 14px 0 0;
  font-size: 30px;
  font-weight: 500;
  color: #1f3040;
}

.booking__houseDesc {
  margin: 12px 0 0;
  max-width: 600px;
  color: #b0bbd4;
  font-size: 14px;
  line-height: 1.45;
}

.booking__houseImage {
  width: 100%;
  max-width: 500px;
  margin-top: auto;
  padding-top: 22px;
  display: block;
}

.booking__right {
  padding-top: 2px;
}

.booking__panelTitle {
  margin: 0 0 14px;
  font-size: 40px;
  font-weight: 500;
  color: #26394c;
  line-height: 1.05;
  white-space: nowrap;
}

.booking__dateRow {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr;
  gap: 10px;
}

.booking__pill {
  min-height: 46px;
  border-radius: 999px;
  border: 1px solid #ebf0f7;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  color: #607081;
  font-size: 16px;
  font-weight: 400;
  white-space: nowrap;
  line-height: 1;
}

.booking__pill_datePicker {
  justify-content: flex-start;
  gap: 8px;
  background: #edf2eb;
  color: #7c9975;
  position: relative;
  overflow: hidden;
}

.booking__pillCalendarIcon {
  width: 16px;
  height: 16px;
}

.booking__pillText {
  white-space: nowrap;
  font-weight: 400;
}

.booking__pill_datePicker input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.booking__pill_term {
  justify-content: flex-start;
  gap: 6px;
  color: #9daacc;
}

.booking__termPrefix {
  font-weight: 400;
  white-space: nowrap;
}

.booking__pill_term select {
  border: none;
  background: transparent;
  color: #607081;
  outline: none;
  font-size: 16px;
  font-weight: 400;
  white-space: nowrap;
}

.booking__separator {
  border: none;
  border-top: 1px solid #dfe8f1;
  margin: 16px 0;
}

.booking__text {
  margin: 0 0 14px;
  color: #b2bfd8;
  font-size: 14px;
  line-height: 1.45;
}

.booking__input {
  width: 100%;
  border-radius: 999px;
  border: 1px solid #ebf0f7;
  background: #fff;
  color: #5b6f84;
  min-height: 46px;
  padding: 10px 18px;
  font-size: 16px;
  font-weight: 400;
  white-space: nowrap;
}

.booking__totalLabel {
  color: #aab8cf;
  font-size: 16px;
  font-weight: 400;
  white-space: nowrap;
}

.booking__totalValue {
  margin-top: 2px;
  color: #23384d;
  font-size: 48px;
  font-weight: 500;
}

.booking__text_bottom {
  margin-top: 10px;
}

.booking__submit {
  margin-top: 10px;
  min-width: 190px;
  min-height: 50px;
  padding: 12px 26px;
  border: none;
  border-radius: 999px;
  background: #dfe6dd;
  color: #709066;
  cursor: pointer;
}

.booking__submit:disabled {
  opacity: 0.8;
  cursor: default;
}

.booking__error {
  margin-top: 8px;
  color: #b00020;
}

.booking__success {
  margin-top: 8px;
  color: #4f7d43;
}

@media (max-width: 1180px) {
  .booking__tabs {
    overflow: visible;
  }

  .booking__layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1100px) {
  .booking__title {
    font-size: 44px;
  }

  .booking__panelTitle {
    font-size: 34px;
    white-space: normal;
  }

  .booking__hintText {
    font-size: 13px;
  }
}
</style>
