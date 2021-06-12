<template>
  <!-- <h1>{{ msg }}</h1>
  <h2>测式123</h2> -->
  <!-- <pre>{{allData}}</pre> -->
  <!-- <p>{{allData}}</p> -->
  <div id="piggysaving">
    <img alt="Vue logo" src="../assets/piggy.svg" />
    <h1>猪猪存钱计划</h1>
    <h2>这里是现在存的钱 €{{sum}}</h2>
    <h3>今天要存的钱 €{{last}}</h3>
    <n-button @click="rollAgain">今天要存的钱太多了，再Roll一次吧</n-button>
    <div>
      <!-- {{items.amount}} -->
      <n-table :bordered="false" :single-line="false">
        <thead>
          <tr>
            <th>日期</th>
            <th>金额</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="items in allData" :key="items.date">
            <td>{{items.date}}</td>
            <td>{{items.amount}}</td>
          </tr>
        </tbody>
      </n-table>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue'
import ax from 'axios'
import { NButton } from 'naive-ui'
import { NTable } from 'naive-ui'

export const axios = ax
export default defineComponent({
  components: {
    NButton,
    NTable
  },
  name: 'HelloWorld',
  props: {
  },
  data() {
    return {
      allData: Array(),
      sum: 0,
      last: 0
    }
  },
  mounted () {
    this.sum = 0
    this.last = 0
    axios
      .get('https://saving.jamesvillage.dev/all')
      .then(response => {
        const { date, amount } = response.data;
        this.allData = response.data;
      })
    axios
      .get('https://saving.jamesvillage.dev/sum')
      .then(response => {
        this.sum = response.data.sum;
      })
    axios
      .get('https://saving.jamesvillage.dev/last')
      .then(response => {
        this.last = response.data.last;
      })
  },
  setup: () => {
  },
  methods: {
    rollAgain: function () {
      axios.get("https://saving.jamesvillage.dev/roll")
      window.location.reload();
    },
    getAll: function() {
      axios
        .get('https://saving.jamesvillage.dev/all')
        .then(response => {
          const { date, amount } = response.data;
          this.allData = response.data;
        })
    },
    getSum: function() {
      axios
        .get('https://saving.jamesvillage.dev/sum')
        .then(response => {
          this.sum = response.data.sum;
        })
    },
    getLast: function() {
      axios
        .get('https://saving.jamesvillage.dev/last')
        .then(response => {
          this.last = response.data.last;
        })
    }
  }
})
</script>

<style scoped>
a {
  color: #42b983;
}

label {
  margin: 0 0.5em;
  font-weight: bold;
}

code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 4px;
  color: #304455;
}
</style>
