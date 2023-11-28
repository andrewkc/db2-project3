<template>
  <div class="search-panel">
    <form @submit.prevent="onSearch">
      <input type="text" v-model="searchQuery" placeholder="Buscar canciones" />

      <select v-model="searchLanguage">
        <option value="">Cualquier idioma</option>
        <option value="es">Español</option>
        <option value="en">Inglés</option>
        <option value="de">Alemán</option> 
        <option value="it">Italiano</option> 
        <option value="pt">Portugués</option>
      </select>

      <select v-model="searchEndpoint">
        <option value="invidx">Índice Invidx</option>
        <option value="gin">Índice Gin</option>
      </select>

      <input type="number" v-model.number="resultLimit" placeholder="Número de resultados" />

      <button type="submit">Buscar</button>
    </form>

    <ul v-if="searchResults.length">
      <li v-for="track in searchResults" :key="track.track_id">
        <div>
          <p>{{ track.track_name }} - {{ track.track_artist }}</p>
          <p>{{ getLyricsPreview(track.lyrics) }}</p>
        </div>
        <button @click="playTrack(track)">{{ buttonText }}</button>
      </li>
    </ul>
  </div>
</template>

  <script>
  
  
  import axios from 'axios';
  import { defineProps } from 'vue';
  
  export default {
    props: defineProps({
      selectedTrackId: Number,
    }),
    data() {
      return {
        searchQuery: '',
        searchLanguage: '',
        resultLimit: 10,
        searchResults: [], 
        searchEndpoint: 'invidx',
      };
    },
    methods: {
      async onSearch() {
      const payload = new FormData();
      payload.append('query', this.searchQuery);
      payload.append('k', this.resultLimit.toString());

      const languageMap = {
        es: 'spanish',
        en: 'english',
        de: 'german',
        it: 'italian',
        pt: 'portuguese'
      };

      const languageToSend = languageMap[this.searchLanguage] || 'defaultLanguage';
      payload.append('language', languageToSend);

      try {
        const endpoint = this.searchEndpoint === 'gin' ? 'gin/knn' : 'invidx/knn';
        const response = await axios.post(`http://localhost:8000/${endpoint}`, payload);
        this.searchResults = Object.values(response.data.content);
      } catch (error) {
        console.error('Error en la búsqueda:', error);
      }
    },
      playTrack(track) {
            if (this.isPlaying && this.currentPlayer && this.currentPlayer.src === `http://127.0.0.1:8000/music/${track.track_id}.mp3`) {
                this.currentPlayer.pause();
                this.isPlaying = false;
                this.currentPlayer = null;
                return;
            }

            if (this.isPlaying && this.currentPlayer) {
                this.currentPlayer.pause();
            }

            this.currentPlayer = document.createElement('audio');
            this.currentPlayer.src = `http://127.0.0.1:8000/music/${track.track_id}.mp3`;
            this.currentPlayer.play();
            this.isPlaying = true;

            this.$emit('track-selected', track.track_id);
            
        },
        getLyricsPreview(lyrics) {
      const previewLength = 500; 
      return lyrics.length > previewLength 
        ? lyrics.substring(0, previewLength) + '...'
        : lyrics;
    },
    },
  };
  </script>
  
  
<style scoped>
.search-panel {
  background-color: #000000; 
  color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px; 
  margin: auto; 
}

.search-panel li {
  display: flex;
  align-items: center; 
  justify-content: space-between; 
  padding: 10px;
  background-color: #161b22;
  margin-top: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input[type="text"], select, input[type="number"] {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #161b22;
  color: white;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #1db954; 
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1ed760; 
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 10px;
  background-color: #161b22;
  margin-top: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

li:hover {
  background-color: #1c2025; 
}
.lyrics-preview {
  color: #c0c0c0; 
  margin-top: 5px; 
}

</style>