from model import GenderClassifier
from model1 import GenderClassifier1
from model2 import GenderClassifier2

path = '/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx'

clf = GenderClassifier2()
clf.ml_model(df=path, output='saved_model2.pickle')

clf = GenderClassifier1()
clf.ml_model(df=path, output='saved_model1.pickle')

clf = GenderClassifier()
clf.ml_model(df=path)