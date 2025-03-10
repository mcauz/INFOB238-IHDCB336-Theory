<script setup>
import { reactive } from "vue";
import router from "@/router/index.js";
import { useUserStore } from "@/stores/user.js";

const userStore = useUserStore();

const state = reactive({
  loginPage: true,
  login: {
    username: "",
    password: "",
    error: false,
  },
  register: {
    username: "",
    password: "",
    confirm: "",
    disabled: true,
    success: false,
    error: false,
  }
});

function changePage() {
  state.loginPage = !state.loginPage;
}

function checkPassword() {
  state.register.disabled = state.register.password !== state.register.confirm || state.register.password.length === 0;
}

async function login() {
  const { username, password } = state.login;
  const response = await userStore.request("POST", "/login", { username, password });
  if (response.success) {
    await userStore.login(response.token);
    await router.push('/');
    return;
  }
  state.login.error = true;
}

async function register() {
  const { username, password, confirm } = state.register;
  const response = await userStore.request("POST", "/register", { username, password, confirm_password: confirm });
  if (response.success) {
    state.register.success = true;
    state.loginPage = true;
  } else {
    state.register.error = true;
  }
}
</script>

<template>
  <section>
    <div class="loginOrRegister">
      Login
      <label class="switch">
        <input id="toggle" type="checkbox" @change="changePage" :checked="!state.loginPage">
        <span class="slider round"></span>
      </label>
      Register
    </div>
    <div v-if="state.loginPage" id="loginForm">
      <p v-if="state.register.success" class="success-message">Registration succeed.</p>
      <p v-if="state.login.error" class="error-message">Invalid username and/or password.</p>
      <label for="username">Username</label>
      <input type="text" id="username" v-model="state.login.username" />
      <label for="password">Password</label>
      <input type="password" id="password" v-model="state.login.password" />
      <button class="btn submit" @click="login">Login</button>
      <a href="" onclick="alert('You are a loser !')">Forget password ?</a>
    </div>
    <div v-else id="registerForm">
      <p v-if="state.register.error" class="error-message">Username already used.</p>
      <label for="usernameR">Username</label>
      <input type="text" id="usernameR" v-model="state.register.username" />
      <label for="passwordR">Password</label>
      <input type="password" id="passwordR" v-model="state.register.password" @keyup="checkPassword" />
      <label for="confirmPasswordR">Confirm password</label>
      <input type="password" id="confirmPasswordR" v-model="state.register.confirm" @keyup="checkPassword" />
      <button class="btn submit" :disabled="state.register.disabled" @click="register">Register</button>
    </div>
  </section>
</template>

<style lang="sass" scoped>
label, input:not([type="checkbox"])
  display: block
  margin: 10px 0

input[type="text"], input[type="password"]
  width: 100%

.loginOrRegister
  text-align: center
  font-size: 2em

/* below code https://www.w3schools.com/howto/howto_css_switch.asp */

.switch
  position: relative
  display: inline-block
  width: 60px
  height: 34px

.switch input
  opacity: 0
  width: 0
  height: 0

.slider
  position: absolute
  cursor: pointer
  top: 0
  left: 0
  right: 0
  bottom: 0
  background-color: #ccc
  -webkit-transition: .4s
  transition: .4s

.slider:before
  position: absolute
  content: ""
  height: 26px
  width: 26px
  left: 4px
  bottom: 4px
  background-color: white
  -webkit-transition: .4s
  transition: .4s

input:checked + .slider:before
  transform: translateX(26px)

.slider.round
  border-radius: 34px

.slider.round:before
  border-radius: 50%
</style>
