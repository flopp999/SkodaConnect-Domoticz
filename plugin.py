# SkodaConnect Python Plugin
#
# Author: flopp999
#
"""
<plugin key="SkodaConnect" name="SkodaConnect 0.25" author="flopp999" version="0.25" wikilink="https://github.com/flopp999/SkodaConnect-Domoticz" externallink="https://www.skoda-connect.com">
    <description>
        <h3>Support me with a coffee &<a href="https://www.buymeacoffee.com/flopp999">https://www.buymeacoffee.com/flopp999</a></h3>
        <h3>Thanks to lendy007 https://github.com/lendy007</h3>
        <br/>
        <h3>Configuration</h3>
        <h4>Use same email address and password as you do for https://www.skoda-connect.com/</h4>
    </description>
    <params>
        <param field="Mode1" label="Email" width="320px" required="true" default="username@domain.com"/>
        <param field="Mode2" label="Password" password="true" width="350px" required="true" default="Password"/>
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
import traceback, sys

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

        try:
            await connection.doLogin()
            await connection.get_vehicles()
            for vehicle in connection.vehicles:
                dashboard = vehicle.dashboard(mutable=True)
            data = await connection.getCharging(vehicle.vin)
            for key, value in data.items():
                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
                    UpdateDevice(name, 0, data)
            Domoticz.Log("Car Updated")
#        else:
#            Domoticz.Error("Something went wrong when access Skoda API")
#            return False
        except:
#            Domoticz.Log(str(traceback.format_exc()))
#            Domoticz.Log(str(sys.exc_info()[0]))
            Domoticz.Log("Something went wrong when access Skoda API")
#            Domoticz.Log(str(e))

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
        self.Count = 8

        if "Skoda" not in Images:
           Domoticz.Image("Skoda.zip").Create()
        self.ImageID = Images["Skoda"].ID

    def onHeartbeat(self):
        WriteDebug("===heartbeat===")
        self.Count += 1
        if self.Count >= 5:
            if CheckInternet() == True:
                asyncio.run(main())
            self.Count = 0


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def UpdateDevice(name, nValue, sValue):
    Pass = True

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
            Domoticz.Error("Please create an issue at github and write this error. Missing connectionState - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing lockState - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing state - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing chargeMode - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing chargingType - "+str(sValue))
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
    elif name == "chargingSettings":
        name = "Charge Settings"
        if sValue == "DEFAULT":
            sValue = 0
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing chargingSettings - "+str(sValue))
            sValue = -1
        Description = ""
        ID = 11
        unit = "?"
    elif name == "maxChargeCurrentAc":
#        name = ""
#        sValue = sValue/60.0
        if sValue == "Maximum":
            sValue = 1
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing maxChargeCurrentAc - "+str(sValue))
            sValue = -1
        Description = ""
        ID = 12
        unit = ""
    elif name == "autoUnlockPlugWhenCharged":
#        name = ""
#        sValue = sValue/60.0
        if sValue == "Permanent":
            sValue = 0
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing connectionState - "+str(sValue))
            sValue = -1
        Description = ""
        ID = 13
        unit = ""
    elif name == "targetStateOfChargeInPercent":
#        name = ""
#        sValue = sValue/60.0
        Description = ""
        ID = 14
        unit = "%"
    else:
        Domoticz.Error("Missing device: "+name)
        Pass = False

#    if name == "dsfgsdfg":
#        ID = 14
#        sValue = sValue.replace('Z', '')
#        sValue = sValue.replace('T', ' ')
#        sValue = sValue + " UTC"
#        unit = ""
#    Devices[ID].Update(nValue, str(sValue), Name=name, Description=Description)

#    Domoticz.Log(str(ID))
#    Domoticz.Log(str(Devices))

    if Pass:
        if ID in Devices:
            if (Devices[ID].sValue != str(sValue)):
                if ID == 1:
                    Range = Devices[9].sValue
                    Devices[9].Update(nValue, str(Range), BatteryLevel=sValue)
                Devices[ID].Update(nValue, str(sValue))

        if (ID not in Devices) and Pass == 1:
            if sValue == "-32768":
                Used = 0
            else:
                Used = 1

            Domoticz.Device(Name=name, Unit=ID, Image=(_plugin.ImageID), TypeName="Custom", Options={"Custom": "0;"+unit}, Used=Used, Description=Description).Create()


def CheckInternet():
    WriteDebug("Entered CheckInternet")
    try:
        WriteDebug("Ping")
        requests.get(url='https://msg.volkswagen.de', timeout=2)
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
