import mailbox
from email import policy
from email.parser import BytesParser
import os
import sys

# check if mbox file path is provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide the path to the mbox file as a command line argument")
    print(sys.argv)
    sys.exit(1)

# read in the mbox file path from command line argument
mbox_file_path = sys.argv[1]

# create a mailbox object
mbox = mailbox.mbox(mbox_file_path)

if len(sys.argv) >= 3:
    read_limit = int(sys.argv[2])
else: 
    read_limit = len(mbox)

# iterate through each email in the mailbox
counter = 0
for message in mbox:
    while counter <= read_limit: 
        # parse the email message
        msg = BytesParser(policy=policy.default).parsebytes(message.as_bytes())

        # get the email sender
        sender = msg['From']

        # get the date received
        date_received = msg['Date']
        # get the email body text
        text = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any non-text parts or attachments
                if ctype not in ['text/plain', 'text/html'] or 'attachment' in cdispo:
                    continue

                # add the plain text to the text variable
                text += part.get_payload(decode=True).decode()

        else:
            # for non-multipart messages, just extract the plain text
            text = msg.get_payload(decode=True).decode()

        # check for attachments
        for part in msg.walk():
            # check if the part is an attachment
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # save the attachment
            filename = part.get_filename()
            if not filename:
                filename = 'untitled'
            with open(os.path.join('.', filename), 'wb') as f:
                f.write(part.get_payload(decode=True))


        # print out the email details
        if sender not in ['Petfinder <petfinder@sfmc.petfinder.com>']:
            print('From:', sender)
            print('Date:', date_received)
            print('Text:', text)
            counter += 1
            print("===" * 10)