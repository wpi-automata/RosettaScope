<template>
  <v-responsive class="border rounded">
    <v-app>
      <v-app-bar title="RosettaScope"></v-app-bar>
      <v-main class="main_style">
        <StreamViewer/>
        <StreamAdder/>
      </v-main>
      <v-footer></v-footer>
    </v-app>
  </v-responsive>
</template>

<script setup>
import StreamAdder from './components/StreamAdder.vue';
import StreamViewer from './components/StreamViewer.vue';
</script>

<style>
  .main_style {
    height: 100%
  }
</style>
