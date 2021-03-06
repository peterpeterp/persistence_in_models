from __future__ import print_function
import sys

if (sys.version_info > (3, 0)):
  from urllib.request import urlretrieve
else:
  from urllib import urlretrieve
def hook(a,b,c): print(a*b,"/",c, "\r", end="")

import os,sys,glob,time,collections,signal,gc

os.chdir('/p/projects/ikiimp/HAPPI/HAPPI_Peter')

sys.path.append('persistence_in_HAPPI/')
import __settings
model_dict=__settings.model_dict

model = 'MIROC5'
scenario = 'Plus20-Future'
var = 'tas'

os.system('mkdir -p raw_data/'+model+'/'+scenario+'/'+var+'/tmp')
os.chdir('raw_data/'+model+'/'+scenario+'/'+var)

for run in model_dict[model]['runs'][scenario]:
    if os.path.isfile("tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21060101-21161231.nc") == False:

        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21060101-21061231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21060101-21061231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21060101-21061231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21070101-21071231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21070101-21071231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21070101-21071231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21080101-21081231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21080101-21081231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21080101-21081231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21090101-21091231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21090101-21091231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21090101-21091231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21100101-21101231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21100101-21101231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21100101-21101231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21110101-21111231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21110101-21111231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21110101-21111231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21120101-21121231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21120101-21121231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21120101-21121231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21130101-21131231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21130101-21131231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21130101-21131231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21140101-21141231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21140101-21141231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21140101-21141231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21150101-21151231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21150101-21151231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21150101-21151231.nc", hook)
        print('\n')
        print("downloading: tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21160101-21161231.nc")
        urlretrieve("http://portal.nersc.gov/cascade/data/rtrack.php?source=NERSCDisk&filename=MIROC/MIROC5/Plus20-Future/CMIP5-MMM-est1/v2-0/day/atmos/tas/"+run+"/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21160101-21161231.nc","tmp/tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21160101-21161231.nc", hook)
        print('\n')

        os.system("cdo mergetime tmp/* tas_Aday_MIROC5_Plus20-Future_CMIP5-MMM-est1_v2-0_"+run+"_21060101-21161231.nc")
        os.system("rm tmp/*")
