#!/bin/bash
#<uses-sdk android:minSdkVersion="3" />
find ./ -name "AndroidManifest.xml" | xargs -i \
	sed -i -r -e 's/minSdkVersion="3"/minSdkVersion="10"/' {}

#target=android-3
find ./ -name "default.properties" | xargs -i \
	sed -i -r -e 's/target=android-3/target=android-10/' {}

#dos2unix
find ./ -name "*.xml" -o -name "*.properties" -o -name "*.java" -name ".classpath" -o -name ".project" |
	xargs -i sed -i -r -e "s/\r//" {}
