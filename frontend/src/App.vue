<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('http://fonts.cdnfonts.com/css/gotham-pro');
@import url(//db.onlinewebfonts.com/c/323b7229abd327d428021a6d49a7413d?family=Gotham+Pro+Light);

#app {
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

html {
  background-color: #F8F8FA;
}

body {
  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
}

* {
  font-family: 'Gotham Pro', sans-serif;
  /* font-family: 'Gotham Pro light', sans-serif; */
}
</style>
