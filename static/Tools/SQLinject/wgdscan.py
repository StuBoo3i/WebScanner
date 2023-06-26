#!/usr/bin/env python
# -*- coding:utf-8 -*-

from static.Tools.SQLinject.lib.core.Spider import SpiderMain

def main():
    root = "http://192.168.1.192:8086/pikachu/"
    threadNum = 10
    # spider
    wgd = SpiderMain(root, threadNum)
    wgd.craw()


if __name__ == '__main__':
    main()