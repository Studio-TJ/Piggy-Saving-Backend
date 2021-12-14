<template>
  <!-- <h1>{{ msg }}</h1>
  <h2>测式123</h2> -->
  <!-- <pre>{{allData}}</pre> -->
  <!-- <p>{{allData}}</p> -->
  <div id="piggysaving">
    <img alt="Vue logo" src="../assets/piggy.svg" />
    <h1>猪猪存钱计划</h1>
    <h2>这里是现在存的钱 €{{sum}}</h2>
    <h2>这是存钱至今的总数 €{{sumAll}}</h2>
    <h3>今天要存的钱 €{{last}}</h3>
    <h3>这是用掉的钱 €{{used}}</h3>
    <h3>这是投资的钱 €{{sumInvested}}</h3>
    <n-button v-if="lastSaved===0" @click="rollAgain">今天要存的钱太多了，再Roll一次吧</n-button>
    <n-space>
      <n-input-number v-model:value="withdraw" clearable />
      <n-input v-model:value="description" type="text" placeholder="取钱说明"/>
      <n-button type="warning" @click="executeWithdraw(withdraw, description)">取钱</n-button>
      <n-input-number v-model:value="invest" clearable />
      <n-input v-model:value="description" type="text" placeholder="投资目标"/>
      <n-button type="warning" @click="executeInvest(invest, description)">投资</n-button>
    </n-space>
    <div id='tableWithdraw'>
      <n-table :bordered="false" :single-line="false" background="#B0757C">
        <thead>
          <tr>
            <th>日期</th>
            <th>取钱金额</th>
            <th>取钱原因</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="items in allDataWithdrawn" :key="items.date">
            <td>{{items.date}}</td>
            <td>{{-items.amount}}</td>
            <td>{{items.description}}</td>
          </tr>
        </tbody>
      </n-table>
    </div>
    <div id='tableWithdraw'>
      <n-table :bordered="false" :single-line="false" background="#B0757C">
        <thead>
          <tr>
            <th>日期</th>
            <th>投资金额</th>
            <th>投资目标</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="items in allDataInvested" :key="items.date">
            <td>{{items.date}}</td>
            <td>{{-items.amount}}</td>
            <td>{{items.description}}</td>
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
import { NButton, NInputNumber, NInput, NSpace } from 'naive-ui'
import { NTable } from 'naive-ui'
export const axios = ax
export default defineComponent({
  components: {
    NButton,
    NTable,
    NInputNumber,
    NInput,
    NSpace
  },
  name: 'PiggySaving',
  props: {
  },
  data() {
    return {
      allData: Array(),
      allDataWithdrawn: Array(),
      allDataInvested: Array(),
      sum: 0,
      sumAll: 0,
      used: 0,
      sumInvested: 0,
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
      .get(document.location.origin + '/invested')
      .then(response => {
        this.allDataInvested = response.data;
      })
    axios
      .get(document.location.origin + '/sum')
      .then(response => {
        this.sum = response.data.sum;
      })
    axios
      .get(document.location.origin + '/sumAll')
      .then(response => {
        this.sumAll = response.data.sumAll;
      })
    axios
      .get(document.location.origin + '/sumInvested')
      .then(response => {
        this.sumInvested = response.data.sumInvested;
      })
    axios
      .get(document.location.origin + '/used')
      .then(response => {
        this.used = response.data.used;
      })
    axios
      .get(document.location.origin + '/last')
      .then(response => {
        this.last = response.data.last.amount;
        this.lastSaved = response.data.last.saved;
      })
  },
  setup () {
    return {
      withdraw: ref(0),
      invest: ref(0),
      description: ref("")
    }
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
    getSumAll: function() {
      axios
        .get(document.location.origin + '/sumAll')
        .then(response => {
          this.sumAll = response.data.sumAll;
        })
    },
    getSumInvested: function() {
      axios
        .get(document.location.origin + '/sumInvested')
        .then(response => {
          this.sumInvested = response.data.sumInvested;
        })
    },
    getUsed: function() {
      axios
        .get(document.location.origin + '/used')
        .then(response => {
          this.used = response.data.used;
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
    },
    executeWithdraw: function ( amount: any, description: any ) {
      axios.post(document.location.origin + '/withdraw', {
          amount: amount,
          description: description
        })
      window.location.reload();
    },
    executeInvest: function ( amount: any, description: any ) {
      axios.post(document.location.origin + '/invest', {
          amount: amount,
          description: description
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