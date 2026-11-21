import pandas as pd, numpy as np
df=pd.read_csv('results/did_panel.csv')
p=df.pivot(index='year',columns='country',values='lny')
coh=df.groupby('country').cohort.first()
ctrl=coh[coh==0].index.tolist(); trt_all=coh[coh>0].index.tolist()
def att_avgs(p,trt_c,ctrl_c,cm):
    pre=[];post=[]
    for g in [2004,2007,2013]:
        trt=[c for c in trt_c if cm[c]==g]
        if not trt: continue
        for t in range(1995,2024):
            if t==g-1: continue
            d=(p.loc[t,trt].mean()-p.loc[g-1,trt].mean())-(p.loc[t,ctrl_c].mean()-p.loc[g-1,ctrl_c].mean())
            (pre if t<g else post).append(d)
    return np.mean(pre), np.mean(post)
est=att_avgs(p,trt_all,ctrl,coh.to_dict())
rng=np.random.default_rng(1); bs=[]
for _ in range(1000):
    tb=list(rng.choice(trt_all,len(trt_all),replace=True)); cb=list(rng.choice(ctrl,len(ctrl),replace=True))
    cols=tb+cb
    q=p[cols].copy(); q.columns=[f'{c}_{i}' for i,c in enumerate(cols)]
    cm={f'{c}_{i}':coh[c] for i,c in enumerate(cols)}
    bs.append(att_avgs(q,list(q.columns[:len(tb)]),list(q.columns[len(tb):]),cm))
bs=np.array(bs)
print('pre-period mean ATT: %.3f (boot SE %.3f)'%(est[0],bs[:,0].std()))
print('post-period mean ATT: %.3f (boot SE %.3f)'%(est[1],bs[:,1].std()))
print('share of boots with pre-mean < 0: %.2f'%(bs[:,0]<0).mean())
