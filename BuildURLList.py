# https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/

print("Hello World!")

f = open("URLList.txt", "w")
f.write("TEST")
f.close()