#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import os
import base64

os.chdir("docs")

def decode(token):
    tb = {
        'A': '1',
        'X': '2',
        'C': '3',
        'F': '4',
        'U': '5',
        'O': '6',
        'T': '7',
        'W': '8',
        'E': '9',
        'P': '0',
    }
    host = base64.encodebytes(b"slaier.github.io").decode("utf-8")
    token = token[:(1 - len(host))]
    token = [tb[c] if c in tb else c for c in token]
    token = "".join(token)
    return token

def main():
    baseurl = "https://slaier.github.io/blog/#/posts/"
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        'Authorization': 'bearer ' + decode('EfCXXcTcaEdCfFaceWOFfOWdXefPeXEWeOXWTcOec2xhaWVyLmdpdGh1Yi5pbw==')
    }
    r = requests.post("https://api.github.com/graphql", headers=headers, json={
    "query": """{
        repository(owner: "slaier", name: "blog") {
            issues(first: 50, states: OPEN) {
            edges {
                node {
                number
                updatedAt 
                }
            }
        }
      }
    }"""
    })
    edges = r.json()["data"]["repository"]["issues"]["edges"]

    for node in edges:
        url = baseurl + str(node["node"]["number"])
        lastmod = node["node"]["updatedAt"].split("T")[0]
        sitemap.append("\t<url>")
        sitemap.append("\t\t<loc>{}</loc>".format(url))
        sitemap.append("\t\t<lastmod>{}</lastmod>".format(lastmod))
        sitemap.append("\t</url>")

    sitemap.append("</urlset>")
    with open("sitemap.xml", "w") as f:
        f.write("\n".join(sitemap))


if __name__ == '__main__':
    main()