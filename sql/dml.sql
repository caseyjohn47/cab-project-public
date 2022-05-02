-- Relevant Queries for OverallMonthlyCostAvg
-- Total average cost of every month
SELECT * 
FROM OverallMonthlyCostAvg
ORDER BY month;

-- Month with highest average cost
SELECT * FROM OverallMonthlyCostAvg 
WHERE averageCost 
IN 
(SELECT MAX(averageCost) 
FROM OverallMonthlyCostAvg);

-- Month with lowest average cost
SELECT * FROM OverallMonthlyCostAvg 
WHERE averageCost 
IN 
(SELECT MIN(averageCost) 
FROM OverallMonthlyCostAvg);

-- Relevant Queries for MeterMonthlyCostAvg
-- Get all monthly averages for a certain meter
SELECT *
FROM MeterMonthlyCostAvg
WHERE meterName = ?
ORDER BY month;

-- Get all monthly averages for a certain month
SELECT *
FROM MeterMonthlyCostAvg
WHERE month = ?
ORDER BY meterName;

-- Month with highest average cost per meter
SELECT meterName, meterType, month, averageCost
FROM MeterMonthlyCostAvg 
WHERE averagecost IN 
(SELECT MAX(averageCost)
FROM MeterMonthlyCostAvg
GROUP BY meterName) 
ORDER BY meterName;

-- Month with lowest average cost per meter
SELECT meterName, meterType, month, averageCost
FROM MeterMonthlyCostAvg 
WHERE averagecost IN 
(SELECT MIN(averageCost)
FROM MeterMonthlyCostAvg
GROUP BY meterName) 
ORDER BY meterName;


-- Relevant queries for TypeMonthlyCostAvg
-- Get all monthly averages for a certain meter type
SELECT * 
FROM TypeMonthlyCostAvg
WHERE meterType = ? 
ORDER BY month;

-- Get the monthly averages for each meter type a certain month
SELECT * 
FROM TypeMonthlyCostAvg
WHERE month = ? 
ORDER BY meterType;

-- Average monthly cost per meter type
SELECT meterType, AVG(averageCost)
FROM TypeMonthlyCostAvg
GROUP BY meterType;

-- Month with highest average cost per meter type
SELECT meterType, month, averageCost
FROM TypeMonthlyCostAvg 
WHERE averagecost IN 
(SELECT MAX(averageCost)
FROM TypeMonthlyCostAvg
GROUP BY meterType) 
ORDER BY meterType;

-- Month with lowest average cost per meter type
SELECT meterType, month, averageCost
FROM TypeMonthlyCostAvg 
WHERE averagecost IN 
(SELECT MIN(averageCost)
FROM TypeMonthlyCostAvg
GROUP BY meterType) 
ORDER BY meterType;