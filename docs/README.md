# RPiCoffee

This project's goal is to make a coffee machine responsive to different HTTP-Requests, like:

**JSON-Request**
```json
{
  "userID": "admin",
  "actions": [
    "turn on",
    "brew espresso"
  ]
}

```
'Cause nobody likes to wait for the machine.

**Possible scenarios are:**
- turn on and shutting down the machine via HTTP-request
- brewing single and double espresso via HTTP-request
- brewing single and double coffee via HTTP-request
- starting the rinse program via HTTP-request (good for preheating the system)
- chaining simple actions like in the example above
- reading out machine status (e.g. water level, coffee bean depot, temperature, errors, ...)
- rendering a responsive web-app for better user experience
- data logging and visualisation in the web-app

The easiest way is to hack the existing frontpanel with overriding its simple pushbuttons. The HTTP-stuff can be handled by a microcontroller with a wifi-shield or a microcomputer like the the RaspberryPi Zero W which has wifi built in.

I will stick to the Raspberry because it is cheap (around 12 Eur for the Zero W) and I do not have to make any hardware modifications to get it up and running. The Raspberry will be prepared with a minimal setup based on Raspbian Lite described in this article: [https://www.heise.de/ct/ausgabe/2017-22-Digitales-Flugblatt-Raspberry-Pi-mit-Batterie-als-anonymer-WLAN-Hotspot-und-Webserver-3851689.html](https://www.heise.de/ct/ausgabe/2017-22-Digitales-Flugblatt-Raspberry-Pi-mit-Batterie-als-anonymer-WLAN-Hotspot-und-Webserver-3851689.html)

It will be powered by its own USB-power supply because I do not know how stable the coffee machines DC rails are and do not have the equipment for measurements. If everything works fine I will parallel the 230V rails of the coffee machine and the Raspberry's power supply.

## Progress

[x] Soldering jumper wires to all of the frontpanel buttons

[x] First Prototype for web app

[ ] Rework on the wire management

[ ] Solder the interface circuit

[ ] Checkout the positions of the relevant sensors (water, coffe grounds level) for direct access

### UI stuff

Some time ago I put together a simple UI-prototype for the planned web app that will be rendered by the raspberry. I used flaticons.com to find some nice icons (see credits below the images). As soon as the technical stuff is working, I will do a redesign with my own icons. Here are some impressions of the first iteration:

![Image of splashscreen](images/UI-Prototype/Mobile_OFFLINE_splash.jpg)
![Image of Offline Screen](images/UI-Prototype/Mobile_OFFLINE.jpg)
![Image of cleaning Screen](images/UI-Prototype/Mobile_cleaning.jpg)

**Credits for the nice icons:**

Icon made by Freepik from www.flaticon.com (coffee cup)

Icon made by Creaticca Creative Agency from www.flaticon.com (shower)

Icon made by Smashicons from www.flaticon.com (pie chart, settings)

### Electromechanical stuff

The frontpanel looked very spacious at first, but there is a grid of plastic under the buttons giving minimal space for running the wires. This plastic construction is for transfering the mechanical force to the actual pushbuttons on the circuit and manages to transfer the light of the SMD-LEDs to the front. So if you really mess up, the buttons stop working, the LED's light will be blocked and the case of the frontpanel will not close anyway. You could cut the grid a little bit, but I wanted to modify the machine as little as possible.

![Image of the openened frontpanel](images/frontpanel_unmodified_opened.JPG)

First step is finished with soldering jumper cables to every switch. I planned to do the same with the LEDs for reading out the machine's status and errors but the SMD-LEDs are pretty small and my solder tip seemed to big for proper soldering. You can see them some of them (DL3 - DL5) in the first row of the circuit board.

I will have to rework the running of the wires a little bit because right now the button press feels softer than before. Meaning, the wires are pressed down by the plastic grid, eventually causing damage to the isolation in the future.

![Image of modified frontpanel](images/frontpanel_modified.JPG)
![Image of modified frontpanel](images/frontpanel_modified_cablerunV1.JPG)

There is a hole for the original flat wire which is big enough for my hacked wires.
![Image of the cable duct](images/kind_of_cable_duct.JPG)

Here is the place where the Raspberry Pi and the interface circuit is planned to stay at. This looks like a safe place for electronics (you have to be aware of humidity) because the mainboard of the machine is placed there, too.
![Image of the cables coming from the fron panel and the area for hacked stuff](images/cables_sideview_place_for_hacked_stuff.jpg)

First test of the hacked frontpanel via "hotwiring" the buttons:

![Hotwiring the espresso button](images/hotwire1.gif)![Espresso out](images/hotwire2.gif)
