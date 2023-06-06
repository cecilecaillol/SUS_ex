   Long64_t       genEventCount;
   Double_t       genEventSumw;

   UInt_t          run;
   UInt_t          luminosityBlock;
   ULong64_t       event;
   Int_t           nLepCand;
   Int_t           LepCand_id[3];   //[nLepCand]
   Float_t         LepCand_pt[3];   //[nLepCand]
   Int_t           nJets;

   // CHANGE: add the variables stored in the flat trees and not defined above (use MakeClass to easily get the list from the Root file)
