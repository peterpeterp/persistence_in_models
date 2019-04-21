import os,sys,glob,time,collections,signal,gc
import numpy as np
from netCDF4 import Dataset,num2date
import random as random
import dimarray as da
import subprocess as sub
import scipy.stats as stats
from scipy import signal
import scipy

model='EOBS'
scenario='All-Hist'


os.chdir('/p/projects/ikiimp/HAPPI/HAPPI_Peter')
corWith_dict = {
	'SPI3':{'file':'data/rr_0p5_1950-2018_mon_SPI3.nc','corWith_start':1950,'corWith_end':2018, 'var_name':'spi'},
	'EKE':{'file':'data/ERA-Interim_eke_1979-2017_850hPa_mon_EOBSgrid.nc','corWith_start':1979,'corWith_end':2017, 'var_name':'eke'}
}

working_path='data/'+model+'/'

for state,pers_file in zip(['dry-warm','warm','dry','5mm'], ['cpd_0.50deg_reg_merged_period_dry-warm.nc','tg_0.50deg_reg_merged_period_warm.nc','rr_0.50deg_reg_merged_period_dry.nc','rr_0.50deg_reg_merged_period_5mm.nc']):

	data =da.read_nc(working_path+scenario+'/'+pers_file)
	pers_start = 1950
	pers_end = 2017

	for corWith_name,corWith_detials in corWith_dict.items():
		corWith_full = da.read_nc(corWith_detials['file'])[corWith_details['var_name']]

		'''
		carefully check time axis of both files
		'''
		corWith_start = corWith_detials['corWith_start']
		corWith_end = corWith_detials['corWith_end']

		index_shift = (pers_start - corWith_start) * 12
		cut_start = corWith_start - pers_start
		cut_end = (min(corWith_end,pers_end) - pers_start ) * 12

		seasons={'MAM':0, 'JJA':1, 'SON':2, 'DJF':3}

		cor = {}
		for style in ['','_lagged','_season','_lagged_season','_mon','_mon_lagged']:
			for stat in ['corrcoef','p-value']:
				cor[stat+style]=da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])
		for stat in ['lr_intercept','lr_slope','lr_pvalue']:
			cor[stat]=da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])

		statistics = {}
		for xxx in [corWith_name,state,corWith_name+'_lagged']:
			for stat in ['mean','10','25','33','50','66','75','90','100']:
				statistics[stat+'_'+xxx]=da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])
		statistics['mean_of_10percLongest_'+state] = da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])
		statistics['mean_of_10percLongest_'+corWith_name] =  da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])
		statistics['mean_of_10percLongest_lagged_'+corWith_name] =  da.DimArray(axes=[seasons.keys(),data.latitude,data.longitude],dims=['season','lat','lon'])


		for y in data.latitude:
			for x in data.longitude:
				pers_loc=data['period_length'][:,y,x].values
				# print(np.nanpercentile(pers_loc,range(101)))
				if pers_loc.sum() != 0:
					print(y,x)

					pre_index=data['period_monthly_index'][:,y,x]
					avail_indices = np.where((pre_index>=cut_start) & (pre_index<=cut_end))[0]

					pers_loc=data['period_length'][avail_indices,y,x].values
					time_loc=data['period_midpoints'][avail_indices,y,x].values
					monIndex_loc=data['period_monthly_index'][avail_indices,y,x].values
					corWith_loc=corWith_full.ix[monIndex_loc+index_shift,:,:][:,y,x].values

					tmp_lagged_index = monIndex_loc+index_shift-1
					issue_months = np.where(tmp_lagged_index < 0)[0]
					tmp_lagged_index[issue_months] = 0
					tmp_tmp = corWith_full.ix[tmp_lagged_index,:,:][:,y,x].values
					tmp_tmp[issue_months] = np.nan
					corWith_loc_lagged = tmp_tmp

					# mask all
					mask = np.isfinite(pers_loc) & np.isfinite(time_loc) & np.isfinite(corWith_loc) & np.isfinite(corWith_loc_lagged)
					time_loc=time_loc[mask]
					if len(time_loc) > 1:
						year_loc =  np.array([date.year for date in num2date(time_loc, units = "days since 1950-01-01 00:00")])
						pers_loc=pers_loc[mask]
						monIndex_loc=monIndex_loc[mask]
						corWith_loc=corWith_loc[mask]
						corWith_loc_lagged=corWith_loc_lagged[mask]
						sea_loc=data['period_season'][:,y,x].values[mask]

						for season_name,season_id in seasons.items():
							valid_season = sea_loc==season_id
							pers_loc_sea = np.array(pers_loc[valid_season], np.float)
							if pers_loc_sea.shape[0]>10:
								time_loc_sea = time_loc[valid_season]
								year_loc_sea = year_loc[valid_season]
								monIndex_loc_sea = monIndex_loc[valid_season]
								corWith_loc_sea = corWith_loc[valid_season]
								corWith_loc_lagged_sea = corWith_loc_lagged[valid_season]


								################
								# mean
								################
								statistics['mean_'+state][season_name,y,x] = np.nanmean(pers_loc_sea)
								for qu in [10,25,33,50,66,75,90,100]:
									statistics[str(qu)+'_'+state][season_name,y,x] = np.nanpercentile(pers_loc_sea,qu)

								statistics['mean_'+corWith_name][season_name,y,x] = np.nanmean(corWith_loc_sea)
								for qu in [10,25,33,50,66,75,90,100]:
									statistics[str(qu)+'_'+corWith_name][season_name,y,x] = np.nanpercentile(corWith_loc_sea,qu)

								statistics['mean_'+corWith_name+'_lagged'][season_name,y,x] = np.nanmean(corWith_loc_lagged_sea)
								for qu in [10,25,33,50,66,75,90,100]:
									statistics[str(qu)+'_'+corWith_name+'_lagged'][season_name,y,x] = np.nanpercentile(corWith_loc_lagged_sea,qu)


								'''
								detrend and normalize
								detrending might be stupid in 10 year runs

								mean eke/spi of 10% longest events

								spi before event
								'''

								# # detrend
								# slope, intercept, r_value, p_value, std_err = stats.linregress(time_loc_sea,pers_loc_sea)
								# pers_loc_sea_detrend = pers_loc_sea-(intercept+slope*time_loc_sea)
								# slope, intercept, r_value, p_value, std_err = stats.linregress(time_loc_sea,corWith_loc_sea)
								# corWith_loc_sea_detrend = corWith_loc_sea-(intercept+slope*time_loc_sea)
								# slope, intercept, r_value, p_value, std_err = stats.linregress(time_loc_sea,corWith_loc_lagged_sea)
								# corWith_loc_lagged_sea_detrend = corWith_loc_lagged_sea-(intercept+slope*time_loc_sea)

								# detrend
								pers_loc_sea = scipy.signal.detrend(pers_loc_sea)
								corWith_loc_sea = scipy.signal.detrend(corWith_loc_sea)
								corWith_loc_lagged_sea = scipy.signal.detrend(corWith_loc_lagged_sea)


								# normalize
								pers_loc_sea_norm = (pers_loc_sea - pers_loc_sea.max()) / (pers_loc_sea.min() - pers_loc_sea.max())
								corWith_loc_sea_norm = (corWith_loc_sea - corWith_loc_sea.max()) / (corWith_loc_sea.min() - corWith_loc_sea.max())
								corWith_loc_lagged_sea_norm = (corWith_loc_lagged_sea - corWith_loc_lagged_sea.max()) / (corWith_loc_lagged_sea.min() - corWith_loc_lagged_sea.max())

								################
								# correlation
								################
								cor['corrcoef'][season_name,y,x],cor['p-value'][season_name,y,x] = stats.pearsonr(pers_loc_sea_norm,corWith_loc_sea_norm)
								cor['corrcoef_lagged'][season_name,y,x],cor['p-value_lagged'][season_name,y,x] = stats.pearsonr(pers_loc_sea_norm,corWith_loc_lagged_sea_norm)

								################
								# regression
								################
								slope, intercept, r_value, p_value, std_err = stats.linregress(pers_loc_sea_norm,corWith_loc_sea_norm)
								cor['lr_slope'][season_name,y,x] = slope
								cor['lr_intercept'][season_name,y,x] = intercept
								cor['lr_pvalue'][season_name,y,x] = p_value

								###################
								# longest in season
								###################
								pers_loc_sea_, corWith_loc_sea_, corWith_loc_lagged_sea_ = np.array([]), np.array([]), np.array([])
								for yr in sorted(set(year_loc_sea)):
									indices_of_year = np.where(year_loc_sea==yr)[0]
									corWith_loc_sea_ = np.append(corWith_loc_sea_,corWith_loc_sea_norm[indices_of_year][0])
									corWith_loc_lagged_sea_ = np.append(corWith_loc_lagged_sea_,corWith_loc_lagged_sea_norm[indices_of_year][0])
									pers_loc_sea_ = np.append(pers_loc_sea_,pers_loc_sea_norm[indices_of_year].max())

								cor['corrcoef_season'][season_name,y,x],cor['p-value_season'][season_name,y,x] = stats.pearsonr(pers_loc_sea_,corWith_loc_sea_)
								cor['corrcoef_lagged_season'][season_name,y,x],cor['p-value_lagged_season'][season_name,y,x] = stats.pearsonr(pers_loc_sea_,corWith_loc_lagged_sea_)


								################
								# longest in month
								################
								pers_loc_sea_, corWith_loc_sea_, corWith_loc_lagged_sea_ = np.array([]), np.array([]), np.array([])
								for ind in sorted(set(monIndex_loc_sea)):
									indices_of_mon = np.where(monIndex_loc_sea==ind)[0]
									corWith_loc_sea_ = np.append(corWith_loc_sea_,corWith_loc_sea[indices_of_mon][0])
									corWith_loc_lagged_sea_ = np.append(corWith_loc_lagged_sea_,corWith_loc_lagged_sea[indices_of_mon][0])
									pers_loc_sea_ = np.append(pers_loc_sea_,pers_loc_sea[indices_of_mon].max())
									# time_ = np.append(time_,time_loc_sea[indices_of_mon][np.argmax(pers_loc_sea[indices_of_mon])])

								# normalize
								pers_loc_sea_norm_ = (pers_loc_sea_ - pers_loc_sea_.max()) / (pers_loc_sea_.min() - pers_loc_sea_.max())
								corWith_loc_sea_norm_ = (corWith_loc_sea_ - corWith_loc_sea_.max()) / (corWith_loc_sea_.min() - corWith_loc_sea_.max())
								corWith_loc_lagged_sea_norm_ = (corWith_loc_lagged_sea_ - corWith_loc_lagged_sea_.max()) / (corWith_loc_lagged_sea_.min() - corWith_loc_lagged_sea_.max())

								################
								# correlation
								################
								cor['corrcoef_mon'][season_name,y,x],cor['p-value'][season_name,y,x] = stats.pearsonr(pers_loc_sea_norm_,corWith_loc_sea_norm_)
								cor['corrcoef_mon_lagged'][season_name,y,x],cor['p-value_lagged'][season_name,y,x] = stats.pearsonr(pers_loc_sea_norm_,corWith_loc_lagged_sea_norm_)

								###################
								# longest in events
								###################
								longest_events = np.argwhere(pers_loc_sea >= np.percentile(pers_loc_sea,90))
								statistics['mean_of_10percLongest_'+state][season_name,y,x] = np.nanmean(pers_loc_sea[longest_events])
								statistics['mean_of_10percLongest_'+corWith_name][season_name,y,x] = np.nanmean(corWith_loc_sea[longest_events])
								statistics['mean_of_10percLongest_lagged_'+corWith_name][season_name,y,x] = np.nanmean(corWith_loc_lagged_sea[longest_events])


								gc.collect()

		ds = da.Dataset(cor)
		ds.write_nc(working_path+'/cor_'+corWith_name+'_'+'_'.join(['EOBS',state])+'.nc')

		da.Dataset(statistics).write_nc(working_path+'/stats_'+corWith_name+'_'+'_'.join(['EOBS',state])+'.nc')
