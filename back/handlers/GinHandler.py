from utils.calculate_exec_time import calculate_exec_time
from os import getenv
import psycopg2

class GinHandler:
    @calculate_exec_time
    def __init__(self, language: str = 'english') -> None:
        self.tablename = f'public.music_{language}'
        self.language = language

    @calculate_exec_time
    def knn_query(self, query: str, k: int, language: str):
        self.tablename = f'public.music_{language}'
        self.language = language
        try:
            conn = psycopg2.connect(
                host=getenv("HOST"),
                port=getenv("PORT"),
                dbname=getenv("DBNAME"),
                user=getenv("USER"),
                password=getenv("PASSWORD")
            )

            cursor = conn.cursor()

            sentence = f"""
                    EXPLAIN ANALYZE
                    SELECT  id, 
                            name,
                            artist, 
                            lyrics, 
                            album_id, 
                            album_name, 
                            album_release_date, 
                            playlist_id,
                            playlist_genre,
                            playlist_subgenre,
                            language,
                            content, 
                            ts_rank(indexed, query) rank
                    FROM {self.tablename}, plainto_tsquery('{self.language}', '{query}') query
                    ORDER BY rank DESC LIMIT {k};
                    """
            cursor.execute(sentence)
            response = cursor.fetchall()
            execution_time = response[-1][0].split('Execution Time: ')[1]
            
            sentence = f"""
                    SELECT id, 
                        name,
                        artist, 
                        lyrics, 
                        album_id, 
                        album_name, 
                        album_release_date, 
                        playlist_id,
                        playlist_genre,
                        playlist_subgenre,
                        language,
                        content, 
                        ts_rank(indexed, query) rank
                    FROM {self.tablename}, plainto_tsquery('{self.language}', '{query}') query
                    ORDER BY rank DESC LIMIT {k};
                    """
            cursor.execute(sentence)
            response = cursor.fetchall()

            conn.close()
            cursor.close()
            return response, execution_time
        except Exception as e:
            return str(e), ''