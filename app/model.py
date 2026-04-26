import os
import pickle
import joblib
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


lstm_model = load_model(os.path.join(BASE_DIR, "models", "lstm_model.keras"))

with open(os.path.join(BASE_DIR, "models", "tokenizer.pkl"), "rb") as f:
    tokenizer = pickle.load(f)

logreg = joblib.load(os.path.join(BASE_DIR, "models", "logreg.pkl"))
tfidf = joblib.load(os.path.join(BASE_DIR, "models", "tfidf.pkl"))

max_len = 80


def predict_lstm(text: str) -> float:
    seq = tokenizer.texts_to_sequences([text])

    if not seq or not seq[0]:
        return 0.5

    pad = pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')

    prob = lstm_model.predict(pad, verbose=0)[0][0]
    return float(prob)


def predict_logreg(text: str) -> float:
    vec = tfidf.transform([text])
    prob = logreg.predict_proba(vec)[0][1]
    return float(prob)


def predict_combined(text: str) -> float:
    lstm_prob = predict_lstm(text)
    logreg_prob = predict_logreg(text)

    print(f"LSTM: {lstm_prob:.4f} | LOGREG: {logreg_prob:.4f}")


    if lstm_prob > 0.8:
       return lstm_prob
    
    if lstm_prob < 0.2:
       return lstm_prob

    final_prob = (0.7 * lstm_prob) + (0.3 * logreg_prob)
    return final_prob


def get_top_features(text: str):
    vec = tfidf.transform([text])
    feature_names = tfidf.get_feature_names_out()

    scores = vec.toarray()[0]
    sorted_idx = scores.argsort()[::-1]

    top_words = []
    for i in sorted_idx:
        word = feature_names[i]

        # filter weak tokens
        if scores[i] > 0.05 and len(word) > 3 and not word.isdigit():
            top_words.append(word)

        if len(top_words) == 5:
            break

    return top_words

