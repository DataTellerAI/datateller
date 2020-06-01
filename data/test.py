from model import GenderClassifier
from model1 import GenderClassifier1
from model2 import GenderClassifier2

clf = GenderClassifier.load_model('saved_model.pickle')
clf1 = GenderClassifier1.load_model('saved_model1.pickle')
clf2 = GenderClassifier2.load_model('saved_model2.pickle')

some_names = ['Maria', 'Jose']

answer = clf.prediction(some_names)
print(answer)

answer = clf1.prediction(some_names)
print(answer)

answer = clf2.prediction(some_names)
print(answer)

