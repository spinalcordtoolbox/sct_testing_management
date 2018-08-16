#==========================================================================
#
#  API Python client for the Web Database management (Tristano)
#
#  Full exmple of how to insert all data
#
#  author: Francisco Perdigon Romero
#  github id: fperdigon
#  Neuropoly
#
#==========================================================================

import API_Python_client as APC

# First you need to import all the information,
# from now the code will assume that the data
# was imported as lits. Also is assumed that each
# acquisitions contains only one image and one
# label per image

acquisition_list = []
images_path_list = []
labels_path_list = []

# Fill you credetials
user = 'REPLACEME'
password = 'REPLACEME'
hostname = 'tristano.neuro.polymtl.ca'
port = '80'

APC.authentication_credentials(user_in=user,
                               password_in=password,
                               hostname_in=hostname,
                               port_in=port)

for i in range(len(acquisition_list)):

    #  Lets create a new object each time to avoid insert
    #  data of previus iterations in the loop

    #  Fill the info. If you do not have info of one field
    #  then comment. The mandatory field will be specified
    #  Replace the 'REPLACEME' for your list with the corresponding
    #  info

    # Fill and save the acquisition
    acquisition = APC.acquisition()

    acquisition.date_of_scan = 'REPLACEME'
    acquisition.center = 'REPLACEME'     #MANDATORY
    acquisition.scanner = 'REPLACEME'    #MANDATORY
    acquisition.study = 'REPLACEME'      #MANDATORY
    acquisition.session = 'REPLACEME'    #MANDATORY

    acquisition.save_to_DB()

    # Fill and save the demographic data
    demographic = APC.demographic()

    demographic.surname = 'REPLACEME'
    demographic.family_name = 'REPLACEME'
    demographic.gender = 'REPLACEME'
    demographic.date_of_birth = 'REPLACEME'
    demographic.pathology = 'REPLACEME'
    demographic.acquisition = acquisition.response['id']

    demographic.save_to_DB()

    # Fill and save the image info
    image = APC.image()

    image.filename = images_path_list[i] #MANDATORY
    image.filestate = 'REPLACEME'
    image.contrast = 'REPLACEME'         #MANDATORY
    image.start_coverage = 'REPLACEME'
    image.end_coverage = 'REPLACEME'
    image.orientation = 'REPLACEME'
    image.is_isotropic = 'REPLACEME'
    image.sagittal = 'REPLACEME'
    image.coronal = 'REPLACEME'
    image.axial = 'REPLACEME'
    image.pam50 = 'REPLACEME'
    image.ms_mapping = 'REPLACEME'
    image.gm_model = 'REPLACEME'
    image.acquisition = acquisition.response['id']

    image.save_to_DB()

    # Fill and save the label info
    label = APC.labeled_image()

    label.filename = labels_path_list(i)  #MANDATORY
    label.filestate = 'REPLACEME'
    label.label = 'REPLACEME'             #MANDATORY
    label.author = 'REPLACEME'
    label.contrast = image.response['id'] #MANDATORY

    label.save_to_DB()


