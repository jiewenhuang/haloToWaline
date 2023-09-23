import json
import os
import time


from func.halo import get_url, get_reply
from func.halo import get_comment
# 你waline导出的数据
waline_data = "/Users/jevon/Downloads/git/waline.json"

# print(response.text)
with open(waline_data, "r") as file:
    json_data = json.load(file)

items = get_comment()
for comment in items:
    metadate = comment["spec"]["subjectRef"]["name"]
    kind = comment["spec"]["subjectRef"]["kind"]
    url = get_url(metadate, kind)
    print(url)
    nick = comment["spec"]["owner"].get("displayName", "匿名")
    ip = comment["spec"].get("ipAddress", "")
    if comment["spec"]["owner"]["kind"] == "Email":
        mail = comment["spec"]["owner"]["name"]
    else:
        mail = ""
    ua = comment["spec"].get("userAgent", "")
    comment_content = comment["spec"]["content"]
    createdAt = comment["spec"]["creationTime"]
    objectId = comment["metadata"]["name"]

    halo_comment = {
        "nick": nick,
        "ip": ip,
        "like": 0,
        "mail": mail,
        "ua": ua,
        "insertedAt": createdAt,
        "status": "approved",
        "link": "",
        "comment": comment_content,
        "url": url,
        "objectId": objectId,
        "createdAt": createdAt,
        "updatedAt": createdAt
    }
    print(halo_comment)
    if comment["status"]["hasNewReply"]:
        relpy_items = get_reply(objectId, url)
        for reply in relpy_items:
            json_data["data"]["Comment"].append(reply)
    json_data["data"]["Comment"].append(halo_comment)
    print("添加成功")
    current_directory = os.path.dirname(__file__)
    new_file_path = os.path.join(current_directory, "waline", "wanline_new.json")
    # 将 JSON 数据保存到新文件
    with open(new_file_path, "w") as file:
        json.dump(json_data, file, indent=4)
    print("写入成功")
    # time.sleep(3)

    # json_data.append(halo_comment)
