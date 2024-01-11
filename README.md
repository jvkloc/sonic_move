Python 3.9 program code for Sonic Move project and dance theatre Minimi's Biodata Sonata performance premiering 15.11.2023 in Kuopio City Theatre, Finland. Human motion data recording through Movella (Xsens) motion capture sensors connected to an Awinda USB Dongle or an Awinda Station, sending it to Open Sound Control environment and displaying the live data graphically. It is also possible to run live recordings again by using log files and the GUI.

If you need to change one or more sensors, you can do it by editing `sensors.py` class dictionary `self.locations` starting from line 76. Also `plot_log()` - the last function of `sensors.py` - needs to be changed. The relevant section begins from line 277. 

Xsens Device API Linux and Windows Python wheel files with installation instructions are in the `wheels` folder.

Sonic Move project: https://uefconnect.uef.fi/en/group/sonic-move-creative-and-expressive-sonification-of-human-movement/

Minimi and Biodata Sonata: https://minimi.fi/fi_FI/biodatasonaatti-blogi/

Ylen artikkeli: https://yle.fi/a/74-20060177 (Finland's national public broadcasting company article)
