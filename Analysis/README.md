# Analysis

Code to make flat trees from NanoAOD with baseline analysis preselection.

## To run locally on a file
```
voms-proxy-init --voms=cms --valid=48:0
python PhysicsTools/NanoAODTools/scripts/nano_postproc.py output root://cms-xrd-global.cern.ch//store/mc/Run3Summer22EENanoAODv11/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/NANOAODSIM/forPOG_126X_mcRun3_2022_realistic_postEE_v1-v1/70000/0153df5d-df28-4515-82c2-04f76d82bb34.root --bi $CMSSW_BASE/src/SUS_ex/Analysis/scripts/keep_in.txt --bo $CMSSW_BASE/src/SUS_ex/Analysis/scripts/keep_out.txt -c "(nMuon>0&&nTau>0&&HLT_IsoMu24)" -I SUS_ex.Analysis.DiTau_analysis analysis_mutaumc -N 1000
```

## To submit jobs for full datasets over Condor

First edit python/EraConfig.py (data or MC, object preselection in NanoAOD) and scripts/runNtuplizer (which channel to run, where to store the output files)

For MC:

```
python $CMSSW_BASE/src/SUS_ex/Analysis/scripts/runNtuplizer.py --in $CMSSW_BASE/src/SUS_ex/Analysis/data/listSamplesMC.txt
```

For data: 

```
python $CMSSW_BASE/src/SUS_ex/Analysis/scripts/runNtuplizer.py --in $CMSSW_BASE/src/SUS_ex/Analysis/data/listSamplesMuonData.txt
```

And follow the instructions printed on the screen (dont forget to type the new voms-proxy-init command printed). 

## To combine the output files once all condor jobs have run

First edit my\_hadd.sh with the location of your output files. Then:
```
sh my_hadd.sh
```

