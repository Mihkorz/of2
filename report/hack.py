# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import csv
import random 

from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, ttest_ind, ranksums

from django.views.generic.base import TemplateView

from sklearn.metrics import roc_auc_score
import itertools


class Hackathon(TemplateView):
    """
    Just Testing Playground
    """
    template_name = 'core/test.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super(Hackathon, self).dispatch(request, *args, **kwargs)
        
    
    def get_context_data(self, **kwargs):
        
        context = super(Hackathon, self).get_context_data(**kwargs)
        
        df = pd.read_csv('/home/mikhail/Downloads/Hackaton/STAGES.csv', sep='\t')
        df.columns = ['sample', 'tissue']
        
        
       
        
        ltis = set(df['tissue'])
        
        
        
        
        df_1 = df[(df['tissue'] == 'Stage I')]
        df_2 = df[(df['tissue'] == 'Stage II') ]
        
        col_1_2 = list(df_1['sample'])+list(df_2['sample'])
        
        df_3 = df[(df['tissue'] == 'Stage III')]
        df_4A = df[(df['tissue'] == 'Stage IVA') ]
        df_4B = df[(df['tissue'] == 'Stage IVB') ]
        df_4C = df[(df['tissue'] == 'Stage IVC') ]
        
        col_1_2 = list(df_1['sample'])+list(df_2['sample'])
        col_3_4 = list(df_3['sample'])+list(df_4A['sample'])+list(df_4B['sample'])+list(df_4B['sample'])
        
        all = pd.read_csv('/home/mikhail/Downloads/Hackaton/HNSC_renamed.tab')
        all.fillna(0, inplace=True)
        
        all.set_index('SYMBOL', inplace=True)
        
        all.columns = [x.replace('Tumour_', '') for x in all.columns]
        
        marker_pathways = []
        for index, row in all.iterrows():
            print index
            s_res = row[col_1_2].fillna(0)
            s_nres = row[col_3_4].fillna(0)
                    
            arScore = np.append(np.array(s_res.values, dtype='float64'), np.array(s_nres.values, dtype='float64'))            
            arRes = np.ones(len(col_1_2))
            arNRes = np.zeros(len(col_3_4))
            arTrue = np.append(arRes, arNRes)
                
            AUC = roc_auc_score(arTrue, arScore) #calculate AUC
                    
            if AUC>0.6:
                marker_pathways.append(index)
        
        
        
        raise Exception('stop')
        
        perm = list(itertools.permutations(ltis, 2))
        
        dMarkers = {}
        i = 0
        for spermutation in perm:
            print str(i)+ " of " + str(len(perm))
            i = i+1
                        
            oral = df[df['tissue'].str.contains(spermutation[0])] 
            floor = df[df['tissue'].str.contains(spermutation[1])]

            all = pd.read_csv('/home/mikhail/Downloads/Hackaton/ipanda_limma_modules_alldb_HNSC_renamed.csv', sep='\t')
            
            all.columns = [x.replace('Tumour_', '') for x in all.columns]
           
            
            
            aaaa = list(oral['sample'])
            aaaa = [x for x in aaaa if x in list(all.columns)]
            
            bbb = list(floor['sample'])
            bbb = [x for x in bbb if x in list(all.columns)]
            
            ccc = set(aaaa).intersection(bbb)
            
            all_oral = all[list(aaaa)]
            all_oral['PATHWAY'] = all['PATHWAY']
            all_oral.set_index('PATHWAY', inplace=True)
            
            all_floor = all[list(bbb)]
            all_floor['PATHWAY'] = all['PATHWAY']
            all_floor.set_index('PATHWAY', inplace=True)
            
            all.set_index('PATHWAY', inplace=True)
            
            
            marker_pathways = []
            for index, row in all.iterrows():
                
                s_res = row[all_oral.columns]
                s_nres = row[all_floor.columns]
                    
                arScore = np.append(np.array(s_res.values, dtype='float64'), np.array(s_nres.values, dtype='float64'))            
                arRes = np.ones(len(all_oral.columns))
                arNRes = np.zeros(len(all_floor.columns))
                arTrue = np.append(arRes, arNRes)
                
                AUC = roc_auc_score(arTrue, arScore) #calculate AUC
                    
                if AUC>0.7:
                    marker_pathways.append(index)
            text = spermutation[0]+' vs '+spermutation[1]
            dMarkers[text] = marker_pathways
         
        df = pd.DataFrame.from_dict(dMarkers, orient='index')
        df = df.transpose()
        df.to_csv('/home/mikhail/Downloads/Hackaton/AUC_HPV.csv')    
        raise Exception('stop')
        return context
        
        
        