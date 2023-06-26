from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import joblib
#加载数据集
data = pd.read_csv('phishing_site_urls.csv')

# Extract features using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['URL'])
y = data['Label']

joblib.dump(vectorizer,'vectorizer.pkl')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('X_train shape:', X_train.shape)
print('y_train shape:', y_train.shape)
print('X_test shape:', X_test.shape)
print('y_test shape:', y_test.shape)


from sklearn.linear_model import LogisticRegression
# Train the logistic regression model
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)


# Make predictions on the test set
y_pred = lr.predict(X_test)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print('Accuracy:', accuracy_score(y_test, y_pred))
print('Precision:', precision_score(y_test, y_pred, pos_label='good'))
print('Recall:', recall_score(y_test, y_pred, pos_label='good'))
print('F1 score:', f1_score(y_test, y_pred, pos_label='good'))

joblib.dump(lr, 'model.pkl')

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=['good', 'bad'])

# Plot the confusion matrix
fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(cm, cmap='Blues')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['good', 'bad'])
ax.set_yticklabels(['good', 'bad'])
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='white')
ax.set_title('Confusion Matrix')
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
plt.show()