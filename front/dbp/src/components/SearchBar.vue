<template>
    <div class="player">
      <audio v-if="trackUrl" :src="trackUrl" controls></audio>
      <div v-else>No hay canción seleccionada.</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      trackId: String
    },
    computed: {
      trackUrl() {
        return this.trackId ? `http://tu-api-url/music/${this.trackId}` : null;
      }
    }
  };
  </script>
  
  <style>
  .player {
  }
  </style>
  