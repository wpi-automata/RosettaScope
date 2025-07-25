<script setup>
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';

// const loading = ref(true)
const streams = ref([])
var foo = []
var ding = 'dong'
// const streams = await axios.get('http://127.0.0.1:8000/stream_manager/get_streams');
// console.log(streams.data.streams);
// console.log('bingus');
async function get_data() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/stream_manager/get_streams');
    return response.data.streams
  }
  catch {
    console.error('data get failed')
  }
  return
}
onBeforeMount(async () => {
  streams.value = await get_data()
  console.log(streams.value)
  console.log(streams.value[0])
})
</script>

<template>
  <v-card variant="outlined">
      <h1> Streams </h1>
      <v-expansion-panels class="stream_panel">
        <v-expansion-panel v-for="stream in streams">
          <v-expansion-panel-title>
            <h3 class="stream_type">{{ stream.type }}</h3>
            <p>{{ stream.name }}</p>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-container>
              <v-row v-for="key in Object.keys(stream)">
                <p class="stream_attr"><b>{{ key }}:</b></p>
                <p>{{ stream[key] }}</p>
              </v-row>
            </v-container>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
  </v-card>
</template>

<style>
.stream_type {
  padding-right: 5ch;
}
.stream_attr {
  padding-right: 2ch;
}
.stream_panel {
  max-width: 20%;
}
</style>
