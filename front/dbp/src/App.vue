<template>
  <div id="app">
    <header>
      <h1>Spotifly</h1>
    </header>

    <div class="panels-container" :class="{ 'selected-track': selectedTrackId }">
      <SearchPanel @track-selected="onTrackSelected" />
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
      selectedTrackId: null, 
      hasPlayedTrack: false,
    };
  },
  methods: {
    onTrackSelected(trackId) {
      this.selectedTrackId = trackId;
      this.hasPlayedTrack = true; 
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
  color: #ffffff;
  background-color: #000000;
}

header {
  background-color: #1db954;
  padding: 20px;
}

h1 {
  font-size: 2em;
}

.panels-container {
  display: flex;
  align-items: start;
  transition: all 0.5s ease; 
}

.search-panel, .recommendation-panel {
  flex: 1;
  transition: width 0.5s ease; 
}

.recommendation-panel {
  transform: translateX(100%);
  width: 0; 
  overflow: hidden;
}


.selected-track .recommendation-panel {
  transform: translateX(0); 
  width: 50%;
}

.selected-track .search-panel {
  width: 50%; 
}
body {
  background-color: #000000; 
  color: #ffffff; 
}

</style>