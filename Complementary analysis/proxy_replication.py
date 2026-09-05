# Independent-proxy replication of the SC24 informational signatures.
# Uses the EXACT metric definitions from SC24_info_analysis.ipynb so the numbers
# are directly comparable to the TSA/PSI results.
#
# INPUT (drop in this folder; monthly cadence, 2008-2019):
#   proxies_monthly.csv  with columns: Date, SSN, F107   (and optionally TSA, PSI)
# The SSN column = SILSO monthly total sunspot number; F107 = 10.7 cm solar flux.
#
# Run:  python3 proxy_replication.py proxies_monthly.csv
import numpy as np, pandas as pd, math, sys
from sklearn.metrics import mutual_info_score

# ---- metric functions copied verbatim from the notebook (CELL 4 / CELL C1) ----
def shannon_entropy(s):
    c=pd.Series(s).value_counts(); p=c/len(s); return float(-np.sum(p*np.log2(p+1e-12)))
def lempel_ziv_complexity(s):
    s=''.join(map(str,np.array(s,dtype=int))); n=len(s)
    if n==0: return 0.0
    d,i,c=set(),0,0
    while i<n:
        j=i
        while j<n and s[i:j+1] in d: j+=1
        d.add(s[i:j+1]); c+=1; i=j+1
    return c/n
def permutation_entropy(s,m=3,normalize=True):
    x=np.array(s); n=len(x)
    if n<m: return np.nan
    pat={}
    for i in range(n-m+1):
        p=tuple(np.argsort(x[i:i+m])); pat[p]=pat.get(p,0)+1
    pr=np.array(list(pat.values()))/sum(pat.values())
    pe=-np.sum(pr*np.log2(pr+1e-12))
    return float(pe/np.log2(math.factorial(m))) if normalize else float(pe)
def mutual_information(a,b):
    return float(mutual_info_score(a,b)/np.log(2))
def mi_kraskov(x,y,k=3):
    from sklearn.feature_selection import mutual_info_regression
    x=np.asarray(x,float).reshape(-1,1)
    return float(mutual_info_regression(x,np.asarray(y,float),n_neighbors=k,random_state=20260531)[0]/np.log(2))
def lmc_complexity(p,N=10):
    from scipy.spatial.distance import jensenshannon
    p=np.array(p,float)+1e-15; p/=p.sum(); u=np.ones(N)/N
    H=-np.sum(p*np.log2(p)); Hn=H/np.log2(N)
    return float(Hn*(jensenshannon(p,u,base=2)**2)), float(Hn)
N_BINS=10; WINDOW=26

def disc(x): return pd.cut(x,N_BINS,labels=False,duplicates='drop')
def static_metrics(series, m_pe=3):
    d=disc(series).dropna()
    p=np.zeros(N_BINS)
    for b,v in d.value_counts().items():
        if pd.notna(b): p[int(b)]=v
    return dict(H=shannon_entropy(d), LZC=lempel_ziv_complexity(d),
                PE=permutation_entropy(series.dropna(),m=m_pe),
                C_LMC=lmc_complexity(p)[0])
def sliding(series):
    d=disc(series).dropna(); out=[]
    for s in range(len(d)-WINDOW+1):
        w=d.iloc[s:s+WINDOW]; cont=series.loc[w.index]
        p=np.zeros(N_BINS)
        for b,v in w.value_counts().items():
            if pd.notna(b): p[int(b)]=v
        out.append(dict(Date=w.index[WINDOW//2],H=shannon_entropy(w),
            LZC=lempel_ziv_complexity(w),PE=permutation_entropy(cont,m=3),
            C_LMC=lmc_complexity(p)[0]))
    return pd.DataFrame(out).set_index('Date')
def cross_mi_series(a,b):
    da,db=disc(a).dropna(),disc(b).dropna(); idx=da.index.intersection(db.index)
    da,db=da.loc[idx],db.loc[idx]
    ca,cb=a.loc[idx],b.loc[idx]; out=[]
    for s in range(len(da)-WINDOW+1):
        wa,wb=da.iloc[s:s+WINDOW],db.iloc[s:s+WINDOW]
        out.append(dict(Date=da.index[s+WINDOW//2],
            MI_plugin=mutual_information(wa,wb),
            MI_kraskov=mi_kraskov(ca.iloc[s:s+WINDOW],cb.iloc[s:s+WINDOW])))
    return pd.DataFrame(out).set_index('Date')

def run(path):
    df=pd.read_csv(path,parse_dates=['Date']).set_index('Date')
    cols=[c for c in ['SSN','F107','TSA','PSI'] if c in df.columns]
    print("proxies present:",cols,"| n months:",len(df))
    print("\n=== static metrics (monthly, m_pe=3) ===")
    st={c:static_metrics(df[c]) for c in cols}
    print(pd.DataFrame(st).T.round(4).to_string())
    print("\n=== sliding-window signatures (modulation = max/min) ===")
    for c in cols:
        sw=sliding(df[c])
        print(f"  {c:5s}  LZC range [{sw.LZC.min():.3f},{sw.LZC.max():.3f}]  "
              f"C_LMC max {sw.C_LMC.max():.3f} @ {sw.C_LMC.idxmax().date()}  "
              f"H mod {sw.H.max()/max(sw.H.min(),1e-9):.2f}x")
        sw.to_csv(f'proxy_sliding_{c}.csv')
    print("\n=== cross-proxy MI modulation through the cycle ===")
    pairs=[('TSA','SSN'),('TSA','F107'),('PSI','F107'),('SSN','F107')]
    for a,b in pairs:
        if a in df.columns and b in df.columns:
            mi=cross_mi_series(df[a],df[b])
            kmin=max(mi.MI_kraskov[mi.MI_kraskov>0].min() if (mi.MI_kraskov>0).any() else 0, 1e-3)
            kmod=mi.MI_kraskov.max()/kmin
            print(f"  I({a};{b})  plug-in mod {mi.MI_plugin.max()/max(mi.MI_plugin.min(),1e-9):6.2f}x  "
                  f"| Kraskov(bias-free) max {mi.MI_kraskov.max():.3f} min(>0) {kmin:.3f} mod {kmod:.1f}x")
            mi.to_csv(f'proxy_MI_{a}_{b}.csv')
    print("\nInterpretation target: LZC near-stability, a descending-branch C_LMC")
    print("maximum, and MI modulation >1 should reproduce across independent proxies")
    print("if the TSA/PSI signatures are solar-activity signals, not catalogue artefacts.")

if __name__=='__main__':
    if len(sys.argv)>1:
        run(sys.argv[1])
    else:
        # self-test on synthetic SC24-like monthly series (no external data)
        print("[SELF-TEST on synthetic data — replace with real proxies_monthly.csv]\n")
        idx=pd.date_range('2008-12-31','2019-10-31',freq='ME')
        t=np.arange(len(idx)); cyc=np.sin(np.pi*t/len(t))**2   # single-hump cycle
        rng=np.random.default_rng(1)
        df=pd.DataFrame({'Date':idx,
            'SSN':120*cyc+8*rng.standard_normal(len(t))+5,
            'F107':70+90*cyc+4*rng.standard_normal(len(t)),
            'TSA':cyc*2000+50*rng.standard_normal(len(t))+100,
            'PSI':cyc*1500+40*rng.standard_normal(len(t))+80}).set_index('Date')
        df.reset_index().to_csv('_synthetic_proxies.csv',index=False)
        run('_synthetic_proxies.csv')
