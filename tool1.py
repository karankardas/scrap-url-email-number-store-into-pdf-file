from bs4 import BeautifulSoup
import requests
import requests.exceptions 
from collections import deque # deque means double ended ques
import re # used for regular expression
import urllib.parse
from fpdf import FPDF
import warnings # ignore warnings 

warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", UserWarning)
pdf = FPDF()
user = str(input('[+] Enter Url : '))
urls = deque([user])

scrap_urls = set()
emails = set()
phone = set()
count = 0
try:
    while len(urls):
        count+=1
        if count==20: # only scan upto 19
            break
        url = urls.popleft()
        scrap_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts) # {0.scheme}://{0.netloc} = url expression

        path = url[:url.rfind('/')+1] if '/' in parts.path else url
		
        with open('link.txt','a') as f:
            f.write('[%d] Processing %s\n'%(count,url))
        # print('[%d] Processing %s'%(count,url))
        
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema,requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+',response.text,re.I))
        emails.update(new_emails)
        new_mobile = set(re.findall(r'^(\+?\d{1,3}[- ]?)?\d{10}$',response.text,re.I))
        phone.update(new_mobile)
        soup = BeautifulSoup(response.text,features='lxml')

        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url+link
            elif not link.startswith('http'):
                link = path+link
            if not link in urls and not link in scrap_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing')


try:
	for mail in emails:
		# print('[Recieved] ',mail)
		with open('email.txt','a') as f:
				f.write('[Recieved] %s\n'%mail)
except:
	print('Email not found')

try:
	for number in phone:
		with open('number.txt','a') as f:
				f.write('[Recieved] %s\n'%number)
			
except:
	print('Number not found')
	
#----------- Add URL in pdf ----------- 
pdf.add_page()

with open('link.txt','r') as f:
	data1 = f.readlines()

# add page for title
pdf.set_font('Arial', 'B', 12)

# Add title name
pdf.cell(0, 10, 'URL : ', 0, 1, 'C')

# max width for adjust the length of the text
max_width = 200

# back to the normal text
pdf.set_font('Arial', '', 12)

for line in data1:
	pdf.multi_cell(max_width, 4, line.strip())
    #pdf.cell(0, 10, line.strip())
	pdf.ln()

#----------- Add email in pdf -----------

try:
	pdf.add_page()
	with open('email.txt','r') as f:
		data2 = f.readlines()
	
	pdf.add_page()

	# add page for title
	pdf.set_font('Arial', 'B', 12)

	# Add title name
	pdf.cell(0, 10, 'EMAIL : ', 0, 1, 'C')

	# back to the normal text
	pdf.set_font('Arial', '', 12)

	for line in data2:
		pdf.multi_cell(max_width, 4, line.strip())
		#pdf.cell(0, 10, line.strip())
		pdf.ln()

except:
	print('Email not found')
	

#----------- Add number in pdf -----------

try:
	with open('number.txt','r') as f:
		data3 = f.readlines()
	
	pdf.add_page()
	
	# add page for title
	pdf.set_font('Arial', 'B', 12)

	# Add title name
	pdf.cell(0, 10, 'Number : ', 0, 1, 'C')

	# back to the normal text
	pdf.set_font('Arial', '', 12)


	for line in data3:
		pdf.multi_cell(max_width, 4, line.strip())
		#pdf.cell(0, 10, line.strip())
		pdf.ln()

except:
	print('Number not found')


# Save the PDF file
pdf.output('output_file_success.pdf', 'F')