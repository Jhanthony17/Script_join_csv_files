import csv
import os
import glob
import pandas as pd

result = glob.glob('*.{}'.format('csv'))
#split_result = result.split(',')
zize=len(result)
frames = []

for i in result:
	df = pd.read_csv(i)
	frames.append(df)

concat_frames = pd.concat(frames)
concat_frames.to_csv('Final_subir_a_bd.csv', index=False)