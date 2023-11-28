from handlers.handlers_dict import handlers
from fastapi import Form

async def get_knn_gin(query: str = Form(...), k: str = Form(...), language: str = Form(...)) -> dict:
    try:
        query: str = query
        k = int(k) if k != '' else 5
        language: str = language

        gin = handlers['gin']
        res, execution_time = gin.knn_query(query, k, language)
        #print(res)
        responses = {}
        for r in res:  
            #print(len(r))
            response = {
                'track_id': r[0], 
                'track_name': r[1],
                'track_artist': r[2],
                'lyrics': r[3],  
                'album_id': r[4],
                'album_name': r[5],
                'album_release_date': r[6], 
                'playlist_id': r[7], 
                'playlist_genre': r[8],
                'playlist_subgenre': r[9],
                'language': r[10],
                'concatenated': r[11],
                'scores': r[12]
            }
            responses[r[0]] = response
            #print(response)

        #print(execution_time)
        #print("-----------------------------------------")
          
        return {'content': responses, 'execution_time': execution_time, 'status_code':200}
    except Exception as e:
        return {
            'content': {}, 
            'status_code': 200
        }
