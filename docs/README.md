# RPiCoffee
## Progress

[x] Soldering jumper wires to all of the frontpanel buttons

[ ] Rework on the wire management

[ ] Solder the interface circuit

### Electromechanical stuff

The frontpanel looked very spacious at first, but there is a grid of plastic under the buttons giving minimal space for running the wires. This plastic construction is for transfering the mechanical force to the actual pushbuttons on the circuit and manages to transfer the light of the SMD-LEDs to the front. So if you really mess up, the buttons stop working, the LED's light will be blocked and the case of the frontpanel will not close anyway. You could cut the grid a little bit, but I wanted to modify the machine as little as possible.

![Image of the openened frontpanel](/docs/images/frontpanel_unmodified_opened.JPG)

First step is finished with soldering jumper cables to every switch. I planned to do the same with the LEDs for reading out the machine's status and errors but the SMD-LEDs are pretty small and my solder tip seemed to big for proper soldering. You can see them some of them (DL3 - DL5) in the first row of the circuit board.

I will have to rework the running of the wires a little bit because right now the button press feels softer than before. Meaning, the wires are pressed down by the plastic grid, eventually causing damage to the isolation in the future.

![Image of modified frontpanel](/docs/images/frontpanel_modified.JPG)

There is a hole for the original flat wire which is big enough for my hacked wires.
![Image of the cable duct](/docs/images/kind_of_cable_duct.JPG)

Here is the place where the Raspberry Pi and the interface circuit is planned to stay at. This looks like a safe place for electronics (you have to be aware of humidity) because the mainboard of the machine also is placed there.
![Image of the cables coming from the fron panel and the area for hacked stuff](/images/cables_sideview_place_for_hacked_stuff.jpg)
