./Make.sh FinalSelection_mutau.cc
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/DY_postEE.root output_mutau_2022/DY_postEE.root DY DY
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/TTTo2L2Nu_postEE.root output_mutau_2022/TTTo2L2Nu_postEE.root TTTo2L2Nu TTTo2L2Nu
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/WW_postEE.root output_mutau_2022/WW_postEE.root WW WW
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/Muon2022E.root output_mutau_2022/Muon2022E.root data_obs data_obs
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/Muon2022F.root output_mutau_2022/Muon2022F.root data_obs data_obs
./FinalSelection_mutau.exe 2022postEE /eos/cms/store/cmst3/user/ccaillol/cmsdas2024/ntuples_mutau_2022/Muon2022G.root output_mutau_2022/Muon2022G.root data_obs data_obs
hadd -f output_mutau_2022/Data.root output_mutau_2022/Muon2022E.root output_mutau_2022/Muon2022F.root output_mutau_2022/Muon2022G.root
python3 Create_fake.py
hadd -f datacard_mutau.root output_mutau_2022/DY_postEE.root output_mutau_2022/TTTo2L2Nu_postEE.root output_mutau_2022/WW_postEE.root output_mutau_2022/Data.root output_mutau_2022/Fake.root
python3 Draw_mutau.py
