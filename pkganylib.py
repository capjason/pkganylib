import os
import dependency
import argparse


def pkg_libs():
    parser = argparse.ArgumentParser(description="package any dylib that binary depends")
    parser.add_argument("--input", metavar='i', type=str, help='binary to be packaged')
    parser.add_argument("--libpath", nargs='?', metavar='l', type=str,
                        help='a directory where dependencies are copied to')
    parser.add_argument("--rpath", metavar='r', action='append', help='additional rpath to search for dependencies',
                        nargs='?', default=[])
    parser.add_argument("--excludedir", metavar='e', action='append',
                        help='directories in which the libraries are ignored',
                        nargs='?', default=[])
    args = parser.parse_args()

    binarypath = args.input
    dirname = os.path.dirname(binarypath)

    print(args.excludedir)

    if args.libpath is None:
        libpath = os.path.join(dirname, "lib")
    else:
        libpath = args.libpath

    dependency.package_shared_libraries(binarypath, libpath, args.rpath, args.excludedir)

    # print('id', dependency.check_library_id('/usr/local/OpenCV3.2/lib/libopencv_core.dylib'))


if __name__ == '__main__':
    pkg_libs()
