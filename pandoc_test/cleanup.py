import os

dir = r'/Users/lau/OneDrive/KogebogRepo/pandoc_test/output'

# clean out dummy files
for root, subdirs, files in os.walk(dir):

    for file in files:
        path = os.path.join(root, file)
        if os.path.getsize(path) == 4: 
            os.remove(path)

# clean empty folders
for root, subdirs, files in os.walk(dir):

    for subdir in subdirs:
        path = os.path.join(root, subdir)
        if len(os.listdir(path)) == 0:
            os.rmdir(path)
