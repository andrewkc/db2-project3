<template>
  <div id="app">
    <header>
      <h1>Spotifly</h1>
    </header>

    <!-- Contenedor Flex para los paneles -->
    <div class="panels-container" :class="{ 'selected-track': selectedTrackId }">
      <!-- Panel de Búsqueda -->
      <SearchPanel @track-selected="onTrackSelected" />

      <!-- Panel de Recomendaciones -->
      <RecommendationPanel :selectedTrackId="selectedTrackId" :isTrackPlayed="hasPlayedTrack" />
    </div>
  </div>
</template>

<script>
import SearchPanel from './components/SearchPanel.vue';
import RecommendationPanel from './components/RecommendationPanel.vue';

export default {
  components: {
    SearchPanel,
    RecommendationPanel,
  },
  data() {
    return {
      selectedTrackId: null, // ID de la pista seleccionada
      hasPlayedTrack: false, // Añade esta propiedad
    };
  },
  methods: {
    onTrackSelected(trackId) {
      // Manejar la selección de la pista aquí
      this.selectedTrackId = trackId;
      this.hasPlayedTrack = true; // Actualiza esto cuando se selecciona una canción
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #ffffff; /* Color del texto principal */
  background-color: #000000; /* Fondo negro */
}

header {
  background-color: #1db954; /* Color de fondo del encabezado */
  padding: 20px;
}

h1 {
  font-size: 2em;
}

.panels-container {
  display: flex;
  align-items: start;
  transition: all 0.5s ease; /* Transición suave para los cambios */
}

.search-panel, .recommendation-panel {
  flex: 1; /* Ambos paneles tomarán igual espacio */
  transition: width 0.5s ease; /* Transición suave para el ancho */
}

.recommendation-panel {
  transform: translateX(100%); /* Inicialmente oculto a la derecha */
  width: 0; /* Inicialmente sin ancho */
  overflow: hidden; /* Oculta el contenido que se desborde */
}

/* Estilos para cuando se selecciona una pista */
.selected-track .recommendation-panel {
  transform: translateX(0); /* Mover el panel a su posición original */
  width: 50%; /* Establecer el ancho deseado */
}

.selected-track .search-panel {
  width: 50%; /* Ajustar el ancho del panel de búsqueda */
}
body {
  background-color: #000000; /* Fondo negro para todo el cuerpo de la página */
  color: #ffffff; /* Texto en blanco */
}

</style>