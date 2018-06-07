#==========================================================================
#
#  API Python client for the Web Database management (Tristano)
#
#  This file contains the python classes that represent the tables that
#  exists en the database system. Using this code you can insert data
#  to de database using a python interface.
#
#  author: Francisco Perdigon Romero
#  github id: fperdigon
#  Neuropoly
#
#==========================================================================

import requests
import requests.auth as auth

user = ""
password = ""
hostname = ""
port = ""

class demographic:
    def __init__(self):
        self.id = ''
        self.surname = ''
        self.family_name = ''
        self.gender = ''
        self.date_of_birth = ''
        self.pathology = ''
        self.researcher = ''
        self.acquisition = ''
        self.response = '' # used to store the json response of the server

    def save_to_DB(self):
        auth_DB = auth.HTTPBasicAuth(username=user, password= password)
        # parsing the object to a dict
        data = {'surname': self.surname,
                'family_name': self.family_name,
                'gender': self.gender,
                'date_of_birth': self.date_of_birth,
                'pathology': self.pathology,
                'researcher': self.researcher,
                'acquisition': self.acquisition} # This is the link to the acquisition table acq['id']

        resp = requests.post('http://' + hostname + ':' + port + '/annotations/v1/api/demographics/', auth=auth_DB, data=data)
        demographic = None
        if resp.status_code == 201:
            print("Data saved successfully")
            demographic = resp.json()
        else:
            print("ERROR: data can't be saved")
            print("ERROR number " + str(resp.status_code))

        self.response = demographic
        return demographic

class image:

    def __init__(self):
        self.id = ''
        self.labeled_images = []
        self.filename = ''
        self.filestate = ''
        self.contrast = ''
        self.start_coverage = ''
        self.end_coverage = ''
        self.orientation = ''
        self.is_isotropic = ''
        self.sagittal = ''
        self.coronal = ''
        self.axial = ''
        self.pam50 = ''
        self.ms_mapping = ''
        self.gm_model = ''
        self.acquisition = ''
        self.response = ''  # used to store the json response of the server

    def save_to_DB(self):
        auth_DB = auth.HTTPBasicAuth(username=user, password= password)
        # parsing the object to a dict
        data = {'filename': self.filename,
                'filestate': self.filestate,
                'contrast' : self.contrast,
                'start_coverage': self.start_coverage,
                'end_coverage': self.end_coverage,
                'orientation': self.orientation,
                'is_isotropic': self.is_isotropic,
                'sagittal' : self.sagittal,
                'corrinal' : self.coronal,
                'axial' : self.axial,
                'pam50' : self.pam50,
                'ms_mapping' : self.ms_mapping,
                'gm_model': self.gm_model,
                'acquisition' : self.acquisition} # This is the link to the image acquisition acq['id']

        resp = requests.post('http://' + hostname + ':' + port + '/annotations/v1/api/images/', auth=auth_DB, data=data)
        img = None
        if resp.status_code == 201:
            print("Data saved successfully")
            img = resp.json()
        else:
            print("ERROR: data can't be saved")
            print("ERROR number " + str(resp.status_code))

        self.response = img
        return img


class labeled_image:

    def __init__(self):
        self.id = ''
        self.filename = ''
        self.filestate = ''
        self.label = ''
        self.author = ''
        self.contrast = ''
        self.response = ''  # used to store the json response of the server

    def save_to_DB(self):
        auth_DB = auth.HTTPBasicAuth(username=user, password= password)
        # parsing the object to a dict
        data = {'filename': self.filename,
                'filestate': self.filestate,
                'label': self.label,
                'author': self.author,
                'contrast': self.contrast} # This is the link to the image table img['id']

        resp = requests.post('http://' + hostname + ':' + port + '/annotations/v1/api/labeledimages/', auth=auth_DB, data=data)
        lb_img = None
        if resp.status_code == 201:
            print("Data saved successfully")
            lb_img = resp.json()
        else:
            print("ERROR: data can't be saved")
            print("ERROR number " + str(resp.status_code))

        self.response = lb_img
        return lb_img

class acquisition:

    def __init__(self):
        self.id = ''
        self.images = []
        self.demographic = demographic()
        self.date_of_scan = ''
        self.center = ''
        self.scanner = ''
        self.study = ''
        self.session = ''
        self.response = ''  # used to store the json response of the server

    def save_to_DB(self):
        auth_DB = auth.HTTPBasicAuth(username=user, password= password)
        # parsing the object to a dict
        data = {'date_of_scan': self.date_of_scan,
                'center': self.center,
                'scanner': self.scanner,
                'study': self.study,
                'session': self.session}
        resp = requests.post('http://' + hostname + ':' + port + '/annotations/v1/api/datasets/', auth=auth_DB, data=data)
        acq = None
        if resp.status_code == 201:
            print("Data saved successfully")
            acq = resp.json()
        else:
            print("ERROR: data can't be saved")
            print("ERROR number " + str(resp.status_code))

        self.response = acq
        return acq

def authentication_credentials(user_in, password_in, hostname_in, port_in):
    global user, password, hostname, port
    user = user_in
    password = password_in
    hostname = hostname_in
    port = port_in



