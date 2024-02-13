# -*- coding: utf-8 -*-
"""DICE_Research_group.ipynb

Automatically generated by Colaboratory.


Original file is located at
    https://colab.research.google.com/drive/18oJYzWKONG2mk3ZjsaQ0wmahaVuxHkk8

Author: **Tchangmena A Nken Allassan**

Date published : *October 29, 2022*

### About:

This note book provide an approach to classify subject of scientific papers. Initially, I taught of a simple machine learning to implement, but with the idea of **network link** in the task proposal, I directed the ideas to **graph machine learning**. The structure of the data is in such a way that it is composed of numerous nodes linked together (5429 links), with each scientific paper in the dataset represented by a 0/1 valued word vector.

The problem is a multiclass classification problem and using the notion of [graph convolutional neural network](https://www.topbots.com/graph-convolutional-networks/),more precisely a stellargraph  we have achieved the task with an accuracy score of approximately $95.716\%$ using **100 epochs** and an accuracy score of approximately $97.415\%$ with **200 epochs*



#### dependencies

1. Uncomment the $4^{th}$ line of the next cell inorder to install stellargraph (#% pip install -q stellargraph)

2. Uncomment the next cell (!unzip "cora.zip") to unzip the file of the cora data set (the code is run in google colab) the zip file was first imported there  (after unziping the data set directory appear to be **cora/cora** this can change of you are working in another enviroment, just need to paste the directory in which the unzip folder is locsted).

3. The function *Gmodel* takes as input the data file directory, the number of folds *k* the learning rate *lr* and the  epoch size *epochs*
"""

import sys,os
#installing stellargraph with the command below

#%pip install -q stellargraph[demos]==1.0.0rc1

#!unzip "cora.zip"

#for this task will use graph convolutional neural network
#our case study will be stellargraph

#loading useful packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import stellargraph as sg
from sklearn.model_selection import KFold ,train_test_split #for cross validation
from sklearn.preprocessing import LabelBinarizer #for preprocessing

###for modeling ########
import tensorflow as tf
from stellargraph.mapper import FullBatchNodeGenerator
from stellargraph.layer import GCN

from tensorflow.keras import layers, optimizers, losses, metrics, Model

######## we start by loading the dataset, (question1) ##########################

data_dir = os.path.expanduser("cora/cora")
column_names =  ["subject"]
nodes= pd.read_csv(os.path.join(data_dir, "cora.content"), sep='\t', header=None, names=column_names)
nodes=pd.DataFrame(nodes).reset_index()
nodes=pd.DataFrame(np.array(nodes['subject']),index=nodes['level_0'],columns=['subject'])

nodes.head()  ###looking at some samples of the data

#now we define a function that performs both the cross validation and the modeling 

def Gmodel(data_dir,K,lr,epochs):
  """
  The function takes as input the data and the number of folds to 

  perform K-fold cross validation, modeling and prediction
  ---input------
  data: the data dir of the cora data_set example: cora/cora
  K: number of folds (our case 10)
  lr: learning rate of the training process
  epochs: Number of epochs 
  """
  
  ######## Loading the data ###################
  
  data_dir = os.path.expanduser(data_dir)
  column_names =  ["subject"]
  data= pd.read_csv(os.path.join(data_dir, "cora.content"), sep='\t', header=None, names=column_names)
  data=pd.DataFrame(data).reset_index()
  data=pd.DataFrame(np.array(data['subject']),index=data['level_0'],columns=['subject'])

  ##### This is also another way of loading the data

  loader=sg.datasets.Cora()
  G,nodes=loader.load()

  #creating a generator
  generator = FullBatchNodeGenerator(G, method="gcn")

  ###### k-fold performing K-fold cross validation ###########

  fold=KFold(n_splits=K, shuffle=False, random_state=1234) #no shuffling inorder not to shuffle the graph

  ### initializing an encoder
  encode=LabelBinarizer()

  ###creating an ndarray to add the predictions and obtain the mean #########
  prediction_=np.zeros((1,2708,7))

  for train_index,test_index in fold.split(data):
    
    x_train,x_test=data.iloc[train_index],data.iloc[test_index] # we split the data into K folds (based on the for loop)
   
    train_target=encode.fit_transform(x_train)        # then we generate the corresponding target for the train and validation set
    
    test_target=encode.fit_transform(x_test)

    ####creating a train generator #############

    train_gen = generator.flow(x_train.index, train_target)

    graph_conv = GCN(layer_sizes=[16, 16], activations=["relu", "relu"], generator=generator, dropout=0.5)  #we use the relu activation
                                                                                                            # and a dropout of 0.5
    x_input, x_output = graph_conv.in_out_tensors()  

    prediction = layers.Dense(units=train_target.shape[1], activation="softmax")(x_output)  #we use the softmax activation 
                                                                                            # because we are predicting 7 classes
    
    ####now we build the model ##############
    model = Model(inputs=x_input, outputs=prediction)
    model.compile(
    optimizer=tf.optimizers.Adam(lr),
    loss=losses.categorical_crossentropy,
    metrics=["acc"],)

    ##### creating a test generator #########

    test_gen = generator.flow(x_test.index, test_target)

    ####### fitting the model ###############

    history = model.fit(
    train_gen,
    epochs=epochs,
    validation_data=test_gen,
    verbose=True,
    shuffle=False)

    ########## now we perform predictions on the entire network ########

    entire_graph=data.index
    entire_generator = generator.flow(entire_graph)
    entire_predictions = model.predict(entire_generator)

    print(entire_predictions.shape)
    print(type(entire_predictions))
    ########appaend the predictions in a list ###################

    prediction_+= entire_predictions

    #######computing the mean of predictions ####################

  pred = prediction_/K       #remember K is the number of folds

    ########now we perform an inverse transformation to obtain the predicted output

  output_to_string = encode.inverse_transform(pred.squeeze())
  print(output_to_string)
  print(type(output_to_string))

  return pd.DataFrame({"paper_id": nodes.index, "class_label": output_to_string})

"""How to run the code?

-Just put in the name of the extracted folder of the cora dataset (zip): eg my case cora/cora (I'm working in google colab)
-number of folds K (can be changed ): our case is 10
-the learning rate (lr)
-the epoch size


"""

######## testing the code ##########################

results=Gmodel("cora/cora",K=10,lr=0.01,epochs=200)

####result obtained #################
results.head()

####saving to tsv file ########

results.to_csv('prediction.tsv', sep='\t', index=False)

#### now we evaluate the performance of the model using accuracy_score ########
from sklearn.metrics import accuracy_score

print('percentage of samples with their label classified correctly: {}%'.format(accuracy_score(nodes.subject.values,results.class_label.values)*100))
