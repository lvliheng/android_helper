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
  parser.add_argument("-f", "--format", help = "format")

  args = parser.parse_args()
  
  global id
  if args.id != None:
    id = args.id
  else:
    id = ""
  global format
  if args.format != None:
    format = args.format
  else:
    format = ""
  
  start()

def start():
  global request_config_file
  request_config_file = "request_config"
  check_config_file(request_config_file)
  global token_file
  token_file = "token"
  check_config_file(token_file)
  
  global request_config
  request_config = ""

  init_config()
  time.sleep(.1)
  
  global token
  token = get_token()
  if token == "":
    login()
  else:
    global id
    if id.startswith("im_"):
      get_imuser_info(id)
    elif id.startswith("1") and len(id) == 11:
      get_mobileuser_info(id)
    else:
      get_user_info(id)

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

def get_user_info(id):
  global request_config
  user = parse_json(request_config, "user")
  url = parse_dict(user, "url")
  global token
  
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}  
  body = {"userId": id}
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  
  if status_code == 200:
    data = response.json()
    code = data["code"]
    message = data["message"]
    if code == 200:
      try:
        user_info = data["data"]
        global format
        if format == "-1":
          json_result = json.dumps(user_info, ensure_ascii = False)
          print(json_result)
        else:
          real_name = user_info['realName'] or "未实名"
          name = user_info['nickName']
          mobile = user_info['mobile']
          user_id = user_info['userId']
          im_id = user_info['imId']
          create = user_info['gmtCreate']
          print(f"{get_short_string(name, 4)}\t{real_name}\t{mobile}\t{user_id}\t{im_id}\t{create}")
      except Exception as e:
        Utils.print_with_datetime(f"[get_user_info: {e}]")
    elif code == 301:
      login()
    else:
      Utils.print_with_datetime(f"[get_user_info: {message}]", )

def get_string_full_length(value_int, max_length):
  return "{:<{}}".format(value_int, max_length)

def get_short_string(s, max_length):
  if len(s) <= 2 * max_length - 1:
        return get_string_full_length(s, 2 * max_length)
  elif len(s) <= 2 * max_length:
        return s
  
  return s[:max_length] + "..." + s[-max_length:]

def get_imuser_info(id):
  global request_config
  user = parse_json(request_config, "imuser")
  url = parse_dict(user, "url")
  global token
  
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  body = [id]
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  
  if status_code == 200:
    data = response.json()
    code = data["code"]
    message = data["message"]
    if code == 200:
      try:
        imuser_info = data["data"]
        user_id = imuser_info[0]["userId"]
        get_user_info(user_id)
      except:
        Utils.print_with_datetime("[get_imuser_info: data error]")
    elif code == 301:
      login()
    else:
      Utils.print_with_datetime(f"[get_imuser_info: {message}]")

def get_mobileuser_info(id):
  global request_config
  user = parse_json(request_config, "mobileuser")
  url = parse_dict(user, "url")
  global token
  
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  params = {"mobile": id}
  response = requests.get(url = url, headers = headers, params = params)
  status_code = response.status_code
  
  if status_code == 200:
    data = response.json()
    code = data["code"]
    message = data["message"]
    if code == 200:
      try:
        mobileuser_info = data["data"]   
        user_id = mobileuser_info["userId"]
        get_user_info(user_id)
      except:
        Utils.print_with_datetime("[get_mobileuser_info: data error]")
    elif code == 301:
      login()
    else:
      Utils.print_with_datetime(f"[get_mobileuser_info: {message}]")

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
          global id
          get_user_info(id)
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