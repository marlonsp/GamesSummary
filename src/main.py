from fastapi import FastAPI, Query
from tfidf_predict import predict_games
import nltk
from nltk.corpus import stopwords
import pandas as pd
import uvicorn

# Baixar stopwords em português
nltk.download('stopwords')
stop_words_pt = stopwords.words('portuguese')

# Carregar o CSV com os jogos
csv_file = "../data/games_data.csv"
df_raw = pd.read_csv(csv_file)
df = df_raw.dropna()

app = FastAPI()

@app.get("/query/")
async def get_recommendations(text: str = Query(..., min_length=1)):
    try:
        # Chamar a função de previsão
        recommendations = predict_games(text, df, stop_words_pt)
        return {"results": recommendations, "message": "OK"}
    except Exception as e:
        return {"message": str(e)}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9191)