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
          <form id="register" @submit="submitForm()">
            <input
              type="text"
              id="name"
              class="fadeIn second"
              placeholder="Имя и фамилия"
              v-model="username"
              pattern=".+?(?:[\s'].+?){1,}"

              />
            <fa icon="check" class="icons check text" />
            <fa icon="times" class="icons fault text" />
            <input
              type="tel"
              id="login"
              class="fadeIn second"
              minlength="12"
              maxlength="12"
              placeholder="Номер телефона (+79...)"
              v-model="phone"

            />
            <fa icon="check" class="icons check tel" />
            <fa icon="times" class="icons fault tel" />
            <input
              type="url"
              id="url"
              class="fadeIn third"
              placeholder="Ссылка на профиль СБИС (http://...)"
              v-model="sbis"

            />
            <fa icon="check" class="icons check url" />
            <fa icon="times" class="icons fault url" />
            <input
              type="password"
              id="password"
              class="fadeIn third"
              placeholder="Пароль"
              v-model="password"

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
                    accept="image/*"
                    class="photo-btn"
                  />
                </div>
              </div>
            </div>

            <input
              type="submit"
              class="fadeIn fourth"
              value="Зарегистрироваться"
            />
          </form>
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
      this.$store.dispatch('createUser', {
        username: this.username,
        phone: this.phone,
        sbis: this.sbis,
        password: this.password})
      // this.$router.push({ name: 'Main' })
      // window.location.href = '/my_profile'
    }
  }
}
</script>

<style scoped src="@/css/logAndReg.css"></style>
