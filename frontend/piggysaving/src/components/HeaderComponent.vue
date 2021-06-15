<template>
  <div class='flex-parent'>
    <h1>&#128055;&#128055;存钱计划</h1>
    <div class="line-div"><div class="the-line"></div></div>
    <h1>快去存钱啦</h1>
  </div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'HeaderComponent',
  props: {
  }

})
</script>

<style scoped>
h1 {
  font-family: Poppins;
  font-style: normal;
  font-weight: bold;
  font-size: 24px;
  line-height: 36px;
  /* identical to box height */

  display: flex;
  align-items: center;

  color: #161616;
  position: relative;
  padding: 0 3%;
}
.flex-parent{
  display: flex;
}
.line-div{
  flex: 1; /* flex-grow */
  padding: 0 3%;
}
.the-line{
  height: 50%;
  border-bottom:4px solid #161616;
}
</style>