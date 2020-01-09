#####################################################################################################
#            Script for convert export file (XML) from Dude to Zabbix Monitoring software           #
#   The request info are putting XML file in input folder and change filename to name of your XML   #
# Result: when procedere is finished, find zabbix file export in OUTPUT folder with the same name   #
# Developed by ARMAN EBRAHIMI MEHR iman.ebrahimimehr@polito.it OR https://github.com/giorgioarman)  #
#####################################################################################################
import datetime
import copy
import xml.etree.ElementTree as ET
filename = 'ivrea.xml'

# Reading Zabbix sample
treeZabbix = ET.parse('zbx_sample.xml')
rootZabbix = treeZabbix.getroot()
rootZabbix.find("./maps/map/name").text = filename.split('.')[0]
rootZabbix.find("./date").text = datetime.datetime.now().isoformat()
zElements = rootZabbix.find("./maps/map/selements")
zElementSample = None
for item in zElements:
    zElementSample = item
    zElements.remove(item)

zLinks = rootZabbix.find("./maps/map/links")
zLinkSample = None
print(len(zLinks))
for item in zLinks:
    zLinkSample = item
    zLinks.remove(item)

# Reading Dude XML
treeDude = ET.parse('input/' + filename)
rootDude = treeDude.getroot()
networkMapDude = rootDude.findall("NetworkMapElement")

# create link element
linkDude = rootDude.findall("Link")
for child in rootDude.iter('Link'):
    netMap_id = child.find('netMapElementID').text
    for map in networkMapDude:
        if map.find('sys-id').text == netMap_id:
            linkFrom = map.find('linkFrom').text
            linkTo = map.find('linkTo').text
            linkFrom = str(int(linkFrom) - 1)
            linkTo = str(int(linkTo) - 1)
            newLink = copy.deepcopy(zLinkSample)
            newLink.find("selementid1").text = linkFrom
            newLink.find("selementid2").text = linkTo
            zLinks.append(newLink)
            break


# create device Element
for child in rootDude.iter('Device'):
    sys_id = child.find('sys-id').text
    sys_name = child.find('sys-name').text + "(" + \
               child.find('addresses').text + ") (" + \
               child.find('macs').text + ")"
    for map in networkMapDude:
        if map.find('itemID') != None:
            if map.find('itemID').text == sys_id:
                sys_X = map.find('itemX').text
                sys_Y = map.find('itemY').text
                networkMapDude.remove(map)
                break
        else:
            networkMapDude.remove(map)

    newElement = copy.deepcopy(zElementSample)
    newElement.find("label").text = sys_name
    newElement.find("selementid").text = sys_id
    newElement.find("x").text = sys_X
    newElement.find("y").text = sys_Y
    zElements.append(newElement)

# to remove the sample element
for zz in zElements:
    if zz.find('selementid').text == str(3):
        zElements.remove(zz)
        break
for ll in zLinks:
    if ll.find('selementid1').text == str(3):
        zLinks.remove(ll)

# CREATE XML FILE
treeZabbix.write("output/" + filename)
