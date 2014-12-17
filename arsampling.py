import numpy as np

__all__ = ['rejectionSampling']

def rejectionSampling(envPDF, envRV, targetPDF, n):
    """Generates n random variates from the target distribution
    using acceptance/rejection sampling with the envelope distribution, envPDF.
    
    Parameters
    ----------
    envPDF : func
        Takes an array of x and returns their probabilities
        times a constant, such that envPDF(x) > targetPDF(x), always.
    envRV : func
        Takes single arg n and returns n random variates from envPDF.
    targetPDF : func
        Takes array of x and returns their probabilities
    n : int
        Number of total samples to draw from targetPDF
    
    Returns
    -------
    arr : array
        Array of samples distributed proportionately to target PDF"""
    
    i = 0
    arr = np.zeros(n)
    acceptanceProbability = 1
    while i < n:
        """Draw as many samples as we expect to need,
        based on the acceptance probability (initially 1)"""
        neededN = n-i
        drawingN = int(np.ceil(neededN * (1/acceptanceProbability)))
        
        samples = envRV(drawingN)
        envPr = envPDF(samples)
        targetPr = targetPDF(samples)
        unifRVs = rand(drawingN)
        
        """Keep the samples that meet the acceptance criteria"""
        keepInds = unifRVs < (targetPr/envPr)
        actualN = keepInds.sum()
        if actualN < neededN:
            """Fill arr with all the samples that were accepted"""
            arr[i:(i+actualN)] = samples[keepInds]
        else:
            """Fill the rest of the arr with as many samples as needed"""
            arr[i:] = samples[keepInds][:neededN]
        
        if i == 0:
            """Estimate the acceptance probability the first time through"""
            acceptanceProbability = (targetPr/envPr).mean()
        
        i += actualN
    
    return arr