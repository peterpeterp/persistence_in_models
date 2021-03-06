




model_dict={'MIROC5':{'grid':'128x256',
					'full_model':'MIROC/MIROC5',
					'in_path':'/project/projectdirs/m1517/C20C/MIROC/MIROC5/',
					'version':{'Plus20-Future':'v2-0','Plus15-Future':'v3-0','All-Hist':'v2-0'},
					'runs':{'All-Hist':['run'+str(i).zfill(3) for i in range(1,51)+range(111,161)],
							'Plus20-Future':['run'+str(i).zfill(3) for i in range(1,101)],
							'Plus15-Future':['run'+str(i).zfill(3) for i in range(1,101)],
					}},
			'NorESM1':{'grid':'192x288',
					'full_model':'NCC/NorESM1-HAPPI',
					'in_path':'/project/projectdirs/m1517/C20C/NCC/NorESM1-HAPPI/',
					'version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'},
					'runs':{'All-Hist':['run'+str(i).zfill(3) for i in range(1,101)],
							'Plus20-Future':['run'+str(i).zfill(3) for i in range(1,101)],
							'Plus15-Future':['run'+str(i).zfill(3) for i in range(1,101)],
					}},
			'ECHAM6-3-LR':{'grid':'96x192',
					'full_model':'MPI-M/ECHAM6-3-LR',
					'in_path':'/project/projectdirs/m1517/C20C/MPI-M/ECHAM6-3-LR/',
					'version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'},
					'runs':{'All-Hist':['run'+str(i).zfill(3) for i in range(1,101)],
							'Plus20-Future':['run'+str(i).zfill(3) for i in range(1,101)],
							'Plus15-Future':['run'+str(i).zfill(3) for i in range(1,101)],
					}},
			'CAM4-2degree':{'grid':'96x144',
					'full_model':'ETH/CAM4-2degree',
					'in_path':'/project/projectdirs/m1517/C20C/ETH/CAM4-2degree/',
					'version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'},
					'runs':{'All-Hist':['ens0'+str(i).zfill(3) for i in range(100)],
							'Plus20-Future':['ens0'+str(i).zfill(3) for i in range(100)],
							'Plus15-Future':['ens0'+str(i).zfill(3) for i in range(100)],
					}},
}

#
# model_dict={'MIROC5':{'grid':'128x256','in_path':'/project/projectdirs/m1517/C20C/MIROC/MIROC5/','version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'}},
# 			'NorESM1':{'grid':'192x288','in_path':'/project/projectdirs/m1517/C20C/NCC/NorESM1-HAPPI/','version':{'Plus20-Future':'v1-0','Plus15-Future':'v1-0','All-Hist':'v1-0'}},
# 			'ECHAM6-3-LR':{'grid':'96x192','in_path':'/project/projectdirs/m1517/C20C/MPI-M/ECHAM6-3-LR/','version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'}},
# 			'CAM4-2degree':{'grid':'96x144','in_path':'/project/projectdirs/m1517/C20C/ETH/CAM4-2degree/','version':{'Plus20-Future':'v2-0','Plus15-Future':'v2-0','All-Hist':'v1-0'}},
# }
