import abc
import requests
import json

from pprint import pprint
from pprint import pformat

maven_repo_template = {
    "name": "SpringPlugins",
    "url": "http://localhost:8081/repository/SpringPlugins",
    "online": True,
    "storage": {
      "blobStoreName": "default",
      "strictContentTypeValidation": True,
      "writePolicy": "ALLOW"
    },
    "cleanup": None,
    "proxy": {
      "remoteUrl": "http://repo.spring.io/plugins-release/",
      "contentMaxAge": -1,
      "metadataMaxAge": 1440
    },
    "negativeCache": {
      "enabled": True,
      "timeToLive": 1440
    },
    "httpClient": {
      "blocked": False,
      "autoBlock": True,
      "connection": None,
      "authentication": None
    },
    "routingRuleName": None,
    "maven": {
      "versionPolicy": "RELEASE",
      "layoutPolicy": "STRICT"
    },
    "format": "maven2",
    "type": "proxy"
  }   


class PyCanister(object):
    """
    A class to contain data. The data can be loaded and saved
    from json. 
    """
    
    def __init__(self):
        
        self.attributes = []
        self.namespace_type = dict 
   
    @classmethod
    def from_dict(cls,data):
    
        pns = PyNameSpace()
        if type(data) == dict:
            for key,value in data.items():
                print(f"attribute: {key}, value: {type(value)}")
                pns.attributes.append(key)
                
                
                if type(value) in [int, str,bool] or value == None:
                    setattr(pns, key,value)
                elif type(value) == dict:
                    setattr(pns, key, PyNameSpace.from_dict(value)) 
        return pns
    
    def to_dict(self):
        
        d = {}
        for attribute in self.attributes:
            value = getattr(self, attribute)
            if type(value) in [int, str,bool] or value == None:
                d.update({attribute:value})
            elif type(value) == PyNameSpace:
                d.update({attribute:value.to_dict()})


        return d
    
    def to_json(self):
        
        return json.dumps(self.to_dict())
    
    def __str__(self):
        return pformat(self.to_dict())
                    
    def __repr__(self):
       
        return self.__str__()
    
    
if __name__ == "__main__":
    
    pns = PyNameSpace.from_dict(maven_repo_template) 
    print(pns.attributes)
    print(pns.name)
    print(pns.online)
    pprint(pns)
    pns.maven.layoutPolicy = "THIS IS NOT EST"
    pprint(pns)
    


