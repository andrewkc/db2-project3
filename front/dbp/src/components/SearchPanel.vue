<template>
    <div class="search-panel">
      <form @submit.prevent="onSearch">
        <!-- Campo de búsqueda -->
        <input type="text" v-model="searchQuery" placeholder="Buscar canciones" />
  
        <!-- Opciones de búsqueda -->
        <select v-model="searchLanguage">
          <option value="">Cualquier idioma</option>
  <option value="es">Español</option>
  <option value="en">Inglés</option>
  <option value="de">Alemán</option> <!-- Alemán agregado -->
  <option value="it">Italiano</option> <!-- Italiano agregado -->
  <option value="pt">Portugués</option> <!-- Portugués agregado -->

          
          <!-- Agrega más idiomas según sea necesario -->
        </select>
  
        <input type="number" v-model.number="resultLimit" placeholder="Número de resultados" />
  
        <!-- Botón de búsqueda -->
        <button type="submit">Buscar</button>
      </form>
  
      <!-- Lista de resultados -->
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
        searchResults: [], // Almacenará los resultados de la búsqueda
      };
    },
    methods: {
      async onSearch() {
        const payload = new FormData();
        payload.append('query', this.searchQuery);
        payload.append('k', this.resultLimit.toString());
  
        // Cambia el valor a 'spanish' si se selecciona 'Español'
        const languageMap = {
  es: 'spanish',
  en: 'english',
  de: 'german',
  it: 'italian',
  pt: 'portuguese'
};

const languageToSend = languageMap[this.searchLanguage] || 'defaultLanguage';
payload.append('language', languageToSend);
        payload.append('language', languageToSend);
  
        try {
          const response = await axios.post('http://localhost:8000/invidx/knn', payload);
          this.searchResults = Object.values(response.data.content);
        } catch (error) {
          console.error('Error en la búsqueda:', error);
          // Manejar el error adecuadamente
        }
      },
      playTrack(track) {
            // Si ya hay un reproductor y está reproduciendo la misma pista, detener la reproducción
            if (this.isPlaying && this.currentPlayer && this.currentPlayer.src === `http://127.0.0.1:8000/music/${track.track_id}.mp3`) {
                this.currentPlayer.pause();
                this.isPlaying = false;
                this.currentPlayer = null;
                return;
            }

            // Si se está reproduciendo otra pista, detenerla
            if (this.isPlaying && this.currentPlayer) {
                this.currentPlayer.pause();
            }

            // Crear un nuevo reproductor para la pista actual
            this.currentPlayer = document.createElement('audio');
            this.currentPlayer.src = `http://127.0.0.1:8000/music/${track.track_id}.mp3`;
            this.currentPlayer.play();
            this.isPlaying = true;

            // Emitir evento con el ID de la pista seleccionada
            this.$emit('track-selected', track.track_id);
            
        },
        getLyricsPreview(lyrics) {
      const previewLength = 500; // Ajusta esto según sea necesario
      return lyrics.length > previewLength 
        ? lyrics.substring(0, previewLength) + '...'
        : lyrics;
    },

    //   async playTrack(track) {
    //     // Lógica para reproducir la pista seleccionada
    //     console.log('Reproducir pista con ID:', track.track_id);
    //     // Hacer una llamada al endpoint de KNN secuencial con el mismo valor de 'k'
    //     try {
    //         const trackIdWithExtension = `${track.track_id}.mp3`;
    //         const trackIdAsString = trackIdWithExtension.toString();
    //         console.log('Reproducir pista con ID:', trackIdAsString);
    //         const payload = new FormData();
    //         payload.append('track_id', trackIdAsString);x
    //         payload.append('k', this.resultLimit.toString());

    //       const knnResponse = await axios.post('http://localhost:8000/sequential/knn', payload);
    //       const recommendations = knnResponse.data.content;
    //       // Emitir un evento para notificar al componente padre (App.vue) sobre la selección de la pista
    //       this.$emit('track-selected', track.track_id);
    //       // Enviar las recomendaciones al componente RecommendationPanel.vue
    //       this.$root.$emit('recommendations-updated', recommendations);
    //     } catch (error) {
    //       console.error('Error al obtener recomendaciones:', error);
    //       // Manejar el error adecuadamente
    //     }
    //   },
    },
  };
  </script>
  
  
<style scoped>
.search-panel {
  background-color: #000000; /* Color de fondo negro */
  color: #ffffff; /* Texto en blanco */
  padding: 20px;
  border-radius: 8px;
  max-width: 600px; /* Ancho máximo */
  margin: auto; /* Centrar el panel */
}

.search-panel li {
  display: flex;
  align-items: center; /* Asegura que los elementos estén alineados verticalmente */
  justify-content: space-between; /* Espacio entre los elementos, empujando el botón a la derecha */
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
  background-color: #161b22; /* Color de fondo para los campos de entrada */
  color: white;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #1db954; /* Color verde de Spotify para el botón */
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1ed760; /* Un tono más claro al pasar el mouse */
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
  background-color: #1c2025; /* Un tono más claro al pasar el mouse */
}
.lyrics-preview {
  color: #c0c0c0; /* Color gris para las letras */
  margin-top: 5px; /* Espacio entre el nombre de la pista y la letra */
}

</style>