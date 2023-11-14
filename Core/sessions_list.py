import re


def main(si):
    si.content.sessionManager.currentSession.key
    list = []
    for session in si.content.sessionManager.sessionList:
        dict = (
            "session key={0.key}, "
            "username={0.userName}, "
            "ip={0.ipAddress}".format(session)
        )
        ipv4 = re.findall("(?:\d{1,3}\.){3}\d{1,3}", dict)[0]
        username = re.findall("username=([^,]+)", dict)[0]
        if ipv4 != "127.0.0.1":
            list.append({"ipv4": ipv4, "username": username})
    si.content.sessionManager.Logout()
    session = si.content.sessionManager.currentSession
    counts = {}
    for item in list:
        ipv4 = item["ipv4"]
        username = item["username"]
        key = (ipv4, username)
        counts[key] = counts.get(key, 0) + 1
    return counts
