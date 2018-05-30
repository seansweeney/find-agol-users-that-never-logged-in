# Log into an ArcGIS Online Organization and find all users that
# have never logged in and print a list.
# 
# Requires: ArcGIS API for Python (https://developers.arcgis.com/python/)
#           Python 3.x
#
from arcgis.gis import GIS
from getpass import getpass
from operator import attrgetter

# Get username and password
username = input('Username: ')
password = getpass(prompt='Password: ')

# Connect to ArcGIS Online
try:
    gis = GIS("https://arcgis.com/", username, password)
except:
    print(sys.exc_info()[0])
    exit(1)

# Get a list of all users
try:
    all_users = gis.users.search(None, max_users=500)
except:
    print(sys.exc_info()[0])
    exit(1)

# Use list comprehension to create a subset list of disabled users
never_logged_in = [user for user in all_users if user.lastLogin == -1]

# Items are either in a folder or not. The latter are called root items. There can only be one folder level, so only one level needs to be traversed.
for user in sorted(never_logged_in, key=attrgetter('lastName', 'firstName')):
    print(user.fullName + " (" + user.username + ")")
    print("Role: " + gis.users.roles.get_role(user.roleId).name)
    print("=" * 50)

print("Total number of users who never logged in: %s" % str(len(never_logged_in)))

exit(0)