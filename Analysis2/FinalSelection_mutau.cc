#include <TH2.h>
#include <TH2F.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphAsymmErrors.h>
#include "TMultiGraph.h"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <utility>
#include <stdio.h>
#include <TF1.h>
#include <TDirectoryFile.h>
#include <TRandom3.h>
#include "TLorentzVector.h"
#include "TString.h"
#include "TLegend.h"
#include "TH1F.h"
#include "TKey.h"
#include "THashList.h"
#include "THStack.h"
#include "TPaveLabel.h"
#include "TFile.h"
#include "TTree.h"
#include "tr_Tree.h"

using namespace std;

int main(int argc, char** argv) {


    std::string year = *(argv + 1);
    std::string input = *(argv + 2);
    std::string output = *(argv + 3);
    std::string sample = *(argv + 4);
    std::string name = *(argv + 5);

    TFile *f_Double = new TFile(input.c_str());
    cout<<"XXXXXXXXXXXXX "<<input.c_str()<<" XXXXXXXXXXXX"<<endl;
    TTree *arbre = (TTree*) f_Double->Get("Events");

    TTree *arbre2 = (TTree*) f_Double->Get("Runs");
    float ngen=0;
    float ngenu=0;
    if (name!="data_obs") {
       Int_t nentries_wtn2 = (Int_t) arbre2->GetEntries();
       arbre2->SetBranchAddress("genEventCount", &genEventCount);
       for (Int_t i = 0; i < nentries_wtn2; i++) {
         arbre2->GetEntry(i);
         ngenu+=genEventCount;
       }
    }
    cout<<"N gen unweighted: "<<ngenu<<endl;

    float weight=1.0;
    // CHANGE: compute the weight for each MC sample based on the integrated luminosity (20 fb-1), the number of generated events (ngenu), and the sample cross section

    cout.setf(ios::fixed, ios::floatfield);
    cout.precision(10);

    arbre->SetBranchAddress("nLepCand", &nLepCand);
    arbre->SetBranchAddress("LepCand_id", &LepCand_id);
    arbre->SetBranchAddress("LepCand_pt", &LepCand_pt);
    arbre->SetBranchAddress("nJets", &nJets);


    TH1F* h_mvis = new TH1F("h_mvis","h_mvis",30,0,300); h_mvis->Sumw2();
    // CHANGE: define here other histograms you want to fill and save

   Int_t nentries_wtn = (Int_t) arbre->GetEntries();
   for (Int_t i = 0; i < nentries_wtn; i++) {
	arbre->LoadTree(i);
        arbre->GetEntry(i);
        if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
        fflush(stdout);
	
	int mu_index=-1;
	for (int j=0; j<nLepCand; ++j){
	   if (mu_index<0 and LepCand_id[j]==13) mu_index=j;
	}
        int tau_index=-1; float pt_tmp=0;
        for (int j=0; j<nLepCand; ++j){
           if (LepCand_id[j]==15 and LepCand_pt[j]>pt_tmp){
	      tau_index=j; 
	      pt_tmp=LepCand_pt[j];
	   }
        }

	// CHANGE: build and fill the four-vectors of the muon and the tau 
        TLorentzVector my_tau; 
        TLorentzVector my_mu; 

	// CHANGE: apply the selection on the muon and the tau (eta, pt, ID, ...)
	// if (my_tau.Pt()<20) continue;
	//
	// CHANGE: apply the selection on the dilepton pair (DR > 0.5, OS, ...)
	//
	// CHANGE: apply the trigger selection
	//


	//CHANGE: fill the histograms
	//h_mvis->Fill((my_mu+my_tau).M(),weight);

    } // end of loop over events

    TFile *fout = TFile::Open(output.c_str(), "RECREATE");
    fout->cd();

    // You can store the histogram directly in the root file...
    h_mvis->Write();
    // or in a directory (necessary for the statistical analysis later)

    TDirectory *dir_OSiso =fout->mkdir("OSiso");
    dir_OSiso->cd();
    h_mvis->SetName(name.c_str());
    h_mvis->Write();

    // CHANGE: save the other histograms you have filled

    fout->Close();
} 

