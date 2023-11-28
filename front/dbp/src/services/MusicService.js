import axios from 'axios';

// Reemplaza con la URL donde se ejecuta tu servidor Uvicorn
const API_BASE_URL = 'http://localhost:8000'; 

const MusicService = {
  // Función para buscar canciones
  searchSongs(query, k, language) {
    return axios.post(`${API_BASE_URL}/invidx/knn`, { query, k, language });
  },

  // Función para obtener una canción específica
  getSong(trackId) {
    return axios.get(`${API_BASE_URL}/music/${trackId}`);
  },

  // Agrega aquí más funciones según sean necesarias para tu proyecto
};

export default MusicService;
