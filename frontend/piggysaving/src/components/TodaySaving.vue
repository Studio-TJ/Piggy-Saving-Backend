<template>
  <div class='todaySaving'>
    <h1>这里是今天要存的钱&#128071;  </h1>
    <h2 :style="{top:'16%',width:'99%'}"></h2>
    <h3>€{{todaySaving}}</h3>
    <h2 :style="{top:'63%',width:'99%'}"></h2>
    <n-button-group id='TodayButton'>
          <n-button round @click="rollAgain">
            再roll一遍吧
          </n-button>
          <n-button round disabled v-if="todaySaved===1">
            今天存过啦
          </n-button>
          <n-button round v-if="todaySaved===0">
            存钱
          </n-button>
    </n-button-group>
  </div>
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
import { NButton, NButtonGroup } from 'naive-ui'
import ax from 'axios'
export const axios = ax
export default defineComponent({
  name: 'TodaySavingComponent',
  props: {
    todaySaving: Number,
    todaySaved: Number
  },
  components: {
    NButton,
    NButtonGroup
  },
  methods: {
    rollAgain: function () {
      axios.get(document.location.origin + '/roll')
      window.location.reload();
    },
  }
})
</script>

<style scoped>
.todaySaving {
  border: 2px solid #000000;
  box-sizing: border-box;
  border-radius: 30px;
  min-width: 400px;
  min-height: 150px;
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
}
h3 {
  font-family: Poppins;
  font-style: normal;
  font-weight: normal;
  font-size: 36px;
  line-height: 2px;
  align-items: center;
  position: absolute;
  top: 25%;
  margin-left: auto;
  margin-right: auto;
  left: 0%;
  right: 0%;
  text-align: center;
}
#TodayButton {
  position: absolute;
  top: 76%;
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>