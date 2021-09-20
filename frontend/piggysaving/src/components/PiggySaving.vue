<template>
  <!-- <h1>{{ msg }}</h1>
  <h2>测式123</h2> -->
  <!-- <pre>{{allData}}</pre> -->
  <!-- <p>{{allData}}</p> -->
  <div id="piggysaving" class='backgroundbox'>
    <header-component/>
    <div id='piggyImage'>
      <img alt="Vue logo" src="../assets/piggy.svg" />
    </div>
    <div id='currentSavingBox'>
      <current-saving-component :currentSaving=sum />
    </div>
    <div id='todaySavingBox'>
      <today-saving-component :todaySaving=last :todaySaved=lastSaved />
    </div>
    <!-- <div id='table'>
      <n-data-table
        :columns="savingColumns"
        :data="allData"
        :pagination="pagination"
        :single-line="false" />
    </div> -->
    <div id='table'>
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
    <div id='dateCalendar'>
      <dates/>
    </div>
    <div id='withdraw'>
      <withdraw/>
    </div>
  </div>
</template>

<script lang="ts">
import '../assets/styles/global.css'
import { defineComponent, h } from 'vue'
import ax from 'axios'
import { NButton } from 'naive-ui'
import { NTable, NDataTable } from 'naive-ui'
import { NInputNumber } from 'naive-ui'
import CurrentSavingComponent from './CurrentSaving.vue'
import TodaySavingComponent from './TodaySaving.vue'
import HeaderComponent from './HeaderComponent.vue'
import Dates from './Dates.vue'
import Withdraw from './Withdraw.vue'

export const axios = ax
export default defineComponent({
  components: {
    NButton,
    NTable,
    NDataTable,
    NInputNumber,
    CurrentSavingComponent,
    HeaderComponent,
    TodaySavingComponent,
    Dates,
    Withdraw
  },
  name: 'PiggySaving',
  props: {
  },
  data() {
    return {
      allData: Array(),
      allDataWithdrawn: Array(),
      sum: 0,
      last: 0,
      lastSaved :0,
      // savingColumns: [
      //   {
      //     title: '日期',
      //     key: 'date'
      //   },
      //   {
      //     title: '金额',
      //     key: 'amount'
      //   },
      //   {
      //     title: '今天存了吗？',
      //     key: 'saved',
      //     render (row: any) {
      //       return h(
      //         NButton,
      //         {
      //           size: 'small',
      //           onClick: () => {
      //             axios.post(document.location.origin + '/save', {
      //                 date: row.date,
      //                 saved: true
      //               })
      //             window.location.reload();
      //           },
      //           disabled: true,
      //           v-if: row.saved
      //         },
      //       )
      //     }
      //   }
      // ],
      pagination: {
        pagSize: 10
      }
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
.backgroundbox {
  background: #FFFFFF;
  box-shadow: 30px 30px 40px rgba(0, 0, 0, 0.25);
  border-radius: 60px;
  position: absolute;
  width: 90%;
  height: 120vh;
  left: 50%;
  transform: translate3d(-50%,0, 0);
}
#piggyImage {
  position: absolute;
  width: 30%;
  /* height: 25vw; */
  left: 10%;
  top: 15%;


}
#currentSavingBox
{
  position: absolute;
  right: 18%;
  top: 20%;
}
#todaySavingBox
{
  position: absolute;
  left: 10%;
  /* top: 100%; */
  bottom: 5%;
}
#dateCalendar {
  position: absolute;
  right: 2%;
  bottom: 20%;
}
#withdraw {
  position: absolute;
  right: 10%;
  bottom: 60%;
}
#table {
  position: absolute;
  display: flex;
  top: 100%;
}
#tableWithdraw {
  position: absolute;
  display: flex;
  top: 100%;
  left: 50%
}
</style>
