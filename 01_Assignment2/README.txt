HOW TO USE THIS PROGRAM

1. Open up a terminal
2. Enter the command: sudo /etc/init.d/apache2 stop.
   This ends an apache server that runs on boot. When running, it uses port 80,
   which is the port we want to use with this program.
3. Connect to the wifi network: Lenovo PHAB2 Pro
   This is only necessary if you are running this script at the MSU campus.
   MSU's firewall stops the flask server from serving the webpage for some reason.
   The important thing is that you can run the script while connected to a network
   That won't prevent you from serving the webpage.
4. Run this script in the terminal
   The exact command depends on where the file is located, but the current command is
   sudo  python3 ROBOT/01_Assignment2/backend.py
5. If you receive no errors after running the command in the terminal, open a browser
   and enter the IP address of the Pi. You can find the IP address by hover the mouse
   over the wifi symbol in the top right of the screen.
   You can enter the IP address on any device connected to the same wifi network as the
   the  pi, including your phone.
6. To stop the flask server, press 'Ctrl-c' while focused on the terminal.
   The robot will respond to commands entered using the webpage for as long as the flask
   server is running. If you update or change backend.py, it will automatically update
   on the flask server as well, no need to restart the server. If you update the html
   file (Found in the 'templates' folder) then you will need to restart the flask server
   for your changes to take effect.
