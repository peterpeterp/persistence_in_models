import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import cPickle as pickle
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




#region_dict=get_regional_distribution('HadGHCND',scenarios=['All-Hist'])

big_dict={}
for dataset in ['HadGHCND','MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree']:
	pkl_file = open('data/'+dataset+'/'+dataset+'_regional_distrs_srex.pkl', 'rb')
	big_dict[dataset]=region_dict = pickle.load(pkl_file)	;	pkl_file.close()
	pkl_file = open('data/'+dataset+'/'+dataset+'_regional_distrs_mid-lat-SH.pkl', 'rb')
	big_dict[dataset]['SHml']=pickle.load(pkl_file)['mid-lat']	;	pkl_file.close()
	pkl_file = open('data/'+dataset+'/'+dataset+'_regional_distrs_mid-lat.pkl', 'rb')
	big_dict[dataset]['NHml']=pickle.load(pkl_file)['mid-lat']	;	pkl_file.close()



# ---------------------------- distr comparison
def legend_plot(subax):
	subax.axis('off')
	for dataset,color in zip(['HadGHCND','MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['black','blue','green','magenta','orange']):
		subax.plot([1,1],[1,1],label=dataset,c=color)
	subax.legend(loc='best',fontsize=9)

def axis_settings(subax,label='off'):
	subax.set_yscale('log')
	subax.set_xlim((0,40))
	subax.set_ylim((0.0001,0.5))
	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom=label,labelsize=8)
	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft=label,labelsize=8)
	subax.locator_params(axis = 'x', nbins = 5)
	return(subax)

