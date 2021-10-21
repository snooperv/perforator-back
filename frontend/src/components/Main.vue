<template>
    <div>
        <div class="header">
            <Header />
        </div>
        <div class="menu">
                <Sidebar/>
        </div>
        <div class="main">
            <div class="content">
                <router-view/>
            </div>
        </div>
    </div>
</template>

<script>
import Header from '@/components/headside/Header'
import Sidebar from '@/components/headside/Sidebar'

export default {
  name: 'home',

  components: {
    Sidebar,
    Header
  }
}
</script>

<style>
@import url('http://fonts.cdnfonts.com/css/gotham-pro');

body {
    overflow-x: hidden;
    background-color: #F8F8FA;
}

.main {
    display: grid;
    grid-template-columns: 20vw auto;
    grid-template-rows: 75px auto;
    background-color: #F8F8FA;
}

.header {

}

.content {
    background-color: #F8F8FA;
    grid-column-start: 2;
    grid-row-start: 2;
}

@media (max-width: 800px) {
    .main {
        grid: unset;
    }

    .menu {
        display: none;
    }
}

</style>
