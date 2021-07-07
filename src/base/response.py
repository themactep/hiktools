'''
**********************[SDK]****************************
*  Please look at websdk.js in your browser for all   *
*  related commands that can be used without any      *
*  permission (the websdk.js file)                    *
*******************************************************

@author MatrixEditor
'''
from base.core import parse

class XmlResponse(object):
    def __init__(self, statusCode: int, statusString: str, subStatusCode: str, 
                 version="2.0", requestUrl="(variable)") -> None:
        super().__init__()

        self.requestUrl = requestUrl
        self.statusCode = statusCode
        self.statusString = statusString
        self.subStatusCode = subStatusCode
        self.version = version

    def toXml(self) -> str:
        return f"""
        <ResponseStatus version="{self.version}">
            <requestURL>{self.requestUrl}</requestURL>
            <statusCode>{self.statusCode}</statusCode>
            <statusString>{self.statusString}</statusString>
            <subStatusCode>{self.subStatusCode}</subStatusCode>
        </ResponseStatus>
        """

def fromstring(text: str) -> XmlResponse:
    if text != None and text != "":
        elem = parse(text)
        if elem.tag == "ResponseStatus":
            return XmlResponse(requestUrl=elem[0], statusCode=elem[1], statusString=elem[2],
            subStatusCode="---" if elem[3] == None else elem[3])
    raise ValueError("Error: cannot read input")


knwonResonses = {
    None,#0
    None,#1
    None,#2
    XmlResponse(3, "Device Error", "deviceError"),
    XmlResponse(4, "Invalid Operation", "invalidOperation | notSupport | methodNotAllowed"),
    None,
    XmlResponse(6, "Invalid XML Content", "badXmlContent")
}