'''
This is a module that will request zoomEye for information about each IP
address passed into it.
'''

import zoomeye
import simplejson
from common import helpers


class IntelGather:

    def __init__(self):
        self.cli_name = "zoomeye"
        self.description = "Requests zoomEye for information on provided IPs"
        self.username = ""
        self.password = ""
        if self.username != "" and self.password != "":
            self.api_token = self.zoomeye.ZoomEye(self.username, self.password).login()

    def collapse(self, var, tabs=0):
        result = ""

        if type(var) is dict:
            for field, value in var.iteritems():
                try:
                    result += "\n" + tabs * "\t" + field.encode('utf-8') + ": " + self.collapse(
                        value, tabs=(tabs + 1))
                except UnicodeDecodeError:
                    result += "\n" + tabs * "\t" + field.encode('utf-8') + ": " + self.collapse(
                        value.encode('utf-8'), tabs=(tabs + 1))

        elif type(var) is list:
            for l in var:
                result += self.collapse(l, tabs=tabs) + "\n"

        elif var is None:
            result += "No Information Available"

        elif type(var) is float or type(var) is int or type(var) is long\
                or type(var) is bool:
            result += str(var)

        else:
            result += str(var.encode('utf-8'))
        return result

    def gather(self, all_ips):
        for path, incoming_ip_obj in all_ips.iteritems():
            if incoming_ip_obj[0].zoomEye_info == "" and incoming_ip_obj[0].ip_address != "":
                if self.api_token is "":
                    print helpers.color("[*] Error: You didn't provide a zoomEye credentials!", warning=True)
                    print helpers.color("[*] Please edit zoomEye module and add in your credentials.", warning=True)

                else:
                    if incoming_ip_obj[0].zoomEye_info is '':
                        print "Querying zoomEye for information about " + incoming_ip_obj[0].ip_address
                        try:
                            json_result = self.zoomeye.dork_search('ip:%s' %incoming_ip_obj[0].ip_address, 125, 'host', [app, device, service, os, port, country, city])
                            incoming_ip_obj[0].zoomEye_info = json_result
                        except simplejson.decoder.JSONDecodeError:
                            pass
                        except:
                            incoming_ip_obj[0].zoomEye_info = "No available information within zoomEye about " + incoming_ip_obj[0].ip_address
        return
