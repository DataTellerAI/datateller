from model import GenderClassifier

clf = GenderClassifier()
clf.ml_model(data_frame='/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx')
clf.load_model('saved_model.pickle')
