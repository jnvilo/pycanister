import abc
import requests
import json
from pprint import pprint

from pprint import pformat
class AttributeExists(Exception):
    pass
    
class PyCanister(object):
    """
    A class to contain data. The data can be loaded and saved
    from json. 
    
    """
    def __init__(self):
        self.__pycanister_attributes__ = []
        self.namespace_type = dict

    def keys(self):
        return self.__pycanister_attributes__

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        
        if type(data) == dict:
            return cls.from_dict(data)
        elif type(data) == list:
            return cls.from_list(data)
            
    @classmethod
    def from_list(cls, data):
        l = []
        for item in data:
            if type(item) == list:
                pns = PyCanister.from_list(item)
            elif type(item) == dict:
                pns = PyCanister.from_dict(item)
            else:
                pns = item
            l.append(pns)
        return l

    @classmethod
    def from_dict(cls,data):
        pns = PyCanister()
        for key,value in data.items():
            if hasattr(cls, key):
                msg = f"{key} is an internal attribute. Can not add this attribute"
                raise AttributeExists(msg)
            pns.__pycanister_attributes__.append(key)
            if type(value) in [int, str,bool] or (value == None):
                setattr(pns, key,value)
            elif type(value) == dict:
                setattr(pns, key, PyCanister.from_dict(value))
            elif type(value) == list:
                setattr(pns, key, PyCanister.from_list(value))
        return pns

    def handle_serialize_list(self, l):
        result = []
        for item in l:
            if type(item) == PyCanister:
                result.append(item.serialize())
            elif type(item) == list:
                result.append(self.handle_serialize_list(item))
            elif type(item) in (str, bool, float):
                result.append(item)
            else:
                raise RuntimeError("Unhandled type Exception")
        return result

    def serialize(self):
        """
        When we serialize ,we need to process
        1. atomic types
        2. list types - may contain a mix of PyCanister or list
        3. PyCanister type

        :return:
        """
        d = {}

        for key in self.__pycanister_attributes__:
            value = getattr(self, key)

            if type(value) == PyCanister:
                #Handle converting pycanister contents to a dict
                result = value.serialize()
            elif type(value) == list:
                #Iterate through the list and return a serialized content.
                #the content of a list could also be a list.
                result = self.handle_serialize_list(value)
            elif type(value) in (str, bool, float,int):
                #everything else is just standard content.
                result = value
            else:
                raise RuntimeError("Unhandled Type Exception")

            d.update({key:result})

        return d


    def wrapped_to_dict(self):
        d = {}
        for attribute in self.__pycanister_attributes__:
            value = getattr(self, attribute)
            if type(value) in [int, str,bool] or value == None:
                d.update({attribute:value})
            elif type(value) == PyCanister:
                d.update({attribute:value.to_dict()})
            elif type(value) == list:
                l = []
                for item in value:
                    if type(value) in [PyCanister,list]:
                        d.update({attribute:value.to_dict()})
                    else:
                        d.update({attribute:value})

        return d

    def to_dict(self):
        try:
            return self.wrapped_to_dict()
        except AttributeError as e:
            print(e)


    def to_json(self):
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return pformat(self.serialize())
                    
    def __repr__(self):
        return self.__str__()
    
if __name__ == "__main__":

    d =  {
        "name": "plugins.gradle.com",
        "format": "maven2",
        "type": "proxy",
        "url": "http://nexus.optiscangroup.com/nexus/repository/plugins.gradle.com",
        "attributes": {
          "proxy": {
            "remoteUrl": "https://plugins.gradle.org/m2/"
          }
        }
      }

    p = PyCanister.from_dict(d)
    
    
