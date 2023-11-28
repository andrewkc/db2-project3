# PROYECTO FINAL 2 Y 3 BASE DE DATOS II 
## Organización del equipo

|            Participante             |   Rol   |
|:-----------------------------------:|:---------:|
|  Stuart Diego Arteaga Montes        |  Backend  |
|  Johan Fabian Callinapa Chunga      |  Frontend|
|  Dimael Rivas                        | Backend |
|  Kelvin                         | Backend |

## Proyecto parte 2 



## Proyecto parte 3

![API DE SPOTIFY ]()

### Obtención de links de canciones 
```python

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

CLIENT_ID = "3f54e3fbacdc45d3bedabd32238802e8"
CLIENT_SECRET = "e5c73a13fc0c47efb49c7bb054f0383b"

def buscar_cancion(artista, titulo_cancion):
    if not artista:
        print("Error: El nombre del artista está vacío.")
        return

    artista = artista.upper()
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
    query = f"{titulo_cancion} {artista}"  
    resultado_busqueda = sp.search(query, type='track', limit=1)

    if resultado_busqueda['tracks']['items']:
        track_uri = resultado_busqueda['tracks']['items'][0]['external_urls']['spotify']
        return track_uri
    else:
        print("No se encontró la canción en Spotify.")

```
### Descarga de canciones

```python

def descargar(artista,name):
    spotify_track_url = buscar(artista,name)
    comando_spotdl = f"spotdl {spotify_track_url}"
    try:
        output = subprocess.check_output(comando_spotdl, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error al descargar la pista:", e)

```

```python

with open('spotify.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        artista=row['track_name']
        name=row['track_artist']
        idioma_track=row['language']
        if idioma_track in idiomas_mapeados:
            nombre_archivo = os.path.join(idioma_track)
        else:
            nombre_archivo = os.path.join('en')
        os.chdir(nombre_archivo)
        descargar(artista, name)
        os.chdir(directorio_original)
```      
* Se usó la librería spotdl para la desarga de canciones.
* Cabe mencionar que para este proyecto se descargo 5000 canciones entre los 5 idiomas que se usaron en el indice invertido de la parte 2.

### Features Songs
Primero capturamos el audio :
```python
    audio, sr = librosa.load(file_path, mono=True)
```  
Para la **extración de características** se uso la librería **librosa** de python y rescatamos 5 distintos tipos de características y son las siguientes:
#### Contraste Espectral
Mide la diferencia en amplitud entre los picos y valles en el espectro.
```python
    contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
```
#### Croma
Representa la distribución de energía de las notas en el espectro musical. Calcula un croma a partir de una transformada de Fourier de corto tiempo (STFT).
```python
 chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
```
#### Tonnetz
Representa el tono de una señal de audio.
```python
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)
```
#### Tempograma
Representa el tempo estimado de una señal de audio.
```python
    tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)
```
#### Coeficientes MFCC (Mel-Frequency Cepstral Coefficients):
Representan la forma en que el espectro de frecuencia de una señal de audio varía con el tiempo.
```python
    tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)
```
Ademas se uso sus variaciones 
##### Delta MFCC y Delta Delta MFCC
Representan las tasas de cambio de los coeficientes MFCC a lo largo del tiempo.

```python
    delta_mfccs = librosa.feature.delta(mfccs)
    delta2_mfccs = librosa.feature.delta(mfccs, order=2)
```

Y para extraer todas estas características de una canción se uso la siguiente función
```python
def extract_features(file_path, max_length=1000):
    audio, sr = librosa.load(file_path, mono=True)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
    mfcc_features = np.concatenate((mfccs.mean(axis=1), mfccs.std(axis=1)))
    delta_mfccs = librosa.feature.delta(mfccs)
    delta_mfcc_features = np.concatenate((delta_mfccs.mean(axis=1), delta_mfccs.std(axis=1)))
    delta2_mfccs = librosa.feature.delta(mfccs, order=2)
    delta2_mfcc_features = np.concatenate((delta2_mfccs.mean(axis=1), delta2_mfccs.std(axis=1)))
    chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
    contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)
    tempo, tempogram = librosa.beat.beat_track(y=audio, sr=sr)
    all_features = np.concatenate((
        mfcc_features,
        delta_mfcc_features,
        delta2_mfcc_features,
        chroma.mean(axis=1),
        contrast.mean(axis=1),
        tonnetz.mean(axis=1),
        tempogram
    ))
    if len(all_features) < max_length:
        all_features = np.pad(all_features, (0, max_length - len(all_features)))
    else:
        all_features = all_features[:max_length]
    return all_features
```
* Se limitó a  1000 características por canción
Este proceso se realizó para todas las canciones de la siguiente manera
```python
ruta_carpeta = "spotify/CANCIONES"
caracteristicas = []
etiquetas = []
for archivo in archivos_carpeta:
    ruta_archivo = os.path.join(ruta_carpeta, archivo)
    features = extract_features(ruta_archivo)
    caracteristicas.append(features)
    etiquetas.append(archivo)

```
Todos estos feautures se guardaron en un archivo csv 
```python
etiquetas = np.array(etiquetas)
df = pd.DataFrame(data=caracteristicas)
df['etiqueta'] = etiquetas
df.to_csv('spotify/caracteristicas.csv', index=False)
```

### Implementación de busquedas :

Pra poder realizar las búsquedas propuestas se abrió el archivo csv, previamente mencionado y se dividió entre etiquetas y caracteristicas además se normalizaron los datos para un mejor resultado.

```python
data = pd.read_csv('caracteristicas.csv')
X = data.iloc[:, :-1].values
scaler = StandardScaler()
X = scaler.fit_transform(X)
```

#### KNN SECUENCIAL CON HEAP :

