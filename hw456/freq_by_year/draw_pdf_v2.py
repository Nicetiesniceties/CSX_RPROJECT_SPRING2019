import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import os
from tqdm import tqdm
import matplotlib.font_manager as mfm

font_path = "./chinese.simhei.ttf"
prop = mfm.FontProperties(fname = font_path)

PATH = "zh2year"
filename = open("zhyearbook") 
for line in tqdm(filename):
	year = os.path.join(PATH, line.strip("\n"))

	DICT = np.load(year).item()
	DICT = dict(sorted(DICT.items(), key = lambda x:x[1], reverse = True))
	keys = list(DICT.keys())
	values = list(DICT.values())
	if(len(keys) > 30):
		keys, values = keys[0:30], values[0:30]

	plt.bar(range(len(values)), values, color = '#fccf0d', edgecolor='#000000', width=1.0, lw=0.4)

	#plt.title("民國" + line.split("th")[0] + "年", fontproperties = prop)
	plt.ylabel("民國" + line.split("th")[0] + "年\n\n" + "Frequency", fontproperties = prop)
	plt.tick_params("y", labelrotation = 90)
	plt.xticks(range(len(keys)), keys, fontproperties = prop, rotation = 90)
	fig = plt.gcf()
	fig.subplots_adjust(bottom = 0.25)
	plt.savefig("民國" + line.split("th")[0] + "年髒話頻率比較"+ '.png', dpi=130, fontproperties = prop)
	plt.clf()

	from skimage import io
	from skimage import transform
	img = io.imread("民國" + line.split("th")[0] + "年髒話頻率比較"+ '.png')
	img = transform.rotate(img, 270, resize = True)
	io.imsave("民國" + line.split("th")[0] + "年髒話頻率比較"+ '.png', img)
