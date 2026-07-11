import numpy as np
from sklearn.metrics import roc_auc_score

def ks_stat(y_true, y_score):
    pos = y_score[y_true == 1]; neg = y_score[y_true == 0]
    def cdf(arr, grid):
        return np.searchsorted(np.sort(arr), grid, side='right') / len(arr)
    grid = np.sort(y_score)
    return np.max(np.abs(cdf(pos, grid) - cdf(neg, grid)))

def safe_roc_auc(y_true, y_score):
    try:
        return roc_auc_score(y_true, y_score)
    except Exception:
        return float("nan")
