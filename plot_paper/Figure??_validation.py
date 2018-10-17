import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,num2date
import matplotlib.pylab as plt
import matplotlib
import dimarray as da
from statsmodels.sandbox.stats import multicomp
import seaborn as sns
sns.set()
import cartopy.crs as ccrs
import cartopy

cmap = {'tas': matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","darksalmon","darkred"]),
		'pr': matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","yellow","saddlebrown"]),
		'cpd': matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","pink","darkmagenta"])}

os.chdir('/Users/peterpfleiderer/Projects/Persistence')

obs_eobs={}
for style in ['tas','pr','cpd']:
	obs_eobs[style] = da.read_nc('data/EOBS/'+style+'_EOBS_SummaryMeanQu.nc')['SummaryMeanQu']

obs_had={}
for style in ['tas']:
	obs_had[style] = da.read_nc('data/HadGHCND/HadGHCND_SummaryMeanQu.nc')['SummaryMeanQu']

if 'models' not in globals():
	models={}
	for style in ['tas','pr','cpd']:
		models[style]={}
		for model in ['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree']:
			models[style][model]=da.read_nc('data/'+model+'/'+style+'_'+model+'_SummaryMeanQu_1x1.nc')


season='JJA'

color_range={'warm':{'mean':(3,7),'qu_95':(5,20)},
			'cold':{'mean':(3,7),'qu_95':(5,20)},
			'dry':{'mean':(3,14),'qu_95':(5,20)},
			'wet':{'mean':(1,4),'qu_95':(2,10)},
			'dry-warm':{'mean':(1,4),'qu_95':(5,14)},
			'wet-cold':{'mean':(1,4),'qu_95':(4,10)},
			}

# ------------------- other
for stat,title in zip(['mean','qu_95'],['Mean','95th percentile of']):
	plt.close('all')
	fig,axes = plt.subplots(nrows=4,ncols=3,figsize=(7,3),subplot_kw={'projection': ccrs.Robinson(central_longitude=0, globe=None)}, gridspec_kw = {'height_ratios':[1,10,10,10],'width_ratios':[6,2,7]})

	for ax in list(axes[0,:].flatten()) :
		ax.outline_patch.set_edgecolor('white')

	for style,state,row in zip(['tas','pr','cpd'],['warm','dry','dry-warm'],range(1,4)):
		for name,data,ax in zip(['HadGHCND','EOBS','HAPPI'],[obs_had,obs_eobs,models],axes[row,:]):
			if name == 'EOBS':
				ax.set_extent([-15,60,10,80],crs=ccrs.PlateCarree())
			else:
				ax.set_extent([-15,345,10,80],crs=ccrs.PlateCarree())

			if name == 'HAPPI':
				ensemble=np.zeros([4,180,360])*np.nan
				for model,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],range(4)):
					ensemble[i,:,:]=models[style][model]['*'.join(['All-Hist',season,state,stat])]
				to_plot=models[style][model]['*'.join(['All-Hist',season,state,stat])].copy()
				to_plot.values=np.roll(np.nanmean(ensemble,axis=0),180,axis=-1)
				to_plot.lon=np.roll(to_plot.lon,180,axis=-1)
			elif (name=='HadGHCND' and style=='pr')==False and (name=='HadGHCND' and style=='cpd')==False:
				to_plot=data[style]['All-Hist',season,state,stat]

			if (name=='HadGHCND' and style=='pr')==False and (name=='HadGHCND' and style=='cpd')==False:
				ax.annotate(name, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')
				crange=color_range[state][stat]
				im[stat]=ax.pcolormesh(to_plot.lon,to_plot.lat,to_plot ,vmin=crange[0],vmax=crange[1],cmap=cmap[style],transform=ccrs.PlateCarree());
				ax.coastlines(color='black')
			else:
				print(name,style)
				ax.coastlines(color='white')
				ax.outline_patch.set_edgecolor('white')

		#cbar_ax=fig.add_axes([0.1,0.1,0.8,0.4])
		#cbar_ax.axis('off')
		cb=fig.colorbar(im[stat],orientation='vertical',label=state,ax=ax) #95th percentile\n persistence [days]
		tick_locator = matplotlib.ticker.MaxNLocator(nbins=5)
		cb.locator = tick_locator
		cb.update_ticks()

	plt.suptitle(title+' persistence', fontweight='bold')
	fig.tight_layout()
	plt.savefig('plots/paper/Figure??_validation_'+stat+'.png',dpi=300)
