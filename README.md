# StellarGraph_approach_research_paper_classification
Author: **Tchangmena A Nken Allassan**

Date published : *August 25, 2021*

### About:

This note book provide an approach to classify subject of scientific papers. Initially, I taught of a simple machine learning to implement, but with the idea of **network link** in the task proposal, I directed the ideas to **graph machine learning**. The structure of the data is in such a way that it is composed of numerous nodes linked together (5429 links), with each scientific paper in the dataset represented by a 0/1 valued word vector.

The problem is a multiclass classification problem and using the notion of [graph convolutional neural network](https://www.topbots.com/graph-convolutional-networks/),more precisely a stellargraph  we have achieved the task with an accuracy score of approximately 95.76% with *100 epochs* and 97.34% with *200 epochs*



#### dependencies

1. Uncomment the 4-th line of the next cell inorder to install stellargraph (#% pip install -q stellargraph)

2. Uncomment the  cell with command (!unzip "cora.zip") to unzip the file of the cora data set (the code is run in google colab) the zip file was first imported there  (after unziping the data set directory appear to be **cora/cora** this can change of you are working in another enviroment, just need to paste the directory in which the unzip folder is locsted).

3. The function *Gmodel* takes as input the data file directory, the number of folds *k* the learning rate *lr* and the  epoch size *epochs*
4. The model takes approximately 4mins:14sec to run (with 100 epochs) and 9min:10sec to run with 200 epochs.
5. Working on colab, you just need to upload the zip file associated to this repository and put in the directory of the unzip file in the function called *Gmodel*

#### How it works
Graph convolutional neural network (GCN) work directly with Graph data in our case the cora dataset, in which each data point is represented as a node
and there exist communications with one another. For each node, we get the feature information from all its neighbors together with the feature of itself. Finally, we feed these average values into a neural network to perform predictions. Similarly with stellargraph , we create a generator (
