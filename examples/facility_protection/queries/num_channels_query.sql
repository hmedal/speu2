SELECT max(date), datasetName, numChannels, lb, ub FROM BaseExpr
WHERE (datasetName='grid-2x2_250')
AND date > '2017-06-27'
AND (numChannels=1 or numChannels=2 or numChannels=3)
AND (jamBudget=2)
GROUP BY datasetName, numChannels, lb, ub
ORDER BY datasetName, numChannels