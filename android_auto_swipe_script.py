#! /usr/bin/python
# 自动滑动脚本. 可用于快手刷金币
# author: sukanka
# updated: 2020-02-17 18:42
import os
import random
import time
# ACTIVITIES=['com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity',"com.jm.video/.ui.main.MainActivity", "com.kuaiyin.player/.MainActivity"]
ACTIVITIES=["com.szbb.life.main.MainActivity"]
# 快手, 刷宝, 快音

def findFrontActivity(device):
    activityList=os.popen("adb -s {} shell \"dumpsys activity | grep -i run\"".format(device)).readlines() # 获取所有正在运行任务
    activity=""
    for string in activityList:
        if "Run #" in string: # 找到最前台的活动
            activity=string
            break
    activity=activity.strip().split(" ") # 删除首尾空格后按中间的空格分割
# ['Run', '#0:', 'ActivityRecord{ab835a9', 'u0', 'com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity', 't8874}']
    if activity !="":
        try:
            activity=activity[4]
            return activity
        except IndexError:
            print(activity)
            return ""
# com.kuaishou.nebula/com.yxcorp.gifshow.HomeActivity

def autoSwipe(ACTIVITIES):
    connected=os.popen("adb devices").readlines()
    devices=[connected[i][0:-8] for i in range(1,len(connected)-1)] # 获取所有设备代号
    x=random.randint(200,800)
    y=random.randint(350,550)
    dx=random.randint(0,50)
    dy=random.randint(900,1200)
    tap_time=random.randint(300,600) # 随机选择滑动参数
    for device in devices:
        if findFrontActivity(device) in ACTIVITIES: # 如果前台运行特定应用就自动滑动
            slide="adb -s {} shell input swipe {} {} {} {} {}".format(device,x+dx,y+dy,x,y,tap_time)
            os.system(slide)
        else:
            continue    
    time.sleep(2+3*random.random()) # 滑动后随机等待2-5秒

if __name__=="__main__":
    while True:
        if os.system("adb devices")==0: # 如果有设备连接．
            autoSwipe(ACTIVITIES)