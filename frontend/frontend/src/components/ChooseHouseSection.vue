<template>
  <section class="choose">
    <div class="choose__top">
      <h1 class="choose__title">Выберите домик</h1>

      <div class="choose__hint">
        <div class="choose__hintIcon">i</div>
        <div class="choose__hintText">
          <div>Выберите домик и ознакомьтесь с условиями бронирования.</div>
          <div>Не забудьте авторизироваться!</div>
        </div>
      </div>
    </div>

    <div class="choose__mapCard">
      <div class="choose__mapWrap">
        <img class="choose__mapImg" :src="mapSvg" alt="map" />

        <!-- Пины -->
        <button
          v-for="h in houses"
          :key="h.id"
          class="pin"
          :class="{ pin_active: h.id === selectedHouseId }"
          :style="pinStyle(h.id)"
          type="button"
          @click="$emit('select-house', h.id)"
        >
          +
        </button>

        <!-- Tooltip справа сверху -->
        <div v-if="currentHouse" class="tooltip">
          <div class="tooltip__title">{{ currentHouse.title }}</div>
          <button class="tooltip__btn" type="button" @click="$emit('go-booking', currentHouse.id)">
            забронировать домик
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from "vue";
import mapSvg from "../assets/map.svg";

const props = defineProps({
  houses: { type: Array, default: () => [] },
  selectedHouseId: { type: Number, default: null },
});
defineEmits(["select-house", "go-booking"]);

const currentHouse = computed(() =>
  props.houses.find((h) => h.id === props.selectedHouseId)
);

/**
 * Координаты пинов (пример).
 * ВАЖНО: подгони под свой map.svg как в Figma (лево/верх в процентах).
 * Домики у тебя id 1..5 (после seed).
 */
const pins = {
  1: { left: "27%", top: "27%" },
  2: { left: "39%", top: "39%" },
  3: { left: "52%", top: "58%" },
  4: { left: "62%", top: "69%" },
  5: { left: "71%", top: "42%" },
};

function pinStyle(id) {
  return pins[id] ?? { left: "10%", top: "10%" };
}
</script>

<style scoped>
.choose {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px 0;
}

.choose__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 18px;
}

.choose__title {
  margin: 0;
  font-size: 54px;
  line-height: 1.05;
  font-weight: 600;
  letter-spacing: -0.02em;
}

.choose__hint {
  margin-top: 10px;
  display: flex;
  gap: 12px;
  align-items: flex-start;

  padding: 16px 18px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid #e7eef5;
  max-width: 420px;
}

.choose__hintIcon {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  background: #7b9a74;
  color: white;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 13px;
  flex: 0 0 auto;
  margin-top: 2px;
}

.choose__hintText {
  font-size: 13px;
  line-height: 1.4;
  color: #3a4a56;
}

.choose__mapCard {
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid #e7eef5;
  padding: 16px;
}

.choose__mapWrap {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
}

.choose__mapImg {
  width: 100%;
  height: auto;
  display: block;
}

/* Пины */
.pin {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 34px;
  height: 34px;
  border-radius: 999px;

  border: none;
  cursor: pointer;

  background: rgba(240, 242, 246, 0.95);
  color: #1f2a33;
  font-size: 18px;
  line-height: 1;
}

.pin:hover { filter: brightness(0.97); }

.pin_active {
  background: #7b9a74;
  color: white;
}

/* Tooltip */
.tooltip {
  position: absolute;
  right: 18px;
  top: 18px;

  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #e7eef5;
  border-radius: 16px;
  padding: 14px 14px;
  min-width: 220px;
}

.tooltip__title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #1e2a33;
}

.tooltip__btn {
  width: 100%;
  border: none;
  border-radius: 999px;
  padding: 10px 12px;

  background: #7b9a74;
  color: white;
  font-size: 13px;
  cursor: pointer;
}
.choose__mapWrap::after{
  content:"";
  position:absolute;
  inset:0;
  background:
    linear-gradient(to right, rgba(0,0,0,.06) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0,0,0,.06) 1px, transparent 1px);
  background-size: 80px 80px;
  pointer-events:none;
  opacity:.15;
}

.tooltip__btn:hover { filter: brightness(0.97); }
</style>
