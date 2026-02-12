<template>
  <div class="authPage">
    <div class="authCard">
      <template v-if="mode === 'login'">
        <section class="authSection">
          <h2 class="authTitle">Ваш email</h2>
          <p class="authSub">Укажите ваши персональные данные</p>

          <input
            id="login-email"
            v-model="loginForm.email"
            class="authInput"
            type="email"
            placeholder="gogo123"
          />
        </section>

        <hr class="authDivider" />

        <section class="authSection">
          <h2 class="authTitle">Ваш персональный пароль</h2>
          <p class="authSub">Укажите ваши персональные данные</p>

          <div class="passwordWrap">
            <input
              id="login-password"
              v-model="loginForm.password"
              class="authInput"
              :type="showPassword ? 'text' : 'password'"
              placeholder="••••••••"
            />
            <button class="eyeBtn" type="button" @click="showPassword = !showPassword">
              <img :src="eyeIcon" alt="показать пароль" />
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
            placeholder="gogo123"
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
import eyeIcon from "../assets/icons/eye.svg";
import { useRouter } from "vue-router";
import { login, register } from "../api/auth";

const router = useRouter();

const mode = ref("login");
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);

const loginForm = reactive({
  email: "",
  password: "",
});

const registerForm = reactive({
  name: "",
  email: "",
  phone: "",
  password: "",
});

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
    router.push("/");
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
    router.push("/");
  } catch (e) {
    error.value = e?.response?.data?.detail || "Ошибка регистрации";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.authPage {
  min-height: 100vh;
  background: #f4f7fb;
  padding: 28px;
  display: grid;
  place-items: center;
}

.authCard {
  width: min(780px, 100%);
  background: #f3f6fb;
  border-radius: 22px;
  border: 1px solid #e1e8f2;
  padding: 42px;
}

.authSection {
  margin-bottom: 10px;
}

.authSection_compact {
  display: grid;
  gap: 10px;
}

.authTitle {
  margin: 0 0 8px;
  color: #25394d;
  font-size: 56px;
  font-weight: 500;
  line-height: 1.03;
}

.authSub {
  margin: 0 0 16px;
  color: #bcc4df;
  font-size: 31px;
}

.authInput {
  width: 100%;
  min-height: 56px;
  padding: 0 20px;
  border-radius: 999px;
  border: 1px solid #dce4ee;
  background: #ffffff;
  color: #24384c;
  font-size: 39px;
}

.authDivider {
  border: none;
  border-top: 1px solid #dce4ee;
  margin: 22px 0;
}

.passwordWrap {
  position: relative;
}

.eyeBtn {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 20px;
}

.submitBtn {
  margin-top: 22px;
  width: 100%;
  min-height: 62px;
  border: none;
  border-radius: 999px;
  background: #7fa673;
  color: #f6f8ff;
  font-size: 26px;
  cursor: pointer;
}

.switchText {
  margin: 16px 0 0;
  text-align: center;
  color: #b9bfd5;
  font-size: 31px;
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
  font-size: 18px;
}

@media (max-width: 900px) {
  .authCard {
    padding: 24px;
  }

  .authTitle {
    font-size: 38px;
  }

  .authSub,
  .switchText {
    font-size: 20px;
  }

  .authInput {
    font-size: 24px;
  }

  .submitBtn {
    font-size: 20px;
  }
}
</style>
