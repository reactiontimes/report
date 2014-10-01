import email, getpass, imaplib, os

def decodePart(string):
    res=string.replace('=\r\n','\n').replace('=3D','=')
    return res

#detach_folder = "C:\attachements" # place to store attachments
print('Email Retriever. Finds emails with subject : Results and'
      '/n finds lines looking like data.  Produces output designed'
      '/n to cut and past into "playtext.txt"'
      'best to have emails in a special folder')
user = input("Gmail Username: ")
#pwd = getpass.getpass("Gmail Password: ")
pwd = input("Gmail Password: ")

folder= input("Gmail Folder: ")
if not folder:
    folder = 'Inbox'
# connect to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user, pwd)

## use m.list() to get all the mailboxes- like this
#for li in m.list()[1]:
#    print(li.decode('utf-8'))

m.select(folder) # here you a can choose a mail box like INBOX instead


resp, items = m.search(None, 'ALL')
items = items[0].split() # getting the mails id

my_msg = [] # store relevant msgs here in please
msg_cnt = 0
stopit = False
for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)")
    #print("data:",len(data),'\n\n')
    #print("data01:",(data[0][1]),'\n\n')

    mesg=  email.message_from_string(data[0][1].decode("utf-8"))
    fromaddr=mesg['From']
    subject=mesg['Subject']
    if subject == 'Results':
        text = mesg.get_payload()
        if mesg.is_multipart():
            text = '\n'.join([decodePart(part.get_payload()) for part in [text[0]]])
        res = '\n'.join([line for line in text.split('\n')
                         if len(line.split(','))==8])
        print('#',fromaddr,'\n',res)
            
