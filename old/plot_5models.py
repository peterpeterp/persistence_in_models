import os,sys,glob,time,collections,gc
import numpy as np
from netCDF4 import Dataset,netcdftime,num2date
import matplotlib.pylab as plt
import dimarray as da
from statsmodels.sandbox.stats import multicomp

os.chdir('/Users/peterpfleiderer/Documents/Projects/Persistence')

# sum_dict={}
#
# for model in ['MIROC5','NORESM1','ECHAM6-3-LR','CAM4-2degree']:
# 	tmp_1=da.read_nc('data/'+model+'/'+model+'_SummaryMeanQu.nc')['SummaryMeanQu']
# 	tmp_2=da.read_nc('data/'+model+'/'+model+'_SummaryKS.nc')['SummaryKS']
# 	sum_dict[model]=da.concatenate((tmp_1,tmp_2),axis='type')
#
# tmp_1=da.read_nc('data/HadGHCND/HadGHCND_SummaryMeanQu.nc')['SummaryMeanQu']
# tmp_3=da.read_nc('data/HadGHCND/HadGHCND_SummaryFit.nc')['SummaryFit']
# sum_dict['HadGHCND']=da.concatenate((tmp_1,tmp_3),axis='type')



# # _________________________ clim mean
# plt.close('all')
# plate_carree = ccrs.PlateCarree()
# asp=1.6
# fig,axes = plt.subplots(nrows=6,ncols=4,figsize=(10*asp,10),subplot_kw={'projection': plate_carree},gridspec_kw = {'height_ratios':[3,3,3,3,3,1]})
# for season,state,col in zip(['JJA','JJA','DJF','DJF'],['warm','cold','warm','cold','cold'],[0,1,2,3]):
# 	for dataset,ax in zip(['HadGHCND','MIROC5','NORESM1','ECHAM6-3-LR','CAM4-2degree'],axes[:5,col]):
# 		ax.set_global()
# 		ax.coastlines(edgecolor='black')
# 		ax.axis('off')
# 		ax.set_extent([-180,180,-66,80],crs=plate_carree)
# 		tmp=sum_dict[dataset]
#
# 		xx,yy=tmp.lon.copy(),tmp.lat.copy()
# 		x_step,y_step=np.diff(xx,1).mean(),np.diff(yy,1).mean()
# 		xx=np.append(xx-x_step,xx[-1]+x_step)
# 		yy=np.append(yy-y_step,yy[-1]+y_step)
# 		lons,lats=np.meshgrid(xx,yy)
# 		to_plot=np.asarray(tmp['All-Hist'][season][state]['mean'])
# 		im=ax.pcolormesh(lons,lats,to_plot,vmin=3,vmax=7,cmap=plt.cm.jet);
# 		ax.annotate(dataset+'\n'+season+' '+state, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')
#
#
# for ax in axes[5,:]:
# 	ax.outline_patch.set_edgecolor('white')
#
# cbar_ax=fig.add_axes([0,0.05,1,0.1])
# cbar_ax.axis('off')
# cb=fig.colorbar(im,orientation='horizontal',label='mean persistence [days]',ax=cbar_ax)
#
# #plt.suptitle('mean persistence', fontweight='bold')
# fig.tight_layout()
# plt.savefig('plots/climatology_mean_full.png',dpi=300)
#
# # ------------------- cold-warm mean
# plt.close('all')
# plate_carree = ccrs.PlateCarree()
# asp=0.8
# fig,axes = plt.subplots(nrows=6,ncols=2,figsize=(10*asp,10),subplot_kw={'projection': plate_carree},gridspec_kw = {'height_ratios':[3,3,3,3,3,1]})
# for season,col in zip(['JJA','DJF'],[0,1]):
# 	for dataset,ax in zip(['HadGHCND','MIROC5','NORESM1','ECHAM6-3-LR','CAM4-2degree'],axes[:5,col]):
# 		ax.set_global()
# 		ax.coastlines(edgecolor='black')
# 		ax.axis('off')
# 		ax.set_extent([-180,180,-66,80],crs=plate_carree)
# 		tmp=sum_dict[dataset]
#
# 		xx,yy=tmp.lon.copy(),tmp.lat.copy()
# 		x_step,y_step=np.diff(xx,1).mean(),np.diff(yy,1).mean()
# 		xx=np.append(xx-x_step,xx[-1]+x_step)
# 		yy=np.append(yy-y_step,yy[-1]+y_step)
# 		lons,lats=np.meshgrid(xx,yy)
# 		to_plot=(tmp['All-Hist'][season]['warm']['mean']+tmp['All-Hist'][season]['cold']['mean'])*0.5
# 		im=ax.pcolormesh(lons,lats,to_plot,vmin=3,vmax=7,cmap=plt.cm.jet);
# 		ax.annotate(season+'\n'+dataset, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')
#
# for ax in axes[5,:]:
# 	ax.outline_patch.set_edgecolor('white')
#
# cbar_ax=fig.add_axes([0,0.05,1,0.1])
# cbar_ax.axis('off')
# cb=fig.colorbar(im,orientation='horizontal',label='mean persistence [days]',ax=cbar_ax)
#
# #plt.suptitle('mean persistence', fontweight='bold')
# fig.tight_layout()
# plt.savefig('plots/climatology_mean_stateIndi.png',dpi=300)
#

