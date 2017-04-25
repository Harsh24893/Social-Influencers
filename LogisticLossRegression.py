import numpy as np
import load_test_data
import pre_process
import scipy as sp
import write_to_csv
from scipy.special import expit

def LogisticLoss(X,Y,W,lmda):
    size = X.shape[0]
    h = expit(X.dot(W))
    loss = lmda * W.dot(W)
    for i in range(len(Y)):
        if h[i]==0 or h[i]==1:
            continue
        logPart = -Y[i]*np.log(h[i])
        logPart -= (1-Y[i])*np.log(1-h[i])
        loss += logPart
    return loss

def LogisticGradient(x,y,W,lmda):
    size = x.shape[0]
    grad = np.zeros(size)
    W = np.transpose(W)
    h = expit(W.dot(x))
    delta = h-y
    grad = np.sum(x.dot(delta))
    grad += lmda*W
    return grad

def predict(W,x):
    W = np.transpose(W)
    h = expit((W.dot(x)))
    return h

def SgdLogistic(X, Y, maxIter, learningRate, lmda):
    W = np.zeros(X.shape[1])
    iter = 0
    loss_old = 0

    while iter < maxIter:
        for (xi, yi) in zip(X, Y):
            grad = LogisticGradient(xi, yi, W, lmda)
            W -= learningRate * grad


        loss = LogisticLoss(X, Y, W, lmda)
        print("Iteration : ", iter, "  Loss : ", loss)
        # if np.abs(loss_old - loss) < 0.001:
        #     break
        # else:
        #     loss_old = loss
        iter += 1

    return W


def LogisticRegression(X, Y, XDev, YDev, XTest, YTest, lmda, learningRate, maxIter=100):
    W = SgdLogistic(X, Y, maxIter, learningRate, lmda)
    nCorrect = 0.
    nIncorrect = 0.
    for i in range(len(Y)):
        y_hat = predict(W, X[i,])
        if y_hat >= 0.5:
            y_hat = 1
        else:
            y_hat = -1
        # y_hat = np.sign(X[i,].dot(W))

        if y_hat == Y[i]:
            nCorrect += 1
        else:
            nIncorrect += 1
    trainAccuracy = nCorrect / (nCorrect + nIncorrect)

    nCorrect = 0.
    nIncorrect = 0.
    for i in range(len(YDev)):
        y_hat = predict(W, XDev[i,])
        if y_hat >= 0.5:
            y_hat = 1
        else:
            y_hat = -1
        # y_hat = np.sign(XDev[i,].dot(W))

        if y_hat == YDev[i]:
            nCorrect += 1
        else:
            nIncorrect += 1
    devAccuracy = nCorrect / (nCorrect + nIncorrect)

    prob = []
    nCorrect = 0.
    nIncorrect = 0.
    for i in range(len(YTest)):
        y_hat = predict(W, XTest[i,])
        prob.append(y_hat)
        if y_hat >= 0.5:
            y_hat = 1
        else:
            y_hat = -1
        #y_hat = np.sign(XTest[i,].dot(W))

        if y_hat == YTest[i]:
            nCorrect += 1
        else:
            nIncorrect += 1

    testAccuracy = nCorrect / (nCorrect + nIncorrect)

    write_to_csv.writeToCSV('predictions.csv', prob)
    return trainAccuracy,devAccuracy,testAccuracy


if __name__ == "__main__":
    X_train, Y_train, X_dev, Y_dev = pre_process.preprocessData('train.csv')
    X_test, Y_test = load_test_data.loadTestData('test.csv')

    lmda = 0.01
    learningRate = 0.001
    maxIter = 100
    accuracyTrain,accuracyDev,accuracyTest = LogisticRegression(X_train, Y_train,X_dev, Y_dev,X_test, Y_test, lmda, learningRate, maxIter)

    print('Accuracy Train: ',accuracyTrain)
    print('Accuracy Dev: ',accuracyDev)
    print('Accuracy Test: ', accuracyTest)