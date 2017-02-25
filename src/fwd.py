from scipy import signal
import numpy as np
import activations as act
import sys
sys.path.append('../')
import config

activation = config.activation
pool = config.pool

def convFwd(X, convFilters, bias):

    featureMaps = []
    for i in range(len(convFilters)):
        featureMap = []
        convFilter = convFilters[i]
        depth = len(convFilter)
        assert(depth == len(X)), 'Dimension Mismatch'
        for j in range(depth):
            featureMap.append(signal.convolve2d(X[j], convFilter[j],'valid'))
        featureMap = sum(featureMap) + bias[i]

        featureMaps.append(act.activation(featureMap, activation))
    return np.asarray(featureMaps)

def poolFwd(X, kernel, stride):
    assert( kernel == 2 ), 'Only Size 2 Kernel Supported Currently'
    assert( stride == 2 ), 'Only Size 2 Stride Supported Currently'
    postPool = []
    for i in range(len(X)):
        pre = X[i].reshape(X[i].shape[0]/2,2,X[i].shape[1]/2,2)
        if pool == 'max':
            postPool.append(pre.max(axis=(1,3)))
        elif pool == 'mean':
            postPool.append(pre.mean(axis=(1,3)))
        else :
            assert(1==2),'Invalid Pool option'
    return np.asarray(postPool)


def convpool(X, convFilters, bias, kernel, stride):
    assert( kernel == 2 ), 'Only Size 2 Kernel Supported Currently'
    assert( stride == 2 ), 'Only Size 2 Stride Supported Currently'

    featureMaps = []
    for i in range(len(convFilters)):
        featureMap = []
        convFilter = convFilters[i]
        depth = len(convFilter)
        assert(depth == len(X)), 'Dimension Mismatch'
        for j in range(depth):
            featureMap.append(signal.convolve2d(X[j], convFilter[j],'valid'))
        featureMap = act.activation(sum(featureMap) + bias[i],activation)

        pre = featureMap.reshape(featureMap.shape[0]/2,2,featureMap.shape[1]/2,2)
        if pool == 'max':
            featureMaps.append(pre.max(axis=(1,3)))
        elif pool == 'mean':
            featureMaps.append(pre.mean(axis=(1,3)))
        else :
            assert(1==2),'Invalid Pool option'

    return np.asarray(featureMaps)

