"""  		   	  			    		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Manan Mehta (replace with your name)
GT User ID: mmehta64 (replace with your User ID)
GT ID: 903390740 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import random as rand  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class QLearner(object):
    def author(self):
        return 'mmehta64'
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  		   	  			    		  		  		    	 		 		   		 		  
        self.s = 0  		   	  			    		  		  		    	 		 		   		 		  
        self.a = 0
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna

        self.q_arr = np.zeros(shape=(num_states,num_actions))

        self.past = [0,0,0,0]
        self.past = np.array(self.past)
  		   	  			    		  		  		    	 		 		   		 		  
    def querysetstate(self, s):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Update the state without updating the Q-table  		   	  			    		  		  		    	 		 		   		 		  
        @param s: The new state  		   	  			    		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        self.s = s

        #action = rand.randint(0, self.num_actions-1)
        action = np.argmax(self.q_arr[s])
        self.a = action
        #print action
        #if self.verbose: print "s =", s,"a =",action
        return action  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def query(self,s_prime,r):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Update the Q table and return an action  		   	  			    		  		  		    	 		 		   		 		  
        @param s_prime: The new state  		   	  			    		  		  		    	 		 		   		 		  
        @param r: The ne state  		   	  			    		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			    		  		  		    	 		 		   		 		  
        """
        if self.dyna!=0:
            new_exp = [self.s,self.a,s_prime,r]
            self.past = np.vstack((self.past,new_exp))
            upper_bound  = self.past.shape[0]
            for i in range(0,self.dyna):
                index = rand.randint(1,upper_bound-1)
                temp = self.past[index]
                self.q_arr[temp[0]][temp[1]] = (1 - self.alpha) * self.q_arr[temp[0]][temp[1]] + self.alpha * (temp[3] + (self.gamma * self.q_arr[temp[2]][np.argmax(self.q_arr[temp[2]])]))
        else:
            self.q_arr[self.s][self.a] = (1-self.alpha)*self.q_arr[self.s][self.a] + self.alpha*(r+(self.gamma*self.q_arr[s_prime][np.argmax(self.q_arr[s_prime])]))
        prob = rand.random()
        if prob > self.rar:
            action = np.argmax(self.q_arr[s_prime])
        else:
            action = rand.randint(0, self.num_actions - 1)
            self.rar = self.rar * self.radr
        self.s = s_prime
        self.a = action
        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "Remember Q from Star Trek? Well, this isn't him"  		   	  			    		  		  		    	 		 		   		 		  
