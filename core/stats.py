# -*- coding: utf-8 -*-
import pandas as pd
import pandas.rpy.common as com
from rpy2.robjects.packages import importr
from collections import defaultdict
import numpy as np
import scipy as sp
import scipy.stats
import scipy.interpolate

def pseudo_ttest_1samp(a, popmean, axis=0):
    """
    Corrected ttest_1samp by InSilico
    """
    
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

def quantile_normalization(df):
    """
    Performs quantile normalization. by InSilico
    
    input and output: Pandas DataFrame
    IMPORTANT: doesn't store column names
    """
        
    my_data = df.as_matrix() #convert DataFrame to numpy
       
    AA = np.zeros_like(my_data)

    I = np.argsort(my_data,axis=0)

    AA[I,np.arange(my_data.shape[1])] = np.mean(my_data[I,np.arange(my_data.shape[1])],axis=1)[:,np.newaxis]
        
    my_data = AA 
    new_col = np.array(df.index.values, dtype='|S15')[...,None] # None keeps (n, 1) shape
    new_col.shape
        
    all_data = np.append( new_col,my_data, 1)
    all_data.shape
        
    result_df = pd.DataFrame(all_data)
    result_df = result_df.convert_objects(convert_numeric=True)
        
    return result_df

def XPN_normalisation(df_pl1, df_pl2, p1_names=0, p2_names=0,
                                 iterations=30, K=10, L=4, log_scale=False):
    """ Performs XPN normalisation """
    
    if log_scale:
            df_pl1 = np.log(df_pl1).fillna(0)
            df_pl2 = np.log(df_pl2).fillna(0)
        
    len_col_pl1 = len(df_pl1.columns)
    len_col_pl2 = len(df_pl2.columns)
        
    if abs(np.log2(float(len_col_pl1)/len_col_pl2))>2:
        raise Exception(u"Error! Datasets can't be compared.\
                                          Number of samples in one dataset is at least 4 \
                                          times larger than in the other."+
                                          str(len_col_pl1)+" and "+str(len_col_pl2))
        
    diff = abs(len_col_pl1-len_col_pl2)
        
    np.random.seed(5) #fix random number generator for the sake of reproducibility
    if len_col_pl1>len_col_pl2:
        if abs(np.log2(float(len_col_pl1)/len_col_pl2)<1):
            choice = np.random.choice(len_col_pl2, diff, replace=False) #create random sample from df columns
        else:
            choice = np.random.choice(len_col_pl2, diff, replace=True)               
            
        adjusted_df = df_pl2[choice]
        adjusted_df = rename_df_columns(adjusted_df)       
        df_pl2 = df_pl2.join(adjusted_df)
    else:
        if abs(np.log2(float(len_col_pl1)/len_col_pl2)<1):
            choice = np.random.choice(len_col_pl1, diff, replace=False)
        else:
            choice = np.random.choice(len_col_pl1, diff, replace=True)
        adjusted_df = df_pl1[choice]            
        adjusted_df = rename_df_columns(adjusted_df)            
        df_pl1 = df_pl1.join(adjusted_df)
            
    Rdf_pl1 = com.convert_to_r_dataframe(df_pl1)
    Rdf_pl2 = com.convert_to_r_dataframe(df_pl2)
        
    try:
        conor = importr("CONOR")
        R_output = conor.xpn(Rdf_pl1, Rdf_pl2, p1_names=p1_names, p2_names=p2_names,
                                 iterations=iterations, K=K, L=L )
    except:
        raise
    py_output = com.convert_robj(R_output)

    df_out_x = pd.DataFrame(py_output['x'])
    df_out_y = pd.DataFrame(py_output['y'])        
    df_out_x.index.name = df_out_y.index.name = 'SYMBOL'
        
    df_output_all = df_out_x.join(df_out_y, lsuffix='_x', rsuffix='_y')
    #raise Exception("XPN Exception")
    return df_output_all
    
def rename_df_columns(df):
        
        name_counts = defaultdict(int)
        new_col_names = []
            
        for name in df.columns:
            new_count = name_counts[name] + 1
            new_col_names.append("{}.{}".format(name, new_count))
            name_counts[name] = new_count 
                
            
        df.columns = new_col_names
        return df    
    
    
    
    
    