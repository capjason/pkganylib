import sys
import os
import dependency


def pkg_libs():
    if len(sys.argv) < 2:
        print("no enough args")
        return
    binarypath = sys.argv[1]
    dirname = os.path.dirname(binarypath)
    libpath = os.path.join(dirname, "lib")
    dependency.package_shared_libraries(binarypath, libpath,
                                        ["/usr/local/OpenCV3.2/lib", "/usr/local/Cellar/ffmpeg/3.2/lib",
                                         "/usr/local/Cellar/glew/1.13.0/lib",
                                         "/Users/capjason/workspace/package/StitcherDependencies/library/libevent/lib",
                                         "/Users/capjason/workspace/package/StitcherDependencies/library/exiv2/lib",
                                         "/Users/capjason/workspace/package/StitcherDependencies/library/glfw3/lib",
                                         "/Users/capjason/workspace/package/StitcherDependencies/library/ceres-solver/lib",
                                         "/Users/capjason/workspace/package/StitcherDependencies/library/gflags/lib"],
                                        ["/usr/lib/system","/usr/lib"])

    # print('id', dependency.check_library_id('/usr/local/OpenCV3.2/lib/libopencv_core.dylib'))


if __name__ == '__main__':
    pkg_libs()
