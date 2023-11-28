<template>
  <div class="recommendation-panel" v-if="isTrackPlayed">
    <!-- Menú desplegable y campo de entrada solo si se ha reproducido una canción -->
    <div v-if="isTrackPlayed">
      <select v-model="selectedEndpoint">
        <option value="sequential/knn">Sequential KNN</option>
        <option value="sequential/range">Sequential Range</option>
        <option value="rtree/knn">RTree KNN</option>
        <option value="highd/knn">HighD KNN</option>
      </select>
      <input type="number" v-model.number="parameter" :placeholder="selectedEndpoint.includes('range') ? 'Ingrese r' : 'Ingrese k'" />
      <button @click="fetchRecommendations">Buscar</button>
    </div>

    <h2>Te puede gustar</h2>
    <ul>
      <li v-for="(recommendation, index) in recommendations" :key="index">
        {{ getSongName(recommendation.trackId) }} - {{ recommendation.artist }}
        <button @click="playTrack(recommendation)">{{ isPlaying && currentPlayer && currentPlayer.src === `http://127.0.0.1:8000/music/${recommendation.trackId}.mp3` ? 'Detener' : 'Reproducir' }}</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  
  watch: {
    // isTrackPlayed(newVal) {
    //   console.log('isTrackPlayed changed:', newVal);
    // },
    
    'recommendations.length'(newLength) {
      console.log('recommendations length changed:', newLength);
    },
    
    selectedTrackId(newVal, oldVal) {
      if (newVal && this.isTrackPlayed && newVal !== oldVal) {
        this.parameter = this.parameter || 10; // valor por defecto para 'k'
        this.fetchRecommendations();
      }
    },
    isTrackPlayed(newVal) {
      console.log('isTrackPlayed changed:', newVal);
      if (newVal && this.selectedTrackId) {
        this.fetchRecommendations();
      }
    },

  },
  
  props: {
    selectedTrackId: {
      type: String,
      default: null,
    },
    isTrackPlayed: {
      type: Boolean,
      default: false,
    },
    csvFilePath: {
      type: String,
      default: 'D:/final_spotify.csv', // Ruta al archivo CSV
    }
    
  },
  data() {
  return {
    recommendations: [],
    selectedEndpoint: 'sequential/knn',
    parameter: 3,
    songNamesMap: {},
    isPlaying: false, // Agrega esta propiedad
    currentPlayer: null, // Para almacenar el reproductor de audio actual
  };
},

  methods: {
    
    
    async fetchRecommendations() {
  if (!this.selectedTrackId || this.parameter == null) {
    return;
  }

  const payload = new FormData();
  payload.append('track_id', `${this.selectedTrackId}.mp3`);
  payload.append(this.selectedEndpoint.includes('range') ? 'r' : 'k', this.parameter.toString());
  console.log('PARAMS');
  console.log(`${this.selectedTrackId}.mp3`);
  console.log(this.parameter.toString())

  
  try {
    const response = await axios.post(`http://localhost:8000/${this.selectedEndpoint}`, payload);
    
    let trackIds = [];
    if (this.selectedEndpoint === 'sequential/knn') {
      // Caso para knn secuencial
      trackIds = response.data.content.map(item => item[0]);
    } else if (this.selectedEndpoint === 'sequential/range' || this.selectedEndpoint === 'highd/knn') {
      // Caso para knn rango y high d
      trackIds = response.data.content.map(item => item[1]);
    } else if (this.selectedEndpoint === 'rtree/knn') {
      // Caso para rtree
      trackIds = response.data.content;
    }

    // Remover la extensión .mp3 y actualizar las recomendaciones
    this.recommendations = trackIds.map(trackIdWithExtension => {
      return {
        trackId: trackIdWithExtension.replace('.mp3', ''),
        // Agrega aquí lógica adicional si necesitas más datos de cada recomendación
      };
    });

  } catch (error) {
    console.error('Error al obtener recomendaciones:', error);
  }
},


    
playTrack(track) {
  if (this.isPlaying && this.currentPlayer && this.currentPlayer.src === `http://127.0.0.1:8000/music/${track.trackId}.mp3`) {
    // Detener la reproducción si la misma canción ya está sonando
    this.currentPlayer.pause();
    this.isPlaying = false;
    this.currentPlayer = null;
  } else {
    if (this.isPlaying && this.currentPlayer) {
      // Si se está reproduciendo otra pista, detenerla
      this.currentPlayer.pause();
    }

    // Crear un nuevo reproductor para la pista actual
    this.currentPlayer = new Audio(`http://127.0.0.1:8000/music/${track.trackId}.mp3`);
    this.currentPlayer.play();
    this.isPlaying = true;
  }
},

        
        getSongName(trackId) {
      // Retorna el nombre de la canción basado en el trackId
      return this.songNamesMap[trackId] || 'Nombre Desconocido';
    },

    async loadCsvData() {
  try {
    // URL del archivo CSV
    const csvUrl = 'https://raw.githubusercontent.com/johancalli/test/main/final_spotify.csv';
    
    // Realizar la petición GET para obtener los datos del CSV
    const response = await axios.get(csvUrl);

    // Los datos del CSV se encuentran en response.data
    const csvData = response.data;

    // Procesar el CSV y actualizar songNamesMap
    csvData.split('\n').forEach((line, index) => {
      // Ignorar la cabecera
      if (index === 0) return;

      const columns = line.split(',');
      const trackId = columns[0];
      const trackName = columns[1];
      const trackArtist = columns[2];

      // Puedes ajustar esta parte según cómo quieras mostrar los nombres
      this.songNamesMap[trackId] = `${trackName} - ${trackArtist}`;
    });
  } catch (error) {
    console.error('Error al cargar datos del CSV:', error);
  }
},





        
        
  },
  
  mounted() {
    this.loadCsvData();
  }
};
</script>
<style scoped>
/* Estilos para el panel de recomendaciones ajustados para coincidir con el panel de búsqueda */
.recommendation-panel {
  background-color: #000000; /* Color de fondo negro */
  color: #ffffff; /* Texto en blanco */
  padding: 20px;
  border-radius: 8px;
  max-width: 600px; /* Ancho máximo ajustado */
  margin-top: 20px; /* Margen solo en la parte superior */
  margin-left: auto; /* Centrado horizontal */
  margin-right: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.recommendation-panel select,
.recommendation-panel input[type="number"] {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #161b22; /* Color de fondo para los campos de entrada */
  color: white;
}

.recommendation-panel button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #1db954; /* Color verde de Spotify para el botón */
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.recommendation-panel button:hover {
  background-color: #1ed760; /* Un tono más claro al pasar el mouse */
}

.recommendation-panel h2 {
  margin-top: 0;
  text-align: center;
  font-size: 1.5em;
}

.recommendation-panel ul {
  list-style: none;
  padding: 0;
}

.recommendation-panel li {
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

.recommendation-panel li:hover {
  background-color: #1c2025; /* Un tono más claro al pasar el mouse */
}

.recommendation-panel audio {
  margin-left: 10px;
}
</style>
