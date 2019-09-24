import os

data_dir = 'data'

source_xml = os.path.join(data_dir, 'Posts.xml')
source_tsv = os.path.join(data_dir, 'Posts.tsv')

train_tsv = os.path.join(data_dir, 'Posts-train.tsv')
test_tsv = os.path.join(data_dir, 'Posts-test.tsv')

train_matrix = os.path.join(data_dir, 'matrix-train.pkl')
test_matrix = os.path.join(data_dir, 'matrix-test.pkl')

model = os.path.join(data_dir, 'model.pkl')
model_metric_path = 'metrics/auc.metric'
