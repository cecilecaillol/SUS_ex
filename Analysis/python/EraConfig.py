import os
""" Year dependent configurations / files """

ANALYSISTRIGGER = {
    '2022': {'mutau':'(1)','mumu':'(HLT_IsoMu24)'}
}

ANALYSISCHANNELCUT = {
    'mutau':'(nMuon>0&&nTau>0)',
    'mumu':'(nMuon>1)'
}

ANALYSISGRL = {
    '2022': 'Cert_Collisions2022_355100_362760_Golden.json'
}

cmssw=os.environ['CMSSW_BASE']
ANALYSISCUT={'': {'mutau' : '-c "%s"'%ANALYSISCHANNELCUT['mutau'],'mumu' : '-c "%s"'%ANALYSISCHANNELCUT['mumu']}}

## for data, json selection
#for y in ANALYSISTRIGGER:
#  ANALYSISCUT[y]={}
#  for c in ANALYSISTRIGGER[y]:
#    ANALYSISCUT[y][c]='--cut %s&&%s --json %s'%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c],cmssw+'/src/CMSDASTools/Analysis/data/'+ANALYSISGRL[y])

## for MC, no json
for y in ANALYSISTRIGGER:
  ANALYSISCUT[y]={}
  for c in ANALYSISTRIGGER[y]:
    ANALYSISCUT[y][c]='--cut %s&&%s '%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c])
