# ios-build-utils
iOS Build Utility Scripts

# ipa Packager

Usage:

```
from ipa_packager import IpaPackager

ipa = IpaPackager("/path/to/MyApp.app","/output/path/MyApp.ipa")
ipa.package()
```
Command Line Usage:

```
python ipa_packager.py -i <AppBundle.app> -o <AppIPA.ipa>
```
This will produce `MyApp.ipa` which bundles `MyApp.app` and the appropriate files for `SwiftSupport` and `WatchKitSupport` as needed.

For example if MyApp was written in swift and included a Watch app, the contents of the ipa file will be

- MyApp.ipa
  - Payload/MyApp.app
  - SwiftSupport
    - libswift....
    - ....
  - WatchKitSupport
    - WK 

# Packager

Usage:

```
from utils.packager import Packager

p = Packager("package.zip")
p.add("/path/to/file")
p.add("/path/to/another/file","another/file")
p.package()
```

This Produces a zip file with

- package.zip
  - file
  - another/file


# Running the tests

There are a few tests which can be run using:

```
python -m unittest discover test
```
