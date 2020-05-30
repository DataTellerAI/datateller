import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix


class GenderClassifier:
    """
    ML algorithm to classify names' nationality
    this class is NameClassifier model class
    Attributes:
        Vectorizer: to vectorize the data for prediction, CountVectorizer
        model: classifier for decision making, based on Naive Bayes
    Methods:
        load_data
        train
        evaluate
        predict_gender
        predict_probability
        prediction
        get_word_dict
        get_label_str
        plot_confusion
        saveModel
        loadModel
        ml_model
    """
    def __init__(self):
        """
        Creating a model to traing
        """
        self.model = MultinomialNB()

    def load_data(self, file_name, tSize=0.3):
        """
        Load the data, encode the labels, and split into train and test set.
        Params:
            file_names(string): file path & name to the csv or xlsx file
            test_size(float): ratio of testing set, between 0 & 1
        Return: x_train, x_test(as pandas series of names), y_train,
                y_test(as numpy arr of labels). These elements will be
                returned on the order above.

            Pandas Series: name data, X_train and X_test
            ndarray: encoded labels, y_train and y_test
        """
        df = pd.read_excel(file_name)
        # This is not always needed
        df = df[df.Genero != 'Ambiguo']
        df = df[df.Probabilidad == 1.0].filter(['Genero', 'Nombres'])
        # This is not always needed
        pd.Categorical(df.Genero)
        X = df['Nombres']
        labels = df['Genero'].values.reshape(-1, 1)
        self.label_encoder = OrdinalEncoder().fit(labels)
        labels = self.label_encoder.transform(labels)
        return train_test_split(X, labels.ravel(), test_size=tSize)

    def train(self, X_train, y_train):
        """
        Given training data, this method will fit the
        vectorizer(bag of words) and train the naive bayes model.
        Param:
            X_train(Pandas Series): training name dataset
            y_train(ndarray): training labels dataset
        """
        # fit the vectorizer
        self.vec = CountVectorizer().fit(X_train)
        self.word_vec = self.vec.transform(X_train)
        # train the ML model
        return self.model.fit(self.word_vec, y_train)

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
        name_vector = self.vec.transform(names)
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
        name_vector = self.vec.transform(names)
        pred = self.model.predict_proba(name_vector)
        array = np.array([])
        for gender_probs in pred:
            result = np.round(np.max(gender_probs), 2)
            array = np.append(array, result)
        return array

    def prediction(self, names, label_str=False):
        """
        Predict gender and probability of the name's gender
        based on the test data.
        Returns full answers with names

        Param:
            names(ndarray/Pandas Series/list): containing names
        Return:
            pd.Dataframe: containing answer.
        """
        gender = self.predict_gender(names)
        probab = self.predict_probability(names)
        df = pd.DataFrame({'Names': names,
                           'Gender': self.get_label_str(gender),
                           'Probability': probab})
        return df

    def evaluate(self, names, labels):
        """
        Make prediction, and evaluate the model's
        - Accuracy
        - Precision: Each element in returned vector represents
                     precision for each class.
        - Recall: Same as above, except recall for each class.
        for each class and overall.
        You can take average to get model wise precision and recall.
        Params:
            names(list/Pandas Series/ndarray): names data
            labels(ndarray): ground truth
        """
        pred = self.predict_gender(names)
        cm = confusion_matrix(labels, pred)
        # Recall
        recall = (np.diag(cm)) / (np.sum(cm, axis=1))
        # Precision
        precision = np.diag(cm) / (np.sum(cm, axis=0))
        # Accuracy
        acc = (pred == labels).mean()
        return {'accuracy': acc, 'precision': precision, 'recall': recall}

    def get_label_str(self, labels):
        """
        Accepts numerically encoded labels and returns
        corresponding label strings
            param:
                labels(ndarray): ndarray containing numerical labels
            returns:
                ndarray: containing label strings
        """
        res = self.label_encoder.inverse_transform(labels.reshape(-1, 1))
        return res.ravel()

    def plot_confusion(self, classifier, X_test, y_test):
        """
        Plot confusion matrix, based on given labels and prediction
        Param:
            yt(ndarray): array of ground truth labels
            prediction_test(ndarray): predicted labels
        """
        np.set_printoptions(precision=2)
        class_names=['Hombre','Mujer']
        
        # Plot non-normalized confusion matrix
        titles_options = [("Confusion matrix, without normalization", None),
                        ("Normalized confusion matrix", 'true')]
        for title, normalize in titles_options:
            disp = plot_confusion_matrix(classifier,
                                         self.vec.transform(X_test),
                                         y_test,
                                         display_labels=class_names,
                                         cmap=plt.cm.Blues,
                                         normalize=normalize)
            disp.ax_.set_title(title)
            # print(title)
            # print(disp.confusion_matrix)
        plt.show()

    def get_word_dict(self, corpus=None):
        """
        This method returns word frequency dictionary, from the training data
        of the model or given corpus if any.
        Params:
            corpus(list/Series): python list or pandas series of names.
            This is default to None, in which case frequency dictionary
            is created on the data the model was trained on.
        Returns:
            dictionary: python dictionary with names as keys,
                        and their frequencies as values.
        """
        freq_dic = {}
        if corpus is None:
            vector = self.vec
            bag_words = self.word_vec
        else:
            vector = CountVectorizer().fit(corpus)
            bag_words = vector.transform(corpus)

        feature = vector.get_feature_names()
        sum_words = bag_words.sum(axis=0).tolist()[0]  # list within list

        for i, word in enumerate(feature):
            freq_dic[word] = sum_words[i]

        return freq_dic

    @classmethod
    def load_model(cls, file_name):  # instance / class method??
        """
        Load saved model obj for use.
        Param:
            file_name(string): path to the model file(pickle).
        Return:
            NameClassifier: the loaded class obj for use.
        """
        # https://stackoverflow.com/questions/2709800/how-to-pickle-yourself
        # loading pickled saved model
        # loading itself from the pickle?? lol
        print('loading the model')
        return pickle.load(open(file_name, 'rb'))

    def save_model(self, file_name):
        """
        Save a trained model obj for future use.
        Param:
            file_name(string): path to the model file(pickle).
        """
        # save this class itself as pickle??
        pickle.dump(self, open(file_name, 'wb'))
    
    def ml_model(self, data_frame):
        """
        Run all model traing proccess and get output.
        Param:
            data_frame(string): path to the data.
        """
        x_train, x_test, y_train, y_test = self.load_data(file_name=data_frame, tSize=0.3)
        clf = self.train(x_train, y_train)
        metrics = self.evaluate(x_test, y_test)
        print('Accuracy: {}%\nPrecision: {}%\nRecall: {}%'.format(metrics['accuracy']*100,
                                                                  metrics['precision'][0]*100,
                                                                  metrics['recall'][0]*100))
        pred = self.predict_gender(x_test)
        self.plot_confusion(clf, x_test, y_test)
        self.save_model('saved_model.pickle')
