
Remote Access Tool (RAT) - Python Script
Description:
This Python-based Remote Access Tool (RAT) allows a connected client to remotely interact with the server, enabling various system operations such as command execution, file transfer, screenshot capture, audio recording, and keylogging. The tool is designed to demonstrate remote system control for educational purposes and ethical use cases.

Features:
Remote Command Execution:

Execute shell commands on the server and receive the output.
File Management:

Upload files from the client to the server.
Download files from the server to the client.
Screenshot Capture:

Take a screenshot of the server's desktop and send it to the client.
Audio Recording:

Record 5 seconds of audio from the server's microphone and transmit it to the client.
Keylogger:

Capture keystrokes on the server's machine.
Send logs periodically to a specified email address.
Requirements:
Python 3.x
Modules: socket, subprocess, os, pyautogui, base64, pyaudio, wave, keyboard, smtplib
SMTP configuration for email reporting (for keylogger functionality).
