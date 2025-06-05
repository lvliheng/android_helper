import time
from pathlib import Path
import argparse
import json
import requests
import base64
import clipboard

from utils import Utils

def init():  
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--path", help = "path")
  parser.add_argument("-m", "--method", required = False, help = "method")
  parser.add_argument("-d", "--data", required = False, help = "data")
  parser.add_argument("-f", "--format", required = False, help = "format")

  args = parser.parse_args()
    
  global path
  if args.path != None:
    path = args.path
  else:
    path = ""
  
  global method
  if args.method != None:
    method = args.method
  else:
    method = ""
  
  global data
  if args.data != None:
    data = args.data
  else:
    data = ""
    
  global format
  if args.format != None:
    format = args.format
  else:
    format = ""
  
  start()

def start():
  global root
  root = ""
  Path(root).mkdir(parents = True, exist_ok = True)
  global request_config_file
  request_config_file = "{}{}".format(root, "request_config")
  check_config_file(request_config_file)
  global token_file
  token_file = "{}{}".format(root, "token")
  check_config_file(token_file)
  
  global request_config
  request_config = ""

  init_config()
  time.sleep(.1)
  
  global base
  base = parse_json(request_config, "base")
  
  global token
  token = get_token()
  if token == "":
    login()
  else:      
    request(token)

def request(token):
  global base
  global path
  global method
  global data
  
  if is_empty(data):
    if is_empty(method):
      command = f"curl --location '{base}{path}' --header 'Content-Type: application/json' --header 'Authorization: Bearer {token}'"
    else:
      command = f"curl --request POST --location '{base}{path}' --header 'Content-Type: application/json' --header 'Authorization: Bearer {token}'"
  else:
    command = f"curl --location '{base}{path}' --header 'Content-Type: application/json' --header 'Authorization: Bearer {token}' --data '{data}'"
  print(command)
  
  url = f"{base}{path}"
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  
  if is_empty(data):
    if is_empty(method):
      response = requests.get(url = url, headers = headers)
    else:
      response = requests.post(url = url, headers = headers)
  else:
    json_data = json.loads(data)
    if method == "get" or method == "GET":
      response = requests.get(url = url, headers = headers, params = json_data)
    else:
      response = requests.post(url = url, headers = headers, json = json_data)
    
  status_code = response.status_code
  
  if status_code == 200:
    result = response.json()
    data = result["data"]
    global format
    if format == "-1":
      json_result = json.dumps(data, ensure_ascii = False)
    else:
      json_result = json.dumps(data, indent = 4, ensure_ascii = False)
    print(json_result)
    clipboard.copy(json_result)
  else:
    print(status_code)

def is_empty(data):
  return data == "" or data == "-1"

def check_config_file(file_path):
  if not Path(file_path).exists():
    open(file_path, "w")

def init_config():  
  global request_config_file
  request_config_data = open(request_config_file, "r")
  global request_config
  request_config = request_config_data.read()
  
def parse_json(data, key):
  try:
    if type(data) == str:
      value = json.loads(data)
      return value[key]
    else:
      return ""
  except:
    return ""
  
def parse_dict(data, key):
  try:
    if type(data) == dict:
      return data[key]
    else:
      return ""
  except:
    return ""

def login():
  global request_config
  login = parse_json(request_config, "login")
  url = parse_dict(login, "url")
  grant_type = parse_dict(login, "grantType")
  account = decode(parse_dict(login, "account"))
  password = decode(parse_dict(login, "password"))
  
  headers = {"Content-Type": "application/json; charset=utf-8"}
  body = {"grantType": grant_type, "userName": account, "password": password}
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  if status_code == 200:
    data = response.json()
    code = data["code"]
    if code == 200:
      try:
        global token
        token = data["data"]["access_token"]
        if token != "":
          set_token()
          request(token)
      except:
        Utils.print_with_datetime("[login: data error]")
    else:
      Utils.print_with_datetime("[login: request error]")
    
def set_token():
  global token_file
  file = open(token_file, "w")
  global token
  file.write(token)
  file.close()
      
def decode(encode_value):
  decode_bytes = base64.b64decode(encode_value.encode("ascii"))
  return decode_bytes.decode("ascii")

def get_token():
  global token_file
  token_data = open(token_file, "r")
  return token_data.read()

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None