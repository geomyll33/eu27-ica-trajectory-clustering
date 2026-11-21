import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
p='data/ICA_27_members_until_2023.xlsx'
X=pd.read_excel(p,sheet_name=0).set_index('date').T
def pc(X): return X.sub(X.mean(axis=1),axis=0).div(X.std(axis=1),axis=0)
def pooled(X): return (X-X.values.mean())/X.values.std()
def idx(X,y): return X.div(X.iloc[:,[y-1995]].values)*100
def logd(X): return np.log(X).diff(axis=1).iloc[:,1:]
S={'A':pc(X),'B':pooled(X),'D':logd(X),'C1995':idx(X,1995),'C2000':idx(X,2000),'C2005':idx(X,2005)}
def draws(Z,labels,k=4,B=2000,seed=42):
    rng=np.random.default_rng(seed); n=len(Z); idx_=np.arange(n); lab=labels.values
    M=np.zeros((B,k))
    subs=[rng.choice(idx_,int(0.8*n),replace=False) for _ in range(B)]
    seeds=[int(rng.integers(1e9)) for _ in range(B)]
    for b in range(B):
        sub=subs[b]
        ls=KMeans(k,n_init=10,random_state=seeds[b]).fit_predict(Z.values[sub])
        for c in range(k):
            A=set(idx_[lab==c]); best=0
            for cc in range(k):
                Bs=set(sub[ls==cc])
                if Bs: best=max(best,len(A&Bs)/len(A|Bs))
            M[b,c]=best
    return M
out={}
for n,Z in S.items():
    L=pd.Series(KMeans(4,n_init=50,random_state=0).fit_predict(Z.values),index=Z.index)
    M=draws(Z,L)
    out[n]={'mean':M.mean(0).round(3).tolist(),'p5':np.percentile(M,5,axis=0).round(3).tolist(),'min_mean':round(float(M.mean(0).min()),3),'sizes':np.bincount(L.values).tolist()}
    print(n,out[n],flush=True)
json.dump(out,open('results/stab_b2000.json','w'),indent=1)
