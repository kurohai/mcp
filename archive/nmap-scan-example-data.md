# Nmap Scan Example Data #


```json
{
    "nmap": {
        "scanstats": {
            "elapsed": "0.56",
            "timestr": "Thu Dec 13 13:02:44 2018",
            "downhosts": "0",
            "totalhosts": "1",
            "uphosts": "1"
        },
        "scaninfo": {
            "tcp": {
                "services": "6668",
                "method": "syn"
            }
        },
        "command_line": "nmap -oX - -p 6668 -PY 10.0.0.33"
    },
    "scan": {
        "10.0.0.33": {
            "status": {
                "state": "up",
                "reason": "arp-response"
            },
            "hostnames": [
                {
                    "type": "",
                    "name": ""
                }
            ],
            "vendor": {},
            "addresses": {
                "mac": "60:01:94:7E:60:32",
                "ipv4": "10.0.0.33"
            },
            "tcp": {
                "6668": {
                    "product": "",
                    "name": "irc",
                    "extrainfo": "",
                    "state": "open",
                    "cpe": "",
                    "reason": "syn-ack",
                    "version": "",
                    "conf": "3"
                }
            }
        }
    }
}
```
