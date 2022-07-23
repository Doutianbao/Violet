import requests
import json
import time
import new_downloader

OWNER=499106648

def get_cookie():
    text=open("./cookies.json").read()
    json_obj=json.loads(str(text))
    cookie_list=json_obj["cookie_info"]["cookies"]
    i=0
    while True:
        if cookie_list[i]["name"]=="SESSDATA":
            SESSDATA=cookie_list[i]["value"]
            break
        i+=1
    return SESSDATA

def no_space(string):
    return string.replace(" ", "")

def get_bilibili_api(url):
    r = requests.get(url,cookies={"SESSDATA": get_cookie()})#,verify=False)
    return json.loads(r.text)

def save(data):
    with open("./data.json", "w") as f:
        f.write(json.dumps(data))

def read(file_name="./data.json"):
    with open(file_name, "r") as f:
        return json.loads(f.read())

def match_url(url):
    urlStringList=url.split("$")
    return no_space(urlStringList[1])

def get_task_list():
    return_list=[]
    task_list=get_bilibili_api("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?talker_id="+str(OWNER)+"&session_type=1")["data"]["messages"]
    i=0
    while i<len(task_list):
        msg_obj=task_list[i]
        if msg_obj["sender_uid"]==OWNER and msg_obj["msg_type"]==1:#鉴权&&防止特殊消息混入
            if msg_obj["content"].find("$")!=-1:
                return_list.append(match_url(msg_obj["content"]))
        i+=1
    return return_list

#debug here
#del it when complete
#print(get_task_list())
#顺带着吐槽下咱们东北的学校，看看人厦门6中合唱团，再看看咱
#还搁着振兴东北呢，振兴你妈
#没事不怕，咱市图书馆有特点，订票的开放时间永远都在闭馆之后...这么玩我TMD有意思吗？\n关键是前端的书只有那里有.......你奶奶的
#end debug
if __name__=="__main__":
    try:
        task_history=read()
    except:
        task_history=[]#initial list task_history
    this_download=False#开始视为没请求过接口
    while True:
        task_list=get_task_list()
        n=0
        while n<len(task_list):
            task=task_list[n]
            if task not in task_history:
                task_history.append(task)
                save(task_history)
                print("new task: "+task)
                new_downloader.main(task)
                this_download=True
            n+=1
        if not this_download:
            time.sleep(2.5*60)
        else:
            this_download=False
#print(get_cookie())
#print(get_bilibili_api("https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs?talker_id=499106648&session_type=1"))