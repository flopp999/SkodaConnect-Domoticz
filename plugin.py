# SkodaConnect Python Plugin
#
# Author: flopp999
#
"""
<plugin key="SkodaConnect" name="SkodaConnect 0.19" author="flopp999" version="0.19" wikilink="https://github.com/flopp999/SkodaConnect-Domoticz" externallink="https://www.skoda-connect.com">
    <description>
        <h2>Support me with a coffee &<a href="https://www.buymeacoffee.com/flopp999">https://www.buymeacoffee.com/flopp999</a></h2><br/>
        <h2>or use my Tibber link &<a href="https://tibber.com/se/invite/8af85f51">https://tibber.com/se/invite/8af85f51</a></h2><br/>
        <h3>Categories that will be fetched</h3>
        <ul style="list-style-type:square">
            <li>...</li>
        </ul>
        <h3>Configuration</h3>
        <h2>Use same email address and password as you do for https://www.skoda-connect.com/</h2>
    </description>
    <params>
        <param field="Mode1" label="Email" width="320px" required="true" default="username@domain.com"/>
        <param field="Mode2" label="Password" width="350px" required="true" default="Password"/>
        <param field="Mode6" label="Debug to file (SkodaConnect.log)" width="70px">
            <options>
                <option label="Yes" value="Yes" />
                <option label="No" value="No" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz

try:
    from aiohttp import ClientSession
except ModuleNotFoundError:
    Package = False

try:
    from skodaconnect import Connection
except ModuleNotFoundError:
    Package = False

try:
    import requests, json, os, logging, asyncio
except ImportError as e:
    Package = False

try:
    from logging.handlers import RotatingFileHandler
except ImportError as e:
    Package = False

try:
    from datetime import datetime
except ImportError as e:
    Package = False

dir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger("SkodaConnect")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(dir+'/SkodaConnect.log', maxBytes=1000000, backupCount=5)
logger.addHandler(handler)


async def main():
    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        connection = Connection(session, _plugin.Email, _plugin.Password, False)
        WriteDebug("===login start===")
        await connection.doLogin()
        WriteDebug("===login done===")
        for vehicle in connection.vehicles:
            dashboard = vehicle.dashboard(mutable=True)
        data = await connection.getCharging(vehicle.vin)
        for key, value in data.items():
            for name, data in value.items():
                Domoticz.Log(str(name))
                Domoticz.Log(str(data))
                UpdateDevice(name, 0, data)

    WriteDebug("===main done===")


class BasePlugin:
    enabled = False

    def __init__(self):
        return


    def onStart(self):
        WriteDebug("===onStart===")
        self.Email = Parameters["Mode1"]
        self.Password = Parameters["Mode2"]
        if len(self.Email) < 5:
            Domoticz.Log("Email too short")
            WriteDebug("Email too short")

        if len(self.Password) < 4:
            Domoticz.Log("Password too short")
            WriteDebug("Password too short")
        self.Count = 5

        if "Skoda" not in Images:
           Domoticz.Image("Skoda.zip").Create()
        self.ImageID = Images["Skoda"].ID

    def onHeartbeat(self):
        WriteDebug("===heartbeat===")
        self.Count += 1
        if self.Count == 6:
            if CheckInternet() == True:
                asyncio.run(main())
            self.Count = 0


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def UpdateDevice(name, nValue, sValue):
    if name == "stateOfChargeInPercent":
        name = "Battery level"
        Description = ""
        ID = 1
        unit = "%"
    elif name == "connectionState":
        name = "Cable connected"
        if sValue == "Disconnected":
            sValue = 0
        elif sValue == "Connected":
            sValue = 1
        else:
            sValue = -1
        Description = "0 = Disconnected\n1 = Connected"
        ID = 2
        unit = ""
    elif name == "lockState":
        name = "Cable locked"
        if sValue == "Unlocked":
            sValue = 0
        elif sValue == "Locked":
            sValue = 1
        else:
            sValue = -1
        Description = "0 = Unlocked\n1 = Locked"
        ID = 3
        unit = ""
    elif name == "state":
        name = "Charge"
        if sValue == "ReadyForCharging":
            sValue = 0
        elif sValue == "Charging":
            sValue = 1
        elif sValue == "Error":
            sValue = 2
        elif sValue == "Conservation":
            sValue = 3
        else:
            sValue = -1
        Description = "0 = Ready to charge\n1 = Charging"
        ID = 4
        unit = ""
    elif name == "chargeMode":
        name = "Charge mode"
        if sValue == "MANUAL":
            sValue = 1
        elif sValue == "TIMER":
            sValue = 2
        else:
            sValue = -1
        Description = "1 = Manuel\n2 = Auto\n-1 = Unknown"
        ID = 5
        unit = ""
    elif name == "chargingPowerInWatts":
        name = "Charging power"
        sValue = sValue/1000.0
        Description = ""
        ID = 6
        unit = "kW"
    elif name == "chargingRateInKilometersPerHour":
        name = "Charging rate"
        Description = ""
        ID = 7
        unit = "km/h"
    elif name == "chargingType":
        name = "Charging type"
        if sValue == "Invalid":
            sValue = 0
        elif sValue == "Ac":
            sValue = 1
        elif sValue == "Dc":
            sValue = 2
        else:
            sValue = -1
        Description = "0 = Unknown\n1 = AC\n2 = DC"
        ID = 8
        unit = ""
    elif name == "cruisingRangeElectricInMeters":
        name = "Range"
        sValue = sValue/1000.0
        Description = ""
        ID = 9
        unit = "km"
    elif name == "remainingToCompleteInSeconds":
        name = "Remaining to complete"
        sValue = sValue/60.0
        Description = ""
        ID = 10
        unit = "minutes"

#    if name == "dsfgsdfg":
#        ID = 14
#        sValue = sValue.replace('Z', '')
#        sValue = sValue.replace('T', ' ')
#        sValue = sValue + " UTC"
#        unit = ""
#    Devices[ID].Update(nValue, str(sValue), Name=name, Description=Description)

    if (ID in Devices):
        if (Devices[ID].sValue != str(sValue)):
            if ID == 1:
                Range = Devices[9].sValue
                Devices[9].Update(nValue, str(Range), BatteryLevel=sValue)
            Devices[ID].Update(nValue, str(sValue))

    if (ID not in Devices):
        if sValue == "-32768":
            Used = 0
        else:
            Used = 1

        Domoticz.Device(Name=name, Unit=ID, Image=(_plugin.ImageID), TypeName="Custom", Options={"Custom": "0;"+unit}, Used=Used, Description=Description).Create()


def CheckInternet():
    WriteDebug("Entered CheckInternet")
    try:
        WriteDebug("Ping")
        requests.get(url='https://api.easee.cloud/', timeout=2)
        WriteDebug("Internet is OK")
        return True
    except:
        WriteDebug("Internet is not available")
        return False


def WriteDebug(text):
    if Parameters["Mode6"] == "Yes":
        timenow = (datetime.now())
        logger.info(str(timenow)+" "+text)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()


    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
