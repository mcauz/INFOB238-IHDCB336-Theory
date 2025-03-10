import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from "@/stores/user.js";
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MarketView from '../views/MarketView.vue'
import CartView from '../views/CartView.vue'
import NotFoundView from "../views/NotFoundView.vue";

function check_auth(to, from) {
  if (!useUserStore().is_connected) return { name: "home" };
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/market',
      name: 'market',
      component: MarketView,
      beforeEnter: check_auth
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
      beforeEnter: check_auth
    },
    {
      path: '/logout',
      name: 'logout',
      redirect: _ => {
        useUserStore().logout();
        return { name: 'home' };
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFoundView
    }
  ],
});

export default router
