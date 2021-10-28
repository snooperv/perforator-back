<template>
  <div class="sidebar">
    <div class="profile-div">
      <div class="profile-pic">
        <img src="@/assets/pic.png" />
      </div>
      <div class="profile-name">
        <h2>
          {{ user["username"] }}
        </h2>
      </div>
    </div>

    <div class="menu-items">
      <!-- <router-link to="/" active-class="active" tag="button" exact class="side-btn">
                <div class="link-container">
                    Мой профиль
                </div>
            </router-link> -->
      <router-link
        to="/perfomance-review"
        active-class="active"
        tag="button"
        exact
        class="side-btn perfomance-review"
        style="font-size: 22px"
      >
        <div class="link-container">
          <img
            src="@/assets/perfomance-review-icon.svg"
            width="20"
            height="20"
          />
          Perfomance Review
        </div>
      </router-link>
      <router-link
        to="/self-review"
        active-class="active"
        tag="button"
        exact
        class="side-btn small"
      >
        <div class="link-container">self reveiw</div>
      </router-link>
      <router-link
        to="/me-estimate"
        active-class="active"
        tag="button"
        exact
        class="side-btn small"
      >
        <div class="link-container">
          я оцениваю

          <!-- Нужно будет поправить, сделал набросок -->
          <div class="amount-bg"></div>
          <span class="amount">10 из 15</span>
          <!-- ------------------------------------- -->
        </div>
      </router-link>
      <router-link
        to="/me-manager"
        active-class="active"
        tag="button"
        exact
        class="side-btn small"
      >
        <div class="link-container">
          я менеджер

          <!-- Нужно будет поправить, сделал набросок -->
          <div class="amount-bg second"></div>
          <span class="amount">1 из 8</span>
          <!-- -------------------------------------- -->
        </div>
      </router-link>
      <router-link
        to="/one-to-one"
        active-class="active"
        tag="button"
        exact
        class="side-btn small"
      >
        <div class="link-container">one to one</div>
      </router-link>
      <router-link
        to="/last-periods"
        active-class="active"
        tag="button"
        exact
        class="side-btn"
      >
        <div class="link-container">
          <img src="@/assets/history.svg" width="20" height="20" />
          Прошлые периоды оценки
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Sidebar',
  computed: mapGetters(['users']),
  methods: {
    deleteUser (user) {
      // Вызываем действие `deleteUser` из нашего хранилища, которое
      // попытается удалить пользователя из нашей базы данных, отправив запрос к API
      this.$store.dispatch('deleteUser', user)
    }
  },
  beforeMount () {
    // Перед тем как загрузить страницу, нам нужно получить список всех
    // имеющихся пользователей. Для этого мы вызываем действие `getUsers` из
    // нашего хранилища
    this.$store.dispatch('getCurrentUser') // TODO
  }
}
</script>

<style scoped src="@/css/sidebar.css"></style>
