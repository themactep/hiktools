# Hikvision UDP-Kommunikation

English version can be found [here](https://github.com/MatrixEditor/hikvision-sdk-cam/blob/main/doc/udp_eng.md).

## HUI

## getcode

Beschreibung: Mit diesem Befehl wird der Code zurückgegeben, der im Falle eines Passwort-Resets an den _technical-support_ gesendet wird.

    Parameter: 
    - MAC: Mac-Addresse des Senders
    - Uuid: eine zufällige UUID

    Anfrage/Request:
        <Probe>
            <Uuid>%s</Uuid>
            <MAC>%s</MAC>
            <Types>%s</Types>
        </Probe>

    Rückgabe/Response:
        <?xml version="1.0" encoding="UTF-8"?>
        <ProbeMatch>
            <Uuid>...</Uuid>
            <MAC>00-00-00-00-00-00</MAC>
            <Types>getcode</Types>
            <Result>success</Result>
            <Code>...</Code>
        </ProbeMatch>

strings from the sadp.dll:

    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setBindList</Types><unbindAll>true</unbindAll><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setBindList</Types><unbindAll>false</unbindAll><Password>%s</Password><DeviceSNList>%s%s</DeviceSNList></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getBindList</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>SetVerificationCode</Types><VerificationCode>%s</VerificationCode><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>SetHCPlatform</Types><HCPlatformEnable>%s</HCPlatformEnable><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>SetMailBox</Types><MailBox>%s</MailBox><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>GUIDReset</Types><GUID>%s</GUID><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>GUIDReset</Types><SyncIPCPassword>true</SyncIPCPassword><GUID>%s</GUID><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getsecurityquestion</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>ExportGUID</Types><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>deviceTypeCustom</Types><DeviceTypeSecretKey>%s</DeviceTypeSecretKey></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>MailReset</Types><Password>%s</Password><SyncIPCPassword>true</SyncIPCPassword></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>reset</Types><Password>%s</Password><Code>%s</Code></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>GetQRcodes</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getcode</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>exchangecode</Types><Code>%s</Code></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>activate</Types><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getencryptstring</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>deviceTypeUnlockCode</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>deviceTypeCustom</Types><DeviceTypeSecretKey>%s</DeviceTypeSecretKey></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>ExportGUID</Types><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>restoreInactive</Types><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setWifiRegion</Types><wifiRegion>%s</wifiRegion><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setWifiRegion</Types><enableWifiEnhancement>%s</enableWifiEnhancement><Password>%s</Password></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><Types>lamp</Types><MAC>%s</MAC><Action>%s</Action></Probe> ['open', 'close']
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><Types>selfCheck</Types><MAC>%s</MAC></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><Types>diskLocate</Types><MAC>%s</MAC></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setChannelDefaultPassword</Types><Password>%s</Password><DefaultPassword>%s</DefaultPassword></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>%s</Types><SSID>%s</SSID><Password>%s</Password><WiFiMode>%s</WiFiMode></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><Types>EHomeEnable</Types><PWErrorParse>true</PWErrorParse><MAC>%s</MAC><Password>%s</Password><DevID>%s</DevID><EHomeKey>%s</EHomeKey></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>getUnbindStatus</Types></Probe>
    # <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>ezvizUnbind</Types><Password>%s</Password></Probe>

long:

 
    <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>AnswerReset</Types><QuestionList><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question>
    <Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question></QuestionList><Password>%s</Password></Probe>


    <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>AnswerReset</Types><SyncIPCPassword>true</SyncIPCPassword><QuestionList><Question><ID>%d</ID><Answer>%s
    </Answer><mark>true</mark></Question><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question></QuestionList>
    <Password>%s</Password></Probe>


    <?xml version="1.0" encoding="utf-8"?><Probe><Uuid>%s</Uuid><MAC>%s</MAC><Types>setsecurityquestion</Types><QuestionList><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question>
    <Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question><Question><ID>%d</ID><Answer>%s</Answer><mark>true</mark></Question></QuestionList><Password>%s</Password></Probe>

~~~
Types:

    + hello
    + Uuid
    + getcode
    + reset
    + MailReset
    + exchangecode
    + activate
    + getencryptstring
    + update
    + deviceTypeUnlockCode
    + deviceTypeCustom
    + ExportGUID
    + getsecurityquestion
    + setsecurityquestion
    + GUIDReset
    + AnswerReset
    + SetHCPlatform
    + SetMailBox
    + GetQRcodes
    + SetVerificationCode
    + getBindList
    + setBindList
    + restoreInactive
    + setWifiRegion
    + lamp
    + selfCheck
    + diskLocate
    + setChannelDefaultPassword
    + wifiParamCfg
    + wifiParamCheck
    + EHomeEnable
    + getUnbindStatus
    + ezvizUnbind
    + inquiry

~~~
Nodes:

    + DeviceType
    + DeviceDescription
    + CommandPort
    + HttpPort
    + MAC
    + Ipv4Address
    + Ipv4SubnetMask
    + Ipv4Gateway
    + Ipv6Address
    + Ipv6Masklen
    + Ipv6Gateway
    + DHCP
    + AnalogChannelNum
    + DigitalChannelNum
    + DSPVersion
    + OEMInfoEncrypt
    + Encrypt
    + ResetAbility
    + DiskNumber
    + Activated
    + PasswordResetAbility
    + SyncIPCPassword
    + PasswordResetModeSecond
    + DetailOEMCode
    + EZVIZCode
    + DeviceLock
    + SupportGUID
    + SupportSecurityQuestion
    + SupportHCPlatform
    + HCPlatformEnable
    + IsModifyVerificationCode
    + Salt
    + SupportBind
    + MaxBindNum
    + SupportRestoreInactive

Options:

    - supportwifiRegion (maybe upper 's') -> {default, china, europe, nothAmerica (where's the 'r'?), japan, world}
    - currentwifiRegion
    - supportWifiEnhancement
    - enableWifiEnhancement
    - Licensed
    - SystemMode {singleControl, doubleControl, singleCluster, doubleCluster}
    - ControllerType {'A', 'B'}
    - SupportChannelDefaultPassword
    - SupportMailBox
    - SpecificDeviceType {Neutral, HIK}
    - supportSSIDAndPasswordCfg
    - EHomeVer
    - DHCPAbility
    - SecurityMode {standard, high-A, high-B, custom}
    - SDKServerStatus
    - SDKOverTLSServerStatus
