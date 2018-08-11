#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
程序主要功能：在特定的项目中，找出含有某个关键字的文件内容以及文件名称
比如：
    [root@localhost ~]# python search_for_file.py 
    Please enter the absolute path of the file (eg: /root/hello, C:\docker-master): /root/moby-17.03.1-ce-rc1
    Please input search words: dmsetup

    Result:
    [
        {
            "file_lines":[
                "// \tDM_ADD_NODE_ON_RESUME, /* add /dev/mapper node with dmsetup resume */",
                "// \tDM_ADD_NODE_ON_CREATE  /* add /dev/mapper node with dmsetup create */"
            ],
            "file_name":"/root/moby-17.03.1-ce-rc1/daemon/graphdriver/devmapper/devmapper_doc.go"
        },
        {
            "file_lines":[
                "// CreatePool is the programmatic example of \"dmsetup create\".",
                "// ReloadPool is the programmatic example of \"dmsetup reload\".",
                "// GetDeps is the programmatic example of \"dmsetup deps\".",
                "// GetInfo is the programmatic example of \"dmsetup info\".",
                "// GetInfoWithDeferred is the programmatic example of \"dmsetup info\", but deferred.",
                "// GetDriverVersion is the programmatic example of \"dmsetup version\".",
                "// GetStatus is the programmatic example of \"dmsetup status\".",
                "// GetTable is the programmatic example for \"dmsetup table\".",
                "// SuspendDevice is the programmatic example of \"dmsetup suspend\".",
                "// ResumeDevice is the programmatic example of \"dmsetup resume\"."
            ],
            "file_name":"/root/moby-17.03.1-ce-rc1/pkg/devicemapper/devmapper.go"
        }
    ]

备注：程序对中文关键字输出支持不是很友好
      当初在研究docker项目的源码，由于对go语言不熟悉以及docker项目过于复杂，因此想要查看具体业务的源代码实现不知道从何下手。比如：想要
      研究docker的devicemapper存储引擎的实现，不太清楚devicemapper实现部分在docker项目中的位置，查看源码就有点困难，想到devicemapper的
      实现主要依据dmsetup命令，因此想到可以通过在整个docker项目中查找包含dmsetup关键字的内容与文件，然后再查看这些文件来了解docker中
      devicemapper的代码实现。当然这些操作更可以通过IDE，find命令等来完成。

"""


import os
import sys
import json

qualified_files = []


def dose_file_exists(file_path):
    value = os.path.exists(file_path)

    if not value:
        print 'File does not exist...'

    return value


def is_file_wanted(file_name, search_word):
    with open(file_name, mode='rb') as fr:
        '''
            引入count计数，当文件中存在连续的三个空行时视为文件遍历结束
        '''
        count = 0
        file_name_with_search_word = None
        file_lines_with_search_word = []

        while 1:
            value = fr.readline().strip()

            if not value:
                count += 1
                if count == 3:
                    break
            else:
                count = 0

            if search_word in value:
                if not file_name_with_search_word:
                    file_name_with_search_word = file_name

                file_lines_with_search_word.append(value)

        if not file_name_with_search_word:
            return None

        return {
            'file_name': file_name_with_search_word,
            'file_lines': file_lines_with_search_word
        }


def search_file(file_path, search_word):
    global qualified_files

    if os.path.isfile(file_path):
        """
            file
        """
        value = is_file_wanted(file_path, search_word)

        if value:
            qualified_files.append(value)

        return
    else:
        """
            directory
        """
        files = os.listdir(file_path)

        for per_file in files:
            search_file(file_path + '/' + per_file, search_word)


def main():
    file_path = raw_input('Please enter the absolute path of the file (eg: /root/hello, C:\docker-master): ').strip()
    search_words = raw_input('Please input search words: ').strip()

    if not file_path or not search_words:
        print 'Both must have input...'
        sys.exit(1)

    if dose_file_exists(file_path):
        search_file(file_path, search_words)

        print '\nResult:'
        
        try:
            print json.dumps(qualified_files, sort_keys=True, indent=4, separators=(',', ':'))
        except Exception:
            print qualified_files


if __name__ == '__main__':
    main()

