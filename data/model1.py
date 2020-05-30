from model import GenderClassifier
from sklearn.linear_model import SGDClassifier


class GenderClassifier1(GenderClassifier):

	def __init__(self):
		self.model = SGDClassifier()