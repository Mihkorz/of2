# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.stats
import scipy.interpolate

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
        prob = scipy.stats.distributions.t.cdf(t, df) 
    else:
        prob = 1 - scipy.stats.distributions.t.cdf(t, df)
        
    if t.ndim == 0:
        t = t[()]

    return t, prob

# False discovery rate(FDR) Correction function

def fdr_corr(pval, m = None, pi0 = None):
    """
    Calculate q-values from p-values

    Arguments:
    pval - array of p-values
    m - number of tests to be conducted (default = length of pval array)
    pi0 - tuning parameter; conservative (default) choice - pi0=1;
    setting to pi0=-1 will use estimation procedure from Storey(2003)

    Return:
    array of qvalues
    """

    if not(pval.min() >= 0 and pval.max() <= 1):
        raise Exception, 'p-values must be between 0 and 1'

    if m == None:
        m = float(len(pval))
    else:
        m *= 1.0

    # for small number of comparisons - set pi0 to 1
    if pi0 == None:
        pi0 = 1
    elif pi0 >= 0:
        pi0 = pi0
    else:
        # calculate pi0 for different parameters
        pi0 = []
        param = np.linspace(0,0.85,86)
        counts = np.array([(pval > i).sum() for i in param])

        for l in range(len(param)):
            pi0.append(counts[l]/(m*(1-param[l])))

        pi0 = np.array(pi0)

        # fit natural cubic spline
        spline_param = sp.interpolate.splrep(param, pi0, k = 3)
        pi0 = sp.interpolate.splev(param[-1], spline_param)

        if pi0 > 1:
            pi0 = 1.0

    if not(pi0 >= 0 and pi0 <= 1):
        raise Exception, 'pi0 must be between 0 and 1'

    p_id = sp.argsort(pval)
    pval_ord = pval[p_id]
    qval = pi0 * m/len(pval_ord) * pval_ord
    qval[-1] = min(qval[-1],1.0)

    for i in xrange(len(pval_ord)-2, -1, -1):
        qval[i] = min(pi0*m*pval_ord[i]/(i+1.0), qval[i+1])

    #reorder qvalues
    qv_temp = qval.copy()
    qval = sp.zeros_like(qval)
    qval[p_id] = qv_temp

    #reshape qvalues
    qval = qval.reshape(pval.shape)

    return qval