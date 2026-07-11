import numpy as np
import pandas as pd

def enforce_k_anonymity(df: pd.DataFrame, group_cols, k=100):
    grouped = df.groupby(group_cols).size().reset_index(name="n")
    valid = grouped[grouped["n"] >= k]
    return df.merge(valid[group_cols], on=group_cols, how="inner")

def add_laplace_noise(series: pd.Series, epsilon=5.0):
    scale = 1.0 / max(epsilon, 1e-6)
    noise = np.random.laplace(loc=0.0, scale=scale, size=len(series))
    return series + noise
