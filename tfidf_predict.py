from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def predict_games(text, df, stop_words_pt):
    # Criação do Vetor TF-IDF para os jogos
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt)
    tfidf_matrix = vectorizer.fit_transform(df['description'])

    # Função para recomendar jogos com base nos interesses do usuário
    def recomendar_jogos(interesses, top_n=10):
        # Transformar os interesses do usuário em um vetor TF-IDF
        interesses_tfidf = vectorizer.transform([interesses])
        
        # Calcular a similaridade do cosseno entre os interesses do usuário e os jogos
        similaridade = cosine_similarity(interesses_tfidf, tfidf_matrix)
        
        # Ordenar os jogos pela similaridade e selecionar as top_n
        indices_recomendados = similaridade[0].argsort()[-top_n:][::-1]
        
        # Construir a lista de recomendações
        recomendacoes = []
        for idx in indices_recomendados:
            relevancia = similaridade[0][idx]
            if relevancia > 0:  # Verifica se a relevância é maior que zero
                recomendacao = {
                    "game_name": df.iloc[idx]['game_name'],
                    "description": df.iloc[idx]['description'][:200] + "...",  # Mostra os primeiros 200 caracteres
                    "url": df.iloc[idx]['url'].rstrip('\n'),
                    "relevance": relevancia
                }
                recomendacoes.append(recomendacao)
        
        return recomendacoes
    
    # Retornar os jogos recomendados como uma lista de dicionários (JSON)
    return recomendar_jogos(text)
