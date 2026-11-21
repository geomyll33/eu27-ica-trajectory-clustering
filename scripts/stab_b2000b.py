import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
p='data/ICA_27_members_until_2023.xlsx'
X=pd.read_excel(p,sheet_name=0).set_index('date').T
Z=X.sub(X.mean(axis=1),axis=0).div(X.std(axis=1),axis=0)
n=len(Z); k=4; B=2000
L=KMeans(4,n_init=50,random_state=0).fit_predict(Z.values); lab=L
rng=np.random.default_rng(42); idx_=np.arange(n)
M=np.zeros((B,k)); co=np.zeros((n,n)); cnt=np.zeros((n,n))
subs=[rng.choice(idx_,int(0.8*n),replace=False) for _ in range(B)]
seeds=[int(rng.integers(1e9)) for _ in range(B)]
for b in range(B):
    sub=subs[b]
    ls=KMeans(k,n_init=10,random_state=seeds[b]).fit_predict(Z.values[sub])
    s=np.zeros(n,bool); s[sub]=True
    cnt[np.ix_(sub,sub)]+=1
    lab_full=np.full(n,-1); lab_full[sub]=ls
    co[np.ix_(sub,sub)]+=(ls[:,None]==ls[None,:])
    for c in range(k):
        A=set(idx_[lab==c]); best=0
        for cc in range(k):
            Bs=set(sub[ls==cc])
            if Bs: best=max(best,len(A&Bs)/len(A|Bs))
        M[b,c]=best
freq=np.divide(co,cnt,out=np.zeros_like(co),where=cnt>0)
within={c: round(float(freq[np.ix_(lab==c,lab==c)][~np.eye((lab==c).sum(),dtype=bool)].mean()),2) for c in range(k)}
between=round(float(freq[np.ix_(lab==0,lab==1)].mean()),2)
out={'mean':M.mean(0).round(3).tolist(),'median':np.median(M,0).round(3).tolist(),'p5':np.percentile(M,5,axis=0).round(3).tolist(),'sizes':np.bincount(lab).tolist(),'within_coclust':within}
print(out)
json.dump(out,open('results/stab_b2000_main.json','w'),indent=1)
bet={}
for a in range(k):
    for c in range(k):
        if a<c:
            bet[f'{a}-{c}']=round(float(freq[np.ix_(lab==a,lab==c)].mean()),2)
print('between',bet)
