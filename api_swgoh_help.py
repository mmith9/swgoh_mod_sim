"""
Created on Tue Sep  4  2018

@author: martrepodi

Built upon code borrowed from platzman and shittybill
"""

import requests
from json import loads, dumps
import time

class api_swgoh_help():
    def __init__(self, settings):
        '''
        :param settings: Currently expects settings class object (defined below) or python dictionary
        username and password are required parameters within the settings
        '''
        # Set defaults
        self.charStatsApi = 'https://crinolo-swgoh.glitch.me/testCalc/api'
        self.statsLocalPort = "8081"
        self.client_id = '123'
        self.client_secret = 'abc'
        self.token = {}
        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.endpoints = {'guilds': '/swgoh/guilds',
                          'guild': '/swgoh/guilds', # alias to support typos in client code
                          'players': '/swgoh/players',
                          'player': '/swgoh/players', # alias to support typos in client code
                          'roster': '/swgoh/roster',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}
        self.verbose = False
        self.debug = False
        if type(settings) is dict:
            if 'username' in settings:
                self.username = settings['username']
            if 'password' in settings:
                self.password = settings['password']
            if 'client_id' in settings:
                self.client_id = settings['client_id']
            if 'client_secret' in settings:
                self.client_secret = settings['client_secret']
            if 'charStatsApi' in settings:
                self.charStatsApi = settings['charStatsApi']
            if 'statsLocalPort' in settings:
                self.statsLocalPort = settings['statsLocalPort']
            if 'statsUrlBase' in settings:
                self.statsUrlBase = settings['statsUrlBase']
            if 'verbose' in settings:
                self.verbose = settings['verbose'] # currently not implemented
            if 'debug' in settings:
                self.debug = settings['debug'] # currently not implemented
            if 'statsLocalPort' in settings:
                self.statsLocalPort = settings['statsLocalPort']
            if 'statsUrlBase' in settings:
                self.statsUrlBase = settings['statsUrlBase']
            else:
                self.statsUrlBase = "http://127.0.0.1:{}/api".format(self.statsLocalPort)
            if 'charStatsApi' in settings:
                self.charStatsApi = settings['charStatsApi']
        else:
            self.username = settings.username
            self.password = settings.password
            self.client_id = settings.client_id
            self.client_secret = settings.client_secret
            self.charStatsApi = settings.charStatsApi
            self.statsLocalPort = settings.statsLocalPort
            self.statsUrlBase = settings.statsUrlBase
            self.verbose = settings.verbose  # currently not implemented
            self.debug = settings.debug # currently not implemented
            self.user = "username=" + settings.username
            self.user += "&password=" + settings.password
            self.user += "&grant_type=password"
            self.user += "&client_id=" + settings.client_id
            self.user += "&client_secret=" + settings.client_secret
            if settings.statsLocalPort:
                self.statsLocalPort = settings.statsLocalPort
            if settings.statsUrlBase:
                self.statsUrlBase = settings.statsUrlBase
            else:
                self.statsUrlBase = "http://127.0.0.1:{}/api".format(self.statsLocalPort)
            if settings.charStatsApi:
                self.charStatsApi = settings.charStatsApi
        # Construct API login URL
        self.user = "username=" + self.username
        self.user += "&password=" + self.password
        self.user += "&grant_type=password"
        self.user += "&client_id=" + self.client_id
        self.user += "&client_secret=" + self.client_secret

    def _getAccessToken(self):
        if 'expires' in self.token.keys():
            token_expire_time = self.token['expires']
            if token_expire_time > time.time():
                return(self.token)
        signin_url = self.urlBase+self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded"}
        r = requests.request('POST',signin_url, headers=head, data=payload, timeout = 10)
        if r.status_code != 200:
            error = 'Login failed!'
            return  {"status_code" : r.status_code,
                     "message": error}
        response = loads(r.content.decode('utf-8'))
        self.token = { 'Authorization': "Bearer " + response['access_token'],
                       'expires': time.time() + response['expires_in'] - 30}
        return(self.token)

    def getVersion(self):
        data_url = self.urlBase + '/version'
        try:
            r = requests.get(data_url)
            if r.status_code != 200:
                data = {"status_code": r.status_code,
                        "message": "Unable to fetch version"}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch version', "exception": str(e)}
        return data

    def fetchAPI(self, url, payload):
        self._getAccessToken()
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        try:
            r = requests.request('POST', data_url, headers=head, data=dumps(payload))
            if r.status_code != 200:
                # error = 'Cannot fetch data - error code'
                error = r.content.decode('utf-8')
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch data', "exception": str(e)}
        return data

    def fetchZetas(self):
        try:
            return self.fetchAPI(self.endpoints['zetas'], {})
        except Exception as e:
            return str(e)

    def fetchSquads(self):
        try:
            return self.fetchAPI(self.endpoints['squads'], {})
        except Exception as e:
            return str(e)

    def fetchBattles(self, payload=None):
        if payload is None:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        try:
            return self.fetchAPI(self.endpoints['battles'], payload)
        except Exception as e:
            return str(e)

    def fetchEvents(self, payload=None):
        if payload is None:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        try:
            return self.fetchAPI(self.endpoints['events'], payload)
        except Exception as e:
            return str(e)

    def fetchData(self, payload):
        if type(payload) != dict:
            return({'message': "Payload ERROR: dict expected."})
        if 'collection' not in payload.keys():
            return({'message': "Payload ERROR: No collection element in provided dictionary."})
        try:
            return self.fetchAPI(self.endpoints['data'], payload)
        except Exception as e:
            return str(e)

    def fetchPlayers(self, payload, project=""):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            if project:
                p['project']=project                                    
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
        except Exception as e:
            return str(e)

    def fetchGuilds(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    def fetchUnits(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['language'] = "eng_us"
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['units'], payload)
        except Exception as e:
            return str(e)

    def fetchRoster(self, payload):
        if type(payload) == list:
            p = {}
            p['allycodes'] = payload
            p['enums'] = True
            payload = p
        elif type(payload) == int:
            p = {}
            p['allycodes'] = [payload]
            p['enums'] = True
            payload = p
        elif type(payload) != dict:
            return({'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"})
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
        except Exception as e:
            return str(e)

    def fetchStats(self, allycode):
        '''Get style stat request via Crinolo API'''
        if not allycode:
            raise ValueError('No allycode provided')
        #apiUrl = self.charStatsApi + '/player/' + str(allycode) + '?flags=gameStyle'
        apiUrl = 'https://swgoh-stat-calc.glitch.me/api' + '/player/' + str(allycode) + '?flags=gameStyle,calcGP'
        
        head = {'Content-Type': 'application/json'}
        r = requests.request('GET', apiUrl, headers=head)
        if r.status_code != 200:
            error = 'Cannot fetch data - error code'
            data = {"status_code": r.status_code,
                    "message": error}
        else:
            data = loads(r.content.decode('utf-8'))
        return (data)

    def fetchStatsLocal(self, rosters):
        '''Calculate player stats via a locally run instance of the Crinolo stats calculator'''
        if type(rosters) != list:
            return({'message': "Input ERROR: dictionary expected."})
        apiUrl = self.statsUrlBase
        head = {'Content-Type': 'application/json'}
        r = requests.request('POST', apiUrl, headers=head, data=rosters)
        if r.status_code != 200:
            error = 'Cannot fetch data - error code'
            data = {"status_code": r.status_code,
                    "message": error}
        else:
            data = loads(r.content.decode('utf-8'))
        return (data)

    def fetchStats2(self, rosters):
        '''Calculate player stats via a locally run instance of the Crinolo stats calculator'''
        if type(rosters) != list:
            return({'message': "Input ERROR: dictionary expected."})
        apiUrl = "https://swgoh-stat-calc.glitch.me/api?flags=gameStyle,calcGP"
        head = {'Content-Type': 'application/json'}
        r = requests.request('POST', apiUrl, headers=head, data=rosters)
        if r.status_code != 200:
            error = 'Cannot fetch data - error code'
            data = {"status_code": r.status_code,
                    "message": error}
        else:
            data = loads(r.content.decode('utf-8'))
        return (data)

class settings():
    def __init__(self, _username, _password, **kwargs):
        self.username = _username
        self.password = _password
        self.client_id = kwargs.get('client_id', '123')
        self.client_secret = kwargs.get('client_secret', 'abc')
        self.charStatsApi = kwargs.get('charStatsApi', '')
        self.statsLocalPort = kwargs.get('statsLocalPort', "8081")
        self.statsUrlBase = kwargs.get('statsUrlBase', "http://127.0.0.1:{}".format(self.statsLocalPort))
        self.verbose = kwargs.get('verbose', False) # currently not implemented
        self.debug = kwargs.get('debug', False) # currently not implemented
        self.dump = kwargs.get('dump', False) # currently not implemented
