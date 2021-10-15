<template>
    <div class="background">
        <div class="register">
            <div class="wrapper fadeInDown">
            <div id="formContent">

                <div class="fadeIn first">
                
                </div>
                <div class="logo-title">
                    <img src="../../public/logo.svg" alt="logo" class="logo">
                    <h1>Perforator</h1>
                </div>

                <form class="log">
                <input type="text" id="name" class="fadeIn second" name="name" placeholder="Имя и фамилия" required>
                <input type="text" id="login" class="fadeIn second" name="login" placeholder="Номер телефона" minlength="11" maxlength="11" required>
                <input type="text" id="url" class="fadeIn third" name="url" placeholder="Ссылка на профиль СБИС" required>
                <input type="password" id="password" class="fadeIn third" name="password" placeholder="Пароль" required>
                <input type="submit" class="fadeIn fourth" value="Зарегистрироваться">
                </form>

            </div>
            </div>

                <div class="enter fadeInDown">
                <div id="formEnter">
                <p>Уже есть аккаунт? <a href="/login" style="color: #2C286D;">Войти</a></p>
                </div>
            </div>
        </div>
</div>
</template>

<script>
    export default {

    }
</script>

<style scoped>

body {
  font-family: 'Gotham Pro', sans-serif;
  height: 100vh;
}

a {
  color: #2C286D;
  display:inline-block;
  text-decoration: none;
  font-weight: 400;
}

p {
    font-family: 'Gotham Pro light';
    font-weight: 1000;
}

h1 {
    position: relative;
    display:inline-block;
    letter-spacing: 2px;
    font-size: 36px;
    font-weight: 1000;
}

.background {
    height: 100vh;
    width: 100vw;
    background-color: #E5E5E5;
}

.register {
    position: relative;
    top: 20vh;
}

.wrapper {
  display: flex;
  align-items: center;
  flex-direction: column; 
  justify-content: center;
  width: 100%;
  padding: 20px;
}

.enter {
  display: flex;
  align-items: center;
  flex-direction: column; 
  justify-content: center;
  padding: 20px;
  width: 100%;
}

#formEnter {
    border-radius: 15px;
    border: 1px solid #414141;
    background: #fff;
    color: #222;
    font-weight: 200;
    font-size: 14px;
    padding: 5px 25px;
    width: 90%;
    max-width: 500px;
    position: relative;
    text-align: center;
    /* -webkit-box-shadow: 0 5px 10px 0 rgba(0,0,0,0.3);
    box-shadow: 0 5px 10px 0 rgba(0,0,0,0.3); */
}

.log {
  margin-top: 20px;
}

.logo {
    position: relative;
    display: inline-block;
    width:40px; 
    top: 5px; 
    margin-right: 10px;
}

.logo-title {
    position: relative;
    left: -10px;
    color: #414141;
    font-weight: 1000;
    margin-top: 20px;
}

#formContent {
  -webkit-border-radius: 15px;
  border-radius: 15px;
  border: 1px solid #414141;
  background: #fff;
  padding: 0 20px;
  width: 90%;
  max-width: 500px;
  position: relative;
  /* -webkit-box-shadow: 0 5px 10px 0 rgba(0,0,0,0.3);
  box-shadow: 0 5px 10px 0 rgba(0,0,0,0.3); */
  text-align: center;
}

input[type=button], input[type=submit], input[type=reset]  {
    font-family: 'Gotham Pro light';
    font-weight: 1000;
    letter-spacing: 1px;
    background-color: #c1c1ec;
    border: none;
    color: white;
    padding: 15px 7px;
    width: 85%;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 18px;
    cursor: pointer;
    -webkit-border-radius: 8px;
    border-radius: 8px;
    margin: 5px 20px 40px 20px;
    -webkit-transition: all 0.3s ease-in-out;
    -moz-transition: all 0.3s ease-in-out;
    -ms-transition: all 0.3s ease-in-out;
    -o-transition: all 0.3s ease-in-out;
    transition: all 0.3s ease-in-out;
    margin-top: 25px
}

input[type=button]:hover, input[type=submit]:hover, input[type=reset]:hover  {
    background-color: rgba(140, 140, 245, 1);
    transition: 0.25s;
    cursor: pointer;
}

input[type=button]:active, input[type=submit]:active, input[type=reset]:active  {
    -moz-transform: scale(0.95);
    -webkit-transform: scale(0.95);
    -o-transform: scale(0.95);
    -ms-transform: scale(0.95);
    transform: scale(0.95);
}

input[type=text], input[type=password], input[type=number], input[type=tel] {
    background-color: #F4F4FA;
    border: none;
    color: #0d0d0d;
    padding: 15px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 5px;
    width: 85%;
    border: 1px solid #414141;
    box-shadow: inset -1px 1px 4px rgba(0, 0, 0, 0.25);
    -webkit-transition: all 0.5s ease-in-out;
    -moz-transition: all 0.5s ease-in-out;
    -ms-transition: all 0.5s ease-in-out;
    -o-transition: all 0.5s ease-in-out;
    transition: all 0.5s ease-in-out;
    -webkit-border-radius: 8px;
    border-radius: 8px;
}

input[type=text]:focus, input[type=password]:focus, input[type=number]:focus, input[type=tel]:focus {
    background-color: #fff;
}

input[type=text]:focus::placeholder, input[type=password]:focus::placeholder, input[type=number]::placeholder, input[type=tel]::placeholder { 
    color: transparent;
}

input[type=text]::placeholder, input[type=password]::placeholder, input[type=number]::placeholder, input[type=tel]::placeholder {
    font-family: 'Gotham Pro light';
    font-size: 20px;
    color: rgba(170, 170, 170, 1);
    text-align: left;
    font-weight: 400;
}

.fadeInDown {
  -webkit-animation-name: fadeInDown;
  animation-name: fadeInDown;
  -webkit-animation-duration: 1s;
  animation-duration: 1s;
  -webkit-animation-fill-mode: both;
  animation-fill-mode: both;
}

@-webkit-keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    -webkit-transform: translate3d(0, -100%, 0);
    transform: translate3d(0, -100%, 0);
  }
  100% {
    opacity: 1;
    -webkit-transform: none;
    transform: none;
  }
}

@-webkit-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@-moz-keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }

.fadeIn {
  opacity:0;
  -webkit-animation:fadeIn ease-in 1;
  -moz-animation:fadeIn ease-in 1;
  animation:fadeIn ease-in 1;

  -webkit-animation-fill-mode:forwards;
  -moz-animation-fill-mode:forwards;
  animation-fill-mode:forwards;

  -webkit-animation-duration:1s;
  -moz-animation-duration:1s;
  animation-duration:1s;
}

.fadeIn.first {
  -webkit-animation-delay: 0.4s;
  -moz-animation-delay: 0.4s;
  animation-delay: 0.4s;
}

.fadeIn.second {
  -webkit-animation-delay: 0.6s;
  -moz-animation-delay: 0.6s;
  animation-delay: 0.6s;
}

.fadeIn.third {
  -webkit-animation-delay: 0.8s;
  -moz-animation-delay: 0.8s;
  animation-delay: 0.8s;
}

.fadeIn.fourth {
  -webkit-animation-delay: 1s;
  -moz-animation-delay: 1s;
  animation-delay: 1s;
}

*:focus {
    outline: none;
} 

* {
  box-sizing: border-box;
}
</style>