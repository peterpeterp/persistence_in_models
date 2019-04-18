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
sns.set_style("white")
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

NH_regs={'ALA':{'color':'darkgreen','pos_off':(+10,+7),'summer':'JJA','winter':'DJF'},
		'WNA':{'color':'darkblue','pos_off':(+20,+15),'summer':'JJA','winter':'DJF'},
		'CNA':{'color':'gray','pos_off':(+8,-4),'summer':'JJA','winter':'DJF'},
		'ENA':{'color':'darkgreen','pos_off':(+18,-5),'summer':'JJA','winter':'DJF'},
		'CGI':{'color':'darkcyan','pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},
		# 'CAM':{'color':'darkcyan','pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},

		'NEU':{'color':'darkgreen','pos_off':(-13,+0),'summer':'JJA','winter':'DJF'},
		'CEU':{'color':'darkblue','pos_off':(+9,+5),'summer':'JJA','winter':'DJF'},
		'CAS':{'color':'darkgreen','pos_off':(-8,+14),'summer':'JJA','winter':'DJF'},
		'NAS':{'color':'gray','summer':'JJA','winter':'DJF'},
		'TIB':{'color':'darkcyan','pos_off':(+2,-4),'summer':'JJA','winter':'DJF'},
		'EAS':{'color':'darkgreen','summer':'JJA','winter':'DJF'},

		'MED':{'color':'gray','pos_off':(-15,-5),'summer':'JJA','winter':'DJF'},
		'WAS':{'color':'darkcyan','pos_off':(-5,-1),'summer':'JJA','winter':'DJF'},
		'mid-lat':{'edge':'darkgreen','color':'none','alpha':1,'pos':(-142,42),'title':'','summer':'JJA','winter':'DJF','scaling_factor':1.3}}

all_regs=NH_regs.copy()

polygons=srex.copy()
polygons['mid-lat']={'points':[(-180,35),(180,35),(180,60),(-180,60)]}

icon_dict = {
	'storm_track':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/storm.png')),
	# 'water':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/drop.png')),
	# 'dry':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/plumbing.png')),
	# 'drought':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/nature.png')),
	'increase':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/increase.png')),
	'decrease':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/decrease.png')),
	'rain':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/rain.png')),
	# 'no_rain':plt.imread(get_sample_data('/Users/peterpfleiderer/Projects/Persistence/plots/icons/no_rain.png')),
}

# ---------------------------- changes
def legend_plot(subax,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None):
	subax.axis('off')

def axis_settings(subax,label=False,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None):
	subax.set_xlim(-2,2)
	subax.set_ylim(-2,2)
	subax.set_yticklabels([])
	subax.set_xticklabels([])
	return(subax)

def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    # ax.autoscale()
    return artists

def distrs(subax,region,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None):
	print('________'+region+'________')
	patches,colors = [], []
	for state,details in state_details.items():
		x,y = details['x'],details['y']
		pc = PatchCollection([matplotlib.patches.Polygon([(x-1.0,y-1.0),(x+1.0,y-1.0),(x+1.0,y+1.0),(x-1.0,y+1.0)])], color=details['color'], edgecolor="k", alpha=0.5, lw=0.5)
		subax.add_collection(pc)
		# pc = PatchCollection([matplotlib.patches.Polygon([(x-0.58,y-0.58),(x+0.58,y-0.58),(x+0.58,y+0.58),(x-0.58,y+0.58)])], color='white', edgecolor="w", alpha=1, lw=0.5)
		# subax.add_collection(pc)

		if region=='mid-lat':
			subax.annotate(legend_dict[state],xy=(x*1.9,y*1.8),ha={-1:'left',1:'right'}[x], va='center', fontsize=8,fontweight='bold')

	for state,icons in arg1[region].items():
		drivers=icons['drive']
		if len(drivers)>0:
			for icon,xx,yy in zip(drivers,{1:[0],2:[-0.33,0.33],3:[-0.5,0,0.5]}[len(drivers)],{1:[0],2:[0,0],3:[-0.33,0.33,-0.33]}[len(drivers)]):
				imscatter(state_details[state]['x']*1.5+xx, state_details[state]['y']*1.2+yy, icon_dict[icon], zoom=0.03 * (1/float(len(drivers)))**0.5, ax=subax)

		if icons['change'] != 'none':
			imscatter(state_details[state]['x']*0.7, state_details[state]['y']*0.9, icon_dict[icons['change']], zoom=0.025, ax=subax)

	# for state,icons in arg1[region].items():
	# 	drivers=icons['drive']
	# 	if len(drivers)>0:
	# 		for icon,xx,yy in zip(drivers,{1:[0],2:[-0.33,0.33],3:[-0.5,0,0.5]}[len(drivers)],{1:[0],2:[0,0],3:[-0.33,0.33,-0.33]}[len(drivers)]):
	# 			imscatter(state_details[state]['x']*0.8+xx, state_details[state]['y']*1.2+yy, icon_dict[icon], zoom=0.025 * (1/float(len(drivers)))**0.5, ax=subax)
	#
	# 	if icons['change'] != 'none':
	# 		imscatter(state_details[state]['x']*1.65, state_details[state]['y']*0.5, icon_dict[icons['change']], zoom=0.02, ax=subax)

	subax.annotate(region, xy=(0.5, 0.5), xycoords='axes fraction', color='k', weight='bold', fontsize=8, ha='center', va='center', backgroundcolor='w')


plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

legend_dict = {'warm':'warm','dry':'dry','dry-warm':'dry-warm','5mm':'rain'}

state_details = {
	'warm':{'x':-1,'y':1,'color':'#FF3030'},
	'dry':{'x':1,'y':1,'color':'#FF8C00'},
	'dry-warm':{'x':-1,'y':-1,'color':'#BF3EFF'},
	'5mm':{'x':1,'y':-1,'color':'#009ACD'},
}

arg1 = {'ALA':{
				'warm':{'drive':[],'change':'none'},
				'dry':{'drive':['rain'],'change':'decrease'},
				'dry-warm':{'drive':[],'change':'decrease'},
				'5mm':{'drive':['rain'],'change':'increase'},
				},
		'WNA':{
				'warm':{'drive':[],'change':'increase'},
				'dry':{'drive':[],'change':'none'},
				'dry-warm':{'drive':[],'change':'none'},
				'5mm':{'drive':['rain'],'change':'decrease'},
				},
		'CNA':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':['storm_track'],'change':'increase'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':[],'change':'increase'},
				},
		'ENA':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':['storm_track'],'change':'increase'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':[],'change':'increase'},
				},
		'CGI':{
				'warm':{'drive':[],'change':'none'},
				'dry':{'drive':['rain'],'change':'decrease'},
				'dry-warm':{'drive':[],'change':'none'},
				'5mm':{'drive':['rain'],'change':'increase'},
				},
		'NEU':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':['storm_track'],'change':'increase'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':[],'change':'increase'},
				},
		'CEU':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':['storm_track'],'change':'increase'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':[],'change':'increase'},
				},
		'CAS':{
				'warm':{'drive':['storm_track'],'change':'none'},
				'dry':{'drive':[],'change':'none'},
				'dry-warm':{'drive':['storm_track'],'change':'none'},
				'5mm':{'drive':[],'change':'none'},
				},
		'NAS':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':['storm_track'],'change':'increase'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':['rain'],'change':'increase'},
				},
		'TIB':{
				'warm':{'drive':[],'change':'increase'},
				'dry':{'drive':[],'change':'none'},
				'dry-warm':{'drive':['storm_track'],'change':'increase'},
				'5mm':{'drive':[],'change':'none'},
				},
		'EAS':{
				'warm':{'drive':[],'change':'none'},
				'dry':{'drive':[],'change':'decrease'},
				'dry-warm':{'drive':[],'change':'none'},
				'5mm':{'drive':[],'change':'increase'},
				},

		'MED':{
				'warm':{'drive':[],'change':'none'},
				'dry':{'drive':[],'change':'increase'},
				'dry-warm':{'drive':[],'change':'none'},
				'5mm':{'drive':[],'change':'none'},
				},
		'WAS':{
				'warm':{'drive':[],'change':'none'},
				'dry':{'drive':[],'change':'none'},
				'dry-warm':{'drive':[],'change':'none'},
				'5mm':{'drive':[],'change':'increase'},
				},
		'mid-lat':{
				'warm':{'drive':['storm_track'],'change':'increase'},
				'dry':{'drive':[],'change':'increase'},
				'dry-warm':{'drive':[],'change':'increase'},
				'5mm':{'drive':[],'change':'increase'},
				},
}


