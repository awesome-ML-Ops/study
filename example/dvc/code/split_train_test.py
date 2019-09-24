import pandas as pd
from sklearn.model_selection import train_test_split
import conf

INPUT = conf.source_tsv

def output_name(fname, suffix):
    idx = fname.rfind('.')
    if idx < 0:
        return fname
    i = len(fname) - idx
    return fname[:-i] + suffix + fname[-i:]

import sys
try: #python2
    reload(sys)
    sys.setdefaultencoding('utf-8')
except: pass

if len(sys.argv) != 3:
    print(len(sys.argv))
    sys.stderr.write('Arguments error. Usage:\n')
    sys.stderr.write('\tpython split_train_test.py TEST_RATIO SEED\n')
    sys.stderr.write('\t\tTEST_RATIO - train set ratio (double). Example: 0.3\n')
    sys.stderr.write('\t\tSEED - random state (integer). Example: 20170423\n')
    sys.exit(1)

test_ratio = float(sys.argv[1])
seed = int(sys.argv[2])
train = conf.train_tsv
test = conf.test_tsv

df = pd.read_csv(
    INPUT,
    encoding='utf-8',
    header=None,
    delimiter='\t',
    names=['id', 'label', 'text']
)

df_positive = df[df['label'] == 1]
df_negative = df[df['label'] == 0]

sys.stderr.write('Positive size {}, negative size {}\n'.format(
    df_positive.shape[0],
    df_negative.shape[0]
))

def sub_df_by_ids(df, ids):
    df_train_order = pd.DataFrame(data={'id': ids})
    return df.merge(df_train_order, on='id')

def train_test_split_df(df, ids, test_ratio, seed):
    train_ids, test_ids = train_test_split(ids, test_size=test_ratio, random_state=seed)
    return sub_df_by_ids(df, train_ids), sub_df_by_ids(df, test_ids)

df_pos_train, df_pos_test = train_test_split_df(df, df_positive.id, test_ratio, seed)
df_neg_train, df_neg_test = train_test_split_df(df, df_negative.id, test_ratio, seed)

df_train = pd.concat([df_pos_train, df_neg_train])
df_test = pd.concat([df_pos_test, df_neg_test])

df_train.to_csv(train, sep='\t', header=False, index=False)
df_test.to_csv(test, sep='\t', header=False, index=False)

