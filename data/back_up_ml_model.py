import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix


df = pd.read_excel('/Users/campopinillos/Documents/Proyecto Final/nombresFull.xlsx')
df = df[df.Genero != 'Ambiguo']
pd.Categorical(df.Genero)
pd.crosstab(index=df['Probabilidad'], columns="count")
pd.crosstab(index=df['Genero'], columns="count")

db = df[df.Probabilidad == 1.0].filter(['Genero','Nombres'])

pd.crosstab(index=db['Genero'], columns="count")
print(db.head())

# Initialize and fit CountVectorizer with given text documents
vectorizer = CountVectorizer().fit(db['Nombres'])
vectorizer
# use the vectorizer to transform the document into word count vectors (Sparse)
name_vec = vectorizer.transform(db['Nombres'])
y = db['Genero'].values
print('shape of the vectorized data is: ', name_vec.shape)

X_train, X_test, y_train, y_test = train_test_split(name_vec, y, shuffle=True)

# train the ML model
model = MultinomialNB()
model.fit(X_train, y_train)
print('training completed!')

classifier = model.fit(X_train, y_train)
prediction = model.predict(X_test)

type(X_test)
print('shape of the vectorized data is: ', X_test.shape)

cm = confusion_matrix(y_test, prediction)
# Recall
recall = np.diag(cm) / np.sum(cm, axis = 1)
# Precision
precision = np.diag(cm) / np.sum(cm, axis = 0)
# Accuracy
acc = (prediction == y_test).mean()

print('accuracy: {}, precision: {}, recall: {}'.format(acc, precision, recall))

model.score(X_test, y_test)

np.set_printoptions(precision=2)
class_names=['Hombre','Mujer']
# Plot non-normalized confusion matrix
titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(classifier, X_test, y_test,
                                 display_labels=class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)
    print(title)
    print(disp.confusion_matrix)

plt.show()

# use vector.vocabulary for predict
name = ['Juliana','Julian','Juan','Juana','Luz','Carmen', 'Sharo', 'Sharito']
vectorizer = CountVectorizer().fit(db['Nombres'])
text_vector = vectorizer.transform(name)
model.predict(text_vector)
model.predict_proba(text_vector)
