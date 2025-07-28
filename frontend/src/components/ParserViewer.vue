<script setup>
import axios from 'axios';
import { onBeforeMount, ref } from 'vue';

const parsers = ref([])

async function get_data() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/parser_manager/get_parsers');
    return response.data.parsers
  }
  catch {
    console.error('data get failed')
  }
  return
}
onBeforeMount(async () => {
  parsers.value = await get_data()
  console.log(parsers.value)
  console.log(parsers.value[0])
})
</script>

<template>
  <v-card >
      <h1> Parsers </h1>
      <v-expansion-panels class="stream_panel">
        <v-expansion-panel v-for="parser in parsers">
          <v-expansion-panel-title>
            <h3 class="stream_type">{{ parser.type }}</h3>
            <p>{{ parser.name }}</p>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-container>
              <v-row v-for="key in Object.keys(parser)">
                <p class="stream_attr"><b>{{ key }}:</b></p>
                <p>{{ parser[key] }}</p>
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
