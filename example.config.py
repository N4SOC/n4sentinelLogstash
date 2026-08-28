envName = ""
appId = ""
appSecret = ""
tenantId = ""
dce = ""


collectors = [
    {
        "name": "paloalto",
        "port": "9514",
        "proto": "udp",
        "dcrId": "",
        "stream": "paloalto",
    },
    {
        "name": "fortigate",
        "port": "6514",
        "proto": "tcp",
        "dcrId": "",
        "stream": "Custom-SOC_Testing_Ingestion_Forti_CL",
    },
]
