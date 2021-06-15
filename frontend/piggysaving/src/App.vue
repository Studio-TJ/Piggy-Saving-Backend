<template>
  <!-- <img alt="Vue logo" src="./assets/piggy.svg" /> -->
  <PiggySavingMobile v-if="isMobile" />
  <PiggySaving v-if="!isMobile" msg="猪猪存钱计划" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import PiggySaving from './components/PiggySaving.vue'
import PiggySavingMobile from './components/PiggySavingMobile.vue'
import { isMobile } from 'mobile-device-detect';

export default defineComponent({
  name: 'App',
  components: {
    PiggySaving,
    PiggySavingMobile
  },
  data() {
    return {
      isMobile: isMobile
    }
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
