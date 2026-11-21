"""Reproduces the web-vs-API agreement (Sec. IV-D) and the image-free prompt results reported in the paper from the CSV files in data/.
Run from the repository root:  python analysis/web_vs_api_and_image_free_prompts.py
"""
import pandas as pd, math, itertools
D='data/'
base=pd.read_csv(D+'combined/combined_full_results_rechecked.csv',dtype=str).fillna('')
def wilson(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=p+z*z/(2*n);h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return round(100*(c-h)/d,1),round(100*(c+h)/d,1)
FLAG={'Outdated Tag','Risky Latest Tag','Nonexistent Tag','Non-Existent Image','Non-Official Image'}
# ---------- Issue 5
i5=pd.read_csv(D+'robustness/issue5_original_via_api.csv',dtype=str).fillna('')
i5['ref']=i5['Image Name']+':'+i5['Tag']
orig=base[base.Batch.str.startswith('Original')].copy(); orig['ref']=orig['Image Name']+':'+orig['Tag']
m=i5.merge(orig[['LLM','Scenario','Automated Category','ref']],on=['LLM','Scenario'],suffixes=('','_web'))
print('ISSUE5 pairs',len(m),'models',m.LLM.unique())
print(' same category %.1f%%'%(100*(m.category==m['Automated Category']).mean()), (m.category==m['Automated Category']).sum())
print(' same image %.1f%%'%(100*(m['Image Name']==m.ref_web.str.split(':').str[0]).mean()))
print(' same exact ref %.1f%%'%(100*(m.ref==m.ref_web).mean()))
print(m.groupby('LLM').apply(lambda g:(g.category==g['Automated Category']).mean()).round(3))
print(pd.crosstab(m['Automated Category'],m.category))
ins=lambda s:s[s!='OUT OF SCOPE']
for lab,col in [('web',m['Automated Category']),('api',m.category)]:
    c=ins(col); print(lab,len(c),(100*c.value_counts(normalize=True)).round(1).to_dict())
print('GPT-OSS on original (API):',i5[i5.LLM=='GPT-OSS-120B'].category.value_counts().to_dict())
apiall=ins(i5.category); print('API all 4 models in-scope',len(apiall),(100*apiall.value_counts(normalize=True)).round(1).to_dict())
# ---------- Issue 5b
b=pd.read_csv(D+'robustness/issue5b_expansion_descriptive.csv',dtype=str).fillna('')
print('\nISSUE5b rows',len(b),'scen',b.Scenario.nunique(),'err',(b.error!='').sum())
bi=b[b.category!='OUT OF SCOPE']; print(' in-scope',len(bi),'OOS',(b.category=='OUT OF SCOPE').sum())
print((100*bi.category.value_counts(normalize=True)).round(1).to_string()); print(bi.category.value_counts().to_string())
print(pd.crosstab(bi.LLM,bi.category))
nonex=bi[bi.category.isin(['Nonexistent Tag','Non-Existent Image'])]; print(nonex[['LLM','Scenario','Image Name','Tag']].to_string())
exp=base[base.Batch.str.startswith('Expansion')&(base['Automated Category']!='OUT OF SCOPE')]
e4=exp[exp.LLM.isin(['ChatGPT','Claude','DeepSeek','GPT-OSS-120B'])]
print(' named-image, same 4 models, in-scope',len(e4),(100*e4['Automated Category'].value_counts(normalize=True)).round(1).to_dict())
print(' latest literal share 5b: %.1f%%'%(100*(bi.Tag=='latest').mean()))
