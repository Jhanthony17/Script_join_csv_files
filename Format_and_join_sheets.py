import pandas as pd
import os
import itertools
import glob
import argparse

# Get the list of all files and directories
#path = "C://Users//Vanshi//Desktop//gfg"
#dir_list = os.listdir('.')

parser = argparse.ArgumentParser(description='Carpeta a trabajar y fecha de escaneo')
parser.add_argument('carpeta',type=str, help='Insertar la carpeta')
parser.add_argument('fecha_escaneo',type=str, help='Insertar la fecha de escaneo')
args = parser.parse_args()

headers_salida = ['Hostname','nombre_red','Plugin','Plugin Name','Plugin Output','IP Address','Severidad','Port','Protocol','Solution','CVSS_Final','fecha_escaneo','Segmento','CVE','Family','Fixed']

carpeta = args.carpeta
fecha_escaneo = args.fecha_escaneo
dir_list = glob.glob(carpeta+"/*.xlsx")
zize_dir_list = len(dir_list)
if zize_dir_list != 0:
	range_pairs = range(2,2*len(dir_list)+2,2)
	range_odds = range(1,(2*len(dir_list)+1),2)
	dataframes = []
	# Read excel file with sheet name
	for (j,k) in itertools.zip_longest(range_odds,range_pairs):
		dict_df_j = pd.read_excel(f'{dir_list[0]}', sheet_name='Vulnerabilidades')
		dict_df_j['Fixed'] = 'No'
		dict_df_k = pd.read_excel(f'{dir_list[0]}', sheet_name='Remediadas')
		dict_df_k['Fixed'] = 'Si'
		dataframes.append(dict_df_j)
		dataframes.append(dict_df_k)
	#print(dataframes['Fixed'])
	dataframes_concatenated = pd.concat(dataframes)
	#dataframes_concatenated = dataframes_concatenated[dataframes_concatenated.Severity != 'Info']
	dataframes_concatenated["CVSS_Final"] = dataframes_concatenated['CVSS V3 Base Score'].fillna(dataframes_concatenated['CVSS V2 Base Score'])
	dataframes_concatenated["CVSS_Final"] = pd.to_numeric(dataframes_concatenated["CVSS_Final"], downcast="float")
	dataframes_concatenated = dataframes_concatenated.rename(columns={'DNS Name':'Hostname'})
	dataframes_concatenated.loc[(dataframes_concatenated['CVSS_Final'] >= 0.0) & (dataframes_concatenated['CVSS_Final'] <= 3.9), 'Severidad'] = 'Baja'
	dataframes_concatenated.loc[(dataframes_concatenated['CVSS_Final'] >= 4.0) & (dataframes_concatenated['CVSS_Final'] <=6.9), 'Severidad'] = 'Media'
	dataframes_concatenated.loc[(dataframes_concatenated['CVSS_Final'] >= 7.0) & (dataframes_concatenated['CVSS_Final'] <=8.9), 'Severidad'] = 'Alta'
	dataframes_concatenated.loc[(dataframes_concatenated['CVSS_Final'] >= 9.0) & (dataframes_concatenated['CVSS_Final'] <= 10.0), 'Severidad'] = 'Critica'
	dataframes_concatenated['nombre_red'] = f'{carpeta}'
	dataframes_concatenated['fecha_escaneo'] = f'{fecha_escaneo}'
	dataframes_concatenated['Segmento'] = f'{carpeta}'
	dataframes_concatenated.to_csv(f'{carpeta}.csv', index=False, columns=headers_salida)

else:
	print(f"No hay archivos en la carpeta {carpeta}")