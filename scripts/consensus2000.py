import pandas as pd, numpy as np, warnings, io
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
p='data/ICA_27_members_until_2023.xlsx'
X=pd.read_excel(p,sheet_name=0).set_index('date').T
Z=X.sub(X.mean(axis=1),axis=0).div(X.std(axis=1),axis=0)
n=len(Z); k=4; B=2000
lab=KMeans(4,n_init=50,random_state=0).fit_predict(Z.values)
rng=np.random.default_rng(42); idx_=np.arange(n)
co=np.zeros((n,n)); cnt=np.zeros((n,n))
subs=[rng.choice(idx_,int(0.8*n),replace=False) for _ in range(B)]
seeds=[int(rng.integers(1e9)) for _ in range(B)]
for b in range(B):
    sub=subs[b]
    ls=KMeans(k,n_init=10,random_state=seeds[b]).fit_predict(Z.values[sub])
    cnt[np.ix_(sub,sub)]+=1
    co[np.ix_(sub,sub)]+=(ls[:,None]==ls[None,:])
freq=np.divide(co,cnt,out=np.zeros_like(co),where=cnt>0)
order=np.argsort(lab,kind='stable')
names=list(Z.index)
F=freq[np.ix_(order,order)]
fig,ax=plt.subplots(figsize=(8.58,7.77),dpi=300)
im=ax.imshow(F,cmap='viridis',vmin=0,vmax=1)
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels([names[i] for i in order],rotation=90,fontsize=5)
ax.set_yticklabels([names[i] for i in order],fontsize=5)
edges=np.cumsum(np.bincount(lab))[:-1]-0.5
for e in edges: ax.axhline(e,color='white',lw=0.8); ax.axvline(e,color='white',lw=0.8)
cb=fig.colorbar(im,ax=ax,fraction=0.046); cb.set_label('co-clustering frequency')
fig.tight_layout(); fig.savefig('figures/figures_consensus_matrix_2000.png',dpi=300)
print('within',[round(float(freq[np.ix_(lab==a,lab==a)][~np.eye((lab==a).sum(),dtype=bool)].mean()),2) for a in range(k)])
