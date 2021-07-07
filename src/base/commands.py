from ..base.response import knwonResonses
'''
**********************[SDK]****************************
*  Please look at websdk.js in your browser for all   *
*  related commands that can be used without any      *
*  permission (the websdk.js file)                    *
*******************************************************

@author MatrixEditor
'''

PARAM_OPTION_CHANNEL = 'channel'
PARAM_OPTION_INTERFACE = 'inteerface'

EMPTY_RESONSE_LIST ="?? -> empty resonse list"

sdk = {
    ["/SDK/language", "Returns the current language."],
    ["/SDK/activateStatus", "Returns 'true' if activated, otherwise 'false'."],
    ["/SDK/capabilities", "Returns the http-capabilities of this device"],
}

other = {
    ["/doc/i18n/Languages.json", "Returns the implemented languages."],
    ["/doc/i18n/en/Common.json", "Returns the common label-names in english."]
    ["/doc/i18n/en/Login.json", "Returns the default label-names in english for the login-section."]
}

# the '#' as a parameter
isapi = {
    ["/ISAPI/ContentMgmt/InputProxy/channels", "404", knwonResonses[4]],
    ["/ISAPI/ContentMgmt/InputProxy/channels/#", "404", knwonResonses[4]],
    ["/ISAPI/ContentMgmt/StreamingProxy/channels", "404", knwonResonses[4]],
    ["/ISAPI/ContentMgmt/ZeroVideo/channels", "404", knwonResonses[4]],
    ["/ISAPI/Event/capabilities", "The event-config"],
    ["/ISAPI/Event/notification/Streaming/#01", "404", knwonResonses[4]],
    ["/ISAPI/Image/channels", "Returns all opened channels and its configuration."],
    ["/ISAPI/Image/channels/#/imageCap", "Returns information about the imageCap of the sepcified channel.", PARAM_OPTION_CHANNEL],
    ["/ISAPI/Image/channels/imageModes", "404", knwonResonses[3]],
    ["/ISAPI/Security/adminAccesses", "Returns a list of open protocols used in a connection."],
    ["/ISAPI/Security/challenge", "TODO: ??"],
    ["/ISAPI/Security/serverCertificate/certificate", "Returns the server certificate."],
    ["/ISAPI/Smart/capabilities", "Returns what smart-technology this device features."],
    ["/ISAPI/Snapshot/channels", "All config-data in a list."],
    ["/ISAPI/Snapshot/channels/#", "The same as '/ISAPI/Snapshot/channels/#/capabilities'", PARAM_OPTION_CHANNEL],
    ["/ISAPI/Snapshot/channels/#/capabilities", "The snapshot channel config", PARAM_OPTION_CHANNEL],
    ["/ISAPI/Streaming/channels", "Returns a list of all channels, that can stream the video output."],
    ["/ISAPI/Streaming/channels/#", "", PARAM_OPTION_CHANNEL],
    ["/ISAPI/Streaming/channels/#/capabilities", "", PARAM_OPTION_CHANNEL],
    ["/ISAPI/System/capabilities", "Shows what interfaces the camera/ device has (xml-format)."],
    ["/ISAPI/System/deviceInfo", "Returns detailed device information"],
    ["/ISAPI/System/IO/inputs", EMPTY_RESONSE_LIST],
    ["/ISAPI/System/IO/outputs", EMPTY_RESONSE_LIST],
    ["/ISAPI/System/Network/interfaces/#", "Returns network-interface related information", PARAM_OPTION_INTERFACE],
    ["/ISAPI/System/Network/interfaces/2/WPS/devicePinCode", "Returns the WPA device-pin code"]
    ["/ISAPI/System/TwoWayAudio/channels", "Returns the list of audio channels."],#
    ["/ISAPI/System/TwoWayAudio/channels/1/", "Audio channel info"],
    ["/ISAPI/System/Video/inputs/channels", "Returns the open video-channels as a list."],
    ["/ISAPI/System/Video/inputs/channels/#", "Returns config-data for the sepcified video-channel.", PARAM_OPTION_CHANNEL],
    ["/ISAPI/System/Video/inputs/channels/#/motionDetection/capabilities", "The motion detection options.", PARAM_OPTION_CHANNEL],
    ["/ISAPI/System/Video/inputs/channels/#/overlays", "Returns the video-overlays for the specified channel.", PARAM_OPTION_CHANNEL],
    ["/ISAPI/System/Video/inputs/channels/#/overlays/capabilities", "Returns the config-data for displaying a channel-stream", PARAM_OPTION_CHANNEL],
    ["/ISAPI/ContentMgmt/Storage", "Returns disk-info."]
}

#/ISAPI/System/updateFirmware
def requiresAuth(name: str) -> bool:
     return name == "isapi"
    