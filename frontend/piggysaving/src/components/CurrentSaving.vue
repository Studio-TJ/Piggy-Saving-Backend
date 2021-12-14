<template>
  <div class='currentSaving'>
    <h1>这是现在存的钱&#128071;  </h1>
    <h2></h2>
    <h3>€{{currentSaving}}</h3>
    <h4>存钱至今€{{savingAll}} 花费了€{{used}} 投资了€{{invested}}</h4>
  </div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'CurrentSavingComponent',
  props: {
    currentSaving: Number,
    savingAll: Number,
    used: Number,
    invested: Number
  }

})
</script>

<style scoped>
.currentSaving {
  background: #ffffff;
  box-shadow: 5px 5px 20px 5px rgba(0, 0, 0, 0.15);
  border-radius: 30px;
  min-width: 358px;
  min-height: 116px;
}
h1 {
  font-family: Poppins;
  font-style: normal;
  font-weight: bold;
  font-size: 18px;
  line-height: 20px;
  /* or 278% */
  /* display: flex; */
  align-items: center;
  left: 8%;
  /* padding-top: 2%; */
  position: absolute;
  top: 0%;
}
h2 {
  border-bottom: 4px solid #000000;
  position: absolute;
  width: 100%;
  top: 16%;
}
h3 {
  font-family: Poppins;
  font-style: normal;
  font-weight: normal;
  font-size: 36px;
  line-height: 2px;
  align-items: center;
  position: absolute;
  top: 30%;
  margin-left: auto;
  margin-right: auto;
  left: 0%;
  right: 0%;
  text-align: center;
}
h4 {
  font-family: Poppins;
  font-style: normal;
  font-weight: normal;
  font-size: 12px;
  line-height: 2px;
  align-items: center;
  position: absolute;
  top: 75%;
  margin-left: auto;
  margin-right: auto;
  left: 0%;
  right: 0%;
  text-align: center;
}
</style>