import os

def make_macc_download(start_year,start_month,start_day):
	start_date= str(start_year)+str(start_month).zfill(2)+str(start_day).zfill(2)	
 	macc_download = open('macc_download.sh',"wb")
	macc_template = ( \
				"#!/bin/bash\n"
				"LINK=$(wget \"http://ows-server.iek.fz-juelich.de/CAMS_cifs_cb05_1606_lower_fc-3hourly_ModelLevel?service=WCS&version=1.1.2&Request=GetCoverage&identifier=CAMS_"+start_date+"&BoundingBox=-96,36,-81,50,urn:ogc:def:crs:OGC::84&format=application/x-netcdf\" -O MACC_"+start_date+".nc)\n"

				"echo $LINK\n"
				"eval ${LINK}\n"
				"tail -n+22 MACC_"+start_date+".nc > MACC_"+start_date+"_tmp.nc\n"
				"mv MACC_"+start_date+"_tmp.nc MACC_"+start_date+".nc\n"
				"\n")
	macc_download.write(macc_template)
	macc_download.close()

def make_macc_inp(start_year,start_month,start_day):
	start_date= str(start_year)+str(start_month).zfill(2)+str(start_day).zfill(2)	
 	macc_inp_file = open('MACC_LMOS_d01.inp',"wb")
	macc_inp_template = (\
				"&control\n\n"
				"do_bc     = .true.\n"
				"do_ic     = .true.\n"
				"domain    = 1\n"
				"dir_wrf   = './'\n"
				"dir_moz = '../'\n"
				"fn_moz  = 'MACC_"+ start_date+".nc'\n\n"
				"spc_map = 'eth -> c2h6',\n"
				"	  'ch4 -> ch4',\n"
          			"	  'hc3 -> c3h8',\n"
				"	  'o3 -> o3',\n"
				"	  'no -> no',\n"
				"	  'ho -> oh',\n"
				"	  'so2 -> so2',\n"
				"	  'sulf -> 0.0*so2',\n"
				"	  'iso -> isop',\n"
				"	  'no2 -> no2',\n"
				"	  'hno3 -> hno3',\n"
				"	  'pan -> pan',\n"
				"	  'co -> co',\n"
                                "/\n"
				)
	macc_inp_file.write(macc_inp_template)
	macc_inp_file.close()
	print macc_inp_template
	
