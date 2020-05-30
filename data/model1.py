import numpy as np
from model import GenderClassifier
from sklearn.linear_model import SGDClassifier
# from sklearn.calibration import CalibratedClassifierCV


class GenderClassifier1(GenderClassifier):

    def __init__(self):
        # self.base_model = SGDClassifier(class_weight='balanced')
        # self.model = CalibratedClassifierCV(base_model)
        self.model = SGDClassifier()

    def predict_probability(self, names):
        """
        Predict probability of the name's gender based on the test data.
        Returns probability

        Param:
            names(ndarray/Pandas Series/list): containing names
        Return:
            array: containing probabilities.
        """
        name_vector = self.vec.transform(names)
        pred = self.model.decision_function(name_vector)
        array = np.array([])
        for gender_probs in pred:
            result = np.round(np.max(gender_probs), 2)
            array = np.append(array, result)
        return array

    # def predict_probability(self, names):
    #     """
    #     Predict probability of the name's gender based on the test data.
    #     Returns probability

    #     Param:
    #         names(ndarray/Pandas Series/list): containing names
    #     Return:
    #         array: containing probabilities.
    #     """
    #     pass
    #     name_vector = self.vec.transform(names)
    #     clf = self.model.fit(self.ml_model.x_train, self.ml_model.y_train)
    #     calibrator = CalibratedClassifierCV(clf, cv='prefit')
    #     mod = calibrator.fit(self.ml_model.x_train, self.ml_model.y_train)
    #     pred = self.mod.predict_proba(name_vector)
    #     array = np.array([])
    #     for gender_probs in pred:
    #         result = np.round(np.max(gender_probs), 2)
    #         array = np.append(array, result)
    #     return array
