import urllib
import urllib2
import cookielib
import os
from bs4 import BeautifulSoup
import types
from optparse import OptionParser

parser = OptionParser()
usage = "Usage: %prog -n [number] -m [text]"
parser = OptionParser(usage=usage, version="%prog 1.0")
parser.add_option("-n", "--number",  action="store", type="string",dest="number",  help="Mobile number to send sms")
parser.add_option("-m", "--text", action="store", type="string", dest="text", help="Text to send")
(options, args) = parser.parse_args()

if options.number and options.text:
	text = options.text +' '+ ' '.join(args)
else:
	print "Fatal: Required arguments are missing!"
	print "Use: -h / --help to get help."
	exit(1)


cj=cookielib.CookieJar()
mobileNo=options.number
message=text

print mobileNo
print message

opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
values = {      'username' : '<Enter your username>',
                'password' : '<Enter your password>',
                'token' : '',
                'hidDetails':'',
                'fbid':'',
                'userMobile1':'<Enter your username>',
                'userPwd1':'<Enter your password>'
                }
data = urllib.urlencode(values)

opener.open('http://www.160by2.com/re-login.action',data)
SessionID=cj._cookies['www.160by2.com']['/']['JSESSIONID'].value
SessionID=SessionID[3:]
print SessionID

#http://www.160by2.com/SendSMS

output=opener.open('http://www.160by2.com/SendSMS',urllib.urlencode({'id':SessionID}))

html=output.read()
smsParams={}

soup = BeautifulSoup(html)

for iput in soup.findAll("input"):
	if iput.has_key('name'):
		if iput.has_key('placeholder'):
			print "\n",iput['placeholder'],"\n"
			if 'Mobile' in iput['placeholder']:
				smsParams[iput['name']]=mobileNo
		elif iput.has_key('value'):
			smsParams[iput['name']]=iput['value']
		else:
			smsParams[iput['name']]=""


smsParams['maxwellapps'] =SessionID
smsParams['hid_exists']='no'
smsParams['fkapps']='SendSMSDec19'

smsParams["by2Hidden"] ="by2sms"
smsParams["UgadHieXampp"] ="ugadicome"
smsParams["aprilfoolc"] ="HoliWed27"
smsParams["reminderDate"] ="01-02-2014"

smsParams["messid_0"]="abc"
smsParams["messid_1"]="abc"
smsParams["messid_2"]="abc"
smsParams["messid_3"]="abc"
smsParams["messid_4"]="abc"

#pTag=soup.findAll("p", { "id" : "p1" })

#smsParams[pTag[0].findAll('input')[1]['name']]=mobileNo

#print smsParams

#print ""

smsParams['sendSMSMsg']=message

'''
beg=html.find('document.createElement("input")')
HiddenName=html[html.find('name", "',beg)+8:html.find(')',html.find('name", "',beg))-1]
smsParams[HiddenName]=''

print "\t",HiddenName,"\n"

beg=html.find('document.createElement("input")',beg+10)
HiddenName=html[html.find('name", "',beg)+8:html.find(')',html.find('name", "',beg))-1]
HiddenVal=html[html.find('value", "',beg)+9:html.find(')',html.find('value", "',beg))-1]
smsParams[HiddenName]=HiddenVal
print "\t",HiddenName,"\n"
'''

print smsParams


opener.addheaders=[
           ("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)"),
           ("Referer", "%s?id=%s" % ("http://www.160by2.com/SendSMS",SessionID)),
           ( "Host","www.160by2.com"),
            ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0"),
            ("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
            ("Accept-Language","en-us,en;q=0.5"),
            ("Accept-Encoding","gzip, deflate"),
            ("Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"),
            ("Connection","keep-alive"),
            ("Cookie",'__gads=ID=8f03a8b282e76a1a:T=1391237241:S=ALNI_MbHkN5hZJg-WUUwOAnYVzMEXW2LTQ; _ga=GA1.2.1334230594.1391237244; '+ '; '.join([str(v.name)+'='+str(v.value) for k,v in cj._cookies['www.160by2.com']['/'].items()]) + '; adCookie=3; shiftpro=axisproapril8th;')
           ]


output=opener.open("http://www.160by2.com/SendSMSDec19",urllib.urlencode(smsParams))

print "Message sent. Thanks for using the script."
