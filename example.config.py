envName = ""
appId = ""
appSecret = ""
tenantId = ""
dce = ""
dcrId = ""

collectors = [
    {"name": "paloalto", "port": "9514", "proto": "udp", "stream": "paloalto"},
    {"name": "fortigate", "port": "6514", "proto": "tcp", "stream": "Custom-SOC_Testing_Ingestion_Forti_CL"},
]