fig,ax_map=srex_overview.srex_overview(distrs, axis_settings, polygons=polygons, reg_info=all_regs, x_ext=[-180,180], y_ext=[0,85], small_plot_size=0.08, legend_plot=legend_plot, legend_pos=[-160,20], \
	arg1=arg1,
	title=None)

legax = fig.add_axes([0.01,0.01,0.3,0.2])
legax.set_yticklabels([])
legax.set_xticklabels([])
x,y = 0,4
for state,details in state_details.items():
	pc = PatchCollection([matplotlib.patches.Polygon([(x-0.5,y-0.9),(x+0.5,y-0.9),(x+0.5,y+0.9),(x-0.5,y+0.9)])], color=details['color'], edgecolor="k", alpha=0.5, lw=0.5)
	legax.add_collection(pc)
	legax.annotate(legend_dict[state],xy=(1,y),ha='left', va='center', fontsize=8,fontweight='bold')
	y-=2
legax.annotate('Persistence',xy=(1,6.5),ha='left', va='center', fontsize=8,fontweight='bold')

x,y = 5,3
for icon_name,icon_realname in zip(['increase','decrease'],['increase','decrease']):
	imscatter(x, y, icon_dict[icon_name], zoom=0.025, ax=legax)
	legax.annotate(icon_realname,xy=(x+1,y),ha='left', va='center', fontsize=8,fontweight='bold')
	y-=3
legax.annotate('Change',xy=(x+1,6.5),ha='left', va='center', fontsize=8,fontweight='bold')

x,y = 10,3
for icon_name,icon_realname in zip(['storm_track','rain'],['storm tracks','water cycle']):
	imscatter(x, y, icon_dict[icon_name], zoom=0.025, ax=legax)
	legax.annotate(icon_realname,xy=(x+1,y),ha='left', va='center', fontsize=8,fontweight='bold')
	y-=3
legax.annotate('Driver',xy=(x+1,6.5),ha='left', va='center', fontsize=8,fontweight='bold')

# legax.axhline(y=5.5,color='k')

legax.set_xlim(-1,16)
legax.set_ylim(-3,8)



plt.savefig('plots/NH_summary_drive.png',dpi=600)
