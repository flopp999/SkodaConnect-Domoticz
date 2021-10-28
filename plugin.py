# SkodaConnect Python Plugin
#
# Author: flopp999
#
"""
<plugin key="SkodaConnect" name="SkodaConnect 0.26" author="flopp999" version="0.26" wikilink="https://github.com/flopp999/SkodaConnect-Domoticz" externallink="https://www.skoda-connect.com">
    <description>
        <h3>Support me with a coffee &<a href="https://www.buymeacoffee.com/flopp999">https://www.buymeacoffee.com/flopp999</a></h3>
        <h3>Thanks to lendy007 https://github.com/lendy007</h3>
        <br/>
        <h3>Configuration</h3>
        <h4>Use same email address and password as you do for https://www.skoda-connect.com/</h4>
    </description>
    <params>
        <param field="Mode1" label="Email" width="320px" required="true" default="username@domain.com"/>
        <param field="Mode2" label="Password" password="true" width="320px" required="true" default="Password"/>
        <param field="Mode3" label="Netto battery kWh" width="70px" required="true" default="50"/>
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
#            Domoticz.Log(str(type(connection)))
            for vehicle in connection.vehicles:
                dashboard = vehicle.dashboard(mutable=True)
#                Domoticz.Log(str(dashboard))
#                for instrument in dashboard.instruments:
#                    Domoticz.Log(str(instrument))
            data = await connection.getCharging(vehicle.vin)
            for key, value in data.items():
                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
                    UpdateDeviceCharge(name, data)
            Domoticz.Log("Car Updated")
#            data = await connection.getTimers(vehicle.vin)
#            Domoticz.Log(str(data))
#            Domoticz.Log(str(type(data)))
#            for key, value in data.items():
#                Domoticz.Log(str(key))
#                Domoticz.Log(str(value))
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getConsentInfo(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getRealCarData(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getHomeRegion(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getOperationList(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getVehicleStatusReport(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getVehicleStatus(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getTripStatistics(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getPosition(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getDeparturetimer(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getClimater(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getCharger(vehicle.vin)
#            Domoticz.Log(str(data))
#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
#            data = await connection.getPreHeater(vehicle.vin)
#            Domoticz.Log(str(data))

#            for key, value in data.items():
#                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
            data = await connection.getAirConditioning(vehicle.vin)
#            Domoticz.Log(str(data))
            for key, value in data.items():
                for name, data in value.items():
#                    Domoticz.Log(str(name))
#                    Domoticz.Log(str(data))
                    UpdateDeviceAirCondition(name, data)
#        else:
#            Domoticz.Error("Something went wrong when access Skoda API")
#            return False
        except:
            Domoticz.Log(str(traceback.format_exc()))
            Domoticz.Log(str(sys.exc_info()[0]))
            Domoticz.Log("Something went wrong when access Skoda API")
#            Domoticz.Log(str(e))

        WriteDebug("===main done===")


class BasePlugin:
    enabled = False

    def __init__(self):
        return


    def onStart(self):
        WriteDebug("===onStart===")
        self.Battery = Parameters["Mode3"]
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
        if self.Count >= 6:
            if CheckInternet() == True:
                asyncio.run(main())
            self.Count = 0


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def UpdateDeviceCharge(name, sValue):
    Pass = True

    if name == "stateOfChargeInPercent":
        name = "Battery level (SOC)"
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
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Unlocked\n1 = Locked"
        ID = 3
        unit = ""
    elif name == "state":
        name = "Charging"
        if sValue == "ReadyForCharging":
            sValue = 0
        elif sValue == "Charging":
            sValue = 1
        elif sValue == "Error":
            sValue = 2
        elif sValue == "Conservation":
            sValue = 3
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
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
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
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
        UpdateDevice(name, sValue, Pass, ID, unit, Description)
        ID = 77
        name = "Charge rate/h %"
        sValue = float(sValue) / int(_plugin.Battery) * 100
        unit = "%/h"


    elif name == "chargingRateInKilometersPerHour":
        name = "Charging rate km/h"
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
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
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
        name = "Charging ready in"
        sValue = sValue/60.0
        Description = ""
        ID = 10
        unit = "minutes"
    elif name == "chargingSettings":
        name = "Charge settings"
        if sValue == "DEFAULT":
            sValue = 0
        elif sValue == "PROFILE":
            sValue = 1
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Default\n1 = Profile"
        ID = 11
        unit = ""
    elif name == "maxChargeCurrentAc":
        name = "Charge max current(AC)"
#        sValue = sValue/60.0
        if sValue == "Maximum":
            sValue = 1
        elif sValue == "Reduced":
            sValue = 0
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Reduced\n1 = Maximum"
        ID = 12
        unit = ""
    elif name == "autoUnlockPlugWhenCharged":
        name = "Cable unlock when charged"
#        sValue = sValue/60.0
        if sValue == "Permanent":
            sValue = 1
        elif sValue == "Off":
            sValue = 0
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = No\n1 = Yes"
        ID = 13
        unit = ""
    elif name == "targetStateOfChargeInPercent":
        name = "Charge battery up to"
#        sValue = sValue/60.0
        Description = ""
        ID = 14
        unit = "%"
    else:
        Domoticz.Error("Missing device: "+name)
        Pass = False

    if Pass:
        UpdateDevice(name, sValue, Pass, ID, unit, Description)

def UpdateDeviceAirCondition(name, sValue):
    Pass = True

    if name == "remainingTimeToReachTargetTemperatureInSeconds":
        name = "Air conditioning remaining time"
        Description = ""
        ID = 20
        sValue = sValue / 60
        unit = "minutes"
    elif name == "state":
        name = "Air conditioning running"
        if sValue == "Off":
            sValue = 0
        elif sValue == "Heating":
            sValue = 1
        elif sValue == "Ventilation":
            sValue = 2
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Off\n1 = Heating"
        ID = 21
        unit = ""
    elif name == "trigger":
        name = "Air conditioning trigger"
        if sValue == "OFF":
            sValue = 0
        elif sValue == "MANUAL":
            sValue = 1
        elif sValue == "TIMER":
            sValue = 2
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Off\n1 = Manual"
        ID = 22
        unit = ""
    elif name == "windowsHeatingStatuses":
        Pass = False
        pass
#        for each in sValue:
#            Domoticz.Log(str(type(each)))
#            Domoticz.Log(str(each["windowLocation"])+str(each["state"]))
#            ID = 23
#            sValue
#        name = ""
#        if sValue == "Disconnected":
#            sValue = 0
#        elif sValue == "Connected":
#            sValue = 1
#        else:
#            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
#            sValue = -1
#        Description = "0 = Disconnected\n1 = Connected"
#        ID = 23
#        unit = ""
    elif name == "seatHeatingSupport":
        Pass = False
        pass
#        Domoticz.Log(str(type(sValue)))
#        for name, data in sValue.items():
#            for a,b in each.items():
#            Domoticz.Log(str(each)+str(data))
#            name = each
#            sValue = data
#        name = ""
#        if sValue == "Disconnected":
#            sValue = 0
#        elif sValue == "Connected":
#            sValue = 1
#        else:
#            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
 #           sValue = -1
 #       Description = "0 = Disconnected\n1 = Connected"
 #       ID = 24
 #       unit = ""
    elif name == "targetTemperatureInKelvin":
        name = "Air conditioning set temperature"
        sValue = sValue - 273.15
        Description = ""
        ID = 25
        unit = "°C"
    elif name == "temperatureConversionTableUsed":
        Pass = False
        pass
#        name = ""
#        if sValue == "CELSIUS_KELVIN":
#            sValue = 0
#        elif sValue == "Connected":
#            sValue = 1
#        else:
#            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
#            sValue = -1
#        Description = "0 = CELSIUS_KELVIN\n1 = ?"
#        ID = 26
#        unit = ""
    elif name == "airConditioningAtUnlock":
        name = "Air conditioning at unlock"
        if sValue == False:
            sValue = 0
        elif sValue == True:
            sValue = 1
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = No\n1 = Yes"
        ID = 27
        unit = ""
    elif name == "windowHeatingEnabled":
#        name = ""
        if sValue == False:
            sValue = 0
        elif sValue == True:
            sValue = 1
        else:
            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = No\n1 = Yes"
        ID = 28
        unit = ""
    elif name == "zonesSettings":
#        name = ""
        if sValue == "Disconnected":
            sValue = 0
        elif sValue == "Connected":
            sValue = 1
        else:
#            Domoticz.Error("Please create an issue at github and write this error. Missing "+str(name)+" - "+str(sValue))
            sValue = -1
        Description = "0 = Disconnected\n1 = Connected"
        ID = 29
        unit = ""
    else:
        Domoticz.Error("Missing device: "+name)
        Pass = False
    if Pass:
        UpdateDevice(name, sValue, Pass, ID, unit, Description)

#    if name == "dsfgsdfg":
#        ID = 14
#        sValue = sValue.replace('Z', '')
#        sValue = sValue.replace('T', ' ')
#        sValue = sValue + " UTC"
#        unit = ""
#    Devices[ID].Update(nValue, str(sValue), Name=name, Description=Description)

#    Domoticz.Log(str(ID))
#    Domoticz.Log(str(Devices))

def UpdateDevice(name, sValue, Pass, ID, unit, Description):
    if Pass:
        if ID in Devices:
            if (Devices[ID].sValue != str(sValue)):
                if ID == 1:
                    Range = Devices[9].sValue
                    Devices[9].Update(0, str(Range), BatteryLevel=sValue)
                Devices[ID].Update(0, str(sValue))

        if (ID not in Devices) and Pass == 1:
            if sValue == "-32768":
                Used = 0
            else:
                Used = 1

            Domoticz.Device(Name=name, Unit=ID, Image=(_plugin.ImageID), TypeName="Custom", Options={"Custom": "0;"+unit}, Used=Used, Description=Description).Create()
            Devices[ID].Update(0, str(sValue), Name=name)


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
