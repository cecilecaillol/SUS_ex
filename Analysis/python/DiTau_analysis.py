#!/usr/bin/env python
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

from long-ex-ztt.Analysis.objectSelector import ElectronSelector, MuonSelector, TauSelector

class Analysis(Module):
    def __init__(self, channel, isMC):
        self.channel = channel
        self.isMC    = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree
        self.out.branch("nLepCand",          "I");
        self.out.branch("LepCand_id",        "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_pt",        "F",  lenVar = "nLepCand");

	# CHANGE: add more variables for the leptons (DNN discriminators, eta, phi, charge, decay mode, dxy, dz, gen info, ...)

        self.out.branch("nJets",             "I");
 
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def selectMuons(self, event, muSel):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if not muSel.evalMuon(mu): continue
            setattr(mu, 'id', 13)
            event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)

    def selectElectrons(self, event, elSel):
        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            if not elSel.evalElectron(el): continue
            #remove overlap with selected muons 
            deltaR_to_leptons=[ el.p4().DeltaR(lep.p4()) for lep in event.selectedMuons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            setattr(el, 'id', 11)
            event.selectedElectrons.append(el)
        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)


    def selectTaus(self, event, tauSel):
        event.selectedTaus = []
        taus = Collection(event, "Tau")
        for tau in taus:
            #remove overlap with selected electrons and muons 
            deltaR_to_leptons=[ tau.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            if not tauSel.evalTau(tau): continue
            setattr(tau, 'id', 15)
            event.selectedTaus.append(tau)
        event.selectedTaus.sort(key=lambda x: x.pt, reverse=True)



    def selectAK4Jets(self, event):
        ## Selected jets: pT>30, |eta|<4.7, pass tight ID
        
        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:

            if j.pt<30 : 
                continue

            if abs(j.eta) > 4.7:
                continue
            
            if j.jetId<1: 
                continue
                
            #remove overlap with selected leptons 
            deltaR_to_leptons=[ j.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons+event.selectedTaus ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            event.selectedAK4Jets.append(j)
            
        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        elSel = ElectronSelector()
        muSel = MuonSelector()
        tauSel = TauSelector()
        
        # apply object selection
        self.selectMuons(event, muSel)
        self.selectElectrons(event, elSel)
        self.selectTaus(event, tauSel)
        self.selectAK4Jets(event)
        
        #apply event selection depending on the channel:
        if self.channel=="mutau":
            # CHANGE: Select events with exactly 1 muon, 0 electron, and 1 tauh
            if len(event.selectedElectrons)>0: return False

	# CHANGE: do the same for other channels you want to analyze (e.g. mumu)
            

        ######################################################
        ##### HIGH LEVEL VARIABLES FOR SELECTED EVENTS   #####
        ######################################################
        
        event.selectedLeptons=event.selectedElectrons+event.selectedMuons+event.selectedTaus
        event.selectedLeptons.sort(key=lambda x: x.pt, reverse=True)
        
        lep_id     = [lep.id for lep in event.selectedLeptons]
        lep_pt     = [lep.pt for lep in event.selectedLeptons]
	# CHANGE: fill other lepton variables too


        ## store branches
        self.out.fillBranch("nLepCand",           len(event.selectedLeptons))
        self.out.fillBranch("LepCand_id" ,        lep_id)
        self.out.fillBranch("LepCand_pt" ,        lep_pt)
	# CHANGE: fill other lepton variables too
        self.out.fillBranch("nJets" ,             len(event.selectedAK4Jets))

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
analysis_mutaumc    = lambda : Analysis(channel="mutau", isMC=True)
analysis_mutaudata  = lambda : Analysis(channel="mutau", isMC=False)

#CHANGE: define modules for other channels (e.g. mumu)

