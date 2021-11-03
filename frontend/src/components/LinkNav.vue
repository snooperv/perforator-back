<template>
  <div class="link-nav">
    <div class="links">
      <router-link
        to="/one-to-one"
        active-class="active"
        tag="button"
        exact
        class="side-btn first"
      >
        <div class="link">текущие</div>
      </router-link>
      <router-link
        to="/one-to-one/last-periods"
        active-class="active"
        tag="button"
        exact
        class="side-btn second"
      >
        <div class="link">прошлые периоды</div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>

.side-btn {
  position: relative;
  display: inline-block;
  font-size: 16px;
  width: 250px;
  height: 40px;
  border: none;
  border-radius: 2em;
  padding: 10px 0px;
  cursor: pointer;
  margin: 0;
  background-color: #fff;
}

.side-btn:hover {
  background-color: rgba(165, 164, 245, 0.25);
  border-radius: 2em;
  transition: 0.2s;
}

.side-btn.active {
  position: relative;
  color: #fff;
  background-color: rgba(165, 164, 245, 1);
  border-radius: 3em;
  transition: 0.2s;
  display: inline-block;
  z-index: 1;
}

.link {
  font-family: 'Gotham Pro light';
  font-weight: 1000;
  letter-spacing: 1px;
  padding: 0 30px;
}

.links {
  margin-top: 20px;
  width: 476px;
  height: 40px;
  display: block;
  float: left;
  margin-left: 30px;
  border: 1px solid #edbd31;
  border-radius: 2em;
  margin-top: -5px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.25);
}

.second {
  margin-left: -30px;
}
</style>
