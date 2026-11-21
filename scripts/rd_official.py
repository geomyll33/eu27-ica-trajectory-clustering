import pandas as pd, numpy as np
import statsmodels.formula.api as smf
from scipy.stats import binomtest
base='data/external/'
m0=pd.read_csv('results/official_cat_check.csv',index_col=0)
g=pd.read_csv(base+'nama_10r_2gdp_pps_nuts2.csv')
g=g[g.unit=='PPS_HAB_EU27_2020']
run=g[g.TIME_PERIOD.isin([2015,2016,2017])].groupby('geo').OBS_VALUE.agg(['mean','count'])
run=run[run['count']==3]['mean'].rename('gdp')
iu=pd.read_csv(base+'isoc_r_iuse_i_nuts2.csv',low_memory=False)
iu=iu[(iu.indic_is=='I_IUSE')&(iu.unit=='PC_IND')]
def fit(yo,bw,c=75,fuzzy=True):
    y=iu[iu.TIME_PERIOD==yo].set_index('geo').OBS_VALUE.rename('y')
    d=pd.concat([run,y,m0[['cat']]],axis=1).dropna()
    d=d[d.index.str[:2].isin(['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK'])]
    d['x']=d.gdp-c; d['D']=(d.gdp<c).astype(int); d['L']=(d.cat=='LDR').astype(int)
    s=d[d.x.abs()<=bw].copy(); s['w']=1-s.x.abs()/bw
    s['xD']=s.x*s.D
    f1=smf.wls('L ~ D + x + xD',data=s,weights=s.w).fit(cov_type='HC1')
    f2=smf.wls('y ~ D + x + xD',data=s,weights=s.w).fit(cov_type='HC1')
    wald=f2.params['D']/f1.params['D']
    p=binomtest(int(s.D.sum()),len(s),0.5).pvalue
    return len(s),int(s.D.sum()),f1.params['D'],f2.params['D'],wald,f2.bse['D'],f2.pvalues['D'],p
for yo in [2024]:
    for bw in [5,10,15,20]:
        n,nl,fs,rf,w,se,p,pd_=fit(yo,bw)
        print(f'out {yo} bw{bw}: n={n} (LDR-side {nl}) first-stage jump={fs:+.2f} ITT={rf:+.2f} (SE {se:.2f}, p={p:.3f}) Wald={w:+.2f} density p={pd_:.2f}')
for c in [65,85]:
    n,nl,fs,rf,w,se,p,pd_=fit(2024,10,c=c)
    print(f'placebo cut {c} bw10: n={n} ITT={rf:+.2f} (SE {se:.2f}, p={p:.3f})')
