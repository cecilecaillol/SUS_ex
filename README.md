# Long SUS exercise for the CMS DAS school 2024 at CERN (stau pair production) 

In "Analysis" there is the code to make flat trees from NanoAOD.

In "Analysis2" there is the code to analyze the flat trees.

In "Analysis3" there is files to run combine

## CMSSW setup
```
cmsrel CMSSW_13_0_10
cd CMSSW_13_0_10/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j 8

#This package
git clone https://github.com/cecilecaillol/SUS_ex.git
scram b -j 8

#Correctionlib
python3 -c 'import correctionlib._core; import correctionlib.schemav2'
```

