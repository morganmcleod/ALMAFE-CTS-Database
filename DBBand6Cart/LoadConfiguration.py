import configparser

def loadConfiguration(iniFile, section):
    '''
    load database credentials from configuration file
    :param iniFile: filename to open
    :param section: which section of the INI file to read
    :return dict{host, database, user, passwd}
    '''
    config = configparser.ConfigParser()
    config.read(iniFile)
    host = config[section]['host']
    database = config[section]['database']
    user = config[section]['user']
    passwd = config[section]['passwd']
    return {'host' : host, 'database' : database, 'user' : user, 'passwd' : passwd}