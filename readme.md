# Transformer/LSTM + XGBoost
Este esquema, el Transformer o el LSTM actua como extractores de caracteristicas
y las ultimas capas ocultas las pasamos al XGBoost para que tome
decision final.

## Estrutura del programa
- data_engine.py ----------> Descarga de yfinance y calculo de FVG/Fibonacci
- featues_deep.py ---------> Definicion y entrenamiento de la LSTM/Transformer
- model_hybrid.py ---------> El XGBoost que une todo y predice la tendencia
- /models         ---------> Carpeta donde se guardan los modelos entrenados

