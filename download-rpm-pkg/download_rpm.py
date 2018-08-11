#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    文件作者: fqs_1991@yeah.net
    @file: download_rpm.py
    @time: 2017/8/23 10:53
"""

"""
程序功能：制作离线安装包的过程中，下载某个rpm包依赖的其他rpm包


比如要制作docker-ce-18.03.1.ce-1.el7.centos.x86_64.rpm的离线包：
1. 在系统上执行yum install docker-ce-18.03.1.ce-1.el7.centos.x86_64.rpm -y
2. 待rpm包安装成功后，将此rpm包的依赖包如下：
Dependency Installed:
  audit-libs-python.x86_64 0:2.8.1-3.el7         checkpolicy.x86_64 0:2.5-6.el7                     container-selinux.noarch 2:2.66-1.el7         libcgroup.x86_64 0:0.41-15.el7           
  libseccomp.x86_64 0:2.3.1-3.el7                libsemanage-python.x86_64 0:2.5-11.el7             libtool-ltdl.x86_64 0:2.4.2-22.el7_3          lz4.x86_64 0:1.7.5-2.el7                 
  pigz.x86_64 0:2.3.3-1.el7.centos               policycoreutils-python.x86_64 0:2.5-22.el7         python-IPy.noarch 0:0.75-6.el7                setools-libs.x86_64 0:3.3.8-2.el7        
Updated:
  systemd.x86_64 0:219-57.el7                                                                                                                                                                
Dependency Updated:
  audit.x86_64 0:2.8.1-3.el7                 audit-libs.x86_64 0:2.8.1-3.el7                 libgudev1.x86_64 0:219-57.el7                            libselinux.x86_64 0:2.5-12.el7       
  libselinux-python.x86_64 0:2.5-12.el7      libselinux-utils.x86_64 0:2.5-12.el7            libsemanage.x86_64 0:2.5-11.el7                          libsepol.x86_64 0:2.5-8.1.el7        
  policycoreutils.x86_64 0:2.5-22.el7        selinux-policy.noarch 0:3.13.1-192.el7_5.4      selinux-policy-targeted.noarch 0:3.13.1-192.el7_5.4      systemd-libs.x86_64 0:219-57.el7     
  systemd-sysv.x86_64 0:219-57.el7
拷贝至某个文件中，假设为docker-ce

3. 按要求执行程序
4. docker-ce-18.03.1.ce-1.el7.centos.x86_64.rpm依赖包会被下载至docker-cedir目录中

注：程序要求操作系统提供 yumdownloader 工具
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

