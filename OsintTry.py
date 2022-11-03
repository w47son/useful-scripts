
import argparse
import sys
import json
import urllib.request


parser = argparse.ArgumentParser(prog = 'OsintTry',formatter_class=argparse.RawDescriptionHelpFormatter,
                                description = '''OsintTry 1.0\n\nCheck a tryhackme api user to see the completed rooms.\nSet a user "-u" and output "-o" to analyze it with the flag file "-f"''',
                                epilog = '''Example:\t python OsintTry.py -u W4tson -o w4tsonrooms.txt\n\t\t python OsintTry.py -f w4tsonrooms.txt -y 2022 -m 9''')
parser.add_argument('-u', '--user',help='Extract info from the user') 
parser.add_argument('-o', '--outfile',nargs='?', type=argparse.FileType('w'),help='Output the user info to a file') 
parser.add_argument('-f', '--file',nargs='?',type=argparse.FileType('r'),help='Select a file to analyze') 
parser.add_argument('-y', '--year',type=int,help='Find the selected year') 
parser.add_argument('-m', '--month',type=int,help='Find the selected month') 
parser.add_argument('-d', '--day',type=int,help='Find the selected day') 
args = parser.parse_args()


if args.file:
  dataClean=args.file.readlines()
  dataClean=dataClean[0]
  dataClean=json.loads(dataClean)
  dataClean=dataClean['data']

elif args.user and args.outfile:
  url = 'https://tryhackme.com/api/user/activity-events?username='+args.user
  req = urllib.request.Request(url, data=None, headers={'User-Agent': 'OsintTry 1.0'})

  response = urllib.request.urlopen(req)
  webContent = response.read().decode('UTF-8')
  dataClean=json.loads(webContent)
  dataClean=dataClean['data']
  dataClean=sorted(dataClean,key=lambda d: (d['_id']['year'],d['_id']['month'],d['_id']['day']), reverse=False)
  args.outfile.write(webContent) 
  
else:
  parser.print_help()
  exit(1)


completedlabs=0
maxRooms=0
dateMaxRooms=''

def sumRooms(rooms,dateOff=False):
  global completedlabs,maxRooms,dateMaxRooms

  completedlabs+=rooms["events"]
  if maxRooms < rooms["events"]:
    maxRooms = rooms["events"]

    if not dateOff:
      dateMaxRooms=rooms["_id"]["day"]+"/"+rooms["_id"]["month"]+"/"+rooms["_id"]["year"]

for i in range(len(dataClean)):
  if args.year and args.month and args.day:
    if dataClean[i]["_id"]["action"]=="complete-room" and int(dataClean[i]["_id"]["year"])==args.year and int(dataClean[i]["_id"]["month"])==args.month and int(dataClean[i]["_id"]["day"])==args.day:
      sumRooms(dataClean[i],True)

  elif args.year and args.month:
    if dataClean[i]["_id"]["action"]=="complete-room" and int(dataClean[i]["_id"]["year"])==args.year and int(dataClean[i]["_id"]["month"])==args.month:
      sumRooms(dataClean[i])

  elif args.year:
    if dataClean[i]["_id"]["action"]=="complete-room" and int(dataClean[i]["_id"]["year"])==args.year:
      sumRooms(dataClean[i])

  else:
    if dataClean[i]["_id"]["action"]=="complete-room":
      sumRooms(dataClean[i])
      
print('Rooms completed:',completedlabs)
if dateMaxRooms!='':
  print('Max rooms:',maxRooms,'in',dateMaxRooms)