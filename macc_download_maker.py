import os

def make_macc_download(start_year,start_month,start_day):
	#start_date = str(start_year)+str(start_month)+str(start_day)
	start_date= str(start_year)+str(start_month).zfill(2)+str(start_day).zfill(2)	
 	macc_download = open('macc_download.sh',"wb")
	macc_template = ( \
				"#!/bin/bash\n"
				"LINK=$(wget \"http://ows-server.iek.fz-juelich.de/CAMS_cifs_cb05_1606_lower_fc-3hourly_ModelLevel?service=WCS&version=1.1.2&Request=GetCoverage&identifier=CAMS_"+start_date+"&BoundingBox=-96,36,-81,50,urn:ogc:def:crs:OGC::84&format=application/x-netcdf\" -O MACC_"+start_date+")\n"

				"echo $LINK\n"
				"eval ${LINK}\n"
				"tail -n+22 MACC_"+start_date+".nc > MACC_"+start_date+"_tmp.nc\n"
				"mv MACC_"+start_date+"_tmp.nc MACC_"+start_date+".nc\n"
				"\n")
	macc_download.write(macc_template)
	macc_download.close()
