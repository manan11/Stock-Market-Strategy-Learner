import numpy as np
import random


class RTLearner(object):

    def __init__(self,leaf_size=1, verbose=False):
        tree = np.array([[]])
        self.leaf_size = leaf_size
        self.mx_count=0
        pass  # move along, these aren't the drones you're looking for

    def author(self):
        return 'mmehta64'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0], dataX.shape[1] + 1])
        newdataX[:, 0:dataX.shape[1]] = dataX
        newdataX[:,-1]=dataY
        #print newdataX
        tree1 = self.build(newdataX)

        #print tree1
        self.tree = tree1



        # build and save the model

    def build(self,data):
        print data
        if data.shape[0] <= self.leaf_size:
            return np.array([[-1,data[0][-1],-1,-1]])
        else:
            mx=random.randint(0,data.shape[1]-2)
            #print mx
            splitval = np.median(data[:,mx])
            if splitval == np.amax(data[:,mx]):
                row = data[:,mx].argmax()
                return np.array([[-1,data[row][-1],-1,-1]])
            left_tree = self.build(data[data[:,mx]<=splitval])
            right_tree = self.build(data[data[:,mx]>splitval])
            root = np.array([[mx,splitval,1,left_tree.shape[0]+1]])
            return np.concatenate((np.concatenate((root,left_tree),axis=0),right_tree),axis=0)


    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        ans = np.empty(shape=points.shape[0])
        j=0
        for val in points:
            i=0
            while int(self.tree[i][0])!=-1:

                index = self.tree[i][0]
                index = int(index)
               #print val[index]
                if val[index] <= self.tree[i][1]:
                    i=i+1
                else:
                    i=i+int(self.tree[i][3])
                #print i
            ans[j]=self.tree[i][1]
            j+=1
        return ans

    def count(self, index, c):
        if int(self.tree[index][0]) == -1:
            return
        l = index + int(self.tree[index][2])
        r = index + int(self.tree[index][3])
        c += 1
        self.mx_count = max(self.mx_count, c)
        self.count(l, c)
        self.count(r, c)


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

