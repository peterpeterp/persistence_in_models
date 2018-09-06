import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import cPickle as pickle
import seaborn as sns
import matplotlib.pylab as plt
import dimarray as da
from scipy.optimize import curve_fit
from lmfit import  Model
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy import stats

os.chdir('/Users/peterpfleiderer/Documents/Projects/Scripts/allgemeine_scripte')
#import plot_map as plot_map; reload(plot_map)
import srex_overview as srex_overview; reload(srex_overview)
os.chdir('/Users/peterpfleiderer/Documents/Projects/Persistence')

try:
	os.chdir('/Users/peterpfleiderer/Documents/Projects/Persistence/')
except:
	os.chdir('/global/homes/p/pepflei/')

pkl_file = open('data/srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

big_dict_dry={}
for dataset in ['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree']:
	pkl_file = open('data/'+dataset+'/pr_'+dataset+'_regional_distrs_wavePolys.pkl', 'rb')
	big_dict_dry[dataset]=region_dict = pickle.load(pkl_file)	;	pkl_file.close()
	pkl_file = open('data/'+dataset+'/pr_'+dataset+'_regional_distrs_mid-lat.pkl', 'rb')
	big_dict_dry[dataset]['NHml']=pickle.load(pkl_file)['mid-lat']	;	pkl_file.close()


big_dict={}
for dataset in ['HadGHCND','MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree']:
	pkl_file = open('data/'+dataset+'/'+dataset+'_regional_distrs_wavePolys.pkl', 'rb')
	big_dict[dataset]=region_dict = pickle.load(pkl_file)	;	pkl_file.close()
	pkl_file = open('data/'+dataset+'/'+dataset+'_regional_distrs_mid-lat.pkl', 'rb')
	big_dict[dataset]['NHml']=pickle.load(pkl_file)['mid-lat']	;	pkl_file.close()

NH_regs={'box1':{'hatch':' ','color':'darkgreen','pos_off':(+0,+0),'summer':'JJA','winter':'DJF'},
		'box2':{'hatch':' ','color':'darkgreen','pos_off':(+0,+0),'summer':'JJA','winter':'DJF'},
		'box3':{'hatch':' ','color':'darkgreen','pos_off':(+0,-0),'summer':'JJA','winter':'DJF'},
		'NHml':{'hatch':'///','color':'white','pos':(-142,37),'xlabel':'period length [days]','ylabel':'change in exceedence\nprobability [%]','title':'','summer':'JJA','winter':'DJF','scaling_factor':1.3}}

all_regs=NH_regs.copy()

polygons={'box1':{'points':[(-117.5,35),(-90,35),(-90,60),(-117.5,60)]},
			'box2':{'points':[(-17.5,35),(12.5,35),(12.5,60),(-17.5,60)]},
			'box3':{'points':[(43.5,35),(65,35),(65,60),(43.5,60)]},
			}
polygons['NHml']={'points':[(-180,35),(180,35),(180,60),(-180,60)]}

maincolor='darkmagenta'

scenario_dict={'HadGHCND':{'early':'1954-1974','late':'1990-2010'},
				'MIROC5':{'early':'All-Hist','late':'Plus20-Future'},
				'NorESM1':{'early':'All-Hist','late':'Plus20-Future'},
				'CAM4-2degree':{'early':'All-Hist','late':'Plus20-Future'},
				'ECHAM6-3-LR':{'early':'All-Hist','late':'Plus20-Future'},
}

# ---------------------------- changes
def legend_plot(subax):
	subax.axis('off')
	# subax.fill_between([1,1],[1,1],[1,1],label='warm persistence',facecolor=maincolor,alpha=0.3)
	subax.plot([1,1],[1,1],label='warm persistence',color=maincolor)
	# subax.fill_between([1,1],[1,1],[1,1],label='dry persistence',facecolor='darkorange',alpha=0.3)
	subax.plot([1,1],[1,1],label='dry persistence',color='darkorange')
	subax.plot([1,1],[1,1],label='historical warm persistence',color='darkcyan')
	subax.legend(loc='lower right',fontsize=9,ncol=1)

def axis_settings(subax,label='off'):
	subax.set_xlim((0,40))
	subax.set_ylim((-50,50))
	subax.plot([0,40],[0,0],'k')
	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom=label,labelsize=8)
	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft=label,labelsize=8)
	subax.locator_params(axis = 'y', nbins = 5)
	subax.locator_params(axis = 'x', nbins = 5)
	return(subax)

def scenario_diff(subax,region,arg1=None,arg2=None,arg3=None):
	season=all_regs[region][arg1]
	ensemble=np.zeros([4,40])*np.nan
	for dataset,color,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['blue','green','magenta','orange'],range(4)):
		tmp_20=big_dict[dataset][region]['Plus20-Future'][season][arg2]
		tmp_h=big_dict[dataset][region]['All-Hist'][season][arg2]
		count_20=np.array([np.sum(tmp_20['count'][ii:])/float(np.sum(tmp_20['count'])) for ii in range(len(tmp_20['count']))])
		count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
		nmax=min(len(count_20),len(count_h),40)
		tmp=(count_20[0:nmax]-count_h[0:nmax])/count_h[0:nmax]*100
		ensemble[i,:nmax]=tmp
	subax.plot(range(1,nmax+1),np.nanmean(ensemble,axis=0),color=maincolor)
	subax.fill_between(range(1,nmax+1),np.nanmin(ensemble,axis=0),np.nanmax(ensemble,axis=0),facecolor=maincolor,alpha=0.3)

	ensemble=np.zeros([4,40])*np.nan
	for dataset,color,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['blue','green','magenta','orange'],range(4)):
		tmp_20=big_dict_dry[dataset][region]['Plus20-Future'][season]['dry']
		tmp_h=big_dict_dry[dataset][region]['All-Hist'][season]['dry']
		count_20=np.array([np.sum(tmp_20['count'][ii:])/float(np.sum(tmp_20['count'])) for ii in range(len(tmp_20['count']))])
		count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
		nmax=min(len(count_20),len(count_h),40)
		tmp=(count_20[0:nmax]-count_h[0:nmax])/count_h[0:nmax]*100
		ensemble[i,:nmax]=tmp
	subax.plot(range(1,nmax+1),np.nanmean(ensemble,axis=0),color='darkorange')
	subax.fill_between(range(1,nmax+1),np.nanmin(ensemble,axis=0),np.nanmax(ensemble,axis=0),facecolor='darkorange',alpha=0.3)

	tmp_20=big_dict['HadGHCND'][region]['1990-2010'][season][arg2]
	tmp_h=big_dict['HadGHCND'][region]['1954-1974'][season][arg2]
	count_20=np.array([np.sum(tmp_20['count'][ii:])/float(np.sum(tmp_20['count'])) for ii in range(len(tmp_20['count']))])
	count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
	nmax=min(len(count_20),len(count_h),40)
	tmp=(count_20[0:nmax]-count_h[0:nmax])/count_h[0:nmax]*100
	subax.plot(range(1,nmax+1),tmp,color='darkcyan')

	subax=axis_settings(subax)
	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points')



fig,ax_map=srex_overview.srex_overview(scenario_diff,axis_settings,polygons=polygons,reg_info=all_regs,arg1='summer',arg2='warm',x_ext=[-180,180],y_ext=[0,85],small_plot_size=0.08,legend_plot=legend_plot, legend_pos=[163,70], title='Relative change in probability of exceeding warm period lengths in JJA')
plt.savefig('plots/Figure3b_boxes.png',dpi=600)