def distrs(subax,region,arg1=None,arg2=None,arg3=None):
	season=all_regs[region][arg1]
	for dataset,color in zip(['HadGHCND','MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['black','blue','green','magenta','orange']):
		try:
			tmp=big_dict[dataset][region]['All-Hist'][season][arg2]
			count=np.asarray(tmp['count'])/float(sum(tmp['count']))
			pers=tmp['period_length']
			subax.plot(pers,count,color=color)
		except:
			pass
	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points')


NH_regs={'ALA':{'color':20,'pos_off':(-23,-2),'summer':'JJA','winter':'DJF'},
		'WNA':{'color':40,'pos_off':(-8,+14),'summer':'JJA','winter':'DJF'},
		'CNA':{'color':60,'pos_off':(0,0),'summer':'JJA','winter':'DJF'},
		'ENA':{'color':20,'pos_off':(+10,0),'summer':'JJA','winter':'DJF'},
		'CGI':{'color':80,'pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},
		'CAM':{'color':80,'summer':'JJA','winter':'DJF'},

		'NEU':{'color':20,'pos_off':(-13,+0),'summer':'JJA','winter':'DJF'},
		'CEU':{'color':40,'pos_off':(+10,+5),'summer':'JJA','winter':'DJF'},
		'CAS':{'color':20,'pos_off':(+0,+10),'summer':'JJA','winter':'DJF'},
		'NAS':{'color':60,'summer':'JJA','winter':'DJF'},
		'TIB':{'color':80,'pos_off':(+0,-14),'summer':'JJA','winter':'DJF'},
		'EAS':{'color':20,'summer':'JJA','winter':'DJF'},

		'MED':{'color':60,'pos_off':(-15,-5),'summer':'JJA','winter':'DJF'},
		'WAS':{'color':80,'pos_off':(-5,-5),'summer':'JJA','winter':'DJF'},
		'NHml':{'color':20,'pos':(-140,30),'xlabel':'days','ylabel':'PDF','title':'','summer':'JJA','winter':'DJF','scaling_factor':1.5}}

SH_regs={'WSA':{'color':20,'pos':(-90,-30),'summer':'DJF','winter':'JJA'},
		'SSA':{'color':40,'pos':(-50,-45),'summer':'DJF','winter':'JJA'},
		'SAF':{'color':60,'summer':'DJF','winter':'JJA'},
		'NAU':{'color':80,'pos_off':(-5,+5),'summer':'DJF','winter':'JJA'},
		'SAU':{'color':20,'pos':(150,-45),'summer':'DJF','winter':'JJA'},
		'SHml':{'color':20,'pos':(-140,-30),'xlabel':'days','ylabel':'PDF','title':'','summer':'DJF','winter':'JJA','scaling_factor':1.5}}

all_regs=NH_regs.copy()
all_regs.update(SH_regs)

polygons=srex.copy()
polygons['SHml']={'points':[(-180,-23),(180,-23),(180,-66),(-180,-66)]}
polygons['NHml']={'points':[(-180,23),(180,23),(180,66),(-180,66)]}

for season in ['summer','winter']:
	for state in ['warm','cold']:
		fig,ax_map=srex_overview.srex_overview(distrs,axis_settings,polygons=polygons,reg_info=all_regs,arg1=season,arg2=state,x_ext=[-180,180],y_ext=[-64,80],small_plot_size=0.08,legend_plot=legend_plot,legend_pos=[93,-30])
		ax_map.plot([-180,180],[0,0],linewidth=3,color='k')
		ax_map.text(164,8,{'summer':'JJA','winter':'DJF'}[season],fontsize=15,verticalalignment='center')
		ax_map.text(164,-8,{'summer':'DJF','winter':'JJA'}[season],fontsize=15,verticalalignment='center')
		plt.savefig('plots/distrs_'+season+'_'+state+'.png',dpi=600)

# ---------------------------- changes
def legend_plot(subax):
	subax.axis('off')
	for dataset,color in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['blue','green','magenta','orange']):
		subax.fill_between([1,1],[1,1],[1,1],label=dataset,facecolor=color,alpha=0.3)
	subax.legend(loc='best',fontsize=9)

def axis_settings(subax,label='off'):
	subax.set_xlim((0,30))
	subax.set_ylim((-10,10))
	subax.plot([0,40],[0,0],'k')
	subax.tick_params(axis='x',which='both',bottom='on',top='on',labelbottom=label,labelsize=8)
	subax.tick_params(axis='y',which='both',left='on',right='on',labelleft=label,labelsize=8)
	subax.locator_params(axis = 'y', nbins = 5)
	subax.locator_params(axis = 'x', nbins = 5)
	return(subax)

def scenario_diff(subax,region,arg1=None,arg2=None,arg3=None):
	season=all_regs[region][arg1]
	for dataset,color in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],['blue','green','magenta','orange']):
		tmp_20=big_dict[dataset][region]['Plus20-Future'][season][arg2]
		tmp_h=big_dict[dataset][region]['All-Hist'][season][arg2]
		count_20=np.asarray(tmp_20['count'])/float(np.nansum(tmp_20['count']))
		count_h=np.asarray(tmp_h['count'])/float(np.nansum(tmp_h['count']))
		nmax=min(len(count_20),len(count_h),40)
		subax.fill_between(tmp_h['period_length'][0:nmax],(count_20[0:nmax]-count_h[0:nmax])/count_h[0:nmax]*100,tmp_h['period_length'][0:nmax]*0,facecolor=color,alpha=0.3)
	subax=axis_settings(subax)
	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', fontsize=10,xytext=(-5, 5), textcoords='offset points')


for season in ['summer','winter']:
	for state in ['warm','cold']:
		fig,ax_map=srex_overview.srex_overview(scenario_diff,axis_settings,polygons=polygons,reg_info=all_regs,arg1=season,arg2=state,x_ext=[-180,180],y_ext=[-64,80],small_plot_size=0.08,legend_plot=legend_plot,legend_pos=[93,-30])
		ax_map.plot([-180,180],[0,0],linewidth=3,color='k')
		ax_map.text(164,8,{'summer':'JJA','winter':'DJF'}[season],fontsize=15,verticalalignment='center')
		ax_map.text(164,-8,{'summer':'DJF','winter':'JJA'}[season],fontsize=15,verticalalignment='center')
		plt.savefig('plots/distr_diff_'+season+'_'+state+'.png',dpi=600)