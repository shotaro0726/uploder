<template>
  <div id="app">
    <h1>Shotaro Up</h1>
    <main id="main">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'app',
  }
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

body {
  line-height: 1;
}

#main {
  padding: 20px;  
}

#side {
  background-color: #ffff;
}

#header-logo {
  width: 150px;
}

@media (min-width: 1024px) {
  #app {
    display: grid;
    grid-template-columns: 300px 1fr;
  }
  #side {
    grid-column: 1;
    position: fixed;
    top:0;
    bottom:0;
    width:300px;
  }
  #main {
    grid-column: 2;
    padding: 20px;
  }
}

</style>
