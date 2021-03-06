import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,num2date
import cPickle as pickle
import dimarray as da

try:
	os.chdir('/Users/peterpfleiderer/Projects/Persistence/')
except:
	os.chdir('/p/projects/ikiimp/HAPPI/HAPPI_Peter/')


def counter_to_list(counter):
	tmp=[]
	lengths=counter.keys()
	if 0 in lengths:
		lengths.remove(0)
	if len(lengths)>2:
		for key in lengths:
			for i in range(counter[key]):
				tmp.append(key)
		tmp=np.array(tmp)
		return -tmp[tmp<0],tmp[tmp>0]
	else:
		return [],[]

def quantile_from_cdf(x,qu):
	counts, bin_edges = np.histogram(x, bins=range(0,max(x)+1), normed=True)
	cdf = np.cumsum(counts)

	quantiles=[]
	for q in qu:
		if q>=1:q/=100.
		x1=np.where(cdf<q)[0][-1]
		quantiles.append(x1+(q-cdf[x1])/(cdf[x1+1]-cdf[x1]))

	return quantiles

model='EOBS'
print model

scenarios=['All-Hist']
seasons=['MAM','JJA','SON','DJF','year']
thresholds=range(1,31)

state_dict = {
	'warm':'tg',
	'dry':'rr',
	'5mm':'rr',
	'10mm':'rr',
	'dry-warm':'cpd',
	}

for state,style in state_dict.items():

	big_dict={}
	for scenario in scenarios:
		pkl_file = open('data/'+model+'/'+style+'_'+model+'_'+scenario+'_'+state+'_counter.pkl', 'rb')
		big_dict[scenario] = pickle.load(pkl_file)	;	pkl_file.close()

	lat=big_dict[scenario]['lat']
	lon=big_dict[scenario]['lon']

	if 'ExceedanceProb' not in globals():
		ExceedanceProb=da.DimArray(axes=[np.asarray(scenarios),np.asarray(seasons),np.asarray(state_dict.keys()),np.asarray(thresholds),lat,lon], dims=['scenario','season','state','period_length','lat','lon'])

	for scenario in scenarios:
		distr_dict = big_dict[scenario]

		for iy in range(len(lat)):
			for ix in range(len(lon)):
				grid_cell=distr_dict[str(lat[iy])+'_'+str(lon[ix])]
				grid_cell['year']=grid_cell['MAM']+grid_cell['JJA']+grid_cell['SON']+grid_cell['DJF']

		for season in seasons:
			print '\n'+season
			for iy in range(len(lat)):
				sys.stdout.write('.')	;	sys.stdout.flush()
				for ix in range(len(lon)):
					counter=distr_dict[str(lat[iy])+'_'+str(lon[ix])][season]
					if len(counter)>3:
						neg,pos=counter_to_list(counter)
						for threshold in thresholds:
							ExceedanceProb[scenario,season,state,threshold,lat[iy],lon[ix]]= len(np.where(pos>threshold)[0])/float(len(pos))


ds=da.Dataset({'ExceedanceProb':ExceedanceProb})
ds.write_nc('data/'+model+'/'+model+'_EsceedanceProb_gridded.nc', mode='w')
