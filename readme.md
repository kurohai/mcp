# mcp #

[Master Control Program]

## Overview ##


## TODO ##


### General ###

1. Move all home APIs to new flask-restplus layout


### mcp Outlet API ###

1. Move device scan results to SQLAlchemy / SQLite
1. Get last scan results from DB
1. Get device MAC Addresses and names from DB


### Kurocast ###

1. Move to flask-restplus API
1. Get devices from MCP Outlet DB
1. Get devices from nmap scans
1. Scan network for cast devices on schedule in background
1. Add manual nmap scan endpoint to API
1. Add more control to web UI


### HDMI Controller ###

1. Move to flask-restplus API
1. Edit template for iframe use
    1. Remove template header
    1. Only port table in one view with it's own view
    1. Maybe add more to UI for dashboard


[Master Control Program]: https://github.com/kurohai/mcp
