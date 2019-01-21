# TuyaDevice Power Monitor Device Status Schema #


```json
[
    {
        "code": "switch_on",
        "desc": "",
        "iconname": "icon-dp_power3",
        "id": 1,
        "mode": "rw",
        "name": "开关",
        "property": {
            "type": "bool"
        },
        "type": "obj"
    },
    {
        "code": "countdown",
        "desc": "",
        "id": 2,
        "mode": "rw",
        "name": "倒计时",
        "passive": true,
        "property": {
            "max": 86400,
            "min": 0,
            "scale": 0,
            "step": 1,
            "type": "value",
            "unit": "秒"
        },
        "type": "obj"
    },
    {
        "code": "add_ele",
        "desc": "上报的为放大100倍之后的值，即上报56，实际值为0.56度",
        "id": 3,
        "mode": "ro",
        "name": "增加电量",
        "property": {
            "max": 500000,
            "min": 0,
            "scale": 3,
            "step": 100,
            "type": "value",
            "unit": "度"
        },
        "type": "obj"
    },
    {
        "code": "cur_current",
        "desc": "",
        "id": 4,
        "mode": "ro",
        "name": "当前电流",
        "property": {
            "max": 30000,
            "min": 0,
            "scale": 0,
            "step": 1,
            "type": "value",
            "unit": "mA"
        },
        "type": "obj"
    },
    {
        "code": "cur_power",
        "desc": "",
        "id": 5,
        "mode": "ro",
        "name": "当前功率",
        "property": {
            "max": 50000,
            "min": 0,
            "scale": 0,
            "step": 1,
            "type": "value",
            "unit": "W"
        },
        "type": "obj"
    },
    {
        "code": "cur_voltage",
        "desc": "",
        "id": 6,
        "mode": "ro",
        "name": "当前电压",
        "property": {
            "max": 2500,
            "min": 0,
            "scale": 0,
            "step": 1,
            "type": "value",
            "unit": "V"
        },
        "type": "obj"
    }
]
```
