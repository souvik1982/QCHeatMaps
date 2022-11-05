import ROOT
import math

crocName = "205_messUp"
sqrt2 = math.sqrt(2)

# Read the CSV file into a 2D array
v_v_image = []
minTemp = 1000
maxTemp = 0
csvFile = open(crocName+".csv")
lines = csvFile.readlines()
for line in lines:
  words = line.split(",")
  v_image = []
  for word in words:
    temp = float(word)
    v_image.append(temp)
    if (temp < minTemp): minTemp = temp
    if (temp > maxTemp): maxTemp = temp
  v_v_image.append(v_image)
print ("minTemp = "+str(minTemp)+", maxTemp = "+str(maxTemp))

# Draw the image without massaging it
h_image_noMassage = ROOT.TH2F("h_image_noMassage", "; x; y", len(v_v_image[0]), 0, len(v_v_image[0]), len(v_v_image), 0, len(v_v_image))
for j in range(0, len(v_v_image)):
  for i in range(0, len(v_v_image[0])):
    h_image_noMassage.SetBinContent(i, j, v_v_image[j][i])
c_image_noMassage = ROOT.TCanvas("c_image_noMassage", "c_image_noMassage", 700, 700)
h_image_noMassage.Draw("COLZ")
c_image_noMassage.SaveAs("c_image_noMassage.png")

# Zero suppression of temperature
#  Plot 1D histogram of temperatures and determine a lower cut off
h_temp = ROOT.TH1F("h_temp", "; T (C)", 20, minTemp, maxTemp)
for j in range(0, len(v_v_image)):
  for i in range(0, len(v_v_image[0])):
    h_temp.Fill(v_v_image[j][i])
i = 2
while (h_temp.GetBinContent(i) > h_temp.GetBinContent(i+1)): i=i+1
temp_CutOff = h_temp.GetBinCenter(i)
c_temp_CutOff = ROOT.TCanvas("c_temp_CutOff", "c_temp_CutOff", 700, 700)
c_temp_CutOff.SetLogy()
h_temp.Draw("HIST")
arrow = ROOT.TArrow(temp_CutOff, 0.5*h_temp.GetMaximum(), temp_CutOff, 0)
arrow.Draw()
c_temp_CutOff.SaveAs("c_temp_CutOff.png")
# Zero suppress the image histogram
for j in range(0, len(v_v_image)):
  for i in range(0, len(v_v_image[0])):
    if (v_v_image[j][i]<temp_CutOff): v_v_image[j][i]=0.
    else: v_v_image[j][i] = v_v_image[j][i] - temp_CutOff

# Draw the image
# Find center of mass
# Find scale from moment of inertia
h_image = ROOT.TH2F("h_image", "; x; y", len(v_v_image[0]), 0, len(v_v_image[0]), len(v_v_image), 0, len(v_v_image))
sum_mx = 0
sum_my = 0
mass = 0
for j in range(0, len(v_v_image)):
  for i in range(0, len(v_v_image[0])):
    h_image.SetBinContent(i, j, v_v_image[j][i])
    sum_mx += h_image.GetXaxis().GetBinCenter(i)*v_v_image[j][i]
    sum_my += h_image.GetYaxis().GetBinCenter(j)*v_v_image[j][i]
    mass += v_v_image[j][i]
mean_x = sum_mx / mass
mean_y = sum_my / mass
sum_mr2 = 0
for j in range(0, len(v_v_image)):
  for i in range(0, len(v_v_image[0])):
    sum_mr2 += v_v_image[j][i]*((h_image.GetXaxis().GetBinCenter(i)-mean_x)**2 + (h_image.GetYaxis().GetBinCenter(j)-mean_y)**2)
    v_v_image[j][i] /= mass
scale = math.sqrt(sum_mr2 / mass)
print ("mean = ("+str(mean_x)+", "+str(mean_y)+")")
print ("scale = "+str(scale))
c_image = ROOT.TCanvas("c_image", "c_image", 700, 700)
h_image.Draw("COLZ")
line1 = ROOT.TLine(mean_x-10, mean_y, mean_x+10, mean_y)
line2 = ROOT.TLine(mean_x, mean_y-10, mean_x, mean_y+10)
line1.Draw()
line2.Draw()
c_image.SaveAs("c_image.png")

# Fill 1-D graphs of T within circle vs r/s
g_T_rs = ROOT.TGraph()
g_T_rs.SetNameTitle("g_T_rs", "; r/scale; T")
dr = 2
point = 0
h_T_rs = ROOT.TH1F("h_T_rs", "; r/scale; T", 25, 0, 2)
for r in range(0, 50, dr):
  print("r = "+str(r))
  x_small_1 = mean_x - r/sqrt2
  x_small_2 = mean_x + r/sqrt2
  y_small_1 = mean_y - r/sqrt2
  y_small_2 = mean_y + r/sqrt2
  x_large_1 = mean_x - r - dr
  x_large_2 = mean_x + r + dr
  y_large_1 = mean_y - r - dr
  y_large_2 = mean_y + r + dr
  sum_T = 0
  #print("r = "+str(r)+", mean_x = "+str(mean_x)+", mean_y = "+str(mean_y))
  #print("x_small_1 = "+str(x_small_1)+", x_small_2 = "+str(x_small_2)+", y_small_1 = "+str(y_small_1)+", y_small_2 = "+str(y_small_2))
  #print("x_large_1 = "+str(x_large_1)+", x_large_2 = "+str(x_large_2)+", y_large_1 = "+str(y_large_1)+", y_large_2 = "+str(y_large_2))
  for j in range(int(y_large_1)+1, int(y_large_2)+1):
    for i in range(int(x_large_1)+1, int(x_large_2)+1):
      x = h_image.GetXaxis().GetBinCenter(i)
      y = h_image.GetYaxis().GetBinCenter(j)
      if (x>x_large_1 and x<x_large_2 and y>y_large_1 and y<y_large_2 and not(x>x_small_1 and x<x_small_2 and y>y_small_1 and y<y_small_2)):
        radius = math.sqrt((x-mean_x)**2 + (y-mean_y)**2)
        if (radius>r and radius<r+dr):
          sum_T += v_v_image[j][i]
          h_T_rs.Fill(r/scale, v_v_image[j][i])
          #print("i = "+str(i)+", j = "+str(j))
  print("sum_T = "+str(sum_T))
  g_T_rs.SetPoint(point, r/scale, sum_T)
  point += 1
c_T_rs = ROOT.TCanvas("c_T_rs", "c_T_rs", 700, 700)
g_T_rs.Draw("AL*")
c_T_rs.SaveAs("c_T_rs_"+crocName+".png")
g_T_rs.SaveAs("g_T_rs_"+crocName+".root")

c_h_T_rs = ROOT.TCanvas("c_h_T_rs", "c_h_T_rs", 700, 700)
h_T_rs.Draw("EP*")
h_T_rs.SaveAs("h_T_rs_"+crocName+".root")

input()
