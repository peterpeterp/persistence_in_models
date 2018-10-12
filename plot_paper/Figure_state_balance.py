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

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", sns.color_palette("cubehelix", 8)[::-1])
cmap_change = matplotlib.colors.LinearSegmentedColormap.from_list("", [sns.color_palette("colorblind")[0],'white',sns.color_palette("colorblind")[4]])

os.chdir('/Users/peterpfleiderer/Projects/Persistence')

season='JJA'

color_range={'warm':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			'cold':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			'dry':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			'wet':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			'dry-warm':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			'wet-cold':{'mean':(-0.25,0.25),'qu_95':(-0.5,0.5)},
			}

# ------------------- cold-warm mean
plt.close('all')
asp=0.5
fig,axes = plt.subplots(nrows=5,ncols=2,figsize=(8,4),subplot_kw={'projection': ccrs.Robinson(central_longitude=0, globe=None)}, gridspec_kw = {'height_ratios':[1,4,4,4,4]})

for ax in axes[0,:]:
	ax.outline_patch.set_edgecolor('white')

for ax in axes[1:,:].flatten():
	ax.coastlines(edgecolor='black')
	ax.set_extent([-180,180,0,80],crs=ccrs.PlateCarree())

for style,state_,state,row in zip(['pr','pr','cpd','cpd'],[-1,1,1,-1],['dry','wet','dry-warm','wet-cold'],range(1,5)):

	ax= axes[row,0]

	ensemble=np.zeros([4,180,360])*np.nan
	for model,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],range(4)):
		state_days = da.read_nc('data/'+model+'/state_stats/'+'_'.join([style,model,'All-Hist','numberState'+str(state_)+'_1x1.nc']))['qu']
		days = da.read_nc('data/'+model+'/state_stats/'+'_'.join(['pr',model,'All-Hist','numberDays_1x1.nc']))['qu']
		ensemble[i,:,:] = state_days.ix[2,:,:] / days.ix[2,:,:] * state_ * 100


	lat,lon = state_days.lat,state_days.lon
	lon=np.roll(lon,len(lon)/2)


	to_plot=np.roll(np.nanmean(ensemble,axis=0),len(lon)/2,axis=-1)
	im=ax.pcolormesh(lon,lat,to_plot ,cmap=cmap,transform=ccrs.PlateCarree());
	ax.annotate(state+'\n'+stat, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')
	cb=fig.colorbar(im,orientation='vertical',label='',ax=ax)
	tick_locator = matplotlib.ticker.MaxNLocator(nbins=5)
	cb.locator = tick_locator
	cb.update_ticks()

for style,state_,state,row in zip(['pr','pr','cpd','cpd'],[-1,1,1,-1],['dry','wet','dry-warm','wet-cold'],range(1,5)):

	ax= axes[row,1]

	ensemble=np.zeros([4,180,360])*np.nan
	for model,i in zip(['MIROC5','NorESM1','ECHAM6-3-LR','CAM4-2degree'],range(4)):
		state_days = da.read_nc('data/'+model+'/state_stats/'+'_'.join([style,model,'All-Hist','numberState'+str(state_)+'_1x1.nc']))['qu']
		days = da.read_nc('data/'+model+'/state_stats/'+'_'.join(['pr',model,'All-Hist','numberDays_1x1.nc']))['qu']
		frac_hist = state_days.ix[2,:,:] / days.ix[2,:,:] * state_ * 100

		state_days = da.read_nc('data/'+model+'/state_stats/'+'_'.join([style,model,'Plus20-Future','numberState'+str(state_)+'_1x1.nc']))['qu']
		days = da.read_nc('data/'+model+'/state_stats/'+'_'.join(['pr',model,'Plus20-Future','numberDays_1x1.nc']))['qu']
		frac_fu = state_days.ix[2,:,:] / days.ix[2,:,:] * state_ * 100

		ensemble[i,:,:] = frac_fu -frac_hist

	lat,lon = state_days.lat,state_days.lon
	lon=np.roll(lon,len(lon)/2)

	to_plot=np.roll(np.nanmean(ensemble,axis=0),len(lon)/2,axis=-1)
	im=ax.pcolormesh(lon,lat,to_plot ,cmap=cmap_change,transform=ccrs.PlateCarree() ,vmin=-5 , vmax=5);
	ax.annotate(state+'\n'+stat, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')
	cb=fig.colorbar(im,orientation='vertical',label='',ax=ax)
	tick_locator = matplotlib.ticker.MaxNLocator(nbins=5)
	cb.locator = tick_locator
	cb.update_ticks()

plt.annotate(s='changes in mean persistence [days]', xy=(0.5,0.5), xycoords='figure fraction',va='center', ha='center',fontsize=12,rotation='90')
plt.annotate(s='changes in 95th percentile of persistence [days]', xy=(0.97,0.5), xycoords='figure fraction',va='center', ha='center',fontsize=12,rotation='90')

plt.suptitle('ensemble mean difference +2$^\circ$C vs 2006-2015', fontweight='bold')
fig.tight_layout()
plt.savefig('plots/paper/Figure_state_percentage.png',dpi=300)


#sdasd
