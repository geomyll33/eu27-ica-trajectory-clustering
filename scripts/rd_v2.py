import pandas as pd, numpy as np
import statsmodels.formula.api as smf
from scipy.stats import binomtest
base='data/external/'
EU=['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK']
g=pd.read_csv(base+'nama_10r_2gdp_pps_nuts2.csv')
g=g[(g.unit=='PPS_HAB_EU27_2020')&(g.geo.str[:2].isin(EU))][['geo','TIME_PERIOD','OBS_VALUE']]
iu=pd.read_csv(base+'isoc_r_iuse_i_nuts2.csv',low_memory=False)
iu=iu[(iu.indic_is=='I_IUSE')&(iu.unit=='PC_IND')&(iu.geo.str[:2].isin(EU))][['geo','TIME_PERIOD','OBS_VALUE']]
def running(years):
    s=g[g.TIME_PERIOD.isin(years)].groupby('geo').OBS_VALUE.agg(['mean','count'])
    return s[s['count']>=2]['mean'].rename('gdp')
def outcome(y): return iu[iu.TIME_PERIOD==y].set_index('geo').OBS_VALUE.rename('iuse')
rules={'2014-20 rule (GDP avg 2007-09)':[2007,2008,2009],'2021-27 rule (GDP avg 2015-17)':[2015,2016,2017]}
outs={'2014-20 rule (GDP avg 2007-09)':[2016,2020],'2021-27 rule (GDP avg 2015-17)':[2020,2024]}
for rn,yrs in rules.items():
    rv=running(yrs)
    for yo in outs[rn]:
        m=pd.concat([rv,outcome(yo)],axis=1).dropna()
        print(f'\n== {rn} -> I_IUSE {yo}: regions={len(m)}')
        for bw in [5,7.5,10,15,20]:
            s=m[(m.gdp-75).abs()<=bw].copy()
            if len(s)<8: print(f' bw {bw}: n={len(s)} too few'); continue
            s['D']=(s.gdp<75).astype(int); s['x']=s.gdp-75; s['w']=1-s.x.abs()/bw
            f=smf.wls('iuse ~ D + x + D:x',data=s,weights=s.w).fit(cov_type='HC1')
            nl=int(s.D.sum()); nh=len(s)-nl
            bt=binomtest(nl,len(s),0.5).pvalue
            print(f' bw {bw}: n={len(s)} (below {nl}, above {nh}) jump={f.params["D"]:+.2f} SE={f.bse["D"]:.2f} p={f.pvalues["D"]:.3f} | density binom p={bt:.2f}')
