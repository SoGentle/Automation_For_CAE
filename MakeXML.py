# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 04:57:31 2018

@author: 1623282
"""
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom

#XML 파일 생성
def XMLprettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    doc = reparsed.createProcessingInstruction('xml version="1.0"', 'encoding="utf-8"')
    reparsed.insertBefore(doc, reparsed.firstChild)
    return reparsed.toprettyxml(indent="  ")


## MAKE XML Files
def MakeXML_CST(Field, frequency):
    root = Element('EmissionScan')
    xml_Nfs_ver = SubElement(root, 'Nfs_ver')
    xml_Nfs_ver.text = '1.0'
    xml_Filename = SubElement(root, 'Filename')
    xml_Filename.text = Field + '.xml'
    xml_Filename = SubElement(root, 'File_ver')
    xml_Filename.text = '1'
    xml_Probe = SubElement(root, 'Probe')
    xml_Probe_Field = SubElement(xml_Probe, 'Field')
    xml_Probe_Field.text = Field.split('_')[0]
    xml_Data = SubElement(root, 'Data')
    xml_Data_Coordinates = SubElement(xml_Data, 'Coordinates')
    xml_Data_Coordinates.text = 'xyz'
    xml_Data_Frequencies = SubElement(xml_Data, 'Frequencies')
    xml_Data_Frequencies_List = SubElement(xml_Data_Frequencies, 'List')
    Freq_list =""
    for freq in frequency:
        freq = freq.replace("Hz", "")
        Freq_list = Freq_list + " " + freq
    xml_Data_Frequencies_List.text = Freq_list #Freq List
    xml_Data_Measurement = SubElement(xml_Data, 'Measurement')
    xml_Data_Measurement_Format = SubElement(xml_Data_Measurement, 'Format')
    xml_Data_Measurement_Format.text = 'ri' ## Format
    xml_Data_Measurement_Data_files = SubElement(xml_Data_Measurement, 'Data_files')
    xml_Data_Measurement_Data_files.text = Field + '.dat' ## Format
    output_file = open( Field+'.xml', 'w' )
    #output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )
    output_file.write(XMLprettify(root).split("\n",1)[1]) #첫번째줄 삭제
    output_file.close()
