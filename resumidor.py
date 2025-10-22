from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def preview_summary(transcribe, segments, top_k=5):
    """
    Retorna uma frase curta representando cada segmento,
    baseada nas palavras mais relevantes do trecho.
    """
    seg_texts = []
    for start, end in segments:
        text = " ".join(d["text"] for d in transcribe if start <= d["start"] < end)
        seg_texts.append(text)

    # TF-IDF para extrair palavras-chave
    vectorizer = TfidfVectorizer(max_features=top_k, stop_words="portuguese")
    tfidf_matrix = vectorizer.fit_transform(seg_texts)
    feature_names = np.array(vectorizer.get_feature_names_out())

    previews = []
    for i in range(len(seg_texts)):
        # pega palavras mais relevantes
        sorted_idx = np.argsort(tfidf_matrix[i].toarray()).flatten()[::-1]
        keywords = feature_names[sorted_idx[:top_k]]
        previews.append({
            "start": segments[i][0],
            "end": segments[i][1],
            "preview": ", ".join(keywords)
        })
    return previews
