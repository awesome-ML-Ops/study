from sklearn.metrics import precision_recall_curve
import sys
import sklearn.metrics as metrics
import conf

try: import cPickle as pickle   # python2
except: import pickle           # python3

model_file = conf.model
test_matrix_file = conf.test_matrix
metrics_file = conf.model_metric_path

with open(model_file, 'rb') as fd:
    model = pickle.load(fd)

with open(test_matrix_file, 'rb') as fd:
    matrix = pickle.load(fd)

labels = matrix[:, 1].toarray()
x = matrix[:, 2:]

predictions_by_class = model.predict_proba(x)
predictions = predictions_by_class[:,1]

precision, recall, thresholds = precision_recall_curve(labels, predictions)

auc = metrics.auc(recall, precision)
#print('AUC={}'.format(metrics.auc(recall, precision)))
with open(metrics_file, 'w') as fd:
    fd.write('AUC: {:4f}\n'.format(auc))

