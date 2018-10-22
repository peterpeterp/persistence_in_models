import os,sys,glob,time,collections,signal,gc
import numpy as np
from netCDF4 import Dataset,num2date
import random as random
import dimarray as da
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('/Users/peterpfleiderer/Projects/Persistence')

data_path='data/EOBS/All-Hist/'

events = {
	#'russianHW2010':{'lon':37.25, 'lat':55.25, 'year':2010},
	#'balkanFL2014':{'lon':20.25, 'lat':44.25, 'year':2014},
	'euroFL2010':{'lon':18.75, 'lat':49.25, 'year':2010, 'name': 'Ostrau 2010'},
	#'euroHW2003':{'lon':2.75, 'lat':48.25, 'year':2003,'name': 'Paris 2003'},
	}

for event_name,event in events.items():

	lat_,lon_ = event['lat'],event['lon']

	nc_period=da.read_nc(data_path+'tg_0.50deg_reg_v17.0_period.nc')
	tas_period={}
	for name, value in nc_period.items():
		tas_period[name]=value[:,lat_,lon_]

	nc_period=da.read_nc(data_path+'rr_0.50deg_reg_v17.0_period.nc')
	pr_period={}
	for name, value in nc_period.items():
		pr_period[name]=value[:,lat_,lon_]

	nc_period=da.read_nc(data_path+'cpd_0.50deg_reg_v17.0_period.nc')
	cpd_period={}
	for name, value in nc_period.items():
		cpd_period[name]=value[:,lat_,lon_]

	nc_tas=da.read_nc(data_path+'tg_0.50deg_reg_v17.0_anom.nc')
	tas_anom=nc_tas['tas_anom'][:,lat_,lon_]
	nc_pr=da.read_nc(data_path+'rr_0.50deg_reg_v17.0.nc')
	pr=nc_pr['rr'][:,lat_,lon_]

	tas_state=da.read_nc(data_path+'tg_0.50deg_reg_v17.0_state.nc')['state'][:,lat_,lon_]
	pr_state=da.read_nc(data_path+'rr_0.50deg_reg_v17.0_state.nc')['state'][:,lat_,lon_]
	cpd_state=da.read_nc(data_path+'cpd_0.50deg_reg_v17.0_state.nc')['state'][:,lat_,lon_]
	gc.collect()

	tas_time=nc_tas['time']
	datevar=num2date(tas_time, units = tas_time.units)
	tas_time_axis=np.array([dd.year + (dd.timetuple().tm_yday-1) / 365. for dd in datevar])

	pr_time=nc_pr['time']
	datevar=num2date(pr_time, units = pr_time.units)
	pr_time_axis=np.array([dd.year + (dd.timetuple().tm_yday-1) / 365. for dd in datevar])


	months={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'Mai',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Okt',11:'Nov',12:'Dez'}
	ticks=np.array([(dd.year,dd.month,yearfrc) for dd,yearfrc in zip(datevar,pr_time_axis) if dd.day == 15 and yearfrc>event['year'] and yearfrc<=event['year']+1])

	pr_time_id=np.where((pr_time_axis>event['year']) & (pr_time_axis<=event['year']+1))[0]
	tas_time_id=np.where((tas_time_axis>event['year']) & (tas_time_axis<=event['year']+1))[0]


	plt.close()
	fig,axes = plt.subplots(nrows=3,ncols=1,gridspec_kw = {'height_ratios':[1,2,4]})
	for ax in axes:
		#ax.set_xlim(time_stamps[0],time_stamps[-1])
		ax.set_xticks([])

	axes[0].axis('off')
	axes[0].set_title('cold+wet - warm+dry')
	mid=cpd_period['period_midpoints'].values
	nona = np.where(np.isfinite(mid))
	mid = np.array([dd.year + (dd.timetuple().tm_yday-1) / 365. for dd in num2date(mid[nona], units = pr_time.units)])
	periods_ = np.where((mid>event['year']) & (mid<=event['year']+1))
	length=cpd_period['period_length'].ix[periods_] / 365.
	for ll,mm in zip(length,mid[periods_]):
		axes[0].fill_between([mm-np.abs(ll)/2.,mm+np.abs(ll)/2.],[-1,-1],[1,1],color={-1:'darkcyan',1:'darkmagenta',0:'white'}[np.sign(ll)],alpha=0.3)

	mid=pr_period['period_midpoints'].values
	nona = np.where(np.isfinite(mid))
	mid = np.array([dd.year + (dd.timetuple().tm_yday-1) / 365. for dd in num2date(mid[nona], units = pr_time.units)])
	periods_ = np.where((mid>event['year']) & (mid<=event['year']+1))
	length=pr_period['period_length'].ix[periods_] / 365.
	for ll,mm in zip(length,mid[periods_]):
		axes[1].fill_between([mm-np.abs(ll)/2.,mm+np.abs(ll)/2.],[7,7],[12,12],color={-1:'brown',1:'cyan'}[np.sign(ll)],alpha=0.3)
	axes[1].plot(pr_time_axis[pr_time_id],pr.ix[pr_time_id],color='gray')
	axes[1].set_title('dry - wet')
	axes[1].set_ylabel('precip [mm]')
	axes[1].set_ylim(0,50)

	mid=tas_period['period_midpoints'].values
	nona = np.where(np.isfinite(mid))
	mid = np.array([dd.year + (dd.timetuple().tm_yday-1) / 365. for dd in num2date(mid[nona], units = tas_time.units)])
	periods_ = np.where((mid>event['year']) & (mid<=event['year']+1))
	length=tas_period['period_length'].ix[periods_] / 365.
	for ll,mm in zip(length,mid[periods_]):
		axes[2].fill_between([mm-np.abs(ll)/2.,mm+np.abs(ll)/2.],[-3,-3],[3,3],color={-1:'blue',1:'red'}[np.sign(ll)],alpha=0.3)
	axes[2].plot(tas_time_axis[tas_time_id],tas_anom.ix[tas_time_id],color='gray')
	axes[2].set_xticks(ticks[:,2])
	axes[2].set_xticklabels([months[mn] for mn in ticks[:,1]])
	axes[2].set_title('cold - warm')
	axes[2].set_ylabel('temp anom [K]')

	plt.suptitle(event['name'])
	# plt.tight_layout()
	plt.savefig('plots/paper/EOBS_compound_'+event_name+'.png')