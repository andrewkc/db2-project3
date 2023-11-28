<template>
  <div>
    <SearchBar @search="handleSearch" />
    <SongList :songs="songs" @selectSong="handleSelectSong" />
    <Player :trackId="selectedTrackId" />
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue';
import SongList from '@/components/SongList.vue';
import Player from '@/components/PlayerPage.vue';
import MusicService from '@/services/MusicService.js';

export default {
  components: {
    SearchBar,
    SongList,
    Player
  },
  data() {
    return {
      songs: [],
      selectedTrackId: null
    };
  },
  methods: {
    async handleSearch({ query, k, language }) {
      const response = await MusicService.searchSongs(query, k, language);
      this.songs = response.data;
    },
    handleSelectSong(trackId) {
      this.selectedTrackId = trackId;
      // Aquí también puedes cargar las recomendaciones
    }
  }
};
</script>
