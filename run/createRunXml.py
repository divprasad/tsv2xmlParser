#!/usr/bin/env python3
import sys, subprocess
import xml.etree.ElementTree as ET

# make the XML pretty
# source: https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def tsv2XML(tsvInFile,xmlOutFile):
    root = ET.Element("RUN_SET")
    runAttrib={}
    expAttrib={}
    fileAttrib={}
    # Loop to read input tsv file and parse each line as a SAMPLE in the Sample_SET XML
    with open(tsvInFile, 'r') as f:
        for line in f:
            line=line.rstrip()
            samAlias, expAlias, gzFile, md5 = line.split('\t')
            runAttrib['alias']=str(samAlias) # parse from tsv
            runAttrib['center_name']='Dutch COVID-19 response team'

            r1 = ET.Element("RUN")
            r1.attrib=runAttrib
            root.append (r1)

            c1 = ET.SubElement(r1,"EXPERIMENT_REF")
            expAttrib['refname']=str(expAlias) # parse from tsv
            c1.attrib= expAttrib

            c2 = ET.SubElement(r1,"DATA_BLOCK")
            c21= ET.SubElement(c2,"FILES")

            c211= ET.SubElement(c21,"FILE")
            fileAttrib['filename']=str(gzFile) # parse from tsv
            fileAttrib['filetype']='fastq'
            fileAttrib['checksum_method']='MD5'
            fileAttrib['checksum']=str(md5) # parse from tsv
            c211.attrib=fileAttrib

    tree = ET.ElementTree(root) #set the root to 1st element i.e. SAMPLE_SET
    indent(root) #make it PRETTY

    # Insert the XML version and encoding
    with open (xmlOutFile, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

    # ElementTree needs to write XML in binary mode; use append option
    with open (xmlOutFile, 'ab') as file:
        tree.write(file,encoding='UTF-8')

if __name__ == '__main__':
    inFile = sys.argv[1]
    outFile=inFile[:-3] + 'xml' # name for the output XML file

    tsv2XML(inFile,outFile) # run parser function and create XML

    # minor esthetic fix
    # replace ' /' with '/' in the XML file
    subprocess.call(["sed", "-i", "-e", 's/ \//\//g', outFile])
