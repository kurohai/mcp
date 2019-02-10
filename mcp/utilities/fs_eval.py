#!/usr/bin/env python


import fs
from pprint import pprint


# from fs import smbfs, open_fs



def main():

    mcp_01_d = fs.open_fs(
        # 'mcp-01.kurohai.local',
        'smb://MCP-01\\evant:M3rmaidPuss@10.0.0.2:139/d',
        # username='MCP-01\\evant',
        # passwd='M3rmaidPuss',
    )

    pprint(dir(mcp_01_d))
