#!/bin/bash
echo 'Iniciando script...'
echo 'Ingresar fecha (Ejem. 01/01/2021):'
read fecha_escaneo
py Format_and_join_sheets.py "Estaciones de trabajo" $fecha_escaneo
py Format_and_join_sheets.py "Servidores" $fecha_escaneo
py Format_and_join_sheets.py "Dispositivos de red" $fecha_escaneo
py join_last_files.py
#mkdir Final
mv 'Final_subir_a_bd.csv' Final/
rm *.csv
echo '######################################'
echo 'Finalizado'
echo '######################################'