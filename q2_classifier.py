import math
import sys
import getopt


def read_data(data):
    """
    data: path of the dataset

    return: dataset in list
    """
    data_feature = []
    file = open(data)
    for line in file:
        # feature_vector = []
        data_feature.append(line)
    return data_feature

def split_data(data):
    """
    data: raw dataset

    return:
    separated data
    """
    for i in range(0,len(data)):
        data[i] = data[i].split(" ")
    return data

def word_occ(mail):
    """
    mail: mail text with the words and counts

    return: dictionary with word and total count in the mails
    """
    dict = {}
    for i in range(0,len(mail)-2,2):
        if mail[i] not in dict.keys():
            dict[mail[i]] = int(mail[i+1])
    return dict

def vocab_gen(data):
    
    """
    data: dataset

    return: list of data in dictionary form
    
    """

    data = split_data(data)
    instances=[]
    for instance in data:
        dict={}
        dict["email"] = instance[0]
        dict["class"] = instance[1]
        dict["mail"] = word_occ(instance[2:])
        instances.append(dict)
    return instances
def get_vocab(instances):
    """"
    instances: dataset

    return: dictionary of word count
    """
    vocab={}
    for instance in instances:
        for word in instance["mail"]:
            if word in vocab:
                vocab[word] = vocab[word] + instance["mail"][word]
            else:
                vocab[word]=instance["mail"][word]
    return vocab

def get_spam(instances):
    """
    instances: dataset

    return: dictionary of spam word count, total count of spam
    """
    vocab_spam={}
    count = 0
    for instance in instances:
        if instance["class"] == 'spam':
            count+=1
            for word in instance["mail"]:
                if word in vocab_spam:
                    vocab_spam[word] = vocab_spam[word] + instance["mail"][word]
                else:
                    vocab_spam[word]=instance["mail"][word]
    return vocab_spam,count

def get_ham(instances):
    """
    instances: dataset

    return: dictionary of ham word count, total count of ham
    """
    vocab_ham={}
    count = 0
    for instance in instances:
        if instance["class"] == 'ham':
            count+=1
            for word in instance["mail"]:
                if word in vocab_ham:
                    vocab_ham[word] = vocab_ham[word] + instance["mail"][word]
                else:
                    vocab_ham[word]=instance["mail"][word]
    return vocab_ham, count
def classify(vocab_ham, vocab_spam, vocab_train, spam_count, ham_count,test, total):
    """"
    vocab_ham: dictionary of ham word count
    vocab_spam: dictionary of spam word count
    vocab_train: dictionary of all word count
    spam_count: number of spam words
    ham_count: number of ham words
    test: test data
    total: number of words

    return: number of test data, predictions, mail_ids
    """
    prob_s = float(spam_count)/total
    prob_h = float(ham_count)/total

    output=[]
    mail_id = []
    count = 0 
    for instance in test:
        p_spam = 0
        p_ham = 0
        for word in instance["mail"]:
            
            if word in vocab_ham:
                p = math.log(float((vocab_ham[word])+1)/(vocab_train[word]))
            else:
                #apply smoothing
                p = math.log(1.0/(ham_count+10))
            p_ham = p_ham + p

            if word in vocab_spam:
                p = math.log(float((vocab_spam[word])+1)/(vocab_train[word]))
            else:
                #apply smoothing
                p = math.log(1.0/(spam_count+10))
            p_spam = p_spam + p

        prob_s_n = prob_s * p_spam
        prob_h_n = prob_h * p_ham

        if prob_s_n >= prob_h_n:
            label = 'spam'
        else:
            label = 'ham'
        output.append(label)
        mail_id.append(instance["email"])
        if label == instance["class"]:
            count =count + 1
            
    return count,output,mail_id


train_path = ""
test_path = ""
output_path =""

opts, args = getopt.getopt(sys.argv[1:], "f1:f2:o:")
for opt,arg in opts:
    if opt == '-1':
        train_path = arg
    if opt =='-2':
        test_path = arg
    if opt =='-o':
        output_path = arg
if train_path=="":
    train_path="train"
if test_path =="":
    test_path = "test"
if output_path =="":
    output_path = "output.csv"

print("\n-----------------Reading Data -----------------\n")
data_train = read_data(train_path)
data_test = read_data(test_path)

print("Data File:", train_path)
print("Number of Rows: ", len(data_train))

print("Data File:", test_path)
print("Number of Rows: ", len(data_test)) 

print("\n-----------------Generating Vocabs-----------------\n")


train = vocab_gen(data_train) # generate vocab of training data
total_train = len(train)      


test = vocab_gen(data_test) # generate vocab of testing data
total_test = len(test)


vocab_train = get_vocab(train) # generate dictionary vocab of training data
vocab_test = get_vocab(test) # generate dictionary vocab of testing data 

vocab_spam, spam_count = get_spam(train)  #generate spam dictionary vocab of training data 
vocab_ham, ham_count = get_ham(train) #generate ham dictionary vocab of training data 

print("\n-----------------Getting Precitions-----------------\n")
count,predictions, mail_id = classify(vocab_ham, vocab_spam, vocab_train, spam_count, ham_count,test, total_train) # classify the testing data
acc = float(count)/total_test                                                                                      # get accuracy of test predictions
print("Total", total_test)  
print("Accuracy", acc)

print("\n-----------------Saving Output-----------------\n")
with open(output_path, 'w') as csv_1:                                                                           # save predictions
    for p in predictions:
        csv_1.write(str(p)+"\n")


