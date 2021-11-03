<template>
  <div class="container">
    <h1>1-on-1</h1>
    <div class="links">
      <LinkNav/>
    </div>
    <div class="peers">
      <div class="date">
        <h2>Q2</h2>
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

<style scoped src="@/css/oneToOne.css"></style>
