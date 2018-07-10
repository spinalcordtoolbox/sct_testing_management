import configparser
import getpass
import os

from typing import Type, Generic, List, Dict, Set

DEFAULT_HOSTNAME = "tristano.neuro.polymtl.ca"
DEFAULT_PORT = "80"
DEFAULT_CONFIGFILE = ".sctdbtool"


def setup(arguments: Dict):
    """This method will ask user input to configure the system
    with the hostname, username, etc, for the web management
    access.

    :param arguments: the CLI arguments.
    """
    print("Please enter the configuration below.")
    print("Press ENTER to accept default values (between brackets).\n")
    hostname = input("Hostname of the Web Management [{}]: ".format(DEFAULT_HOSTNAME))
    hostname = hostname or DEFAULT_HOSTNAME

    port = input("Port of the Web Management [{}]: ".format(DEFAULT_PORT))
    port = port or DEFAULT_PORT

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    config = configparser.ConfigParser()
    config['Global'] = {
        'hostname': hostname,
        'port': int(port),
        'username': username,
        'password': password,
    }

    userdir = os.path.expanduser("~")
    config_path = os.path.join(userdir, DEFAULT_CONFIGFILE)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    print("Configuration saved successfully !")


def read_setup():
    """Read the system configuration file.

    :return: a dict with the configuration parameters.
    """
    userdir = os.path.expanduser("~")
    config_path = os.path.join(userdir, DEFAULT_CONFIGFILE)

    if not os.path.exists(config_path):
        raise RuntimeError("Please run 'sct_dbtool setup' before.")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config['Global']
