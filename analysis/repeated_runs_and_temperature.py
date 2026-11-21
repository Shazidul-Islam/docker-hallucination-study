"""Reproduces the repeated-run and temperature-0 results (Sec. IV-D) reported in the paper from the CSV files in data/.
Run from the repository root:  python analysis/repeated_runs_and_temperature.py
"""
import pandas as pd, numpy as np, itertools
D='data/'
d=pd.read_csv(D+'robustness/issue4_repeated_runs.csv',dtype=str).fillna('')
d=d[d.error==''].copy(); d['ref']=d['Image Name']+':'+d['Tag']
d['eff']=np.where(d.temperature_used=='0','t0','default')
print('scenarios',d.Scenario.nunique(), d.groupby(['LLM','eff']).size().to_dict())
base=pd.read_csv(D+'combined/combined_full_results_rechecked.csv',dtype=str).fillna('')
sc=base.drop_duplicates('Scenario').set_index('Scenario')[['Batch','Popularity']]
d=d.join(sc,on='Scenario'); d['batch']=d.Batch.str[:4]
print(d.drop_duplicates('Scenario').groupby(['batch','Popularity']).size())
dd=d[(d.temperature_requested=='default')]   # runs 1-4
g=dd.groupby(['LLM','Scenario']).agg(nc=('category','nunique'),nr=('ref','nunique'),n=('category','size'),ni=('Image Name','nunique'))
g=g[g.n==4]
print('pairs',len(g)); print('all4 same category %.1f%%  same image %.1f%%  same exact ref %.1f%%'%(100*(g.nc==1).mean(),100*(g.ni==1).mean(),100*(g.nr==1).mean()))
print(g.assign(c=g.nc==1,r=g.nr==1).groupby('LLM')[['c','r']].mean().round(3))
# pairwise agreement
def pw(df,col):
    a=t=0
    for _,x in df.groupby(['LLM','Scenario'])[col]:
        v=list(x)
        for i,j in itertools.combinations(range(len(v)),2): t+=1;a+=v[i]==v[j]
    return a/t
print('pairwise cat agreement default %.3f'%pw(dd,'category'))
# modal agreement: fraction of runs equal to modal category
mod=dd.groupby(['LLM','Scenario']).category.agg(lambda s:s.value_counts().iat[0]/len(s)); print('mean modal share %.3f'%mod.mean())
# Fleiss kappa over categories for default runs (4 raters per item)
cats=sorted(dd.category.unique()); tab=dd.groupby(['LLM','Scenario']).category.value_counts().unstack(fill_value=0)[cats]
tab=tab[tab.sum(1)==4]; n=4; N=len(tab)
P=((tab**2).sum(1)-n)/(n*(n-1)); Pbar=P.mean(); pj=tab.sum()/(N*n); Pe=(pj**2).sum()
print('Fleiss kappa %.3f N=%d'%((Pbar-Pe)/(1-Pe),N))
# per-run distribution stability (flag rate)
ins=dd[dd.category!='OUT OF SCOPE']
pr=ins.groupby('run').category.value_counts(normalize=True).unstack(fill_value=0)*100
print(pr.round(1)); print('range per cat'); print((pr.max()-pr.min()).round(1)); print('mean±sd');print(pr.mean().round(1).astype(str)+' ± '+pr.std().round(1).astype(str))
valid=ins.groupby(['run']).apply(lambda x:(x.category=='Valid Official Image').mean()*100); print('valid per run',valid.round(1).to_dict())
nonex=ins.groupby('run').apply(lambda x:x.category.isin(['Nonexistent Tag','Non-Existent Image']).mean()*100); print('nonex per run',nonex.round(1).to_dict())
# per model valid sd
pm=ins.groupby(['LLM','run']).apply(lambda x:(x.category=='Valid Official Image').mean()*100).unstack(); print(pm.round(1)); print(pm.std(1).round(1))
# variation type: among pairs that vary, which categories flip
var=dd.groupby(['LLM','Scenario']).category.agg(lambda s:' / '.join(sorted(set(s))))
print(var[var.str.contains('/')].value_counts().head(15))
# temperature 0 (DeepSeek, GPT-OSS): two t0 runs agree?
t0=d[d.eff=='t0']
g0=t0.groupby(['LLM','Scenario']).agg(nc=('category','nunique'),nr=('ref','nunique'),n=('ref','size')); g0=g0[g0.n==2]
print('t0 pairs',len(g0),'same cat %.1f%% same ref %.1f%%'%(100*(g0.nc==1).mean(),100*(g0.nr==1).mean()))
print(g0.assign(c=g0.nc==1,r=g0.nr==1).groupby('LLM')[['c','r']].mean())
# compare to default runs pairwise for same models (runs1-2 only, equal footing)
dd2=dd[dd.LLM.isin(['DeepSeek','GPT-OSS-120B'])&dd.run.isin(['1','2'])]
g2=dd2.groupby(['LLM','Scenario']).agg(nc=('category','nunique'),nr=('ref','nunique'))
print('default runs1-2 same models: same cat %.1f%% same ref %.1f%%'%(100*(g2.nc==1).mean(),100*(g2.nr==1).mean()))
# t0 modal vs default modal category
mt0=t0.groupby(['LLM','Scenario']).category.agg(lambda s:s.mode().iat[0]); md=dd.groupby(['LLM','Scenario']).category.agg(lambda s:s.mode().iat[0])
j=pd.concat([mt0,md],axis=1,keys=['t0','d']).dropna(); print('t0 vs default modal cat agree %.1f%% n=%d'%(100*(j.t0==j.d).mean(),len(j)))
# original (paper) category vs reruns: how often was the original single answer equal to the modal rerun category
o=base[['LLM','Scenario','Automated Category']].set_index(['LLM','Scenario'])['Automated Category']
jj=pd.concat([md,o],axis=1,keys=['m','o']).dropna(); print('original single answer == rerun modal cat %.1f%% n=%d'%(100*(jj.m==jj.o).mean(),len(jj)))
inrun=dd.join(o.rename('o'),on=['LLM','Scenario']).dropna(subset=['o']); print('runs matching original cat %.1f%% n=%d'%(100*(inrun.category==inrun.o).mean(),len(inrun)))
# ChatGPT: all 6 runs default
c6=d[d.LLM=='ChatGPT'].groupby('Scenario').category.nunique(); print('ChatGPT 6 default runs all same %.1f%%'%(100*(c6==1).mean()))
