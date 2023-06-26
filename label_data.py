#!/usr/bin/env python
"""
This file gathers data to be used for pre-processing in training and prediction.
"""
import pandas as pd

def main():

    blacklist = 'phishing_database.csv'
    whitelist = 'whitelist.txt'

    urls = {}
    
    blacklist = pd.read_csv(blacklist)

    #Assign 0 for non-malicious and 1 as malicious for supervised learning.
    for url in blacklist['url']:
        urls[url] = 1
    
    with open(whitelist, 'r') as f:
        lines = f.read().splitlines()
        for url in lines:
            urls[url] = 0

    return urls

if __name__ == "__main__":
    main()


'''
定义黑名单文件路径（blacklist）和白名单文件路径（whitelist）。

创建一个空字典urls，用于存储URL和对应的标签。

使用pd.read_csv(blacklist)读取黑名单文件，并将其存储在blacklist变量中。

遍历黑名单文件中的每个URL，并将其作为键，对应的标签（1）作为值，添加到urls字典中，表示这些URL是恶意的。

使用open(whitelist, 'r')打开白名单文件，并逐行读取文件内容。

遍历白名单文件中的每个URL，并将其作为键，对应的标签（0）作为值，添加到urls字典中，表示这些URL是非恶意的。

返回包含URL和标签的字典urls。

该函数的主要作用是从黑名单文件和白名单文件中读取URL，并为每个URL分配相应的标签（0表示非恶意，1表示恶意）。通过调用main()函数，可以获取一个字典，其中包含了所有URL及其对应的标签，以供后续的处理和预测使用。
'''