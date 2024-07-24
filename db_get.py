#!/usr/bin/python3
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages/')
import socket
import cgi
from pymongo import MongoClient
from pymongo import ASCENDING
from pymongo import DESCENDING
from bson.json_util import dumps, loads
from bson import decode
import os

Title="NSX Solution Demo: フルーツ在庫表示"
MongoHost = os.environ['MONGO_HOST'] 
MongoPort = os.environ['MONGO_PORT']

def get_host_info():
# Get Socket to investigate Pod address and hostname
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    h = socket.gethostname()
    return ip, h

def startup_db_client():
    myclient = MongoClient("mongodb://mongoadmin:password@" + MongoHost + ":" + MongoPort + "/?authSource=fruitsdb&authMechanism=SCRAM-SHA-1")
    return myclient

def shutdown_db_client(myclient):
    myclient.close()

def find_from(mycol):
    if (data := mycol.find()) is not None:
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

# Check if Get query type is HTML or JSON, and get host ip nad hostname
form = cgi.FieldStorage()
query = form.getvalue("query")
ip, h = get_host_info()

#  connect to mongodb and get fruits table data
myclient = startup_db_client()

mydb   = myclient["fruitsdb"]
mycol  = mydb["fruits"]
cursor = mycol.find(projection={'_id':0, 'id':1, 'name':1, 'production':1, 'quantity':1}, sort=[('id',ASCENDING)])

# Output html or json data based on query option
if "query" not in form or query == "html":

    color_seed = int(ip.split('.')[3]) % 6
    if color_seed == 0:
        color = '#FFA0A0'  # red
    if color_seed == 1:
        color = '#FFFFA0'  # yellow
    if color_seed == 2:
        color = '#A0FFA0'  # green
    if color_seed == 3:
        color = '#A0FFFF'  # bluegreen
    if color_seed == 4:
        color = '#A0A0FF'  # blue
    if color_seed == 5:
        color = '#FFA0FF'  # purple
    
    print("Content-Type: text/html;")
    print("")
    print("<!DOCTYPE html>")
    print("<html lang='ja'>")
    print("<head>")
    print("    <meta charset='utf-8'>")
    print("    <title>%s</title>" % ip)
    print("</head>")
    print("<body>")
    print("    <h1>%s</h1>" % Title)
    print("    <table border=\"0\">")
    print("        <tbody align=\"left\" style=\"background-color:%s;\">" % color)
    print("            <tr>")
    print("                <th>IP address</th>")
    print("                <th>%s</th>" % ip)
    print("            </tr>")
    print("            <tr>")
    print("                <th>Hostname</th>")
    print("                <th>%s</th>" % h)
    print("            </tr>")
    print("            <tr>")
    print("                <th>DB Info</th>")
    print("                <th>%s:%s</th>" % (MongoHost, MongoPort) )
    print("            </tr>")
    print("        </tbody>")
    print("    </table>")
    print("    <table border=\"0\" width=\"640\">")
    print("        <caption>Query Result</caption>")
    print("        <thead style=\"background-color:#E0E0F0;\">")
    print("            <tr>")
    print("                <th>Name</th>")
    print("                <th>Production</th>")
    print("                <th>Quantity</th>")
    print("            </tr>")
    print("        </thead>")
    print("        <tbody align=\"left\" style=\"background-color:#F0F0F0;\">")
    try:
        for x in cursor:
            print("            <tr>")
            print("                <th>%s</th>" % x["name"])
            print("                <th>%s</th>" % x["production"])
            print("                <th>%s</th>" % x["quantity"])
            print("            </tr>")
    except:
            print("            <tr>")
            print("                <th><font color=\"red\">DB Read Error</font></th>")
            print("                <th></th>")
            print("                <th></th>")
            print("            </tr>")
    print("        </tbody>")
    print("    </table>")
    print("</body>")
    print("</html>")

elif query == "json":
    res = {"name":Title, "address":ip, "hostname":h, "db_info":MongoHost + ":" + MongoPort}
    print("Content-Type: text/json;")
    print("")
    res["result"] = []
    try:
        for x in cursor:
            res["result"].append(x)
    except:
        res["result"].append({"error":"DB Read Error"})
    print(dumps(res, indent=2, ensure_ascii=False))

else:
    raise Exception("Invalid Parameter: query=" + query)

# shutdown db connection
shutdown_db_client(myclient)

# end script