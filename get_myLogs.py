import os
import subprocess

# Capture log folder name
myLogFolder = input("Please enter folder log folder name: ")
if(myLogFolder != ''):
    print('Gotcha! Folder name, will be ' + myLogFolder)
else:
   myLogFolder = input("Please enter folder log folder name: ")

#Check if the logs folder exists, if not create it
print('Creating log folder!')
try:
    os.makedirs(myLogFolder)
except FileExistsError:
    print('Folder already exists, and therefore the existing log folder will be used.')
    input("If so please press Enter to continue...")
    pass

#Get a list of all pods
print('Retrieving all pods list')
result = subprocess.run(['kubectl', 'get','pods','--no-headers'], stdout=subprocess.PIPE)
result = result.stdout.decode('utf-8').split('\n')
total = len(result) - 1
podCounter = 0

searchValue1 = 'dqix'
searchValue2 = 'indexer'
searchValue3 = 'indexing-manager'
searchValue4 = 'profile'
searchValue5 = 'qix-sessions'
searchValue6 = 'hub-'
searchValue7 = 'elastic-infra-mongodb'
#searchValues = ['dqix','indexer']

for line in result:
    x = line.split(' ', maxsplit=2)[0]
    if searchValue1 in x or searchValue2 in x or searchValue3 in x or searchValue4 in x or searchValue5 in x or searchValue6 in x or searchValue7 in x:
        if(x!= ''):
                logs = ''
                describe = ''
                podCounter += 1
                podCount = '(' + str(podCounter) + ')'
                
                print('Retrieving pod description for', x, podCount)
                describe = subprocess.run(['kubectl', 'describe', 'pod', x], stdout=subprocess.PIPE)
                describe = describe.stdout.decode('utf-8')
                print('Writing pod description for', x, 'to logs' + os.sep + x + '.describe')
                f = open(myLogFolder + os.sep + x + '.describe', 'w')
                f.write(describe)
                f.close()

                print('Retrieving logs for', x, podCount)
                logs = subprocess.run(['kubectl', 'logs', x, '--all-containers'], stdout=subprocess.PIPE)
                logs = logs.stdout.decode('utf-8')
                print('Writing logs for', x, 'to logs' + os.sep + x + '.log')
                f = open(myLogFolder + os.sep + x + '.log', 'w')
                f.write(logs)
                f.close()

                print('Checking for logs from previous instances of', x, podCount)
                logs = subprocess.run(['kubectl', 'logs', '-p', x, '--all-containers'], stdout=subprocess.PIPE)
                logs = logs.stdout.decode('utf-8')
                if(logs != ''): #Filter out instances with no previous logs
                        print('Writing logs for', x, 'to logs' + os.sep + x + '_old.log')
                        f = open(myLogFolder + os.sep + x + '_old.log', 'w')
                        f.write(logs)
                        f.close()


print('##############################################################')
print('Logs have been saved and can be found in ' + myLogFolder + ' folder!')
print('##############################################################')


# Request for compressing or not the folder
compAnswer = ['Yes','yes','y','Y','YES']
compQuest = input('Do you need to compress ' + myLogFolder + ' folder [Y/N]?  :  ')
while compQuest in compAnswer:
    print('Compressing... please wait...')
    compression = subprocess.call(['tar','-zcpvf', myLogFolder+'.tar.gz', myLogFolder], stdout=subprocess.PIPE)
    print('Folder compression is completed!')
    break
else:
    print('No compression. So, I guess we are done here!!!')



