#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    文件作者: fqs_1991@yeah.net
    @file: download_rpm.py
    @time: 2017/8/23 10:53
"""

import subprocess
import os
import sys


RPM_PKG_ARCH = ['x86_64', 'noarch']


def filter_list(element):
    if element:
        return True


def get_rpms(file_name):
    rpm_list = []
    blankline_count = 0

    with open(file_name, 'rb') as fr:
        while 1:
            line = fr.readline().strip()

            if not line:
                blankline_count += 1
            else:
                rpm_list += filter(filter_list, line.split(' '))
                blankline_count = 0

            if blankline_count >= 3:
                '''
                    如果文件中空白行的数量大于2，则结束对文件内容的遍历
                '''
                break

    return rpm_list


def execute_shell_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()[0]


def download(file_name):
    rpms = get_rpms(file_name)
    download_dir = '{0}dir'.format(file_name)
    rpm_installed_count = 0
    output_is_empty_count = 0

    for rpm in rpms:
        if rpm.split('.')[-1] in RPM_PKG_ARCH:
            rpm_installed_count += 1 
            result = execute_shell_cmd('yumdownloader --destdir={0} {1}'.format(download_dir, rpm))

            if not result:
                output_is_empty_count += 1
            else:
                print 'Ready to download rpm package: {0}'.format(rpm)

    if rpm_installed_count and output_is_empty_count and rpm_installed_count == output_is_empty_count:
        '''
            当安装的每个rpm包输出均为空时，则表示系统没有安装yundownloader工具
        '''
        print 'Please check if yumdownloader is installed'

    print ''


def main():
    file_path = raw_input('Please enter the valid filename (eg: /root/hello or hello): ').strip()
    print ''
   
    if not os.path.exists(file_path):
        print 'Filename {0} dose not exist'.format(file_path)
        sys.exit(1)

    if not os.path.isfile(file_path):
        print 'Filename {0} needs to be a file'.format(file_path)
        sys.exit(1)

    download(file_path)


if __name__ == '__main__':
    main()