# ------------------- changes
plt.close('all')
plate_carree = ccrs.PlateCarree()
fig,axes = plt.subplots(nrows=5,ncols=4,figsize=(16,8),subplot_kw={'projection': plate_carree},gridspec_kw = {'height_ratios':[3,3,3,3,2]})
for season,state,col in zip(['JJA','JJA','DJF','DJF'],['warm','cold','warm','cold'],[0,1,2,3]):
	for dataset,ax in zip(['MIROC5','NORESM1','ECHAM6-3-LR','CAM4-2degree'],axes[:4,col]):
		ax.set_global()
		ax.coastlines(edgecolor='black')
		ax.axis('off')
		ax.set_extent([-180,180,-66,80],crs=plate_carree)
		tmp=sum_dict[dataset]

		xx,yy=tmp.lon.copy(),tmp.lat.copy()
		x_step,y_step=np.diff(xx,1).mean(),np.diff(yy,1).mean()
		xx=np.append(xx-x_step,xx[-1]+x_step)
		yy=np.append(yy-y_step,yy[-1]+y_step)
		lons,lats=np.meshgrid(xx,yy)
		to_plot=(tmp['Plus20-Future'][season][state]['mean']-tmp['All-Hist'][season][state]['mean'])*0.5
		im=ax.pcolormesh(lons,lats,to_plot,vmin=-0.2,vmax=0.2,cmap=plt.cm.PiYG_r);


		significance=np.asarray(tmp['Plus20-Future'][season][state]['KS_vs_All-Hist'])
		#significance=multicomp.multipletests(significance.reshape((len(tmp.lat)*len(tmp.lon))), method='fdr_bh')[1].reshape((len(tmp.lat),len(tmp.lon)))
		significance[significance>0.05]=0
		significance[np.isfinite(significance)==False]=0
		xy=np.where(significance!=0)
		stip = ax.contourf(tmp.lon, tmp.lat, significance, levels=[-1, 0, 1, 2],colors='none', hatches=[None,'.....', '/'])

		ax.annotate(season+' '+state+'\n'+dataset, xy=(0.02, 0.05), xycoords='axes fraction', fontsize=9,fontweight='bold')

for ax in axes[4,:]:
	ax.outline_patch.set_edgecolor('white')

cbar_ax=fig.add_axes([0,0.08,1,0.2])
cbar_ax.axis('off')
cb=fig.colorbar(im,orientation='horizontal',label='changes in mean persistence [days]',ax=cbar_ax)
cbar_ax.tick_params(labelsize=10)

#plt.suptitle('mean persistence', fontweight='bold')
fig.tight_layout()
plt.savefig('plots/diff_map.png',dpi=300)
