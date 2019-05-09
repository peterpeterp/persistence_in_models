import os,sys,glob,time,collections,gc

sys.path.append('/Users/peterpfleiderer/Projects/allgemeine_scripte')
import regional_panels_on_map as regional_panels_on_map; reload(regional_panels_on_map)
os.chdir('/Users/peterpfleiderer/Projects/Persistence')

os.chdir('persistence_in_HAPPI/plot_paper')
import __plot_imports; reload(__plot_imports); from __plot_imports import *
os.chdir('../../')

sns.set_style("white")

try:
	os.chdir('/Users/peterpfleiderer/Projects/Persistence/')
except:
	os.chdir('/global/homes/p/pepflei/')

pkl_file = open('data/srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

all_regs={'ALA':{'color':'darkgreen','pos_off':(+40,+3),'summer':'JJA','winter':'DJF'},
		'WNA':{'color':'darkblue','pos_off':(-6,-8),'summer':'JJA','winter':'DJF'},
		'CNA':{'color':'gray','pos_off':(+8,-8),'summer':'JJA','winter':'DJF'},
		'ENA':{'color':'darkgreen','pos_off':(+23,-5),'summer':'JJA','winter':'DJF'},
		'CGI':{'color':'darkcyan','pos_off':(+0,-5),'summer':'JJA','winter':'DJF'},

		'NEU':{'color':'darkgreen','pos_off':(-23,+5),'summer':'JJA','winter':'DJF'},
		'CEU':{'color':'darkblue','pos_off':(+4,+7),'summer':'JJA','winter':'DJF'},
		'CAS':{'color':'darkgreen','pos_off':(-5,+13),'summer':'JJA','winter':'DJF'},
		'NAS':{'color':'gray','pos_off':(-13,+11),'summer':'JJA','winter':'DJF'},
		'TIB':{'color':'darkcyan','pos_off':(-15,-16),'summer':'JJA','winter':'DJF'},
		'EAS':{'color':'darkgreen','pos_off':(-13,0),'summer':'JJA','winter':'DJF'},

		'MED':{'color':'gray','pos_off':(-20,-10),'summer':'JJA','winter':'DJF'},
		'WAS':{'color':'darkcyan','pos_off':(-16,-10),'summer':'JJA','winter':'DJF'},
		# 'mid-lat':{'edge':'darkgreen','color':'none','alpha':1,'pos':(-143,27),'summer':'JJA','winter':'DJF','scaling_factor':1.1}
}

polygons=srex.copy()
polygons['mid-lat']={'points':[(-180,35),(180,35),(180,60),(-180,60)]}

def axis_settings(subax,info_dict,label=False,region=None):
	subax.set_xlim(-2,2)
	subax.set_ylim(-2,2)
	subax.set_yticklabels([])
	subax.set_xticklabels([])
	return(subax)

def distrs(subax,region,info_dict):
	print('________'+region+'________')
	patches,colors = [], []
	for state,details in state_details.items():

		x,y = details['x'],details['y']
		pc = PatchCollection([Polygon([(x-1.0,y-1.0),(x+1.0,y-1.0),(x+1.0,y+1.0),(x-1.0,y+1.0)])], cmap=details['cmap'], alpha=1, edgecolor='k', linewidth=2)
		if np.max(info_dict['icons'][region,state,['decrease','increase']]) != 0:
			excee_change = np.nanmean((info_dict['exceed'][:,'Plus20-Future',region,details['style'],details['excee']] - info_dict['exceed'][:,'All-Hist',region,details['style'],details['excee']]) / info_dict['exceed'][:,'All-Hist',region,details['style'],details['excee']] *100)
			subax.annotate(legend_dict[state], xy=(details['x']-0.95,details['y']*1.75), color='k', weight='bold', fontsize=8, ha='left', va='center', backgroundcolor='none')

		else:
			excee_change = 0

		pc.set_array(np.array([excee_change]))
		pc.set_clim(details['c_range'])
		subax.add_collection(pc)


	for state,details in state_details.items():
		drivers=info_dict['icons'][region,state,['EKE','SPI3','rain']]
		drivers = drivers.icon[drivers == 1]
		print(region,state,drivers)

		if len(drivers)>0:
			for icon,xx,yy in zip(drivers,{1:[1],2:[0.7,1.3],3:[0.7,1,1.3]}[len(drivers)],{1:[1],2:[1.3,0.7],3:[1.3,0.7,1.3]}[len(drivers)]):
				imscatter(state_details[state]['x']*xx, state_details[state]['y']*yy, icon_dict[icon]['icon'], zoom=icon_dict[icon]['scale'] * 0.035 * (1/float(len(drivers)))**0.1, ax=subax)

	subax.annotate(region, xy=(0.5, 0.5), xycoords='axes fraction', color='k', weight='bold', fontsize=8, ha='center', va='center', backgroundcolor='w')

legend_dict = {'warm':'warm','dry':'dry','dry-warm':'dry-warm','5mm':'rain'}

colors = {
	'<-75': {'range':(-np.inf,-75),'color':'b'},
	'<-50': {'range':(-75,-50),'color':'g'},
	'<-10': {'range':(-20,-10),'color':'red'},
	' ': {'range':(-5,5),'color':'red'},
	'>5': {'range':(5,10),'color':'o'},
	'>10': {'range':(10,20),'color':'m'},
	'>20': {'range':(20,50),'color':'c'},
}

state_details = {
	'warm' : {'x':-1,'y':1,'color':'#FF3030','name':'warm', 'style':'tas_warm', 'excee':'14','c_range':(-20,20),'cmap':'PiYG_r'},
	'dry' : {'x':1,'y':1,'color':'#FF8C00','name':'dry', 'style':'pr_dry', 'excee':'14','c_range':(-20,20),'cmap':'PiYG_r'},
	'dry-warm' : {'x':-1,'y':-1,'color':'#BF3EFF','name':'dry-warm', 'style':'cpd_dry-warm', 'excee':'14','c_range':(-20,20),'cmap':'PiYG_r'},
	'5mm' : {'x':1,'y':-1,'color':'#009ACD','name':'rain', 'style':'pr_5mm', 'excee':'7','c_range':(-75,75),'cmap':'PuOr'},
}

info_dict = {}
info_dict['icons'] = da.read_nc('data/drive*summary.nc',align=True, axis='icon')['drive']
info_dict['exceed'] = da.read_nc('data/JJA_summary_srex.nc')['exceed_prob']

fig,ax_map=regional_panels_on_map.regional_panels_on_map(distrs, axis_settings, polygons=polygons, reg_info=all_regs, info_dict=info_dict, x_ext=[-150,180], y_ext=[0,85], small_plot_size=0.1)

legax = fig.add_axes([0.85,0.05,0.145,0.9])
legax.set_yticklabels([])
legax.set_xticklabels([])
legax.set_xlim(-1,12)
legax.set_ylim(0,20)
x,y = 0,20
y-=1
legax.annotate('Driver',xy=(x,y),ha='left', va='center', fontsize=8,fontweight='bold')
legax.plot([x+0,x+4.5],[y-0.5,y-0.5],'k')
y-=1.5
for icon_name,icon_realname in zip(['EKE','SPI3','rain'],['EKE','SPI3','\nchange in\nnumber of\nrain/dry days']):
	imscatter(x, y, icon_dict[icon_name]['icon'], zoom=icon_dict[icon_name]['scale'] * 0.025, ax=legax)
	legax.annotate(icon_realname,xy=(x+1,y),ha='left', va='center', fontsize=7,fontweight='bold')
	y-=1.5

ax = fig.add_axes([0.86,0.5,0.13,0.06])
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=state_details['warm']['c_range'][0], vmax=state_details['warm']['c_range'][1])
cb1 = mpl.colorbar.ColorbarBase(ax, cmap=state_details['warm']['cmap'],norm=norm,orientation='horizontal')
cb1.ax.tick_params(labelsize=7)
cb1.set_label('rel. change in exceedance probabilites\nof warm, dry and dry-warm\n14-day periods [%]', fontsize=7)

ax = fig.add_axes([0.86,0.25,0.13,0.06])
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=state_details['5mm']['c_range'][0], vmax=state_details['5mm']['c_range'][1])
cb1 = mpl.colorbar.ColorbarBase(ax, cmap=state_details['5mm']['cmap'],norm=norm,orientation='horizontal')
cb1.ax.tick_params(labelsize=7)
cb1.set_label('rel. change in exceedance\nprobabilites of rain\n7-day periods [%]', fontsize=7)



plt.savefig('plots/NH_summary_drive.png',dpi=600)



#
