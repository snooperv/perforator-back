<template>
  <div class="background">
    <div class="register">
      <div class="wrapper fadeInDown">
        <div id="formContent">
          <div class="fadeIn first"></div>
          <div class="logo-title">
            <img :src="image" :alt="altText" class="logo" />
            <h1>Perforator</h1>
          </div>

            <input
              type="text"
              id="name"
              class="fadeIn second"
              name="name"
              placeholder="Имя и фамилия"
              v-model="username"
              pattern=".+?(?:[\s'].+?){1,}"
              required
              />
            <fa icon="check" class="icons check text" />
            <fa icon="times" class="icons fault text" />
            <input
              type="tel"
              id="login"
              class="fadeIn second"
              name="login"
              minlength="12"
              maxlength="12"
              placeholder="Номер телефона (+79...)"
              v-model="phone"
              required
            />
            <fa icon="check" class="icons check tel" />
            <fa icon="times" class="icons fault tel" />
            <input
              type="url"
              id="url"
              class="fadeIn third"
              name="url"
              placeholder="Ссылка на профиль СБИС (http://...)"
              v-model="sbis"
              required
            />
            <fa icon="check" class="icons check url" />
            <fa icon="times" class="icons fault url" />
            <input
              type="password"
              id="password"
              class="fadeIn third"
              name="password"
              placeholder="Пароль"
              v-model="password"
              required
            />
            <fa icon="check" class="icons check password" />
            <fa icon="times" class="icons fault password" />

            <div class="photo fadeIn third">
              <div class="empty">
                <img :src="avatar" :alt="altText" class="avatar" />
              </div>
              <div class="background-photo-upload">
                <div class="inner-wrapper">
                  <p class="photo-text">Ваша аватарка</p>
                  <label for="img">Выбрать файл</label>
                  <input
                    type="file"
                    id="img"
                    name="img"
                    accept="image/*"
                    class="photo-btn"
                  />
                </div>
              </div>
            </div>

            <input
              type="submit"
              class="fadeIn fourth"
              @click="submitForm()"
              value="Зарегистрироваться"
            />

          <p class="agreement">
            Регистрируясь, вы принимаете наши
            <a href="#">Условия, Политику использования данных</a> и
            <a href="#">Политику в отношении файлов cookie.</a>
          </p>
        </div>
      </div>
      <div class="enter fadeInDown">
        <div id="formEnter">
          <p>
            Уже есть аккаунт? <a href="/login" style="color: #2c286d">Войти</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      'username': '',
      'phone': '',
      'sbis': '',
      'password': '',
      image: require('@/assets/logo.svg'),
      avatar: require('@/assets/avatar.png'),
      altText: 'Picture'
    }
  },
  methods: {
    submitForm () {
      this.createUser()
      // Т.к. мы уже отправили запрос на создание заметки строчкой выше,
      // нам нужно теперь очистить поля title и body
      this.username = ''
      this.phone = ''
      this.sbis = ''
      this.password = ''
      // preventDefault нужно для того, чтобы страница
      // не перезагружалась после нажатия кнопки submit
      window.location.href = '/my_profile'
    },
    createUser () {
      // Вызываем действие `createNote` из хранилища, которое
      // отправит запрос на создание новой заметки к нашему API.
      this.$store.dispatch('createUser', {
        username: this.username,
        phone: this.phone,
        sbis: this.sbis,
        password: this.password})
    }
  }
}
</script>

<style scoped src="@/css/logAndReg.css"></style>
