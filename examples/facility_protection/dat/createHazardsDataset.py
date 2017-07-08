import csv
import json
import math
import os

from examples.facility_protection.src import facpro

EARTH_RADIUS = 6378137     # earth circumference in meters

def great_circle_distance(latlong_a, latlong_b):
    lat1, lon1 = latlong_a
    lat2, lon2 = latlong_b
 
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
            math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d_meters = EARTH_RADIUS * c
    d_miles = (1.0/1000)*0.621371*d_meters
    return d_miles

def getHazardLevelForLocationInScenario(coorOfHazardCenter, coorOfLoc, severityRadii):
    distFromCenterToLocation = great_circle_distance(coorOfHazardCenter, coorOfLoc)
    hazardLevel = 0
    numLevels = len(severityRadii)
    #print "distFromCenterToLocation", coorOfHazardCenter, coorOfLoc, distFromCenterToLocation
    for level in reversed(range(numLevels)):
        if(distFromCenterToLocation <= severityRadii[level]):
            hazardLevel = numLevels - level
    #print "hazardLevel", hazardLevel
    return hazardLevel


def setPaths():
    global dataPath
    dataPath = 'daskin_data'

def readFromCSVFile(filepath, numLevels):
    centers = []
    severityRadii = []
    probabilities = []
    with open(filepath, 'rb') as csvfile:
        myReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        myReader.next()
        for row in myReader:
            index = 4
            latIndex = index
            index += 1
            lngIndex = index
            index += 1
            centers.append([float(row[latIndex]), float(row[lngIndex])])
            levelsRadii = []
            for levelIndex in range(numLevels):
                levelsRadii.append(float(row[index]))
                index += 1
            severityRadii.append(levelsRadii)
            probabilities.append(float(row[index]))
            #print ','.join(row)
    #print centers
    #print severityRadii
    #print probabilities
    return centers, severityRadii, probabilities
        
def createHazardsFile_allFullyExposedAlways(numFacs, numHazardLevels):
    endingStr = "_allFullyExposedAlways"
    hazards_dict = {}
    hazards_dict["numHazardLevels"] = numHazardLevels
    hazards_dict = {}
    for scenIndex in range(1):
        hazards_dict[scenIndex] = {}
        hazards_dict[scenIndex]['probability'] = 1.0
        hazards_dict[scenIndex]['exposures'] = [numHazardLevels - 1] * numFacs
    filename = dataPath + '/Hazards/hazardsDef_custom_facs' +str(numFacs) + '_levels' +str(numHazardLevels) \
               + endingStr + '.json'
    with open(filename, 'w') as outfile:
        json.dump(hazards_dict, outfile, indent=2)
    
def createHazardsFile_HalfExposedAlways(numFacs, numHazardLevels):
    endingStr = "_halfExposedAlways"
    hazards_dict = {}
    hazards_dict["numHazardLevels"] = numHazardLevels
    hazards_dict = {}
    for scenIndex in range(1):
        hazards_dict[scenIndex] = {}
        hazards_dict[scenIndex]['probability'] = 1.0
        hazards_dict[scenIndex]['exposures'] = [1] * numFacs
    filename = dataPath + '/Hazards/hazardsDef_custom_facs' +str(numFacs) + '_levels' +str(numHazardLevels) \
               + endingStr + '.json'
    with open(filename, 'w') as outfile:
        json.dump(hazards_dict, outfile, indent=2)

#conditional: if True, probabilities are normalized; meaning that the normalized probabilities are conditional
# probabilities, given that a hazard occurs
#
#
def createHazardsFile_readFromFile(numFacs, hazardsFilepath, locCoor, numLevels, conditional = True):
    centers, severityRadii, probabilities = readFromCSVFile(hazardsFilepath, numLevels)
    endingStr = ""
    print "probabilities", probabilities
    if(conditional):
        sumOfProbs = sum(probabilities)
        probabilitiesToWrite = [prob/sumOfProbs for prob in probabilities]
        endingStr = "_conditional"
    else:
        probabilitiesToWrite = probabilities
    print "probabilitiesToWrite", probabilitiesToWrite
    numScenarios = len(centers)
    numHazardLevels = len(severityRadii[0])+1
    hazards_dict = {}
    hazards_dict["numHazardLevels"] = numHazardLevels
    hazards_dict = {}
    for scenIndex in range(numScenarios):
        hazards_dict[scenIndex] = {}
        hazards_dict[scenIndex]['probability'] = probabilitiesToWrite[scenIndex]
        hazards_dict[scenIndex]['exposures'] = \
            [getHazardLevelForLocationInScenario(centers[scenIndex], locCoor[fac], severityRadii[scenIndex])
             for fac in range(numFacs)]
    if(not conditional):
        hazards_dict[numScenarios] = {}
        hazards_dict[numScenarios]['probability'] = 1-sum(probabilities)
        hazards_dict[numScenarios]['exposures'] = [0] * numFacs
    filename = dataPath + '/Hazards/hazardsDef_custom_facs' +str(numFacs) + '_levels' +str(numHazardLevels) \
               + endingStr + '.json'
    with open(filename, 'w') as outfile:
        json.dump(hazards_dict, outfile, indent=2)

if __name__ == "__main__":
    print "cwd", os.getcwd()
    num_hazard_levels = 2
    setPaths()
    hazardsFilePath = 'daskin_data/Hazards/list_of_hazard_scenarios_2_levels.csv'
    for p in [2,3,4,5,6,7,8,9,10]:
        dataset = facpro.Dataset(dataPath + '/Daskin49_FacPro_p' + str(p) + '.xml')
        locCoor = dataset.coor
        numFacs = len(locCoor)
        createHazardsFile_readFromFile(numFacs, hazardsFilePath, locCoor, num_hazard_levels, True)
        createHazardsFile_allFullyExposedAlways(numFacs, num_hazard_levels)
        createHazardsFile_HalfExposedAlways(numFacs, num_hazard_levels)
    print "completed"