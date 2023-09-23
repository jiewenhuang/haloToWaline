import base64

import requests
import json
# 输入你的网站完整URL，不要结尾反斜杠
url = "http://localhost:8090"
comment_api_url = "/apis/content.halo.run/v1alpha1/comments"
post_api_url = "/apis/api.content.halo.run/v1alpha1/posts/"
singleness_api_url = "/apis/api.content.halo.run/v1alpha1/singlepages/"
# 网站的账号
user = "admin"
# 网站的密码
password = "P@88w0rd"
auth_header = "Basic " + base64.b64encode((user + ":" + password).encode()).decode()

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/116.0.0.0 Safari/537.36',
    'Authorization': auth_header
}


def get_comment():
    response = requests.request("GET", url + comment_api_url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data["items"]
    else:
        return None


def get_url(metadate, kind):
    if kind == "Post":
        post_response = requests.request("GET", url + post_api_url + metadate, headers=headers)
        if post_response.status_code == 200:
            post_response_json = json.loads(post_response.text)
            return post_response_json["status"]["permalink"]
        else:
            return None
    if kind == "SinglePage":
        if metadate == 'links':
            return '/links'
        else:
            post_response = requests.request("GET", url + singleness_api_url + metadate, headers=headers)
            if post_response.status_code == 200:
                post_response_json = json.loads(post_response.text)
                return post_response_json["status"]["permalink"]
            else:
                return None

    if kind == "Moment":
        return '/moments/' + metadate


def get_reply(id, comment_url):
    reply_list = []
    r_url = url + "/apis/api.halo.run/v1alpha1/comments/" + id + "/reply"
    response = requests.get(url=r_url, headers=headers).json()
    items = response["items"]
    for comment in items:
        r_url = comment_url
        r_nick = comment["spec"]["owner"].get("displayName", "匿名")
        r_ua = comment["spec"].get("userAgent", "")
        comment_content = comment["spec"]["content"]
        created_at = comment["spec"]["creationTime"]
        object_id = comment["metadata"]["name"]

        halo_comment = {
            "nick": r_nick,
            "ip": "",
            "like": 0,
            "mail": "",
            "ua": r_ua,
            "insertedAt": created_at,
            "pid": id,
            "status": "approved",
            "link": "",
            "comment": comment_content,
            "url": r_url,
            "rid": id,
            "objectId": object_id,
            "createdAt": created_at,
            "updatedAt": created_at
        }
        reply_list.append(halo_comment)
    return reply_list


if __name__ == '__main__':
    get_comment()
