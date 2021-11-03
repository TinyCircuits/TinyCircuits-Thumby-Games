# https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/

import os
print("Starting URL list builder using Python in GH Action...")

print(os.listdir())

f = open("URLList.txt", "w")
f.write("TEST")
f.close()