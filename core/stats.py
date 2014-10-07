# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import distributions

def pseudo_ttest_1samp(a, popmean, axis=0):
   
    
    a, axis = _chk_asarray(a, axis)
    n = a.shape[axis]
    df = n - 1

    d =  popmean - np.mean(a, axis)
    v = np.var(a, axis, ddof=1)
    denom = np.sqrt(v / (float(n)/(float(n)+1) ))

    t = np.divide(d, denom)
    t, prob = _ttest_finish(df, t)

    return t, prob


def _chk_asarray(a, axis):
    if axis is None:
        a = np.ravel(a)
        outaxis = 0
    else:
        a = np.asarray(a)
        outaxis = axis
    return a, outaxis

def _ttest_finish(df,t):
    if t<0:
        prob = distributions.t.cdf(t, df) 
    else:
        prob = 1 - distributions.t.cdf(t, df)
        
    if t.ndim == 0:
        t = t[()]

    return t, prob