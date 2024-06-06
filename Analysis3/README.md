## CMSSW setup
```
cmssw-el7 #singularity needed

cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v9.2.1

scramv1 b clean; scramv1 b # always make a clean build
```

Move script to CombineHarvester
```
cp mutauDAS2024.py CombineHarvester/CombineTools/scripts/mutauDAS2024.py
```

Make sure that auxiliaries exist:
```
ls -l auxiliaries
```


Make the data card (remember to use singularity!)

```
cd $CMSSW_BASE/src/
cmsenv
python CombineHarvester/CombineTools/scripts/mutauDAS2024.py

```

Ensure that data card and root file were made:

```
ls -l mt*
```


Run limits

```
combine -M AsymptoticLimits mt.txt
```


