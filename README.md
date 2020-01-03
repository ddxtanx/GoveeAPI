# What this is.
This is a library I created to use python to control Govee Home lights. I would not have been able to make this without [this](https://github.com/egold555/Govee-H6113-Reverse-Engineering) insight into the packet format Govee uses. You can use this library with minimal technical knowledge of bluetooth.

# Requirements
This should be done on a Raspberry Pi in whatever room your lights are in. This unfortunately will not work on a Mac/PC (unless you can install [gattlib](https://github.com/labapart/gattlib) on it).

You need to have both python (3.6+) and [gattlib](https://github.com/labapart/gattlib) installed, if it is not already. Gattlib might throw some weird errors during install, but all of the problems I encountered had solutions on StackOverflow. *If you can already run* `gatttool --help` *you do not need to install gattlib.*

For the python requirements, just run
`pip3 install -r requirements.txt`
and you'll have all the required components.

# Recommended Components
I would recommend using a tool called IFTTT, which you can use to create custom workflows with Google Home, Amazon Alexa, etc. If you just want to use the python library without the Smart Home connection & wakeup functionality, you can delete `server.py` and just run through all the files and add in whatever is relevant to you. If you want to integrate this into a smart home, make sure you have a Google Home/Amazon Alexa/some smart assistant that works with IFTTT.

Also, this is best installed onto a Raspberry Pi, as I said above, both because it is very low profile and because it has gatttool pre-installed. They're also quite cheap and easy to set up!

# Integrating this into a Smart Home
More likely than not, you will first need to expose your pi (or whatever device you want to control the Govee lights) to the internet. While there isn't one guide for every single router, you need to log onto your router and find some setting along the lines of "NAT Forwarding." There should be options to add either rules or devices, and click that option.
The external port is the port that gets exposed to the internet, the IP address should be the IP address of the device controlling the Govee lights and the internal port is the port you choose to set the server up on, on the device.

Also, make sure you know your public IP address (which you can find out by Googling "whats my ip address").

Once that is done, go to constants.py and set server_port to whatever you chose your *internal* port to be, and set your server_secret to whatever you can use as a unique identifier. This is just so hackers and tech-savvy friends can't mess with you and strobe your lights or make fake alarms whenever they want.

Then, just go through each of controller.py, tool.py, and server.py and fill in details that are relevant to you or add functionality if you see fit.

## Using IFTTT with Google Home/Amazon Alexa
Once you've installed IFTTT and made an account, create a new applet. The "If" part should be either from Google Assistant or Amazon Alexa depending on what smart device you have, so search it in the toolbar and connect the service. You can choose to have whatever voice command trigger the service, it's up to you! Make sure you use a "$" if you want to arguments in your command like "Wake me up at $" to wake you up at whatever time "$" becomes.

Then the "then that" part should be a webhooks service. The URL should be your public ip with port formatted like "http://URL:PORT" with one of "/alarm" "/strobe" "/end_strobe" or a custom endpoint you put in server.py.

"/alarm" uses POST requests, so set the request type to "POST" and body to "alarm=[TextField]&key=[Whatever your server key was]". The textfield ingredient can be added by clicking the "Add Ingredient" button at the top-left of the keyboard.

"/strobe" and "/end_strobe" use GET requests, so set the request type to that. Instead of placing the key in the body, place it in the URL after the endpoint like so "http://URL:PORT/endpoint?key=[Whatever your server key was.]"

If you add other endpoints to server.py, add them to IFTTT and you'll be all good!

Then, to start up the server, just run `nohup python3 server.py > server_log 2>&1 &` to start up the webserver in the background, and enjoy the control you now posses over your Govee devices!
