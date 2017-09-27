import telepot
from pprint import pprint
import sys
import time
import telepot
import platform
import socket
import os
import psutil
import transmissionrpc
from datetime import timedelta
import logging

def checkinfo(chat_id,info):
 data=[]
 tc = transmissionrpc.Client('localhost', port=9091, user='****', password= '****')
 if chat_id == 0000000: #insert telegram ids if you want to limit access
	 if info =='ip':
                gw = os.popen("ip -4 route show default").read().split()
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((gw[2], 0))
                ipaddr = s.getsockname()[0]
                gateway = gw[2]
                data=ipaddr
	 elif info =='help':
		 data =('Command List: \n'+
                        'ip: Shows current IP address \n'+
                        'help: shows this message \n'+
                        'ram: shows used, free and total ram\n'+
                        'disk: shows used, free and total disk\n'+
                        'system: \n'+
                        'cpu: \n'+
                        'list: Lists torrents\n'+
                        'add [magnetic link]: adds torrent to the list \n'+
                        'remove [id]: removes selected torrent from list\n'+
                        'info [id]: shows info for the selected torrent')
         elif info =='ram':
                data.append(['Total: ',psutil.virtual_memory().total])
                data.append(['Used: ',psutil.virtual_memory().used])
                data.append(['Free: ',psutil.virtual_memory().available])
         elif info == 'disk':
                data = psutil.disk_usage('/')
         elif info == 'system':
                with open('/proc/uptime', 'r') as f:
                        uptime_seconds = float(f.readline().split()[0])
                        uptime_string = str(timedelta(seconds = uptime_seconds))
                        data = uptime_string
         elif info == 'cpu':
                p = psutil.Process()
                data = p.cpu_times()
         elif info == 'list'  or info == 'List':
		data = str(tc.get_torrents())
		if data == '[]':
			data = 'Torrent list is empty'
         elif info.startswith('add')or info.startswith('Add') :
		tc.add_uri(info[4:])
		data = 'Torrent added'
         elif info.startswith('remove')or info.startswith('Remove'):
 		tc.remove(info[7:],delete_data=False)
		data = 'Torrent ' + info[7:] + ' removed'
         elif info.startswith('info') or info.startswith('Info'):
		tor = transmissionrpc.Torrent(tc,tc.get_torrents())
		data = str(tor.progress())
         if not data:
		bot.sendMessage(chat_id,"Command not found")	
         else:
		bot.sendMessage(chat_id,data)	
 else:
	bot.sendMessage(chat_id,"Not authorized user")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    str3 = (content_type, chat_type, chat_id,msg['text'])
    print(str3)
    if content_type == 'text':
	checkinfo(chat_id,msg['text'])
	logger.info(str3)
TOKEN = '---------------' #insert your token here
logger = logging.getLogger('pibot')
hdlr = logging.FileHandler('/home/pi/logbot.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)

