import numpy as np
import random
from scipy import stats

class BagLearner(object):

    def __init__(self,learner,kwargs,bags,boost,verbose):

        self.bags=bags
        tree = np.array([[]])
        self.learners = []
        for i in range(0,self.bags):
            #self.learner = learner()
            self.learners.append(learner(**kwargs))


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
        for i in range(0, self.bags):
            data=np.empty([newdataX.shape[0],newdataX.shape[1]])
            for j in range(0,newdataX.shape[0]):
                index = random.randrange(newdataX.shape[0])
                #print index
                data[j,:] = newdataX[index,:]
                #print data[j,:]

            dataX=data[:,0:dataX.shape[1]]
            dataY=data[:,-1]
        #print dataX
        #print dataY

            self.learners[i].addEvidence(dataX,dataY)
            #print tree1
            #self.tree = tree1




        # build and save the model

    '''def build(self,data):
        if data.shape[0] <= self.leaf_size:
            return np.array([[-1,data[0][-1],-1,-1]])
        else:
            coef = np.zeros(data.shape[1]-1)
            #temp = np.corrcoef(data[:, 1],data[:, data.shape[1]-1])
            #print data.shape[1]
         #   print np.corrcoef(data[: 0,data.shape[1]-1],data[: data.shape[1]-1])
            for i in range(0,data.shape[1]-1):
                temp = np.corrcoef(data[:, i],data[:, -1])
                coef[i]=np.absolute(temp[0][1])

            mx=coef.argmax()

            splitval = np.median(data[:,mx])
            if splitval == np.amax(data[:,mx]):
                row = data[:,mx].argmax()
                return np.array([[-1,data[row][-1],-1,-1]])
            left_tree = self.build(data[data[:,mx]<=splitval])
            right_tree = self.build(data[data[:,mx]>splitval])
            root = np.array([[mx,splitval,1,left_tree.shape[0]+1]])
            return np.concatenate((np.concatenate((root,left_tree),axis=0),right_tree),axis=0) '''

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        ans1=np.empty([points.shape[0],self.bags])
        j=0
        #ans = np.empty(shape=points.shape[0])
        for i in range(0,self.bags):
            ans1[:,j]=self.learners[i].query(points)
            j+=1
        ans=np.empty(shape=ans1.shape[0])
        for i in range(0,ans.shape[0]):
            res = stats.mode(ans1[i, :])
            ans[i] = res[0][0]

        return ans


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"

