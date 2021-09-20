<template>
  <n-space>
    <n-input-number v-model:value="withdraw" clearable />
    <n-button type="warning" @click="executeWithdraw(withdraw)">取钱</n-button>
  </n-space>
</template>

<script lang='ts'>
import { defineComponent, ref } from 'vue'
import { NInputNumber, NButton, NSpace } from 'naive-ui';
import ax from 'axios'

export const axios = ax
export default defineComponent({
  name: 'Withdraw',
  components: {
    NInputNumber,
    NButton,
    NSpace
  },
  setup () {
    return {
      withdraw: ref(0)
    }
  },
  methods: {
    executeWithdraw: function ( amount: any ) {
      axios.post(document.location.origin + '/withdraw', {
          amount: amount
        })
      window.location.reload();
    }
  }
})
</script>
