<template>
  <Calendar />
  <DatePicker v-model="date" />
</template>

<script lang='ts'>
import { defineComponent } from 'vue'
import { Calendar, DatePicker } from 'v-calendar';

export default defineComponent({
  name: 'Dates',
  components: {
    Calendar,
    DatePicker,
  },
  data() {
    return {
      date: new Date(),
    };
  },
})
</script>
