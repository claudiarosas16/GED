#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 10:53:46 2021

@author: macbookpro
"""
#%%

from nltk.corpus import wordnet as wn
from nltk.wsd import lesk as lesk
import pandas as pd
import numpy as np

#%%
df = pd.read_csv('/Users/macbookpro/OneDrive/PHD/ArtículoJCR/codeIEEE/words.csv')
#%%
df['w1syns'] = [ wn.synsets(word) for word in df.w1 ]
df['w2syns'] = [ wn.synsets(word) for word in df.w2 ]
#%%
for index in range (len(df)):
    wsd1 = "" 
    wsd2 = ""
    final_res = []
    for syn1 in df['w1syns'][index]:
        lch_lst = []
        for syn2 in df['w2syns'][index]:
            if(syn1.pos()==syn2.pos() and (syn1.pos()=='a' or syn1.pos()=='n')):
                    print("---")
                    print(syn1, syn2)
                    lch = syn1.lowest_common_hypernyms(syn2)[0]
                    print('lch: ',lch)
                    if lch: #por si no hay hyperonimos en comun
                        sch = syn1._shortest_hypernym_paths(syn2)
                        best_hyper = {'w1':syn1, 'w2':syn2, 'lch':lch, 'distance': sch[lch]}
                        lch_lst.append(best_hyper)
                    else:
                        continue
            
        if lch_lst: #fuerza a que haya al menos un hypernónimo en común
            print('····lista ',lch_lst)
            mindistance =  min(lch_lst, key=lambda x:x['distance'])
            print('%%%%',mindistance)
            df['lowest_hyper'] = mindistance['lch']
            df['distance_to_hyp'] = mindistance['distance']
            print('++++', mindistance['distance'])
