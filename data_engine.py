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