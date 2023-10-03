# StellarGraph approach research paper classification
Author: **Tchangmena A Nken Allassan**

Date published : `August 21th, 2021`

Date Updated :   `June 26th, 2023`

### About:

This note book provide an approach to classify subject of scientific papers. Initially, we taught of a simple machine learning to implement, but with the idea of **network link** in the task proposal, we directed the ideas to **graph machine learning**. The structure of the data is in such a way that it is composed of numerous nodes linked together (5429 links), with each scientific paper in the dataset represented by a 0/1 valued word vector.

The problem is a multiclass classification problem and using the notion of [graph convolutional neural network](https://www.topbots.com/graph-convolutional-networks/) (`GCN`),more precisely a stellargraph  we have achieved the task with an accuracy score of approximately 95.76% with *100 epochs* and 97.34% with *200 epochs*



#### dependencies

1. Uncomment the 4-th line of the next cell inorder to install stellargraph
  ```python
 pip install -q stellargraph
   ```

4. Uncomment the  cell with command (!unzip "cora.zip") to unzip the file of the cora data set (the code is run in google colab) the zip file was first imported there  (after unziping the data set directory appear to be **cora/cora** this can change if you are working in another enviroment, just need to paste the directory in which the unzip folder is located).

5. The function *Gmodel* takes as input the data file directory, the number of folds *k* the learning rate *lr* and the  epoch size *epochs*
6. The model takes approximately 4mins:14sec to run (with 100 epochs) and 9min:10sec to run with 200 epochs.
7. Working on colab, you just need to upload the zip file associated to this repository and put in the directory of the unzip file in the function called *Gmodel*

#### How it works
Graph convolutional neural network (GCN) work directly with Graph data in our case the cora dataset, in which each data point is represented as a node
and there exist communications with one another. For each node, we get the feature information from all its neighbors together with the feature of itself. Finally, we feed these average values into a neural network to perform predictions. Similarly with stellargraph , we create a generator to convert the graph structure and node features into a format that can easily be fitted into the a deeplearning model for training or prediction.

The generator just encodes the information required to produce the model inputs. A function called *generator.flow* taking as input  a set of nodes and their true labels produces an object that can be used to train the model, on those nodes and labels that were specified.Using the *K-fold* cross validation function of sklearn, we create a set of training and testing set. We then perform the mean of the set of predicted output from each fold to minimize our error. The output are in the form of probabilities (using softmax function),so we perform an inverse transformation to obtain the original labels.

The metric used is the *accuracy_score* 

#### major update
`Revisited the GCN architecture used and accuracy slightly improved see notebook`

#### NB
1. The function *LabelBinarizer* transform the labels into an a tensor (adjacency tensor) describing the relation between set of nodes (1 if there's a relation and 0 if there isn't)
2.  Scroll down the bottom of the notebook to see the results of the model performance
3.  Enjoy :)
