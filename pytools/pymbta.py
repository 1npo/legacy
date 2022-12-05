#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# PyMBTA -- An example implementation of the MBTA API.
#

import cmd
import urllib
import json
from prettytable import PrettyTable
from geopy.geocoders import Nominatim


class PyMBTA(cmd.Cmd):
    """Main class. Starts a command-line prompt for the user to submit
    commands."""
    
    intro = 'PyMBTA -- An example implementation of the MBTA API.\n' + \
            'Type help or ? to list commands.\n'
    prompt = 'pymbta >> '
    addrstr = 0

    # kinda hacky, but there's really no need for configparser here
    f = open('./mbta.key', 'r')
    apikey = f.read()
    
    #
    # begin helper functions
    #
    def geolocate(self, loc):
        """Convert the user's street address to latitude and longitude
        coordinates, and return them."""
        
        geolocator = Nominatim()
        location = geolocator.geocode(loc)
        lat = float("{0:.6f}".format(location.latitude))
        lon = float("{0:.6f}".format(location.longitude))
        return lat, lon

    def build_url(self, req, args):
        return 'http://realtime.mbta.com/developer/api/v2/' + \
            req + '?api_key=' + self.apikey + args + '&format=json'

    def get_json(self, apistr, params):
        url = self.build_url(apistr, params)
        u = urllib.urlopen(url)
        data = u.read()
        parsed = json.loads(data)
        return parsed

    
    #
    # begin Cmd functions
    #
    def do_EOF(self, line):
        return True
    
    def do_setloc(self, addr):
        """setloc <location>
        Set your location as the street address <location>"""
        
        if addr:
            self.addrstr = addr
            print '[+] your location has been set.'
        else:
            print '[-] error: no address provided.'
    
    def do_nearby(self, arg):
        """nearby
        Display all stops near your location."""

        print '[+] displaying all stops near your location...'
        
        lat, lon = self.geolocate(self.addrstr)
        params = '&lat={:f}&lon={:f}'.format(lat, lon)
        data = self.get_json('stopsbylocation', params)
        
        print ''
        t = PrettyTable(['Stop ID', 'Stop Name'])
        for item in data['stop']:
            t.add_row([item['stop_id'], item['stop_name']])

        print t
        
    def do_routesfor(self, stop):
        """routesfor <stopid>
        Display all the routes that service the stop [stopid]"""

        print '[+] displaying the routes serving stop {}'.format(arg)

        params = '&stop={}'.format(stop)
        data = self.get_json('routesbystop', params)
        
        print ''
        t = PrettyTable(['Type of Route', 'Route Name'])
        for item in data['mode']:
            for item2 in item['route']:
                t.add_row([item['mode_name'], item2['route_name']])

        print t

    def do_schedule(self, stop, num=5):
        """schedule <stopid> [num=5]
        Display the schedule for stop <stopid>. The default is 5 entries."""

        print '[+] displaying the schedule for stop {}'.format(stop)
 
        params = '&stop={}&max_trips={}'.format(stop, num)
        data = self.get_json('schedulebystop', params)

        print ''
        t = PrettyTable(['Route Name', 'Direction', 'Trip Times'])
        for item in data['mode']:
            for item2 in item['route']:
                for item3 in item2['direction']:
                    for item4 in item3['trip']:
                        t.add_row([item2['route_name'], item3['direction_name'],
                                   item4['trip_name']])

        print t
        
if __name__ == "__main__":
    """Start up the commandline interface."""
    PyMBTA().cmdloop()
