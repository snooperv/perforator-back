<template>
  <div class="background">
    <div class="login">
      <div class="wrapper fadeInDown">
        <div id="formContent">
          <div class="fadeIn first"></div>
          <div class="logo-title">
            <img :src="image" :alt="altText" class="logo" />
            <h1>Perforator</h1>
          </div>
          <form class="log">
            <input
              type="tel"
              id="login"
              class="fadeIn second"
              name="login"
              placeholder="Номер телефона"
              minlength="11"
              maxlength="11"
              required
            />
            <fa icon="check" class="icons check tel" />
            <fa icon="times" class="icons fault tel" />
            <input
              type="password"
              id="password"
              class="fadeIn third"
              name="password"
              placeholder="Пароль"
              required
            />
            <fa icon="check" class="icons check password" />
            <fa icon="times" class="icons fault password" />
            <input type="submit" class="fadeIn fourth" value="Войти" />
          </form>
          <div class="admin fadeIn fourth">
            <button class="adminLogin">Администратор</button>
          </div>
        </div>
      </div>

      <div class="enter fadeInDown">
        <div id="formEnter">
          <p>
            У вас еще нет аккаунта?
            <a href="/" style="color: #2c286d">Зарегистрироваться</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data () {
    // eslint-disable-next-line standard/object-curly-even-spacing
    return { image: require('@/assets/logo.svg')}
  }
}
</script>

<style scoped src="@/css/logAndReg.css"></style>
