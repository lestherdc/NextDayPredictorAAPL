import numpy as np
import yfinance as download


def get_data(ticker):
    df = download.download(ticker, start="2023-01-01")

    # Retornos logarítmicos (estacionariedad)
    df['returns'] = np.log(df['Close'] / df['Close'].shift(1))

    # Feature de FVG (Simplificada: Gap entre High[i-2] y Low[i])
    df['fvg_bull'] = (df['Low'] > df['High'].shift(2)).astype(int)

    # Fibonacci 0.618 (basado en el rango de los últimos 20 días)
    rolling_high = df['High'].rolling(window=20).max()
    rolling_low = df['Low'].rolling(window=20).min()
    df['fib_618'] = rolling_low + (rolling_high - rolling_low) * 0.618

    return df.dropna()

data_aapl = get_data("AAPL")


def detect_fvg(df):
    """
    Detecta Gaps de Valor Justo (FVG) Alcistas y Bajistas.
    Retorna la distancia del precio actual al FVG más cercano.
    """
    df['fvg_top'] = np.nan
    df['fvg_bottom'] = np.nan

    for i in range(2, len(df)):
        # FVG Alcista (Bullish): Low[i] > High[i-2]
        if df['Low'].iloc[i] > df['High'].iloc[i - 2]:
            df.at[df.index[i], 'fvg_bottom'] = df['High'].iloc[i - 2]
            df.at[df.index[i], 'fvg_top'] = df['Low'].iloc[i]

        # FVG Bajista (Bearish): High[i] < Low[i-2]
        elif df['High'].iloc[i] < df['Low'].iloc[i - 2]:
            df.at[df.index[i], 'fvg_top'] = df['Low'].iloc[i - 2]
            df.at[df.index[i], 'fvg_bottom'] = df['High'].iloc[i]

    # Llenamos hacia adelante para que el modelo "recuerde" el último FVG abierto
    df[['fvg_top', 'fvg_bottom']] = df[['fvg_top', 'fvg_bottom']].ffill()
    df['dist_to_fvg'] = (df['fvg_top'] + df['fvg_bottom']) / 2 - df['Close']
    return df