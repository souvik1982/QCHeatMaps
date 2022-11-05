import ROOT
from scipy import stats

crocName1 = "203"
crocName2 = "205_messUp"

file1 = ROOT.TFile("h_T_rs_"+str(crocName1)+".root")
file2 = ROOT.TFile("h_T_rs_"+str(crocName2)+".root")

h_T_rs_1 = file1.Get("h_T_rs")
h_T_rs_2 = file2.Get("h_T_rs")
h_T_rs_2.SetMarkerColor(ROOT.kRed); h_T_rs_2.SetLineColor(ROOT.kRed)

c_T_rs = ROOT.TCanvas("c_T_rs", "c_T_rs", 700, 700)
h_T_rs_1.SetMaximum(h_T_rs_1.GetMaximum()*1.5)
h_T_rs_1.Draw("HIST")
h_T_rs_2.Draw("hist SAME")

ks = h_T_rs_1.KolmogorovTest(h_T_rs_2)
print ("ks = "+str(ks))

'''
croc1 = []
croc2 = []
for i in range(0, g_T_rs_1.GetN()):
  rs = ROOT.Double()
  T = ROOT.Double()
  g_T_rs_1.GetPoint(i, rs, T)
  croc1.append((rs, T))
for i in range(0, g_T_rs_2.GetN()):
  rs = ROOT.Double()
  T = ROOT.Double()
  g_T_rs_2.GetPoint(i, rs, T)
  croc2.append((rs, T))
ks = stats.kstest(croc1, croc2)
print ("ks = "+str(ks))
'''

input()
