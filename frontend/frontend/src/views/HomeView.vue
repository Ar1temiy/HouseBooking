<template>
  <div class="page">
    <HeaderBar />

    <main class="page__content">
      <ChooseHouseSection
        :houses="houses"
        :selectedHouseId="selectedHouseId"
        @select-house="selectHouse"
        @go-booking="goBooking"
      />

      <PromoCard />

      <!-- ниже позже будет BookingSection -->
      <div ref="bookingEl" style="height: 1px;"></div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import HeaderBar from "../components/HeaderBar.vue";
import ChooseHouseSection from "../components/ChooseHouseSection.vue";
import PromoCard from "../components/PromoCard.vue";
import { fetchHouses } from "../api/houses";

const houses = ref([]);
const selectedHouseId = ref(null);
const bookingEl = ref(null);

onMounted(async () => {
  try {
    houses.value = await fetchHouses();
    selectedHouseId.value = houses.value[0]?.id ?? null;
  } catch (e) {
    console.error("fetchHouses failed", e);
    houses.value = [];
    selectedHouseId.value = null;
  }
});


function selectHouse(id) {
  selectedHouseId.value = id;
}

function goBooking(id) {
  if (id) selectedHouseId.value = id;
  bookingEl.value?.scrollIntoView({ behavior: "smooth", block: "start" });
}
</script>

<style scoped>
.page__content {
  display: flex;
  flex-direction: column;
  gap: 18px; /* расстояние между блоками */
}
</style>

