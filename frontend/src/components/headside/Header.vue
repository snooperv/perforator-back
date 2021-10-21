<template>
  <div class="header">
    <div class="wrapper">
      <div class="toggle">
        <input type="checkbox" id="check" />
        <label for="check" class="icons">
          <fa icon="bars" id="bars" />
          <fa icon="times" id="cancel" />
        </label>
      </div>
      <div class="logo-div">
        <img src="@/assets/logo.svg" alt="logo" class="logo" />
      </div>
      <div class="logo-title">
        <h3>Perforator</h3>
      </div>
    </div>
    <div class="rightWrapper">
      <a href="#popup"
        ><img
          src="@/assets/settings.svg"
          alt="settings"
          class="settings rightIcon btn"
      /></a>
    </div>

    <div class="popup" id="popup">

      <div class="popup-content">
        <a href="#" class="close"><fa icon="times" /></a>
        <h3>Мои данные</h3>
        <div class="user">
          <img class="avatar" src="@/assets/pic.png" />
          <div class="user-info">
            <p class="name">Имя и фамилия:
              <span class="text">
                Марк Цукерберг
              </span>
            </p>
            <p class="tel">Номер телефона:
              <span class="text">
                89221337228
              </span>
            </p>
            <p class="url">Профиль СБИС:
              <a class="url-sbis text" href="#">
                Марк Цукерберг
              </a>
            </p>
          </div>
        </div>
        <div class="buttons">
          <button class="change">Изменить данные</button>
          <button class="exit">
            <img src="@/assets/exit.png" class="exit-icon">
            Выйти из аккаунта</button>
        </div>
      </div>

    </div>
    <a href="#" class="close-popup"></a>
  </div>
</template>

<script>
export default {}
</script>

<style scoped src="@/css/header.css"></style>
