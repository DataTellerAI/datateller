
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt



df = pd.read_excel('/Users/campopinillos/Documents/Proyecto Final/nombres.xlsx')
print(type(df))
print(df.head())
df.types
df = df[df.Genero != 'Ambiguo']
pd.Categorical(df.Genero)

df = df[df.Genero != 'Ambiguo']

pd.crosstab(index=df['Probabilidad'], columns="count")
pd.crosstab(index=df['Genero'], columns="count")

db = df[df.Probabilidad == 1.0].filter(['Genero','Nombres'])
print(type(db))

pd.crosstab(index=db['Genero'], columns="count")


print(db.head())


# Initialize and fit CountVectorizer with given text documents
vectorizer = CountVectorizer().fit(db['Nombres'])
vectorizer
# use the vectorizer to transform the document into word count vectors (Sparse)
word_mat = vectorizer.transform(db['Nombres'])
word_mat

name_vec = vectorizer.fit_transform(db['Nombres'])
y = db['Genero'].values
print('shape of the vectorized data is: ', name_vec.shape)

X_train, X_test, y_train, y_test = train_test_split(name_vec, y, shuffle=True)

# train the ML model
model = MultinomialNB()
model.fit(X_train, y_train)
print('training completed!')

classifier = model.fit(X_train, y_train)

prediction = model.predict(X_test)

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




# input = sys.argv[1].lower()
# gender = ''
# probability = ''
# # if (len(input) == 2): 
	
# name = input.split(" ") 

# if (name[0][-1] == 'a'): 
# 	gender = 'Female'
# 	probability = 1
# elif (name[0][-1] == 'o'): 
# 	gender = 'Male'
# 	probability = 1

print('Name: {}\nGender: {}\nProbability: {}'.format(input.title(), gender, probability))


