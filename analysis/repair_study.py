"""Reproduces the repair study (Table IV) reported in the paper from the CSV files in data/.
Run from the repository root:  python analysis/repair_study.py
"""
import pandas as pd, math
D='data/repair/'
def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=p+z*z/(2*n);h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return round(100*(c-h)/d,1),round(100*(c+h)/d,1)
raw=pd.read_csv(D+'issue7_repair_raw.csv',dtype=str).fillna('')
last=raw[raw.error==''].drop_duplicates('key',keep='last')
o=pd.read_csv(D+'issue7_repair_outcomes_auto.csv',dtype=str).fillna('')
assert set(o.key)==set(last.key), (len(o),len(last))
print('n',len(o), o.groupby(['stratum']).size().to_dict(), o.LLM.value_counts().to_dict())
# Manual re-reading of 10 rows whose FROM line the regex mis-split (markdown bold or an @sha256 digest)
fix={ # key: (image, tag, corrected category, outcome, note)
'I7|141':('nvidia/cuda','12.6.3-cudnn-devel-ubuntu22.04','Non-Official Image','Still flagged','digest placeholder'),
'I7|176':('tomcat','10.1.31-jdk17-temurin','NEEDS MANUAL CHECK','Uncertain','digest placeholder; no EOL data'),
'I7|341':('traefik','2.13-alpine','Nonexistent Tag','Still flagged','invented sha256 digest'),
'I7|35':('mysql','8.0.40','Outdated Tag','Still flagged','cycle 8.0 EOL 2026-04-30'),
'I7|26':('golang','1.23.4-alpine3.21','Outdated Tag','Still flagged','cycle 1.23 EOL 2025-08-12; unverifiable digest'),
'I7|317':('haskell','9.6.6-slim','NEEDS MANUAL CHECK','Uncertain','digest placeholder; no EOL data'),
'I7|33':('rust','1.82.0-slim-bookworm','Outdated Tag','Still flagged','rust 1.82 superseded; digest placeholder'),
'I7|41':('nginx','1.27.4-alpine','Outdated Tag','Still flagged','cycle 1.27 EOL 2025-06-24; unverifiable digest'),
'I7|322':('swift','5.10-jammy','NEEDS MANUAL CHECK','Uncertain','no EOL data'),
'I7|191':('rocker/tidyverse','4.4.1','Non-Official Image','Still flagged','non-official namespace'),
}
for k,(im,tg,c,out,n) in fix.items():
    i=o.index[o.key==k][0]; print(k,o.at[i,'category'],'->',c, o.at[i,'outcome'],'->',out)
    o.loc[i,['Image Name','Tag','category','outcome']]=[im,tg,c,out]; o.at[i,'note']=n+' (re-parsed manually)'
o.to_csv(D+'issue7_repair_outcomes_final.csv',index=False)
print(o.outcome.value_counts().to_dict())
def rep(g):
    k=(g.outcome=='Repaired').sum(); n=len(g); res=g[g.outcome!='Uncertain']; kr=len(res)
    return pd.Series({'n':n,'rep':k,'all%':round(100*k/n),'CI_all':wilson(k,n),'resolved':kr,'res%':round(100*k/kr) if kr else None,'CI_res':wilson(k,kr) if kr else None,'still':(g.outcome=='Still flagged').sum(),'unc':(g.outcome=='Uncertain').sum()})
order=['Non-existent','Outdated Tag','Risky Latest Tag','Non-Official Image']
t=o.groupby('stratum').apply(rep).loc[order]; t.loc['ALL']=rep(o); print(t.to_string())
print(o.groupby('LLM').apply(rep)[['n','rep','all%','resolved','res%']].to_string())
print('new nonexistent tags among repairs:',o[o.category.isin(['Nonexistent Tag','Non-Existent Image'])][['LLM','original_ref','Image Name','Tag']].to_string())
print('uncertain breakdown', o[o.outcome=='Uncertain'].category.value_counts().to_dict())
print('still flagged breakdown', o[o.outcome=='Still flagged'].category.value_counts().to_dict())
# verbosity: responses not just a FROM line
o['multiline']=o.raw_response.str.strip().str.replace('```dockerfile','').str.replace('```','').str.strip().str.count('\n')>0
print('multi-line responses by LLM', o.groupby('LLM').multiline.sum().to_dict())
# non-official stratum: moved to official?
no=o[o.stratum=='Non-Official Image']; print('non-official -> official image (no slash):',(~no['Image Name'].str.contains('/')).sum(),'of',len(no))
