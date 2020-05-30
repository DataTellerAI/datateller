from model import GenderClassifier
from model1 import GenderClassifier1

clf = GenderClassifier()
clf.ml_model(df='/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx')

clf = GenderClassifier1()
clf.ml_model(df='/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx',
			 output='saved_model1.pickle')
