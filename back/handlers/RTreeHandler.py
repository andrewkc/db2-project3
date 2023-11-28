from utils.calculate_exec_time import calculate_exec_time
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import List, Tuple
from rtree import index
import pandas as pd
import numpy as np


class RTreeHandler:
    @calculate_exec_time
    def __init__(self, index_file='music/song_features.csv') -> None: 
        p = index.Property()
        p.dimension = 100
        p.buffering_capacity = 3
        self.data = pd.read_csv(index_file)
        new_data = self.reduce_dimensionality(self.data)
        self.collection = new_data
        self.core = index.Index(properties = p)
        for itr in range(len(self.collection)):
            self.core.insert(id=itr,coordinates=self.collection[itr][:-1])

    
    @calculate_exec_time
    def reduce_dimensionality(self, data: pd.DataFrame) -> List[List[float]]:
        new_data = []
        for i in range(len(data)):
            new_data.append(data.iloc[i][:-1])
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(new_data)
        pca = PCA(n_components=100) #100
        data_pca = pca.fit_transform(data_scaled)
        new_data_pca =[]
        for i in range(len(data_pca)):
            temp = list(data_pca[i])
            temp.append(data.iat[i, -1])  # Cambio aquí
            new_data_pca.append(temp)
        return new_data_pca


    @calculate_exec_time
    def knn_query(self, filename: str, k: int) -> List[List[str]]:
        # Suponiendo que query es el vector de dimensiones de la cancion
        num = self.data.loc[self.data['etiqueta'] == filename].index[0]
        query = self.collection[num]
        ans = []
        result = self.core.nearest(coordinates=query[:-1],num_results=k)
        for itr in result:
            ans.append(self.collection[itr][len(self.collection[itr])-1])
        return ans

