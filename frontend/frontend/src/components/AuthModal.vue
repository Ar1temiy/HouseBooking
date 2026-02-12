<template>
  <div class="authOverlay" @click.self="$emit('close')">
    <div class="authCard">
      <button class="authClose" type="button" @click="$emit('close')">×</button>

      <template v-if="mode === 'login'">
        <section class="authSection">
          <h2 class="authTitle">Ваш email</h2>
          <p class="authSub">Укажите ваши персональные данные</p>
          <input
            v-model="loginForm.email"
            class="authInput"
            type="email"
            placeholder="example@mail.com"
          />
        </section>

        <hr class="authDivider" />

        <section class="authSection">
          <h2 class="authTitle">Ваш персональный пароль</h2>
          <p class="authSub">Укажите ваши персональные данные</p>

          <div class="passwordWrap">
            <input
              v-model="loginForm.password"
              class="authInput"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
            />
            <button class="eyeBtn" type="button" @click="showPassword = !showPassword">
              👁
            </button>
          </div>
        </section>

        <button class="submitBtn" :disabled="loading" @click="submitLogin">
          {{ loading ? "входим..." : "войти в кабинет" }}
        </button>

        <p class="switchText">
          Нет аккаунта?
          <button type="button" class="switchBtn" @click="switchMode('register')">
            Зарегистрируйтесь
          </button>
        </p>
      </template>

      <template v-else>
        <section class="authSection">
          <h2 class="authTitle">Ваше Имя</h2>
          <p class="authSub">Укажите Ваше Имя</p>
          <input
            v-model="registerForm.name"
            class="authInput"
            type="text"
            placeholder="Ваше имя"
          />
        </section>

        <hr class="authDivider" />

        <section class="authSection authSection_compact">
          <h2 class="authTitle">Ваш email</h2>
          <input
            v-model="registerForm.email"
            class="authInput"
            type="email"
            placeholder="example@mail.com"
          />

          <h2 class="authTitle">Ваш номер телефона</h2>
          <input
            v-model="registerForm.phone"
            class="authInput"
            type="tel"
            placeholder="+7..."
          />

          <h2 class="authTitle">Введите пароль</h2>
          <input
            v-model="registerForm.password"
            class="authInput"
            :type="showPassword ? 'text' : 'password'"
            placeholder="••••••••"
          />
        </section>

        <button class="submitBtn" :disabled="loading" @click="submitRegister">
          {{ loading ? "создаем..." : "войти в кабинет" }}
        </button>

        <p class="switchText">
          Есть аккаунт?
          <button type="button" class="switchBtn" @click="switchMode('login')">
            Войти
          </button>
        </p>
      </template>

      <p v-if="error" class="formError">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { login, register } from "../api/auth";

const emit = defineEmits(["close", "authenticated"]);

const mode = ref("login");
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);

const loginForm = reactive({ email: "", password: "" });
const registerForm = reactive({ name: "", email: "", phone: "", password: "" });

function switchMode(nextMode) {
  mode.value = nextMode;
  error.value = "";
}

async function submitLogin() {
  error.value = "";
  loading.value = true;
  try {
    const data = await login(loginForm.email, loginForm.password);
    localStorage.setItem("token", data.access_token);
    emit("authenticated");
    emit("close");
  } catch (e) {
    error.value = e?.response?.data?.detail || "Ошибка входа";
  } finally {
    loading.value = false;
  }
}

async function submitRegister() {
  error.value = "";
  loading.value = true;
  try {
    const data = await register({
      name: registerForm.name,
      email: registerForm.email,
      phone: registerForm.phone || null,
      password: registerForm.password,
    });
    localStorage.setItem("token", data.access_token);
    emit("authenticated");
    emit("close");
  } catch (e) {
    error.value = e?.response?.data?.detail || "Ошибка регистрации";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.authOverlay {
  position: fixed;
  inset: 0;
  background: rgba(18, 24, 33, 0.45);
  display: grid;
  place-items: center;
  z-index: 30;
  padding: 16px;
}
.authCard {
  position: relative;
  width: min(780px, 100%);
  max-height: calc(100vh - 32px);
  overflow: auto;
  background: #f3f6fb;
  border-radius: 22px;
  border: 1px solid #e1e8f2;
  padding: 42px;
}
.authClose {
  position: absolute;
  right: 14px;
  top: 10px;
  border: none;
  background: transparent;
  font-size: 30px;
  cursor: pointer;
  color: #5f7184;
}
.authSection { margin-bottom: 10px; }
.authSection_compact { display: grid; gap: 10px; }
.authTitle {
  margin: 0 0 8px;
  color: #25394d;
  font-size: 40px;
  font-weight: 500;
  line-height: 1.03;
}
.authSub {
  margin: 0 0 16px;
  color: #bcc4df;
  font-size: 20px;
}
.authInput {
  width: 100%;
  min-height: 56px;
  padding: 0 20px;
  border-radius: 999px;
  border: 1px solid #dce4ee;
  background: #fff;
  color: #24384c;
  font-size: 24px;
}
.authDivider {
  border: none;
  border-top: 1px solid #dce4ee;
  margin: 22px 0;
}
.passwordWrap { position: relative; }
.eyeBtn {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  cursor: pointer;
}
.submitBtn {
  margin-top: 22px;
  width: 100%;
  min-height: 62px;
  border: none;
  border-radius: 999px;
  background: #7fa673;
  color: #f6f8ff;
  font-size: 24px;
  cursor: pointer;
}
.switchText {
  margin: 16px 0 0;
  text-align: center;
  color: #b9bfd5;
  font-size: 22px;
}
.switchBtn {
  border: none;
  background: transparent;
  color: #7fa673;
  cursor: pointer;
  font-size: inherit;
}
.formError {
  margin-top: 14px;
  text-align: center;
  color: #d13a4e;
}
</style>