#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
import os

os.chdir("docs")

def main():
    baseurl = "https://slaier.github.io/#/posts/"
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        'Authorization': 'bearer 7e3453f7a4ba9ba326316b65ef9cb4a0fc13a0bc'
    }
    r = requests.post("https://api.github.com/graphql", headers=headers, json={
    "query": """{
        repository(owner: "slaier", name: "slaier.github.io") {
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