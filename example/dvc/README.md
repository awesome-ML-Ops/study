## 1. 초기화
```bash
    git clone git@github.com:awesome-ML-Ops/study.git
    # dvc 설치는 https://dvc.org/
    dvc init 
```

## 2. 가상환경 설정
```
   # lmza를 사용함으로 없는 경우 설치 필요 
    pyenv install 3.7.1
    pyenv virtualenv -f [pipeline-test] 3.7.1
    pyenv shell [pipeline-test]
```

## 3. data 다운로드
```bash
    mkdir data
    wget -P data https://data.dvc.org/tutorial/nlp/25K/Posts.xml.zip
dvc add data/Posts.xml.zip

git add data/Posts.xml.zip.dvc data/.gitignore
git commit -m "add dataset"
```

## 4. 작업단위 스테이지 정의

```bash
dvc run -d data/Posts.xml.zip \
          -o data/Posts.xml \
          -f extract.dvc \
          unzip data/Posts.xml.zip -d data
```

설명

- `data/Posts.xml.zip` 를 의존으로 두고 `data/Posts.xml` 를 산출물로 만드는 작업 명령 `unzip data/Posts.xml.zip -d data` 등록

```bash
dvc run -d code/xml_to_tsv.py -d data/Posts.xml \
          -o data/Posts.tsv \
          -f prepare.dvc \
          python code/xml_to_tsv.py 
```

설명 
- 해당 파이썬 코드를 참고하세요 

```bash
dvc run -d code/split_train_test.py -d data/Posts.tsv \
          -o data/Posts-train.tsv -o data/Posts-test.tsv \
          -f split.dvc \
          python code/split_train_test.py 0.2 20170426 
```

설명 
  - 파이썬 코드를 참고하세요


```bash
dvc run -d code/featurization.py -d data/Posts-train.tsv -d data/Posts-test.tsv \
          -o data/matrix-train.pkl -o data/matrix-test.pkl \
          -f featurize.dvc \
          python code/featurization.py
```

설명 
  - 파이썬 코드를 참고하세요

```bash
  dvc run -d code/train_model.py -d data/matrix-train.pkl \
          -o data/model.pkl \
          -f train.dvc \
          python code/train_model.py 20170426 
```

설명
- 파이썬 코드를 참고하세요.

```bash
  dvc run -d code/evaluate.py -d data/model.pkl -d data/matrix-test.pkl \
          -M metrics/auc.metric \
          -f evaluate.dvc \
          python code/evaluate.py
```

설명
- 파이썬 코드를 참고하세요.

## 5. 메트릭 보기

```
 dvc metric show -a
```

## 6. 전체 파이프라인 시각화 하기

```
   dvc pipeline show --ascii
```