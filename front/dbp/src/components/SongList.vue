<template>
    <div class="song-list">
      <ul>
        <li v-for="song in songs" :key="song.id" @click="selectSong(song.id)">
          {{ song.title }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      songs: Array
    },
    methods: {
      selectSong(id) {
        this.$emit('selectSong', id);
      }
    }
  };
  </script>
  
  <style>
  .song-list {
    /* Estilos para tu lista de canciones */
  }
  </style>
  