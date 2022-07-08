version = "2.8"
getver = version.split('.')

debug = 0
startGUI = 1
retrymax = 3
phonefilter = '()-. '

sfAgentlink = "https://raptor--icagentconsole.na137.visual.force.com/apex/inContactAgentConsole?sfdcIFrameOrigin=https%3A%2F%2Fraptor.my.salesforce.com&nonce=0085020de1e69e334cf89a2290ca9835a175c47b55666a1f9bfa84e6dc91ed35&isAdapterUrl=true"
caseLink = "https://raptor.my.salesforce.com/500?fcf=00BU0000004L8j3"

#globals
driver = None
B1 = None
B2 = None
B3 = None
action = None
addminutes = 2
retry = 0
config = None
autorun = None
root = None
autoChk = None
isStopped = 0
preStage = 0
finished = False
bgc = "#262a2e"
bgaccent = "#56595d"
fgc = "white"
stage = 0
result = None
commitscreated = 0

