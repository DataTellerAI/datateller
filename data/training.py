from model import GenderClassifier

clf = GenderClassifier()
clf.ml_model()
clf.load_model('saved_model.pickle')
