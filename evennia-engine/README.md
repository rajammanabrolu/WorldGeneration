## Directory Navigation

### graph2world

This directory contains all of the files needed to turn normal .dot graph files into code which Evennia can understand. This includes some basic parsing with the help of mxGraph as well as some minor pre-processing which give the engine some flexibility.

### evennia

The game worlds created in this project utilize standard features of the Evennia engine. However, the flow of our user study did not entirely mesh with the normal Evennia account setup process, so some slight changes were made to the core framework to handle dynamic anonymous loading into specified regions.

### engine

This is the folder generated from the original `evennia --init` command. See the original [Evennia documentation](https://github.com/evennia/evennia/wiki) for more information. Changes here include custom character attributes for tracking exploration and changes to the home page.
