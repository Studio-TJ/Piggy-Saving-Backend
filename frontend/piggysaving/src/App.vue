<template>
  <!-- <img alt="Vue logo" src="./assets/piggy.svg" /> -->
  <PiggySaving msg="猪猪存钱计划" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import PiggySaving from './components/PiggySaving.vue'

export default defineComponent({
  name: 'App',
  components: {
    PiggySaving
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
