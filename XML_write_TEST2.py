from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from xml.dom import minidom
## xml write

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


root = Element('EmissionScan')
xml_Nfs_ver = SubElement(root, 'Nfs_ver')
xml_Nfs_ver.text = '1.0'
xml_Filename = SubElement(root, 'Filename')
xml_Filename.text = 'Ex.xml'
xml_Filename = SubElement(root, 'File_ver')
xml_Filename.text = '1'
xml_Probe = SubElement(root, 'Probe')
xml_Probe_Field = SubElement(xml_Probe, 'Field')
xml_Probe_Field.text = 'Ex'
xml_Data = SubElement(root, 'Data')
xml_Data_Coordinates = SubElement(xml_Data, 'Coordinates')
xml_Data_Coordinates.text = 'xyz'
xml_Data_Frequencies = SubElement(xml_Data, 'Frequencies')
xml_Data_Frequencies_List = SubElement(xml_Data_Frequencies, 'List')
xml_Data_Frequencies_List.text = '1e6' #Freq List
xml_Data_Measurement = SubElement(xml_Data, 'Measurement')
xml_Data_Measurement_Format = SubElement(xml_Data_Measurement, 'Format')
xml_Data_Measurement_Format.text = 'ri' ## Format
xml_Data_Measurement_Data_files = SubElement(xml_Data_Measurement, 'Data_files')
xml_Data_Measurement_Data_files.text = 'Ex.dat' ## Format

output_file = open( 'Emission.xml', 'w' )
output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )
output_file.write( prettify(root))
output_file.close()
