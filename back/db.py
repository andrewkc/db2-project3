import psycopg2
import pandas as pd
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def insert_music(id, 
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
                 tablename='public.music'):
    query = f"INSERT INTO {tablename} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id, name, artist, lyrics, album_id, album_name, album_release_date, playlist_id, playlist_genre, playlist_subgenre, language, content)
    #print(query, values)
    return query, values


def create_table(tablename):
    conn = psycopg2.connect(
        host=getenv("HOST"),
        port=getenv("PORT"),
        database=getenv("DBNAME"),
        user=getenv("USER"),
        password=getenv("PASSWORD")
    )
    #track_id,track_name,track_artist,lyrics,track_album_id,track_album_name,track_album_release_date,playlist_id,playlist_genre,playlist_subgenre,language,concatenated

    cursor = conn.cursor()
    sentence = f"""CREATE TABLE IF NOT EXISTS {tablename}(
                   id TEXT, 
                   name TEXT,
                   artist TEXT,
                   lyrics TEXT,
                   album_id TEXT, 
                   album_name TEXT,
                   album_release_date TEXT, 
                   playlist_id TEXT, 
                   playlist_genre TEXT,
                   playlist_subgenre TEXT,
                   language TEXT,
                   content TEXT
                );"""
    cursor.execute(sentence)

    conn.commit()
    cursor.close()
    conn.close()

def insert_musics(n, csvfile, tablename = 'public.music'):
    conn = psycopg2.connect(
        host=getenv("HOST"),
        port=getenv("PORT"),
        dbname=getenv("DBNAME"),
        user=getenv("USER"),
        password=getenv("PASSWORD")
    )

    cursor = conn.cursor()
    # N
    df = pd.read_csv(csvfile)
    i = 0
    for _, row in df.iterrows():
        #content = ' '.join(map(lambda x: str(x), list(row.iloc[3:-2]))).replace('\'', '\'\'')
        if i == n: break
        id = row.iloc[0]
        name = str(row.iloc[1]).replace('\'', '')
        artist = str(row.iloc[2]).replace('\'', '')
        lyrics = str(row.iloc[3]).replace('\'', '')
        album_id = str(row.iloc[4]).replace('\'', '')
        album_name = str(row.iloc[5]).replace('\'', '')
        album_release_date = str(row.iloc[6]).replace('\'', '\'\'')
        playlist_id = str(row.iloc[7]).replace('\'', '\'\'')
        playlist_genre = str(row.iloc[8]).replace('\'', '\'\'')
        playlist_subgenre = str(row.iloc[9]).replace('\'', '\'\'')
        language = str(row.iloc[10]).replace('\'', '\'\'')
        #content = ' '.join(map(lambda x: str(x), list(row.iloc[3:-2]))).replace('\'', '\'\'')

        selected_columns = row[['track_name', 'track_artist', 'lyrics', 'track_album_name','playlist_genre', 'playlist_subgenre', 'language']]
        # Realizar la concatenación
        content = ' '.join(map(lambda x: str(x), selected_columns)).replace('\'', '\'\'')
        
        query, values = insert_music(
            id, 
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
            tablename
            )
        cursor.execute(query, values)
        i = i+1
        #print(i)

    conn.commit()
    cursor.close()
    conn.close()

def create_index(lang, tablename='public.music'):
    conn = psycopg2.connect(
        host=getenv("HOST"),
        port=getenv("PORT"),
        dbname=getenv("DBNAME"),
        user=getenv("USER"),
        password=getenv("PASSWORD")
    )

    cursor = conn.cursor()
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')

    cursor.execute(f"ALTER TABLE {tablename} ADD COLUMN indexed tsvector;")
    cursor.execute(f"""UPDATE {tablename} SET indexed = T.indexed FROM (
                    SELECT id, setweight(to_tsvector('{lang}', name), 'A') || setweight(to_tsvector('{lang}', content), 'B') AS indexed FROM {tablename}
                   ) AS T WHERE {tablename}.id = T.id;""")
    cursor.execute(f'CREATE INDEX IF NOT EXISTS content_idx_gin ON {tablename} USING gin (indexed);')

    conn.commit()
    cursor.close()
    conn.close()

N = 100

#create_table('public.music_spanish')
#insert_musics(457, 'idx/spanish.csv', 'public.music_spanish')
#create_index('spanish', 'public.music_spanish')

#create_table('public.music_english')
#insert_musics(4329, 'idx/english.csv', 'public.music_english')
#create_index('english', 'public.music_english')

#create_table('public.music_italian')
#insert_musics(36, 'idx/italian.csv', 'public.music_italian')
#create_index('italian', 'public.music_italian')

###
#create_table('public.music_german')
#insert_musics(71, 'idx/german.csv', 'public.music_german')
#create_index('german', 'public.music_german')
#

create_table('public.music_portuguese')
insert_musics(39, 'idx/portuguese.csv', 'public.music_portuguese')
create_index('portuguese', 'public.music_portuguese')

"""
DROP TABLE public.music_spanish CASCADE;
"""
