SELECT max(date), datasetName, lb, ub FROM BaseExpr
WHERE (datasetName='grid-2x2_250')
AND date > '2017-06-27'
AND (numChannels=1)
AND (jamBudget=2)
GROUP BY datasetName, lb, ub
ORDER BY datasetName, numChannels