<template>
  <div class="page">
    <h1>Вход</h1>

    <form class="card" @submit.prevent="submit">
      <label>Email</label>
      <input v-model="email" type="email" placeholder="b@example.com" />

      <label>Пароль</label>
      <input v-model="password" type="password" placeholder="••••••••" />

      <button :disabled="loading">
        {{ loading ? "Входим..." : "Войти" }}
      </button>

      <p v-if="error" class="err">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth";

const router = useRouter();
const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function submit() {
  error.value = "";
  loading.value = true;

  try {
    const data = await login(email.value, password.value);
    localStorage.setItem("token", data.access_token);
    router.push("/"); // на главную
  } catch (e) {
    error.value = e?.response?.data?.detail || "Ошибка входа";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page { padding: 24px; max-width: 520px; margin: 0 auto; }
.card { display: grid; gap: 10px; padding: 16px; border: 1px solid #eee; border-radius: 16px; }
input { padding: 10px 12px; border: 1px solid #ddd; border-radius: 12px; }
button { padding: 10px 12px; border: none; border-radius: 12px; cursor: pointer; }
.err { color: #b00020; }
</style>
