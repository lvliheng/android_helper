import time
from pathlib import Path
import argparse
import json
import requests
import base64

from utils import Utils

def init():  
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--id", help = "user id")

  args = parser.parse_args()
  
  global id
  if args.id != None:
    id = args.id
  else:
    id = ""
  
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
  time.sleep(2)
  
  global token
  token = get_token()
  if token == "":
    login()
  else:
    get_user_info()

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

def get_user_info():
  global request_config
  user = parse_json(request_config, "user")
  url = parse_dict(user, "url")
  global token
  
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  global id
  body = {"userId": id}
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  if status_code == 200:
    data = response.json()
    code = data["code"]
    print("code:", code)
    message = data["message"]
    print("message:", message)
    if code == 200:
      try:
        user_info = data["data"]
        print(user_info)
      except:
        Utils.print_with_datetime("[get_user_info: data error]")
    else:
      Utils.print_with_datetime("[get_user_info: request error]")

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
          get_user_info()
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