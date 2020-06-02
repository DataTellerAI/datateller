import matplotlib.pyplot as plt
import numpy as np
from model import GenderClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier


class GenderClassifier2(GenderClassifier):

    def __init__(self):
        self.model = DecisionTreeClassifier()

    def features(self, names):
        list_dic = []
        if not isinstance(names, list):
            names = names.tolist()
        for name in names:
            dic = {
                'first-letter': name[0],
                'last-letter': name[-1],
                'first2-letters': name[:2],
                'last2-letters': name[-2:],
                'first3-letters': name[:3],
                'last3-letters': name[-3:]}
            list_dic.append(dic)
        return list_dic

    def train(self, X_train, y_train):
        """
        Given training data, this method will fit the
        vectorizer(bag of words) and train the naive bayes model.
        Param:
            X_train(Pandas Series): training name dataset
            y_train(ndarray): training labels dataset
        """
        # preprocess data
        self.vec = DictVectorizer().fit(self.features(X_train))
        self.word_vec = self.vec.transform(self.features(X_train))
        # train the ML model
        self.clf = self.model.fit(self.word_vec, y_train)
        return self.clf

    def predict_gender(self, names, label_str=False):
        """
        Predict name's origin based on the test data.
        Returns encoded label by default, but returns
        label strings when label_str=True

        Param:
            names(ndarray/Pandas Series/list): containing names
            label_str(bool): default False, to return label
            integers, set it to True to return label strings
        Return:
            array: containing label integers or strings.
        """
        name_vector = self.vec.transform(self.features(names))
        pred = self.model.predict(name_vector)
        if not label_str:
            return pred
        else:
            result = self.label_encoder.inverse_transform(pred.reshape(-1, 1))
            return result.ravel()

    def predict_probability(self, names):
        """
        Predict probability of the name's gender based on the test data.
        Returns probability

        Param:
            names(ndarray/Pandas Series/list): containing names
        Return:
            array: containing probabilities.
        """
        name_vector = self.vec.transform(self.features(names))
        pred = self.model.predict_log_proba(name_vector)
        array = np.array([])
        for gender_probs in pred:
            result = np.round(np.max(gender_probs), 2)
            array = np.append(array, result)
        return array

    def plot_confusion(self, X_test, y_test):
        """
        Plot confusion matrix, based on given labels and prediction
        Param:
            yt(ndarray): array of ground truth labels
            prediction_test(ndarray): predicted labels
        """
        np.set_printoptions(precision=2)
        class_names = ['Hombre', 'Mujer']
        # Plot non-normalized confusion matrix
        titles_options = [("Confusion matrix, without normalization", None),
                          ("Normalized confusion matrix", 'true')]
        for title, normalize in titles_options:
            disp = plot_confusion_matrix(self.clf,
                                         self.vec.transform(self.features(X_test)),
                                         y_test,
                                         display_labels=class_names,
                                         cmap=plt.cm.Blues,
                                         normalize=normalize)
            disp.ax_.set_title(title)
            # print(title)
            # print(disp.confusion_matrix)
        plt.show()