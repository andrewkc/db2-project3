from handlers.handlers_dict import handlers
from fastapi import Form

async def get_knn_invidx(query: str = Form(...), k: str = Form(...), language: str = Form(...)) -> dict:
    try:
        query: str = query
        k = int(k) if k != '' else 5
        language: str = language

        indivx = handlers['invidx']
        results, scores, execution_time = indivx.knn_query(query, k, language)
        if results.shape[0] == 0: 
            res = {}
        else:
            df = results.copy()  
            df['scores'] = scores
            res = df.to_dict(orient='index')

            ress = {}
            for k, v in res.items():
                ress[v['track_id']] = v          
                
        return {
            'content': ress, 
            'execution_time': f"{execution_time} ms", 
            'status_code': 200
        }
    except Exception as e:
        return {
            'content': {}, 
            'status_code': 200
        }
