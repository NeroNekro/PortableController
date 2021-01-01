### How to install?
Download and enjoy

### Prepation for using?
You should be sure, that port 80 is not in use or change the port number in the config.ini file

### How I start the service?
Start main.py

### I can't connect from other devices.
Maybe your firewall block all connections.
For Windows:
1) Start CMD with admin rights
2) netsh firewall add portopening TCP 80 "PortableController"
If you want another port, you have to change the port number in config.ini and in the line above

### What is the link to the server?

http://YOUR-IP:PORT/www/TEMPLATE:NAME/index.html

### Which Buttons are available?
F1-F12, a-z, 0-9, alt, shift, ctrl, del, enter, up, down, left, right

### Are combinations possible?
No. In the next version, I want add some extra features for combinations.

### How much is the delay?
<= 1 second

### Why is the delay so long?
The delay comes together for several reasons. Partly it is due to the Wlan and partly an HTML request is data intensive.

### Is it possible to find out the key-status in SC?
No, StarCitizen does not currently offer an API.

### Can it be used for other games?
All games and software products which work with hotkeys are possible.

### What are the limits of the surface?
You can design anything with HTML/Javascipt.

### Under which license is the software published?
Flask: BSD 3-Clause
My Scripts: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)