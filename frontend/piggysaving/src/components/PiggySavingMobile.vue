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
    <n-button v-if="lastSaved===0" @click="rollAgain">今天要存的钱太多了，再Roll一次吧</n-button>
    <v-card elevation="2"></v-card>
    <div id='tableWithdraw'>
      <n-table :bordered="false" :single-line="false" background="#B0757C">
        <thead>
          <tr>
            <th>日期</th>
            <th>取钱金额</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="items in allDataWithdrawn" :key="items.date">
            <td>{{items.date}}</td>
            <td>{{-items.amount}}</td>
          </tr>
        </tbody>
      </n-table>
    </div>
    <div>
      <n-table :bordered="false" :single-line="false" background="#B0757C">
        <thead>
          <tr>
            <th>日期</th>
            <th>金额</th>
            <th>今天存了吗？</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="items in allData" :key="items.date">
            <td>{{items.date}}</td>
            <td>{{items.amount}}</td>
            <td>
              <n-button disabled type="success" v-if="items.saved===1">今天存过了</n-button>
              <n-button type="error" v-if="items.saved===0" @click="updateSaved(items.date, true)">今天还没存，现在存</n-button>
            </td>
          </tr>
        </tbody>
      </n-table>
    </div>
  </div>
</template>

<script lang="ts">
import '../assets/styles/global.css'
import { ref, defineComponent } from 'vue'
import ax from 'axios'
import { NButton } from 'naive-ui'
import { NTable } from 'naive-ui'
export const axios = ax
export default defineComponent({
  components: {
    NButton,
    NTable,
  },
  name: 'HelloWorld',
  props: {
  },
  data() {
    return {
      allData: Array(),
      allDataWithdrawn: Array(),
      sum: 0,
      last: 0,
      lastSaved :0
    }
  },
  mounted () {
    this.sum = 0
    this.last = 0
    axios
      .post(document.location.origin + '/all', {
          desc: true,
          withdraw: false,
        })
      .then(response => {
        this.allData = response.data;
      })
    axios
      .post(document.location.origin + '/all', {
        desc: true,
        withdraw: true,
      })
      .then(response => {
        this.allDataWithdrawn = response.data;
      })
    axios
      .get(document.location.origin + '/sum')
      .then(response => {
        this.sum = response.data.sum;
      })
    axios
      .get(document.location.origin + '/last')
      .then(response => {
        this.last = response.data.last.amount;
        this.lastSaved = response.data.last.saved;
      })
  },
  setup: () => {
  },
  methods: {
    rollAgain: function () {
      axios.get(document.location.origin + '/roll')
      window.location.reload();
    },
    getAll: function() {
      axios
        .post(document.location.origin + '/all', {
          desc: true
        })
        .then(response => {
          this.allData = response.data;
        })
    },
    getSum: function() {
      axios
        .get(document.location.origin + '/sum')
        .then(response => {
          this.sum = response.data.sum;
        })
    },
    getLast: function() {
      axios
        .get(document.location.origin + '/last')
        .then(response => {
          this.last = response.data.last.amount;
          this.lastSaved = response.data.last.saved;
        })
    },
    updateSaved: function( date:String, saved:boolean ) {
      axios.post(document.location.origin + '/save', {
          date: date,
          saved: saved
        })
      window.location.reload();
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