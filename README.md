# paswd_import
Imports passwords from/to various password managers in a CSV format.

License
=======
<begin of the license text>
Copyright (c) 2020 by Igor Royzis.
The program can be freely used, distributed and modified if:
a) this note, as a whole chapter, is not removed or modified from the readme, documentation and the source code;
b) the program or its derived work is not used for commercial purposes. For a commercial license please contact the author.
The official project page: https://github.com/royzis/paswd_import
<end of the license text>

Supported managers in this version:
===================================
Lastpass          (tested on Lastpass 4.59.0)
Firefox Lockwise  (tested on Firefox v82)
Dropbox Passwords (tested with Dropbox Passwords 7.2.15)

Usage:
======

./password_import.py input_csv input_format (ff|lp|dp) output_csv out_format (ff|lp|dp)

IMPORTANT NOTE! Don't forget to wipe the CSV files containg your passwords carefully after a successful export/import operation. Leaving temporary CSV files may compromise all your passwords!

Technical details:
==================
CSV formats:
------------
Lastpass: url,username,password,extra,name,grouping,fav     
where extra - notes, names - title, grouping - the Lastpass folder, (will be empty for the program), fav - 1 or 0 (will be 0 for the program)
Example: https://www.netflix.com/login,netflix_user1@email.com,mypassword1234!,,Netflix,,0

Dropbox Passwords: title,url,username,password,notes
Example: Netflix,https://www.netflix.com,user@mail.com,mypassword1,


Firefox Lockwize: "url","username,"password","httpRealm","formActionOrigin","guid","timeCreated","timeLastUsed","timePasswordChanged"
where httpRealm is the HTTP realm (will be empty for the program), guid will be a random GUID, formActionOrigin will be equal to URL, times - the unix time in miliseconds (will be the current time in the program).
Example: "https://www.facebook.com","user@mail.com","mypassword1234!",,"https://www.facebook.com","{ca2153a1-5128-1347-8705-72de564d288c}","1562667989642","1602795147324","1562667989642"

Useful stuff:
-------------
Erasing all saved passwords in Firefox:
chrome://pippki/content/resetpassword.xhtml  (deletes all passwords including the master password and personal keys)

Enable importing a CSV file passwords in Firefox:
about:config
signon.management.page.fileImport.enabled  set it to True
