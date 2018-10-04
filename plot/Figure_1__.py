import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,num2date
import cPickle as pickle
import dimarray as da
from scipy.optimize import curve_fit
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy import stats

import matplotlib.pylab as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns
sns.set_style("whitegrid")
import matplotlib.ticker as mticker

sys.path.append('/Users/peterpfleiderer/Projects/allgemeine_scripte')
import srex_overview as srex_overview; reload(srex_overview)
os.chdir('/Users/peterpfleiderer/Projects/Persistence')

try:
	os.chdir('/Users/peterpfleiderer/Projects/Persistence/')
except:
	os.chdir('/global/homes/p/pepflei/')

pkl_file = open('data/srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

if 'big_dict' not in globals():
	big_dict={}
	for style in ['tas','pr','cpd']:
		big_dict[style]={}
		for dataset in ['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree','HadGHCND','EOBS']:
			infile = 'data/'+dataset+'/'+dataset+'_regional_distrs_srex.pkl'
			if os.path.isfile(infile):
				pkl_file=open(infile, 'rb')
				big_dict[style][dataset] = pickle.load(pkl_file);	pkl_file.close()
			infile = 'data/'+dataset+'/'+dataset+'_regional_distrs_mid-lat.pkl'
			if os.path.isfile(infile):
				pkl_file=open(infile, 'rb')
				big_dict[style][dataset]['NHml'] = pickle.load(pkl_file)['mid-lat'];	pkl_file.close()

			infile = 'data/'+dataset+'/'+style+'_'+dataset+'_regional_distrs_srex.pkl'
			if os.path.isfile(infile):
				pkl_file=open(infile, 'rb')
				big_dict[style][dataset] = pickle.load(pkl_file);	pkl_file.close()
			infile = 'data/'+dataset+'/'+style+'_'+dataset+'_regional_distrs_mid-lat.pkl'
			if os.path.isfile(infile):
				pkl_file=open(infile, 'rb')
				big_dict[style][dataset]['NHml'] = pickle.load(pkl_file)['mid-lat'];	pkl_file.close()

NH_regs={'ALA':{'color':'darkgreen','pos_off':(+10,+7),'summer':'JJA','winter':'DJF'},
		'WNA':{'color':'darkblue','pos_off':(+20,+15),'summer':'JJA','winter':'DJF'},
		'CNA':{'color':'gray','pos_off':(+8,-4),'summer':'JJA','winter':'DJF'},
		'ENA':{'color':'darkgreen','pos_off':(+18,-5),'summer':'JJA','winter':'DJF'},
		'CGI':{'color':'darkcyan','pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},
		'CAM':{'color':'darkcyan','pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},

		'NEU':{'color':'darkgreen','pos_off':(-13,+0),'summer':'JJA','winter':'DJF'},
		'CEU':{'color':'darkblue','pos_off':(+9,+5),'summer':'JJA','winter':'DJF'},
		'CAS':{'color':'darkgreen','pos_off':(-8,+10),'summer':'JJA','winter':'DJF'},
		'NAS':{'color':'gray','summer':'JJA','winter':'DJF'},
		'TIB':{'color':'darkcyan','pos_off':(+2,-4),'summer':'JJA','winter':'DJF'},
		'EAS':{'color':'darkgreen','summer':'JJA','winter':'DJF'},

		'MED':{'color':'gray','pos_off':(-15,-5),'summer':'JJA','winter':'DJF'},
		'WAS':{'color':'darkcyan','pos_off':(-5,-5),'summer':'JJA','winter':'DJF'},
		'NHml':{'edge':'darkblue','color':'none','alpha':1,'pos':(-142,28),'xlabel':'period length [days]','ylabel':'exceedence probability [%]','title':'','summer':'JJA','winter':'DJF','scaling_factor':1.3}}

all_regs=NH_regs.copy()

polygons=srex.copy()
polygons['NHml']={'points':[(-180,23),(180,23),(180,66),(-180,66)]}

colors=['black']+sns.color_palette("colorblind", 4)

# ---------------------------- changes
def legend_plot(subax,arg1=None,arg2=None,arg3=None,arg4=None):
	subax.axis('off')
	legend_elements=[]
	legend_elements.append(Line2D([0], [0], color='w', label='HadGHCND'))
	legend_elements.append(Line2D([0], [0], color='w', linestyle='--', label='EOBS'))
	legend_elements.append(Patch(facecolor='w', alpha=0.3, label='Model Spread'))
	for style,state,color in zip(arg2,arg3,arg4):
		# legend_elements.append(Line2D([0], [0], color='w', label=state))
		legend_elements.append(Line2D([0], [0], color=color, label=' '))
		legend_elements.append(Line2D([0], [0], color=color, linestyle='--', label=' '))
		legend_elements.append(Patch(facecolor=color,alpha=0.3, label=' '))


	#subax.legend(handles=legend_elements ,title='                                     '+arg3[0]+'        '+arg3[1]+'       '+arg3[2] ,loc='lower right',fontsize=9,ncol=4, frameon=True, facecolor='w', framealpha=1, edgecolor='w').set_zorder(1)


def axis_settings(subax,label='off',arg1=None,arg2=None,arg3=None,arg4=None):
	subax.set_yscale('log')
	subax.set_xlim((0,35))
	subax.set_ylim((0.0001,1))
	subax.set_xticks([7,14,21,28,35])
	subax.tick_params(axis='x',which='both',bottom=True,top=True,labelbottom=label,labelsize=8)
	#subax.set_yticks([0.0001,0.001,0.01,0.1,1])
	#subax.tick_params(axis='y',which='both',left=True,right=True,labelleft=label,labelsize=8)
	#locmin = mticker.LogLocator(base=10, subs=[1.0])
	#subax.yaxis.set_minor_locator(locmin)
	#subax.yaxis.set_minor_formatter(mticker.NullFormatter())
	#subax.yaxis.get_label().set_backgroundcolor('w')
	#for tick in subax.yaxis.get_major_ticks():
	#	tick.label.set_backgroundcolor('w')
	subax.grid(True,which="both",ls="--",c='gray',lw=0.5)
	return(subax)

#model_data=da.read_nc('data/CAM4-2dgree/tas_CAM4-2degree_All-Hist_distrs.nc')['distrs']

def distrs(subax,region,arg1=None,arg2=None,arg3=None,arg4=None):
	season=all_regs[region][arg1]
	for style,state,color in zip(arg2,arg3,arg4):
		ensemble=np.zeros([4,35])*np.nan
		nmax=35
		for dataset,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],range(4)):
			tmp_h=big_dict[style][dataset][region]['All-Hist'][season][state]
			count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
			nmax=min(nmax,len(count_h))
			ensemble[i,:nmax]=count_h[0:nmax]
			#subax.plot(range(1,nmax+1),ensemble[i,:nmax])
		#subax.plot(range(1,nmax+1),np.nanmean(ensemble[:,0:nmax],axis=0),color=color,linestyle=':')
		subax.fill_between(range(1,nmax+1),np.nanmin(ensemble[:,0:nmax],axis=0),np.nanmax(ensemble[:,0:nmax],axis=0),facecolor=color,alpha=0.3)

	tmp = model_data[region,1,1,:,:].copy()
	excee = model_data[region,1,1,:,:].copy()
	for i in model_data.length:
		excee[:,i]=np.nansum(tmp[:,i:],axis=1) / np.array(np.nansum(tmp[:,:],axis=1),np.float)

	percentiles=np.nanpercentile( excee,[0,1/6.*100,50,5/6.*100,100],axis=0)
	subax.fill_between(model_data.length,percentiles[0,:],percentiles[4,:],facecolor='darkorange',alpha=0.3)
	subax.plot(model_data.length,percentiles[2,:],color='darkorange',linestyle=':')

	tmp_h=big_dict['tas']['HadGHCND'][region]['All-Hist'][season][arg3[0]]
	count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
	subax.plot(range(1,len(count_h)+1),count_h,color=arg4[0])

	for style,state,color in zip(arg2,arg3,arg4):
		if region in ['CEU','NEU','MED','WAS']:
			tmp_h=big_dict[style]['EOBS'][region]['All-Hist'][season][state]
			count_h=np.array([np.sum(tmp_h['count'][ii:])/float(np.sum(tmp_h['count'])) for ii in range(len(tmp_h['count']))])
			subax.plot(range(1,len(count_h)+1),count_h,color=color,linestyle='--')

	subax.annotate('   '+region, xy=(0, 0), xycoords='axes fraction', color=all_regs[region]['color'], weight='bold', fontsize=10,xytext=(-5, 5), textcoords='offset points')


fig,ax_map=srex_overview.srex_overview(distrs, axis_settings, polygons=polygons, reg_info=all_regs, x_ext=[-180,180], y_ext=[0,85], small_plot_size=0.08, legend_plot=legend_plot, legend_pos=[164,9], \
	arg1='summer', arg2=['tas'], arg3=['warm'], arg4=sns.color_palette("hls", 3), title='exceedance probabilites of persistence in JJA')
plt.savefig('plots/paper/Figure1_a__.png',dpi=600)

# fig,ax_map=srex_overview.srex_overview(distrs, axis_settings, polygons=polygons, reg_info=all_regs, x_ext=[-180,180], y_ext=[0,85], small_plot_size=0.08, legend_plot=legend_plot, legend_pos=[164,9], \
# 	arg1='summer', arg2=['tas','pr','cpd'], arg3=['cold','wet','wet-cold'], arg4=sns.color_palette("hls", 3), title='exceedance probabilites of persistence in JJA')
# plt.savefig('plots/paper/Figure1_b.png',dpi=600)

# fig,ax_map=srex_overview.srex_overview(distrs,axis_settings,polygons=polygons,reg_info=all_regs,arg1='summer',arg2=['cold','wet'], x_ext=[-180,180], y_ext=[0,85], small_plot_size=0.08, legend_plot=legend_plot, legend_pos=[150,12], title='exceedance probabilites for warm persistence in JJA')
# plt.savefig('plots/paper/Figure1_DJF.png',dpi=600)