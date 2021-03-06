## Class to perform the following algorithms for Comp 551 course
#	1. Logistic Regression with Gradient Descent
#	2. Naive Bayes
#	3. Linear Regression
#	Also with regularization


import numpy as np

class logistic:

	def __init__(self, alpha=0.07,iter_n=9000, lambd=0.01, ephsilon=1e-8):
		# initialization
		self.alpha = alpha
		self.iter_n = iter_n # Number of iterations for gradient descent
		self.lambd = lambd # regularization
		self.ephsilon = ephsilon # stopping parameter

	# Sigmoid function
	def sigmoid(self,a):
		return (1 / (1 + np.exp(-a)))

	def loss(self):
		# calculate wTx
		wTx = self.sigmoid(self.X.dot(self.W))
		#
		c1 = (-self.y.dot(np.log(wTx)))
		c2 = (1 - self.y).dot(np.log(1 - wTx))
		# Regularization
		r = 0.5 * 0.01 * np.sum(self.W[1:,] ** 2)
		loss = (c1 - c2 + r) / self.m
		return np.sum(loss)

	def gradient_descent(self):
		for i in range(0,self.iter_n):
			w = self.W
			wTx = self.sigmoid(np.dot(self.X,np.transpose(self.W)))
			diff = wTx - self.y
			# Update W. For first row skip
			self.W[0] = w[0] - self.alpha * (1.0 / self.m) * np.sum(diff.dot(self.X[:,0]))
			n = self.X.shape[1]
			# Can be done in vector operation
			for j in range(1,n):
				tempTheta = w[j] - self.alpha * (1.0 / self.m) * (np.sum(diff.dot(self.X[:,j])) + self.lambd * self.m * w[j])
				#print np.linalg.norm(tempTheta)
				self.W[j] = tempTheta
			#grad = np.sum(np.dot(diff,self.X))
			#self.W = self.W - self.alpha * (1.0 / self.m) * grad
			cost = self.loss()
			#print 'Iteration',i,'\tCost',cost

	def featureNormalize(self,X):
		Xc = X.copy()
		Xc = np.asarray(Xc)
		mean = np.mean(Xc,axis=0)
		std = np.std(Xc,axis=0)
		std[std == 0.0] = 1.0
		Xr = np.rollaxis(Xc, 0)
		Xr = Xr - mean
		Xr /= std
		return Xr

	def fit(self,X,y):
		# store dimensions for future use
		# m : Number of rows
		# n : Number of features
		self.m, self.n = X.shape
		# Feature Normalization
		Xn = X.copy()
		Xn = self.featureNormalize(Xn)
		# padding of X with 1's
		ones = np.array([1] * self.m).reshape(self.m, 1)
		self.X = np.append(ones,Xn,axis=1)
		self.y = y
		# Initialize W
		# Can be modified to random values
		self.W = np.array([0.0] * (self.n + 1))
		self.gradient_descent()

	def predict(self, X):
		X = np.array(X)
		# Feature Normalization
		Xn = X.copy()
		Xn = self.featureNormalize(Xn)
		m = Xn.shape[0]
		ones = np.array([1] * m).reshape(m, 1)
		Xi = np.append(ones,Xn,axis=1)
		p = self.sigmoid(np.dot(Xi,np.transpose(self.W)))
		np.putmask(p, p >= 0.5, 1.0)
		np.putmask(p, p < 0.5, 0.0)
		#print p
		return p

class linearRegression():
	def __init__(self, X=[0], y=0, alpha=0.07, model=1,iter_n=100, W=0, lambd=0.01):
		# Initialization
		self.alpha = alpha
		self.iter_n = iter_n # Number of iterations for gradient descent
		self.lambd = lambd # regularization

	def loss(self):
		wTx = np.dot(self.X,np.transpose(self.W))
		diff = wTx - self.y
		loss = (1. / (2 * self.m)) * (diff ** 2)
		return np.sum(loss)

	def gradient_descent(self):
		for i in range(0,self.iter_n):
			w = self.W
			wTx = np.dot(self.X,np.transpose(self.W))
			diff = wTx - self.y
			self.W = w - self.alpha * (1. / self.m) * diff.dot(self.X)
			#grad = np.sum(np.dot(diff,self.X))
			#self.W = self.W - self.alpha * (1.0 / self.m) * grad
			cost = self.loss()
			#print 'Iteration',i,'\tCost',cost

	# Feature Normalization Snippet
	def featureNormalize(self,X):
		Xc = X.copy()
		Xc = np.asarray(Xc)
		mean = np.mean(Xc,axis=0)
		std = np.std(Xc,axis=0)
		std[std == 0.0] = 1.0
		Xr = np.rollaxis(Xc, 0)
		Xr = Xr - mean
		Xr /= std
		return Xr

	def fit(self,X,y):
		self.m, self.n = X.shape
		Xn = X.copy()
		Xn = self.featureNormalize(Xn)
		ones = np.array([1] * self.m).reshape(self.m, 1)
		self.X = np.append(ones,Xn,axis=1)
		self.y = y
		self.W = np.array([0.0] * (self.n + 1))
		self.gradient_descent()

	def predict(self, X):
		X = np.array(X)
		m = X.shape[0]
		Xn = X.copy()
		Xn = self.featureNormalize(Xn)
		ones = np.array([1] * m).reshape(m, 1)
		Xr = np.append(ones,Xn,axis=1)
		p = np.dot(Xr,np.transpose(self.W))
		#print p
		return p

