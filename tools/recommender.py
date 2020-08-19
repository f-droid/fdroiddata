# This file is a utility that adds additional information to the
# apps metadata (.yml) file by using simple Content-based filtering.

# Content based filtering takes the description of the item (apps in our case)
# and finds the top 3 apps with description closest to the current one.
# Here, no user data is required. Everything is calculated based on the
# description provided by the developer.

import os
import yaml  # to open and write yaml files
import pandas as pd
import numpy as np
import nltk  # open source NLP processing Toolkit to preprocess description
import string
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer # to createa bag of words and balance the weight
                                                            # This will help combat keyword-stuffing


###################################################
# prepare a dataframe with filename, appname and description
def get_meta_df():
    print("Accessing metadata...")
    os.chdir(os.getcwd()+'/..')
    print(os.getcwd())
    rowlist = []
    i = 0
    # get all .yml files from metadata
    for each in os.listdir('metadata/'): 
        if each.endswith('.yml') or each.endswith('.yaml'):
            each_row = {}
            with open('metadata/'+each) as f:
                hold_yaml_contents = yaml.safe_load(f)
            if 'Description' in hold_yaml_contents  :
                each_row['Filename'] = each
                if 'AutoName' in hold_yaml_contents:
                    each_row['AppName'] = hold_yaml_contents['AutoName']
                else:
                    each_row['AppName'] = 'Unnamed App'
                each_row['Description'] = hold_yaml_contents['Description']
            rowlist.append(each_row)
    print("Creating dataframe...")
    print("Dataframe created.")
    desc_df = pd.DataFrame(rowlist)
    desc_df['Description'] = desc_df['Description'].astype(str)
    desc_df['AppName'] = desc_df['AppName'].astype(str)
    desc_df = desc_df.dropna()
    return desc_df

###################################################
# Text preprocessing starts here
def text_preprocess(stri):
    # Remove Punctuations
    stri = "".join([str(c) for c in stri if c not in string.punctuation])
    # Tokenize
    tokens = nltk.word_tokenize(stri)
    tokens = [word.lower() for word in tokens]
    # Remove stopwords
    filtered_words = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]
    # get stemwords for each
    ps = PorterStemmer()
    stem_words = [ps.stem(word) for word in filtered_words]
    return ' '.join(stem_words)

###################################################
# a function to remove unwanted characters, words and find root words
def pre_process_descriptions(desc_df):
    # preprocess and update each description 
    print("Pre-processing app descriptions...")
    for index, row in desc_df.iterrows():
        row['Description'] = text_preprocess(row['Description'])
    print("Pre-processing complete.")
    return desc_df

###################################################
# Remove punctuations, get root words (walk, walking, walker, walked -> walk)
# and remove words with little information (a, the, is, to, etc)
def get_similar_idx(desc_df):
    print("Calculating similarities for each app...")
    vectorizer = TfidfVectorizer(min_df=1, stop_words='english')
    desc_corpus = list(desc_df['Description'].values)
    tfidf = vectorizer.fit_transform(desc_corpus)  
    similarity = tfidf * tfidf.T
    similarity_mat = similarity.toarray()
    print("Getting Top 3 most similar apps...")
    idx = (-similarity_mat).argsort()[:,:4]
    print(len(desc_df),len(similarity_mat), len(idx), len(idx))
    idx = idx[:,1:4]
    print(idx[:5,:]) 
    print("Top 3 apps calculated.")
    return idx, similarity_mat

# get top 3 similar appnames and add them to the yaml files
def update_metadata(idx,desc_df,similarity_mat):
    print("Adding similar app name and percentage to metadata...")
    for i, each in enumerate(idx):
            # uncomment next line if you want to see the progress
            print(i,each,desc_df.iloc[[each[2]]].Filename.values[0])  
            with open('metadata/'+str(desc_df.iloc[[i]].Filename.values[0])) as f:
                hold_yaml_contents = yaml.safe_load(f)
            # add the filenames
            hold_yaml_contents['Recommendation_1'] = desc_df.iloc[[each[0]]].Filename.values[0]
            hold_yaml_contents['Recommendation_2'] = desc_df.iloc[[each[1]]].Filename.values[0]
            hold_yaml_contents['Recommendation_3'] = desc_df.iloc[[each[2]]].Filename.values[0]
            # add correspomding similarity percentage for more information
            hold_yaml_contents['Recommendation_1_percent'] = float(similarity_mat[i][each[0]])*100
            hold_yaml_contents['Recommendation_2_percent'] = float(similarity_mat[i][each[1]])*100
            hold_yaml_contents['Recommendation_3_percent'] = float(similarity_mat[i][each[2]])*100
            # write
            if desc_df.iloc[[i]].Filename.values[0] != np.nan:
                with open('metadata/'+desc_df.iloc[[i]].Filename.values[0],'w') as f:
                    f.write(yaml.dump(hold_yaml_contents))
    print("Metadata updated.")

# simple calls
desc_df = pre_process_descriptions(get_meta_df())
idx, similarity_mat = get_similar_idx(desc_df)
update_metadata(idx,desc_df,similarity_mat)
