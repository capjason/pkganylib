#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import check_output
from shutil import copyfile
import re
import os

' a dependency module '

__author__ = 'capjason'


def escape_library_path(libpathstr):
    regexp = re.compile(r'^\s*(.+\.dylib)\s+\(', re.IGNORECASE)
    searchres = regexp.search(libpathstr)
    if searchres is not None:
        return searchres.group(1)
    else:
        return ''


def check_shared_libraries(binary):
    out = check_output(["/usr/bin/otool", "-L", binary])
    outstr = out.decode('utf-8')
    binaryid = check_library_id(binary)
    return list(filter(lambda s: s != '' and s != binaryid, list(map(escape_library_path, outstr.split('\n')))))


def check_rpath(binary):
    out = check_output(["/usr/bin/otool", "-l", binary])
    outstr = out.decode('utf-8')
    regexp = re.compile(r'cmd\s+LC_RPATH[\s\S]+?path\s+(.+)\s+\(offset', re.IGNORECASE)
    return regexp.findall(outstr)


def add_rpath(binary, path):
    try:
        print("add rpath", binary, path)
        check_output(["/usr/bin/install_name_tool", "-add_rpath", path, binary])
    except Exception as e:
        print("error when add rpath", e, binary, path)


def delete_rpath(binary, path):
    try:
        print("delete rpath", binary, path)
        check_output(["/usr/bin/install_name_tool", "-delete_rpath", path, binary])
    except AttributeError as e:
        print("error when delete rpath", e, binary, path)


def check_library_id(binary):
    out = check_output(["/usr/bin/otool", "-D", binary])
    outstr = out.decode("utf-8")
    arr = outstr.split("\n")
    if len(arr) < 2:
        return ''
    regexp = re.compile(r'^\s*(.+\.dylib)', re.IGNORECASE)
    res = regexp.search(arr[1])
    if res is not None:
        return res.group(1)
    else:
        return ''


def change_id(libpath, libid):
    try:
        print("change id to rpath", libpath, libid)
        check_output(["/usr/bin/install_name_tool", "-id", libid, libpath])
    except AttributeError as e:
        print("error when change id", e, libpath)


def change_id_to_rpath(libpath):
    libname = os.path.basename(libpath)
    libid = os.path.join("@rpath", libname)
    change_id(libpath, libid)


def locate_library(id, rpathlist=[]):
    if id.startswith("@rpath"):
        for rpath in rpathlist:
            libpath = id.replace('@rpath', rpath)
            if os.path.isfile(libpath):
                return libpath
        return ''
    return id


def change_dependency(libpath, dependency, repl):
    print("change dependency", libpath, dependency, repl)
    try:
        check_output(["/usr/bin/install_name_tool", "-change", dependency, repl, libpath])
    except AttributeError as e:
        print("error when change dependency", libpath, dependency, repl)


def package_shared_libraries(binary='', dstDir='', rpathlist=[], excludelibdir=[]):
    print("package libraries of binary:", binary)
    if not os.path.exists(dstDir):
        os.mkdir(dstDir)
    libraries = check_shared_libraries(binary)
    libtobepackaged = []
    binaryrpathlist = check_rpath(binary)
    rpathlist += binaryrpathlist
    for lib in libraries:
        libpath = locate_library(lib, rpathlist)
        if libpath == '':
            print("failed to find library", lib, "dependency of", binary)
            continue
        try:
            libname = os.path.basename(libpath)
            dstlibpath = os.path.join(dstDir, libname)
            libraryid = check_library_id(libpath)
            libdirname = os.path.dirname(libpath)
            if (not os.path.exists(dstlibpath)) and (not libdirname in excludelibdir):
                print("copy file from", libpath, "to", dstlibpath)
                copyfile(libpath, dstlibpath)
                if not libraryid.startswith("@rpath"):
                    change_id_to_rpath(dstlibpath)
                    libraryid = check_library_id(dstlibpath)
                libtobepackaged.append(dstlibpath)

            if not lib == libraryid:
                change_dependency(binary, lib, libraryid)
        except AttributeError as e:
            print(e, libname)
    for library in libtobepackaged:
        package_shared_libraries(library, dstDir, rpathlist, excludelibdir)
