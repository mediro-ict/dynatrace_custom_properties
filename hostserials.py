import configparser,csv
import requests
import json
from collections import OrderedDict


settings_config =  'settings.ini'
csv_file = open("DT_Entities.csv", "w")
config = configparser.ConfigParser()
config.read(settings_config)
dt_Tenant = config.get("Settings", "DT_URL")
dt_key = config.get("Settings", "DT_API_KEY")
url = dt_Tenant + "/api/v1/entity/infrastructure/hosts?includeDetails=false"
api_token = {'Api-Token': dt_key}
body = requests.get(url=url,params=api_token)


ids= []
hostSerials = []
jsn_list = json.loads(body.text)
for lis in jsn_list:
    for key,val in lis.items():
       
       if key == "entityId":
            #print(val)
            ids.append(val)
print(ids)
for j in ids:
    cust_prop_name = config.get("Settings", "CUSTOM_PROP")
    cust_prop_value = ""
    res = requests.get (url = dt_Tenant + '/api/v2/entities/' + j +'?fields=properties',params=api_token)
    serials = json.loads(res.text)
    
    entity_id = serials['entityId']
    displayName= serials['displayName']
    #print(serials)
    for k,v in serials['properties'].items():
        if 'customHostMetadata' in k:
            data = v
            for entry in data:
                if entry['key']['key'] == config.get("Settings", "CUSTOM_PROP"):
                    
                    cust_prop_value = entry['value']
                    cust_prop_name = entry['key']['key'] 
            
    row = entity_id,displayName,cust_prop_value    
    writer = csv.writer(csv_file, delimiter=',', lineterminator="\n", quoting=csv.QUOTE_NONNUMERIC) 
    writer.writerow(row)          
     