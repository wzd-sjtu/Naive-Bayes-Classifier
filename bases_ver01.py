import os
encoding='utf-8'

#  首先导入数据

train_cha=[]
train_sex=[]

with open("data/train.txt",'r',encoding='utf-8',errors='ignore') as f:
    first_line=True
    for line in f:
        if first_line is True:
            first_line=False
            continue
        sample=line.strip().split(',')
        train_cha.append(sample[1])
        if sample[2]=='0':
            train_sex.append("男") # man
        else:
            train_sex.append("女") #female

counter=0
vocabulary={}
girl_vocabulary={}
boy_vocabulary={}
for name,ssex in zip(train_cha, train_sex):
    counter+=1
    tokens=[word for word in name]
    sex=ssex
    for word in tokens:
        if word in vocabulary:
            vocabulary[word]+=1
        else:
            vocabulary[word]=1
        if sex=="女":
            if word in girl_vocabulary:
                girl_vocabulary[word]+=1
            else:
                girl_vocabulary[word]=1
        if sex=="男":
            if word in boy_vocabulary:
                boy_vocabulary[word]+=1
            else:
                boy_vocabulary[word]=1

print(vocabulary)
print("girl",girl_vocabulary)
print("boy",boy_vocabulary)

p_vocabulary_girl={}
p_vocabulary_boy={}
for key,value in vocabulary.items():
    if key in girl_vocabulary:
        p_vocabulary_girl[key]=girl_vocabulary[key]/value
        p_vocabulary_boy[key]=1-p_vocabulary_girl[key]
    else:
        p_vocabulary_boy[key]=boy_vocabulary[key]/value
        p_vocabulary_girl[key]=1-p_vocabulary_boy[key]

print("girl",p_vocabulary_girl)
print("boy",p_vocabulary_boy)
#  完成对数据的清洗

boy=0
girl=0

for key,value in girl_vocabulary.items():
    value=int(value)
    girl+=value
for key,value in boy_vocabulary.items():
    value=int(value)
    boy+=value

p_gender_boy=boy/(boy+girl)
p_gender_girl=girl/(boy+girl)
#  下面进入主循环
test_cha=[]
test_sex=[]

with open("data/test.txt",'r',encoding='utf-8',errors='ignore') as f:
    first_line=True
    for line in f:
        if first_line is True:
            first_line=False
            continue
        sample=line.strip().split(',')
        test_cha.append(sample[1])

result=[]
for name in train_cha:
    p_boy=1
    p_girl=1
    tokens = [word for word in name]
    for word in tokens:
        if word in p_vocabulary_boy:
            p_tmp_boy=p_vocabulary_boy[word]
            p_boy*=p_tmp_boy
            p_tmp_girl=p_vocabulary_girl[word]
            p_girl*=p_tmp_girl
        else:
            p_tmp_girl = p_vocabulary_girl[word]
            p_girl *= p_tmp_girl
    p_boy*=p_gender_boy
    p_girl*=p_gender_girl
    if p_boy>=p_girl:
        result.append(0)
    else:
        result.append(1)

print(result)


judge=[]

with open("data/sample_submit.csv",'r',encoding='utf-8',errors='ignore') as f:
    first_line=True
    for line in f:
        if first_line is True:
            first_line=False
            continue
        sample=line.strip().split(',')
        judge.append(sample[1])
print(judge)

counters=0
miss=0

for qq,mm in zip(result,judge):
    counter+=1
    if qq!=int(mm):
        miss+=1

print(1-miss/counter)

# 成功率居然有百分之八十九  还是可以的嘛。。