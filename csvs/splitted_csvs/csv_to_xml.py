__author__ = 'dmitrii'
import csv
import sys
import xml.etree.cElementTree as ET

root = ET.Element("results")

tr = {"1": "1", "2": "2", "4": "3", "8": "4", "16": "5", "32": "6"}


with open(sys.argv[1], 'r') as csv_file:
    with open("xmls/" + sys.argv[1][:-4] + ".xml", 'ab') as xml_file:
        writer = xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    reader = csv.DictReader(csv_file)
    for row in reader:
        with open("xmls/" + sys.argv[1][:-4] + ".xml", 'ab') as xml_file:
	    row_xml = ET.SubElement(root, "row")
	    if float(row["FR"]) == 2901.:
		ET.SubElement(row_xml, "data", column="Variable Features").text =  "freq;" + str(3000.0)+",tr;" + tr[row["TR"]]
	    else:
                ET.SubElement(row_xml, "data", column="Variable Features").text =  "freq;" + row["FR"]+",tr;" + tr[row["TR"]]
            ET.SubElement(row_xml, "data", column="Performance").text = row["EN"]
tree = ET.ElementTree(root)
tree.write("xmls/" + sys.argv[1][:-4] + ".xml")
