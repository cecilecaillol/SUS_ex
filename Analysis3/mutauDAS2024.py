from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch

import ROOT as R
import glob
import os

cb = ch.CombineHarvester()
cb.SetVerbosity(3)

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/auxiliaries/'

chns = ['mt']

bkg_procs = {'mt' : ['DY', 'TTTo2L2Nu', 'WW', 'Fake']}

sig_procs = {'mt': ['stau_right', 'stau_left']}

cats = {
    'mt_13TeV' : [
    (0, 'OSiso'),
  ],
}

for chn in chns:
    cb.AddObservations(  ['*'],  [''], ['13TeV'], [chn],                 cats[chn+"_13TeV"]      )
    cb.AddProcesses(     ['*'],  [''], ['13TeV'], [chn], bkg_procs[chn], cats[chn+"_13TeV"], False  )
    cb.AddProcesses(     ['*'],  [''], ['13TeV'], [chn], sig_procs[chn],  cats[chn+"_13TeV"], True   )


print '>> Adding systematic uncertainties...'
cb.cp().process({"DY", "TTTo2L2Nu", "WW", "stau_right", "stau_left"}).AddSyst(cb, 'lumi_13TeV', 'lnN', ch.SystMap()(1.03))
cb.cp().process({"DY", "TTTo2L2Nu", "WW", "stau_right", "stau_left"}).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(1.02));
cb.cp().process({"DY", "TTTo2L2Nu", "WW", "stau_right", "stau_left"}).AddSyst(cb, "CMS_eff_t", "lnN", ch.SystMap()(1.08));
cb.cp().process({"Fake"}).AddSyst(cb, "norm_fakes", "lnN", ch.SystMap()(1.5));

print '>> Extracting histograms from input root files...'
for chn in chns:
    file = auxiliaries + chn + "/datacard_mutau_new.root" 
    cb.cp().channel([chn]).era(['13TeV']).backgrounds().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).era(['13TeV']).signals().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')


bins = cb.bin_set()

output=R.TFile("mt.input.root", "RECREATE");

for b in bins:
  cb.cp().bin({b}).WriteDatacard("mt.txt", output);

