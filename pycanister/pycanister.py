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
            pns = PyCanister.from_dict(item)
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
            if type(value) in [int, str,bool] or value == None:
                setattr(pns, key,value)
            elif type(value) == dict:
                setattr(pns, key, PyCanister.from_dict(value))
            
        return pns
    
    def to_dict(self):
        
        d = {}
        for attribute in self.__pycanister_attributes__:
            value = getattr(self, attribute)
            if type(value) in [int, str,bool] or value == None:
                d.update({attribute:value})
            elif type(value) == PyCanister:
                d.update({attribute:value.to_dict()})
        return d
    
    def to_json(self):
        
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return pformat(self.to_dict())
                    
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
    
    