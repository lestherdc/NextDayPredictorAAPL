from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_feature_extractor(input_shape):
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32, return_sequences=False), # Este nivel genera el 'vector de estado'
        Dense(16, activation='relu')
    ])
    return model

# El output de 16 neuronas será la entrada "inteligente" para XGBoost