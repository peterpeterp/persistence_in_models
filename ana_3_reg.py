import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import cPickle as pickle
import dimarray as da
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


import persistence_support as persistence_support; reload(persistence_support)
from persistence_support import *

try:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/HAPPI_persistence/')
except:
	os.chdir('/global/homes/p/pepflei/')

pkl_file = open('data/srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

def get_regional_distribution(dataset,scenarios=['Plus20-Future','Plus15-Future','All-Hist']):
	region_dict={}
	for region in srex.keys():	
		region_dict[region]={}
		for scenario in scenarios:
			pkl_file = open('data/'+dataset+'_'+scenario+'_counter.pkl', 'rb')
			distr_dict = pickle.load(pkl_file)	;	pkl_file.close()  
			region_dict[region][scenario]={}
			tmp={}
			for season in ['MAM','JJA','SON','DJF']:
				print region,scenario,season
				region_dict[region][scenario][season]={'cold':{},'warm':{}}
				tmp[season]=collections.Counter()
			polygon=Polygon(srex[region]['points'])
			for x in distr_dict['lon']:
				if x>180:
					x__=x-360
				else:
					x__=x
				for y in distr_dict['lat']:
					if polygon.contains(Point(x__,y)):
						for season in ['MAM','JJA','SON','DJF']:
							if len(distr_dict[str(y)+'_'+str(x)][season].keys())>10:
								tmp[season]+=distr_dict[str(y)+'_'+str(x)][season]

			for season in ['MAM','JJA','SON','DJF']:
				if len(tmp[season])>5:
					for state,state_name in zip([-1,1],['cold','warm']):
						count,pers=counter_to_pers(tmp[season],state)
						region_dict[region][scenario][season][state_name]['period_length']=pers
						region_dict[region][scenario][season][state_name]['count']=count
						region_dict[region][scenario][season]['counter']=tmp[season]

	output = open('data/'+dataset+'_regional_distrs.pkl', 'wb')
	pickle.dump(region_dict, output)
	output.close()
	return region_dict

region_dict=get_regional_distribution('CAM4')




