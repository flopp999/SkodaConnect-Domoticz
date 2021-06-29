# SkodaConnect Python Plugin
#
# Author: flopp999
#
"""
<plugin key="SkodaConnect" name="SkodaConnect 0.1" author="flopp999" version="0.1" wikilink="https://github.com/flopp999/SkodaConnect-Domoticz" externallink="https://www.skoda-connect.com">
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
        if await connection.doLogin():
            instruments = set()
            for vehicle in connection.vehicles:
                dashboard = vehicle.dashboard(mutable=True)
                for instrument in dashboard.instruments:
                    Domoticz.Log(str(instrument.attr))
                    Domoticz.Log(str(instrument.state))
                    UpdateDevice(instrument.attr, 0, instrument.state)
        else:
            return False

        data = await connection.getCharging(vehicle.vin)
        for charge,value in data["charging"].items():
            Domoticz.Log(str(charge))
            Domoticz.Log(str(value))
            UpdateDevice(charge, 0, value)


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


    def onHeartbeat(self):
        Domoticz.Log("HeartBeat")
        self.Count += 1
        if self.Count == 6:
            asyncio.run(main())
            self.Count = 0


global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def UpdateDevice(name, nValue, sValue):

    if name == "charging":
        ID = 1
        unit = ""
    if name == "battery_level":
        ID = 2
        unit = "%"
    if name == "charging_time_left":
        ID = 3
        unit = ""
    if name == "electric_range":
        ID = 4
        unit = "km"
    if name == "external_power":
        ID = 5
        unit = ""
    if name == "charging_cable_connected":
        ID = 6
        unit = ""
    if name == "charging_cable_locked":
        ID = 7
        unit = ""
    if name == "state":
        ID = 8
        unit = ""
    if name == "remainingToCompleteInSeconds":
        unit = ""
        ID = 9
    if name == "chargingPowerInWatts":
        ID = 10
        unit = ""
    if name == "chargingRateInKilometersPerHour":
        ID = 11
        unit = ""
    if name == "chargingType":
        ID = 12
        unit = ""
    if name == "chargeMode":
        ID = 13
        unit = ""
    if name == "latestPulse":
        ID = 14
        sValue = sValue.replace('Z', '')
        sValue = sValue.replace('T', ' ')
        sValue = sValue + " UTC"
        unit = ""
    if name == "chargerFirmware":
        ID = 15
        unit = ""
    if name == "latestFirmware":
        ID = 16
        unit = ""
    if name == "voltage":
        ID = 17
        unit = "Volt"
    if name == "chargerRAT":
        ID = 18
        unit = ""
    if name == "lockCablePermanently":
        ID = 19
        unit = ""
    if name == "inCurrentT2":
        ID = 20
        unit = ""
    if name == "inCurrentT3":
        ID = 21
        unit = ""
    if name == "inCurrentT4":
        ID = 22
        unit = ""
    if name == "inCurrentT5":
        ID = 23
        unit = ""
    if name == "outputCurrent":
        ID = 24
        unit = ""
    if name == "isOnline":
        ID = 25
        unit = ""
    if name == "inVoltageT1T2":
        ID = 26
        unit = "Volt"
    if name == "inVoltageT1T3":
        ID = 27
        unit = "Volt"
    if name == "inVoltageT1T4":
        ID = 28
        unit = "Volt"
    if name == "inVoltageT1T5":
        ID = 29
        unit = "Volt"
    if name == "inVoltageT2T3":
        ID = 30
        unit = "Volt"
    if name == "inVoltageT2T4":
        ID = 31
        unit = "Volt"
    if name == "inVoltageT2T5":
        ID = 32
        unit = "Volt"
    if name == "inVoltageT3T4":
        ID = 33
        unit = "Volt"
    if name == "inVoltageT3T5":
        ID = 34
        unit = "Volt"
    if name == "inVoltageT4T5":
        ID = 35
        unit = "Volt"
    if name == "ledMode":
        ID = 36
        unit = ""
    if name == "cableRating":
        ID = 37
        unit = ""
    if name == "dynamicChargerCurrent":
        ID = 38
        unit = ""
    if name == "circuitTotalAllocatedPhaseConductorCurrentL1":
        ID = 39
        unit = ""
    if name == "circuitTotalAllocatedPhaseConductorCurrentL2":
        ID = 40
        unit = ""
    if name == "circuitTotalAllocatedPhaseConductorCurrentL3":
        ID = 41
        unit = ""
    if name == "circuitTotalPhaseConductorCurrentL1":
        ID = 42
        unit = ""
    if name == "circuitTotalPhaseConductorCurrentL2":
        ID = 43
        unit = ""
    if name == "circuitTotalPhaseConductorCurrentL3":
        ID = 44
        unit = ""
    if name == "reasonForNoCurrent":
        ID = 45
        unit = ""
    if name == "wiFiAPEnabled":
        ID = 46
        unit = ""
    if name == "lifetimeEnergy":
        ID = 47
        unit = ""
    if name == "offlineMaxCircuitCurrentP1":
        ID = 48
        unit = ""
    if name == "offlineMaxCircuitCurrentP2":
        ID = 49
        unit = ""
    if name == "offlineMaxCircuitCurrentP3":
        ID = 50
        unit = ""
    if name == "errorCode":
        ID = 51
        unit = ""
    if name == "fatalErrorCode":
        ID = 52
        unit = ""
    if name == "errors":
        ID = 53
        unit = ""
    if name == "isEnabled":
        ID = 54
        unit = ""
    if name == "lockCablePermanently":
        ID = 55
        unit = ""
    if name == "authorizationRequired":
        ID = 56
        unit = ""
    if name == "remoteStartRequired":
        ID = 57
        unit = ""
    if name == "smartButtonEnabled":
        ID = 58
        unit = ""
    if name == "wiFiSSID":
        ID = 59
        unit = ""
    if name == "detectedPowerGridType":
        ID = 60
        unit = ""
    if name == "offlineChargingMode":
        ID = 61
        unit = ""
    if name == "circuitMaxCurrentP1":
        ID = 62
        unit = ""
    if name == "circuitMaxCurrentP2":
        ID = 63
        unit = ""
    if name == "circuitMaxCurrentP3":
        ID = 64
        unit = ""
    if name == "enableIdleCurrent":
        ID = 65
        unit = ""
    if name == "limitToSinglePhaseCharging":
        ID = 66
        unit = ""
    if name == "phaseMode":
        ID = 67
        unit = ""
    if name == "localNodeType":
        ID = 68
        unit = ""
    if name == "localAuthorizationRequired":
        ID = 69
        unit = ""
    if name == "localRadioChannel":
        ID = 70
        unit = ""
    if name == "localShortAddress":
        ID = 71
        unit = ""
    if name == "localParentAddrOrNumOfNodes":
        ID = 72
        unit = ""
    if name == "localPreAuthorizeEnabled":
        ID = 73
        unit = ""
    if name == "localAuthorizeOfflineEnabled":
        ID = 74
        unit = ""
    if name == "allowOfflineTxForUnknownId":
        ID = 75
        unit = ""
    if name == "maxChargerCurrent":
        ID = 76
        unit = ""
    if name == "ledStripBrightness":
        ID = 77
        unit = ""
    if name == "chargingSchedule":
        ID = 78
        unit = ""

    if (ID in Devices):
        if (Devices[ID].sValue != sValue):
            Devices[ID].Update(nValue, str(sValue))

    if (ID not in Devices):
        if sValue == "-32768":
            Used = 0
        else:
            Used = 1
        if ID == 14:
            Domoticz.Device(Name=name, Unit=ID, TypeName="Text", Used=1).Create()

        else:
            Domoticz.Device(Name=name, Unit=ID, TypeName="Custom", Options={"Custom": "0;"+unit}, Used=Used, Description="ParameterID=\nDesignation=").Create()


def CheckInternet():
    WriteDebug("Entered CheckInternet")
    try:
        WriteDebug("Ping")
        requests.get(url='https://api.easee.cloud/', timeout=2)
        WriteDebug("Internet is OK")
        return True
    except:
        if _plugin.GetToken.Connected():
            _plugin.GetToken.Disconnect()
        if _plugin.GetState.Connected():
            _plugin.GetState.Disconnect()
        if _plugin.GetConfig.Connected():
            _plugin.GetConfig.Disconnect()
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
