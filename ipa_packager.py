
from utils.packager import Packager

import os

class IpaPackager():
    """
    An ipa packager utility that creates an ipa file from an app 
    and includes the SwiftSupport and WatchKitSupport folders.

        path_to_app: path to the .app file to be packaged 
        path_to_ipa: the output path to place the .ipa file

    Usage:

        ipa = IpaPackager("/path/to/MyApp.app","/output/path/MyApp.ipa")
        ipa.package()

    """
    def __init__(self, path_to_app, path_to_ipa, developer_dir = None):

        self.app_path = path_to_app
        self.ipa_path = path_to_ipa
        self.app_name = os.path.splitext(os.path.basename(self.app_path))[0]
        self.frameworks_path = os.path.join(path_to_app, "Frameworks")

        self.developer_dir = "/Applications/Xcode.app/Contents/Developer"

        if developer_dir:
            self.developer_dir = developer_dir
        elif "DEVELOPER_DIR" in os.environ:
            self.developer_dir = os.environ["DEVELOPER_DIR"]

        self.os_libs_path = os.path.join(self.developer_dir, "Toolchains/XcodeDefault.xctoolchain/usr/lib/swift/iphoneos/")
        self.watchkit_binary = os.path.join(self.developer_dir, "Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/Library/Application Support/WatchKit/WK")

    def __should_include_watchkit(self):

        extension_path = os.path.join(self.app_path,"Plugins","%s WatchKit Extension.appex" % self.app_name)
        extension_exists = os.path.exists(extension_path)

        return extension_exists

    def __filtered_swift_libs(self, libs):
        return [ lib for lib in libs if lib.startswith("libswift") ]

    def __swift_libs_to_copy(self):

        app_swift_libs = self.__filtered_swift_libs(os.listdir(self.frameworks_path))
        os_swift_libs = self.__filtered_swift_libs(os.listdir(self.os_libs_path))

        # We only need the swift libraries in use by the app
        libs_to_copy = set(app_swift_libs).intersection(set(os_swift_libs))

        return libs_to_copy


    def package(self):
        
        ipa = Packager(self.ipa_path)

        # Include App
        ipa.add(self.app_path,"Payload/%s.app" % self.app_name)

        # Include WatchKit Binary
        if self.__should_include_watchkit():
            ipa.add(self.watchkit_binary, "WatchKitSupport/WK")
        
        # Include Swift Libraries
        swift_libs_to_include = self.__swift_libs_to_copy()
        
        for lib in swift_libs_to_include:
            lib_path = os.path.join(self.os_libs_path, lib)
            ipa.add(lib_path, "SwiftSupport/%s" % os.path.basename(lib))

        ipa.package()
