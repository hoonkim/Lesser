import json


def parse_url(url):
    return list(filter(None, url.split("/")))

def parse_body(body):
    return json.loads(body)