class NaiveBayes():
	def __init__(self, X=[0],y=0,alpha=0.001,cutoff=0.5):
		# Initialization
		self.alpha = alpha
		self.cutoff = cutoff

	def value_counts(self,k):
		#print k
		uniq = set(list(k))
		d = {}
		for u in uniq:
			d[u] = np.sum(k==u)
		return d

	def featureMeanStd(self, col):
		mu = np.mean(col)
		sigma = np.std(col)
		return mu, sigma

	def pdf_Gaussian(self, xj, mu, sigma):
		return (1/(np.sqrt(2*np.pi) * sigma) * np.exp(-((xj - mu) ** 2)/(2*sigma ** 2)))

	def fit(self,X,y):
		self.X = np.array(X)
		self.y = np.array(y)
		self.m, self.n = self.X.shape
		Xt = self.X.T
		self.count_value = [self.value_counts(k) for k in Xt]  # list of dictionaries for every feature
		rec_where_pos = self.X[self.y == 1].T
		rec_where_neg = self.X[self.y == 0].T
		self.parameter_pos = []
		self.parameter_neg = []
		for index, item in enumerate(self.count_value):
		    if len(item) == 2:
		        self.parameter_pos.append(self.value_counts(rec_where_pos[index]))
		        self.parameter_neg.append(self.value_counts(rec_where_neg[index]))
		    elif len(item) > 2:
		        mu1, sigma1 = self.featureMeanStd(rec_where_pos[index])
		        mu0, sigma0 = self.featureMeanStd(rec_where_neg[index])
		        self.parameter_pos.append(np.array([mu1, sigma1]))
		        self.parameter_neg.append(np.array([mu0, sigma0]))
		self.total_pos = float(sum(self.y==1))
		self.total_neg = float(sum(self.y==0))
		total = self.total_pos + self.total_neg
		self.prior_prob_pos = self.total_pos / total
		self.prior_prob_neg = self.total_neg / total
		#print self.count_pos
		#print self.count_neg

	def predict(self,X_test):
		X_test = np.array(X_test)
		m, n = X_test.shape
		predictions = np.zeros(m)
		for i, rows in enumerate(X_test):  # i: sample index
		    probXneg = np.zeros(n)
		    probXpos = np.zeros(n)
		    for j, value in enumerate(rows): # j: feature index
		        if type(self.parameter_pos[j]) == type(X_test[0]):
		            mu1 = self.parameter_pos[j][0]
		            sigma1 = self.parameter_pos[j][1]
		            mu0 = self.parameter_neg[j][0]
		            sigma0 = self.parameter_neg[j][1]
		            probXpos[j] = self.pdf_Gaussian(value, mu1, sigma1)
		            probXneg[j] = self.pdf_Gaussian(value, mu0, sigma0)
		        elif type(self.parameter_pos[j] == type(self.count_value[j])):
		            n_count = self.parameter_neg[j].get(value,0)
		            p_count = self.parameter_pos[j].get(value,0)
		            probXpos[j] = (p_count + self.alpha) / (self.total_pos + self.alpha * len(self.parameter_pos[j]))
		            probXneg[j] = (n_count + self.alpha) / (self.total_neg + self.alpha * len(self.parameter_neg[j]))
		    predictions[i] = np.log(self.prior_prob_pos) + np.sum(np.log(probXpos)) - np.log(self.prior_prob_neg) - np.sum(np.log(probXneg))
		p = predictions
		np.putmask(p, p >= self.cutoff, 1.0)
		np.putmask(p, p < self.cutoff, 0.0)
		return p

# Implementing cross validation keeping a bit similarity with scikit-learn api
class cross_validation:
	def cross_val_score(self,clf,X,y,cv=1):
		scores = []
		preds = []
		splitX = np.split(np.array(X),cv,axis=0)
		splitY = np.split(np.array(y),cv,axis=0)
		for i in range(cv):
			splX = splitX[:]
			splY = splitY[:]
			X_test = splX.pop(i)
			X_train = np.concatenate(splX,axis=0)
			y_test = splY.pop(i)
			y_train = np.concatenate(splY,axis=0)
			clf.fit(X_train,y_train)
			y_pred = clf.predict(X_test)
			preds.extend(y_pred.tolist())
			if isinstance(clf,linearRegression):
				score = ((y_pred - y_test) ** 2).mean()
				print "Iteration ", i, "MSE :",score
			else:
				score =  np.mean(y_test == y_pred)
				print "Iteration ", i, "Accuracy :",score
			scores.append(score)
		return scores,preds