```python
def knn_search_priority_queue(query, k):
    similarities = cosine_similarity(query.reshape(1, -1), X).flatten()
    priority_queue = PriorityQueue()
    for i, sim in enumerate(similarities):
        priority_queue.put((-sim, data.iloc[i]['Nombre']))  
    vecinos = []
    for i in range(k):
        sim, neighbor = priority_queue.get()
        vecinos.append((neighbor, -sim))
    return vecinos
```

#### KNN POR RANGO :
```python
def range_search(query_object, radius):
    query_object_2d = query_object.reshape(1, -1)
    within_radius = [(euclidean_distances(query_object_2d, X[i].reshape(1, -1))[0, 0], data.iloc[i]['Nombre']) for i in range(len(X)) if euclidean_distances(query_object_2d, X[i].reshape(1, -1))[0, 0] <= radius]
    return within_radius
```

#### KNN RTREE :
* Para esta parte , el índice RTREE no soporta vectores de mucha dimensionalidad , así que la solucion que planteamos es usar un algoritmo de reducción de dimensionalidad llamado PCA, lo convertimos a una dimensión de 500.

```python
def reducir_dimensionalidad(data):

    new_data = []
    for i in range(len(data)):
        new_data.append(data.iloc[i][:-1])
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(new_data)
    pca = PCA(n_components=500)
    data_pca = pca.fit_transform(data_scaled)
    new_data_pca =[]
    for i in range(len(data_pca)):
        temp=list(data_pca[i])
        temp.append(data.iloc[i][len(data.iloc[0])-1])
        new_data_pca.append(temp)
    return new_data_pca

```
* Implemetación
```python
class RtreeIndex:
    def __init__(self,c):
        p = index.Property()
        p.dimension = 500
        self.collection = c
        self.core = index.Index(properties=p)
        for itr in range(len(self.collection)):
            self.core.insert(id=itr,coordinates=self.collection[itr][:-1])
    def knn_rtree(self,query,k):
        ans = []
        result = self.core.nearest(coordinates=query[:-1],num_results=k)
        for itr in result:
            ans.append((self.collection[itr][len(self.collection[itr])-1],itr))
        return ans
```

#### Búsqueda usando la librería faiss :
![Librería faiss ]()

FAISS es una biblioteca desarrollada por Facebook para la búsqueda eficiente de similitudes en grandes conjuntos de datos. Está especialmente diseñada para trabajar con vectores de alta dimensionalidad, como los que se encuentran comúnmente en problemas de aprendizaje profundo y recuperación de información. A continuación, se presentan algunos aspectos clave de la biblioteca FAISS:
1. Recuperación de Similitud:
FAISS está diseñada para realizar operaciones eficientes de búsqueda de similitudes en grandes conjuntos de datos. Puede encontrar los vecinos más cercanos de un vector dado en un espacio de características de alta dimensión.
2. Índices de Recuperación:
FAISS implementa varios índices de recuperación que son eficientes para diferentes tipos de datos y patrones de acceso. Algunos de estos índices incluyen el índice de búsqueda binaria (Binary Flat), el índice IVF (Inverted File), y otros índices específicos para datos de alta dimensión.
3. Soporte para GPU:
Una de las características distintivas de FAISS es su capacidad para aprovechar GPU para acelerar la búsqueda de similitudes. Esto es crucial para manejar grandes conjuntos de datos y dimensiones elevadas de manera eficiente.
4. Algoritmos Optimizados:
FAISS implementa algoritmos optimizados para la búsqueda eficiente en espacios de alta dimensión. Esto incluye métodos para reducir el costo computacional de operaciones como la distancia euclidiana en dimensiones elevadas.

Indexación :
```python
import  faiss
X = data.iloc[:, :-1].values.astype('float32')  
scaler = StandardScaler()
X = scaler.fit_transform(X)
dimension = X.shape[1]  
nlist = 10
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)
index.train(X)
index.add(X)
```
Búsqueda:
```python
def knn_faiss(query_object, k):
    query_object = query_object.astype('float32')
    distances, indices = index.search(np.expand_dims(query_object, axis=0), k)
    return [(distances[0][i], data.iloc[indices[0][i]]['Nombre']) for i in range(k)]
```
* Para esta implementación se uso el índice **IndexIVFFlat**, aquí hay una explicación de cómo funciona el índice IndexIVFFlat:
1. Creación del Cuantizador (Quantizer):
Primero, se debe crear un cuantizador, que es responsable de asignar un vector de datos a uno de los centroides (grupos) en el índice plano. En el ejemplo proporcionado, se utiliza IndexFlatL2 como cuantizador, lo que significa que los vectores se asignarán a los centroides basándose en la distancia euclidiana.
2. Creación del Índice IVF:
Luego, se crea el índice IVF (IndexIVFFlat) utilizando el cuantizador. Este índice IVF divide el espacio de búsqueda en grupos (o celdas) utilizando el cuantizador. Cada grupo contiene un conjunto de vectores.
3. Parámetros Importantes:
quantizer: El cuantizador que se utilizará para asignar vectores a grupos.
dimension: La dimensionalidad de los vectores de características.
nlist: El número de centroides (grupos) en el índice IVF.
metric: La métrica de distancia utilizada para medir la similitud entre vectores. En el ejemplo, se utiliza la distancia euclidiana (faiss.METRIC_L2).
4. Entrenamiento del Índice:
Antes de utilizar el índice para búsquedas, se puede entrenar. El entrenamiento ayuda al índice a aprender estructuras internas que facilitan las futuras búsquedas de vecinos más cercanos.
5. Añadir Datos al Índice:
Después del entrenamiento (si es necesario), se añaden los datos al índice utilizando el método add. Esto permite que el índice construya las estructuras internas necesarias para facilitar la búsqueda eficiente.

### Experimentación  












