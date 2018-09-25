import json
import os

#This script uses the json dump directly from the DJANGO server interface and not the web

# Function to write data to json
# Ref: https://gist.github.com/keithweaver/ae3c96086d1c439a49896094b5a59ed0
def writeToJSONFile(path, fileName, data):
    filePathNameWExt = path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

# Function to open json file from the DB dump
def readJSONFile(path):
    with open(path) as f:
        data = json.load(f)
        return data

# Define paths
root_input_data_acquisition = '/Users/alfoi/Desktop/json_db/db_acquisition.json'
root_input_data_demographic = '/Users/alfoi/Desktop/json_db/db_demographic.json'
root_input_data_image = '/Users/alfoi/Desktop/json_db/db_image.json'
root_input_data_labeledimage = '/Users/alfoi/Desktop/json_db/db_labeledimage.json'


root_save_data = '/Users/alfoi/Desktop/generated_jsons'

fileNameDataset = 'dataset_description'
fileNameDemographics = 'dataset_demographics'


# Read the json file for acquisition table
buffer_data_acquisition = readJSONFile(root_input_data_acquisition)
print len(buffer_data_acquisition)

# Loop on data to generate json for acquisition table
for count in range(0, len(buffer_data_acquisition)):
    json_data = {}
    json_data['Date_of_scan'] = buffer_data_acquisition[count]['fields']['date_of_scan']
    json_data['InstitutionName'] = buffer_data_acquisition[count]['fields']['center']
    json_data['Manufacturer'] = buffer_data_acquisition[count]['fields']['scanner']
    json_data['Study'] = buffer_data_acquisition[count]['fields']['study']
    json_data['Session'] = buffer_data_acquisition[count]['fields']['session']
    data_folder = buffer_data_acquisition[count]['fields']['center'] + '_' + \
        buffer_data_acquisition[count]['fields']['study'] + \
        '_' + buffer_data_acquisition[count]['fields']['session']
    path = root_save_data + '/' + data_folder
    os.mkdir(path) #this is used for local test purposes
    writeToJSONFile(path, fileNameDataset, json_data)

# Read the json file for demographics table
buffer_data_demographics = readJSONFile(root_input_data_demographic)
print len(buffer_data_demographics)

# Loop on data to generate json for demographics table
for count in range(0, len(buffer_data_demographics)):
    #Find demographics associated with acquisition
    for count_acq in range(0, len(buffer_data_acquisition)):
        if buffer_data_demographics[count]['fields']['acquisition'] == buffer_data_acquisition[count_acq]['pk']: 
            json_data = {}
            json_data['Surname'] = buffer_data_demographics[count]['fields']['surname']
            json_data['Family_name'] = buffer_data_demographics[count]['fields']['family_name']
            json_data['Gender'] = buffer_data_demographics[count]['fields']['gender']
            json_data['Date_of_birth'] = buffer_data_demographics[count]['fields']['date_of_birth']
            json_data['Pathology'] = buffer_data_demographics[count]['fields']['pathology']
            json_data['Researcher'] = buffer_data_demographics[count]['fields']['researcher']
            data_folder = buffer_data_acquisition[count_acq]['fields']['center'] + '_' + \
                buffer_data_acquisition[count_acq]['fields']['study'] + '_' + \
                buffer_data_acquisition[count_acq]['fields']['session']
            path = root_save_data + '/' + data_folder
            writeToJSONFile(path, fileNameDemographics, json_data)

# Read the json file for image table
buffer_data_image = readJSONFile(root_input_data_image)
print len(buffer_data_image)


jj = 0
# Loop on data to generate json for image table 
# The current version does not address sup/inf
for count in range(0, len(buffer_data_image)):
    #Find image associated with acquisition
    for count_acq in range(0, len(buffer_data_acquisition)):
        if buffer_data_image[count]['fields']['acquisition'] == buffer_data_acquisition[count_acq]['pk']:
            json_data = {}
            buffer_contrast = buffer_data_image[count]['fields']['contrast']
            if buffer_contrast == 't1':
                buffer_contrast = 'T1w'

            elif buffer_contrast == 't2':
                buffer_contrast = 'T2w'

            elif buffer_contrast == 't2s':
                buffer_contrast = 'T2star'

            elif buffer_contrast == 'dmri':
                buffer_contrast = 'dwi'

            elif buffer_contrast == 'mt':
                buffer_contrast = 'MTw'

            json_data['Contrast'] = buffer_contrast
            json_data['Start_coverage'] = buffer_data_image[count]['fields']['start_coverage']
            json_data['End_coverage'] = buffer_data_image[count]['fields']['end_coverage']
            json_data['Orientation'] = buffer_data_image[count]['fields']['orientation']
            json_data['Is_isotropic'] = buffer_data_image[count]['fields']['is_isotropic']
            json_data['Sagittal'] = buffer_data_image[count]['fields']['sagittal']
            json_data['Corronal'] = buffer_data_image[count]['fields']['corrinal']
            json_data['Axial'] = buffer_data_image[count]['fields']['axial']
            json_data['Pam50'] = buffer_data_image[count]['fields']['pam50']
            json_data['Ms_mapping'] = buffer_data_image[count]['fields']['ms_mapping']
            json_data['Gm_model'] = buffer_data_image[count]['fields']['gm_model']
            data_folder = buffer_data_acquisition[count_acq]['fields']['center'] + '_' + \
                buffer_data_acquisition[count_acq]['fields']['study'] + \
                '_' + \
                buffer_data_acquisition[count_acq]['fields']['session']
            fileNameImage = data_folder + '_' + buffer_contrast
            path = root_save_data + '/' + data_folder
            writeToJSONFile(path, fileNameImage, json_data)

