DROP VIEW IF EXISTS MeterMonthlyCostAvg;
DROP VIEW IF EXISTS TypeMonthlyCostAvg;
DROP VIEW IF EXISTS OverallMonthlyCostAvg;
DROP TABLE IF EXISTS GREEN_POWER_INFO;
DROP TABLE IF EXISTS DISPOSED_WASTE_METER_INFO;
DROP TABLE IF EXISTS RENEWABLE_METER_INFO;
DROP TABLE IF EXISTS GENERATION_FACILITY;
DROP TABLE IF EXISTS METER_ENTRY;
DROP TABLE IF EXISTS CUSTOM_METER_INFO;
DROP TABLE IF EXISTS METER_INFO;

CREATE TABLE METER_INFO (
meterName varchar(50) PRIMARY KEY,
propertyName varchar(255), 
portfolioManagerId varchar(7), 
portfolioManagerMeterId varchar(8), 
meterType varchar(255), 
units varchar(255), 
measurementMethod varchar(255), 
includedInPropertyMetricsYn BOOLEAN, 
dateActive Date, 
dateInactive Date, 
dateFirstEntry Date, 
dateLastEntry Date, 
aggregateYn BOOLEAN, 
rateCode varchar(10), 
rateCodeDescription varchar(255)
);

CREATE TABLE CUSTOM_METER_INFO ( 
meterName varchar(50) REFERENCES METER_INFO, 
customIdName varchar(255), 
customIdValue varchar(255), 
priority int
);

CREATE TABLE METER_ENTRY ( 
meterConsumptionId bigint PRIMARY KEY, 
meterName varchar(50) REFERENCES METER_INFO, 
month int, 
year int, 
usage NUMERIC(10,2), 
cost NUMERIC(10,2), 
estimationYn BOOLEAN, 
lastModifiedDate Date, 
lastModifiedBy varchar(255)
);

CREATE TABLE GENERATION_FACILITY ( 
generationFacilityId varchar(255) PRIMARY KEY, 
generationLocation varchar(255), 
egridSubregion varchar(255), 
generationFacilityLocation varchar(255)
);

CREATE TABLE GREEN_POWER_INFO ( 
meterConsumptionId int REFERENCES METER_ENTRY, 
quantity int, 
biogasPercent NUMERIC(5,3), 
geothermalPercent NUMERIC(5,3), 
hydropowerPercent NUMERIC(5,3), 
solarPercent NUMERIC(5,3), 
windPercent NUMERIC(5,3), 
unknownPercent NUMERIC(5,3), 
generationFacilityId varchar(255) REFERENCES GENERATION_FACILITY
);

CREATE TABLE RENEWABLE_METER_INFO (
meterConsumptionId int REFERENCES METER_ENTRY, 
usedOnSiteYn BOOLEAN, 
usedOnSiteUnits int, 
exportedOffSiteYn BOOLEAN, 
exportedOffSiteUnits int, 
Cost NUMERIC(20,2), 
recOwnership varchar(255),
generationFacilityId varchar(255) REFERENCES GENERATION_FACILITY
);

CREATE TABLE DISPOSED_WASTE_METER_INFO ( 
meterConsumptionId int REFERENCES METER_ENTRY, 
landfillPercent NUMERIC(5,3), 
incinerationPercent NUMERIC(5,3), 
unknownPercent NUMERIC(5,3)
);

CREATE VIEW MeterMonthlyCostAvg AS
SELECT METER_INFO.meterName, METER_INFO.meterType, METER_INFO.units, METER_ENTRY.month, AVG(METER_ENTRY.usage)::numeric(10,2)  as averageUsage, AVG(METER_ENTRY.cost)::numeric(10,2)  as averageCost
FROM METER_ENTRY LEFT JOIN METER_INFO ON METER_ENTRY.meterName = METER_INFO.meterName
GROUP BY METER_INFO.meterName, METER_ENTRY.month;

CREATE VIEW TypeMonthlyCostAvg AS
SELECT METER_INFO.meterType, METER_ENTRY.month, AVG(METER_ENTRY.usage)::numeric(10,2) as averageUsage, AVG(METER_ENTRY.cost)::numeric(10,2) as averageCost
FROM METER_ENTRY LEFT JOIN METER_INFO ON METER_ENTRY.meterName = METER_INFO.meterName
GROUP BY METER_INFO.meterType, METER_ENTRY.month;

CREATE VIEW OverallMonthlyCostAvg AS
SELECT month, AVG(cost)::numeric(10,2) as averageCost
FROM METER_ENTRY 
GROUP BY month;
