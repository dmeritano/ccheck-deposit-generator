import logging
import os
import io
import os.path
import shutil
import math
from time import sleep
from datetime import datetime
import pytz
import xml.etree.ElementTree as gfg
from xml.dom import minidom


# import Config
from config import Config

# App Config
cfg = None

app_config = Config({})

# Logging system
logger = logging.getLogger(__name__)


def start(config):
    global app_config
    app_config = config
    st_login = None

    logger.info("Main process started")

    GenerateXML("Catalog.xml")

    logger.info("Main process finished")


def GenerateXML(fileName):

    root = gfg.Element("content")
    root.set("xmlns:ns2", "http://xml.ipsa.es/atril/contentSchema")

    # Header
    tag_aux = get_header()
    root.append(tag_aux)

    # Info lote
    tag_aux = get_info_lote_aggregate(20240827, 3, 1)
    root.append(tag_aux)

    # Boleta virtual
    tag_aux = get_boleta_virtual_aggregate("391000937725953")
    root.append(tag_aux)

    # Pretty output
    pretty_xml = minidom.parseString(
        gfg.tostring(root)).toprettyxml(indent="   ", encoding='iso-8859-1', standalone=True)
    with open(fileName, "wb") as xml_file:
        xml_file.write(pretty_xml)


def get_time_stamp():

    # Set the timezone offset you need
    # Example for +02:00 offset
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')

    # Get the current time in that timezone
    now = datetime.now(timezone)

    # Format the timestamp
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # Adjust the format to include the colon in the timezone offset
    formatted_timestamp = timestamp[:-2] + ':' + timestamp[-2:]

    return formatted_timestamp


def get_header():

    header = gfg.Element("ns2:header")
    sub_element = gfg.SubElement(header, "ns2:source")
    sub_element.text = "Importacion Web Cheque Digital"
    sub_element = gfg.SubElement(header, "ns2:created")
    sub_element.text = get_time_stamp()
    sub_element = gfg.SubElement(header, "ns2:sequence")
    sub_element.text = "1"

    return header


def get_info_lote_aggregate(fecha, id_origen, norma):

    aggregate = gfg.Element("ns2:aggregate")
    aggregate.set("id", "A0000001")
    sub_element = gfg.SubElement(aggregate, "ns2:type")
    sub_element.text = "Informacion Lote"

    attribute = gfg.Element("ns2:attribute")
    sub_element = gfg.SubElement(attribute, "ns2:name")
    sub_element.text = "FechaProceso"
    sub_element = gfg.SubElement(attribute, "ns2:value")
    sub_element.text = str(fecha)
    aggregate.append(attribute)

    attribute = gfg.Element("ns2:attribute")
    sub_element = gfg.SubElement(attribute, "ns2:name")
    sub_element.text = "Id_Origen"
    sub_element = gfg.SubElement(attribute, "ns2:value")
    sub_element.text = str(id_origen)
    aggregate.append(attribute)

    attribute = gfg.Element("ns2:attribute")
    sub_element = gfg.SubElement(attribute, "ns2:name")
    sub_element.text = "Norma"
    sub_element = gfg.SubElement(attribute, "ns2:value")
    sub_element.text = str(norma)
    aggregate.append(attribute)

    return aggregate


def get_boleta_virtual_aggregate(id: str):

    aggregate = gfg.Element("ns2:aggregate")
    aggregate.set("id", "A" + id)
    sub_element = gfg.SubElement(aggregate, "ns2:type")
    sub_element.text = "003"

    attribute = gfg.Element("ns2:attribute")
    sub_element = gfg.SubElement(attribute, "ns2:name")
    sub_element.text = "Id_Dms"
    sub_element = gfg.SubElement(attribute, "ns2:value")
    sub_element.text = id
    aggregate.append(attribute)

    sub_element = gfg.SubElement(aggregate, "ns2:parent")
    sub_element.text = "A0000001"

    return aggregate
