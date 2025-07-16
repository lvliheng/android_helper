import time
from pathlib import Path
import argparse
import json
import requests
import base64

from utils import Utils

def init():  
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--pagef", help = "page from")
  parser.add_argument("-t", "--paget", help = "page to")
  parser.add_argument("-n", "--name", help = "nickname")

  args = parser.parse_args()
  
  global page_from
  if args.pagef != None:
    page_from = args.pagef
  else:
    page_from = ""
    
  global page_to
  if args.paget != None:
    page_to = args.paget
  else:
    page_to = ""
    
  global nick_name
  if args.name != None:
    nick_name = args.name
  else:
    nick_name = ""
  if nick_name == "-1":
    nick_name = ""
    
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
  
  global page_num
  global page_from
  page_num = string_to_int(page_from)
  if page_num < 1:
    page_num = 1
    
  global page_max
  global page_to
  page_max = string_to_int(page_to)
  if page_max < 0:
    page_max = 10
  
  global page_size
  page_size = 10
  global list
  list = []
  
  global start
  start = ""
  global end
  end = ""
  
  global token
  token = get_token()
  if token == "":
    login()
  else:
    get_user_list()

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

def get_user_list():
  global request_config
  user = parse_json(request_config, "userlist")
  url = parse_dict(user, "url")
  global token
  
  headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer {}".format(token)}
  global page_num
  global page_size
  global nick_name
  body = {"pageNum": page_num, "pageSize": page_size, "nickName": nick_name}
  response = requests.post(url = url, headers = headers, json = body)
  status_code = response.status_code
  
  if status_code == 200:
    data = response.json()
    code = data["code"]
    message = data["message"]
    if code == 200:
      try:
        user_list = data["data"]
        
        if nick_name == "":
          global page_max
          print(f"{page_num}/{page_max}")
          
          global start
          global end
          for user in user_list:
            if end == "":
              end = user["gmtCreate"]
            start = user["gmtCreate"]
            
            if user["state"] != 1:
              continue
            
            if user["nickName"].endswith(" "):
              print("    ", f"{user['nickName']}_", " :: ", user["deviceId"], " :: ", user["parentMobile"])
              list.append(user["id"])
            elif user["deviceId"] == '3b36ce2650173adeebc6565d9a139c5b':
              print("    ", f"{user['nickName']}", " :: ", user["deviceId"], " :: ", user["parentMobile"])
              list.append(user["id"])
            elif user["parentMobile"] == None:
              print("    ", f"{user['nickName']}", " :: ", user["deviceId"], " :: ", user["parentMobile"])
              list.append(user["id"])
              
          if page_num < page_max:
            time.sleep(1)
            page_num += 1
            get_user_list()
          else:
            if len(list) > 0:
              print(f"------------{start}~{end}------------")
              for id in list:
                time.sleep(1)
                get_user_info(id)
            else:
              print(f"------------{start}~{end}------------")
            print(len(list), "results found.")
        else:
          index = 0
          for user in user_list:
            index += 1
            json_result = json.dumps(user, ensure_ascii = False)
            print(index, json_result)
          print(len(user_list), "results found.")
      except Exception as e:
        Utils.print_with_datetime(f"[get_user_list: error: {e}]")
    elif code == 301:
      login()
    else:
      Utils.print_with_datetime(f"[get_user_list: fail: {message}]", )

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
        real_name = user_info['realName'] or "未实名"
        print(f"{user_info['nickName']}  {real_name}  {user_info['mobile']}  {user_info['userId']}  {user_info['imId']}  {user_info['gmtCreate']}")
      except Exception as e:
        Utils.print_with_datetime(f"[get_user_info: error: {e}]")
    elif code == 301:
      login()
    else:
      Utils.print_with_datetime(f"[get_user_info: fail: {message}]", )

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
          get_user_list()
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

def string_to_int(value):
  try:
    result = int(value)
    return result
  except:
    return -1

if __name__=="__main__":
  try:
    init()
  except Exception as e:
    Utils.print_with_datetime("-cancel\n{}".format(e))
  except KeyboardInterrupt:
    None