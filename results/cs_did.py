import pandas as pd, numpy as np
df=pd.read_csv('results/did_panel.csv')
p=df.pivot(index='year',columns='country',values='lny')
coh=df.groupby('country').cohort.first()
ctrl=coh[coh==0].index.tolist()
rows=[]
# Callaway-Sant'Anna style: for each cohort g and year t, ATT(g,t)=mean change from g-1 (treated) minus same for never-treated
for g in [2004,2007,2013]:
    trt=coh[coh==g].index.tolist()
    for t in range(1995,2024):
        if t==g-1 or g-1<1995: continue
        base=g-1
        d_t=p.loc[t,trt].mean()-p.loc[base,trt].mean()
        d_c=p.loc[t,ctrl].mean()-p.loc[base,ctrl].mean()
        rows.append((g,t,t-g,d_t-d_c))
att=pd.DataFrame(rows,columns=['cohort','year','e','att'])
# pre-trend placebo: base at g-1 vs earlier years (event times <-1)
pre=att[att.e<0]; post=att[att.e>=0]
print('pre-period ATT by event time (mean over cohorts):')
print(att[att.e<0].groupby('e').att.mean().round(3).to_string())
print('post ATT by event time (mean over cohorts):')
print(att[att.e>=0].groupby('e').att.mean().round(3).head(12).to_string())
print('overall post mean (cohort-size-free average over post cells):', round(post.att.mean(),3))
