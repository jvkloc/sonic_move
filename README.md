<b>IN RETROSPECT</b><br> This was my first project after graduating. I wrote it completely solo and the theatre performance I wrote it for featured in Finland's national broadcasting company's article so I got a nice self-confidence boost right from the start. The style is partly 'physicist code': some variables are obscurely named instead of providing clarity to the non-initiated (or myself after a year after writing the program) with descriptive names. Another clear target for refactoring would be the overtly long functions. Most, if not all, of them could be split into nice short ones. Also a file or a few for grouping the helper functions would be a great improvement in addition to adding type hints and grouping constants to their own file(s) for easy manipulation.<br>   

<b>README</b><br>
Python 3.9 program code for Sonic Move project and dance theatre Minimi's Biodata Sonata performance premiering 15.11.2023 in Kuopio City Theatre, Finland. Human motion data recording through Movella (Xsens) motion capture sensors connected to an Awinda USB Dongle or an Awinda Station, sending it to Open Sound Control environment and displaying the live data graphically. It is also possible to run live recordings again by using log files and the GUI.

One or more sensors (ids are hardcoded) can be changed by editing `sensors.py` dictionary `self.locations` starting from line 85 and `plot_log()` function starting from line 226. 

Xsens Device API Linux and Windows Python wheel files with installation instructions are in the `wheels` folder.

Sonic Move project: https://uefconnect.uef.fi/en/group/sonic-move-creative-and-expressive-sonification-of-human-movement/

Minimi and Biodata Sonata: https://minimi.fi/fi_FI/biodatasonaatti-blogi/

Ylen artikkeli: https://yle.fi/a/74-20060177 (an article by Finland's national public broadcasting company)
