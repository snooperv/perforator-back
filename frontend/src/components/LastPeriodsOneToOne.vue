<template>
  <div class="lastPeriods">
    <h1>1-on-1</h1>
    <div class="links">
      <LinkNav/>
    </div>
    <div class="peers">
      <div class="date">
        <h2>Q1</h2>
        <span class="period"> 01.01.2021 - 14.01.2021</span>
      </div>
      <button @click="myFunction()" class="peer dropbtn">
        <img src="@/assets/pic.png" class="peer-avatar"/>
        <span class="name">Коновалов Илья</span>
        <span class="position"> Мой руководитель</span>
        <a href="#" class="chevron">
          <fa icon="chevron-right"/>
        </a>
      </button>
      <div id="myDropdown" class="dropdown-content">
        <h3 class="dropdownTitle">Общие заметки</h3>
        <textarea
          name="generalNotes"
          id="generalNotes"
          rows="5"
          class="ta"
          maxlength="512"
        ></textarea>
        <h3 class="dropdownTitle">
          <fa icon="lock" class="icon"/>
          Личные заметки
        </h3>
        <textarea
          name="personalNotes"
          id="personalNotes"
          rows="5"
          class="ta"
          maxlength="512"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script>
import LinkNav from '@/components/LinkNav'

export default {
  name: 'nav',
  components: {
    LinkNav
  },
  methods: {
    myFunction () {
      document.getElementById('myDropdown').classList.toggle('show')
    }
  }
}
</script>

<style scoped>
h1 {
  text-align: left;
  color: #222;
  margin-top: 30px;
  font-size: 38px;
  align-self: start;
  margin-left: 75px;
}

h2 {
  display: inline-block;
  color: #222;
  font-size: 32px;
}

.lastPeriods {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-size: 20px;
}

.links {
  align-self: flex-start;
  margin-left: 50px;
}

.peers {
  width: 90%;
  background: #ffffff;
  padding: 20px 0;
  border-radius: 30px;
  position: relative;
  top: 50px;
  padding: 0 0 35px 50px;
}

.peers span {
  font-size: 22px;
  color: #222222;
}

.peers p {
  font-weight: 1000;
  text-align: left;
  font-size: 14px;
  margin-left: 30px;
  color: #414141;
}

.peer {
  display: block;
  width: 95%;
  background-color: #ececf2;
  border-radius: 15px;
  height: 65px;
  margin-top: 20px;
  cursor: pointer;
}

.peer .name {
  float: left;
  margin-left: 60px;
  position: relative;
  color: #331969;
  font-family: "Gotham Pro";
  font-size: 22px;
  font-weight: 1000;
}

.peer .position {
  color: #edbd31;
  font-weight: 400;
  position: relative;
  left: 350px;
}

.peer-avatar {
  position: absolute;
  float: left;
  left: -20px;
  top: -5px;
  width: 75px;
}

.chevron {
  position: relative;
  float: right;
  margin-right: 25px;
  font-size: 1.5em;
}

.dropbtn {
  background-color: #ececf2;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
  position: relative;
  z-index: 2;
}

.dropbtn:hover, .dropbtn:focus {
  background-color: #ececf2;
}

.dropdown-content {
  display: none;
  padding-top: 50px;
  background-color: #ececf2;
  width: 95%;
  border-radius: 15px;
  transform: translateY(-50px);
  position: relative;
  z-index: 1;
}

.show {
  display: block;
}

.ta {
  border-radius: 15px;
  border: none;
  width: 95%;
  padding: 5px;
  font-size: 16px;
  resize: none;
  margin-bottom: 30px;
  line-height: 1.5;
}

.dropdownTitle {
  text-align: left;
  margin: 20px 0 15px 20px;
  color: #000;
}

.icon {
  width: 12px;
  padding: 0 5px 0 5px;
  border-radius: 50%;
  background-color: #331969;
  color: #fff;
  margin-right: 5px;
}

.date {
  font-weight: 400;
  text-align: left;
  line-height: 1;
  height: 70px;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-size: 20px;
  color: rgb(167, 167, 167);
  font-weight: 600;
}
</style>
