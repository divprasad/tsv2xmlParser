#!/usr/bin/env python3
import sys, subprocess
import xml.etree.ElementTree as ET

# make XML pretty
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
    root = ET.Element("EXPERIMENT_SET")
    expAttrib={}
    studyAttrib={}
    samAttrib={}
    fileAttrib={}
    # Loop to read input tsv file and parse each line as a SAMPLE in the Sample_SET XML
    with open(tsvInFile, 'r') as f:
        for line in f:
            line=line.rstrip()
            samAlias, expAlias, _, _ = line.split('\t')
            expAttrib['alias']=expAlias # parse from tsv
            r1=ET.Element("EXPERIMENT")
            r1.attrib=expAttrib
            root.append (r1)

            c1=ET.SubElement(r1, "TITLE")
            c1.text="GridION sequencing"

            c2=ET.SubElement(r1, "STUDY_REF")
            studyAttrib['accession']="PRJEB39014"
            c2.attrib=studyAttrib

            c3=ET.SubElement(r1, "DESIGN")
            c31=ET.SubElement(c3, "DESIGN_DESCRIPTION")
            c32=ET.SubElement(c3, "SAMPLE_DESCRIPTOR")
            samAttrib['accession']=samAlias
            c32.attrib=samAttrib

            c33=ET.SubElement(c3, "LIBRARY_DESCRIPTOR")
            c331=ET.SubElement(c33, "LIBRARY_NAME")
            c332=ET.SubElement(c33, "LIBRARY_STRATEGY")
            c332.text="AMPLICON"
            c333=ET.SubElement(c33, "LIBRARY_SOURCE")
            c333.text="VIRAL RNA"
            c334=ET.SubElement(c33, "LIBRARY_SELECTION")
            c334.text="PCR"
            c335=ET.SubElement(c33, "LIBRARY_LAYOUT")
            c3351=ET.SubElement(c335, "SINGLE")

            c4=ET.SubElement(r1, "PLATFORM")
            c41=ET.SubElement(c4, "OXFORD_NANOPORE")
            c411=ET.SubElement(c41, "INSTRUMENT_MODEL")
            c411.text="GridION"

            c5= ET.SubElement(r1, "EXPERIMENT_ATTRIBUTES")
            c51= ET.SubElement(c5, "EXPERIMENT_ATTRIBUTE")
            c511=ET.SubElement(c51, "TAG")
            c511.text="library preparation date"
            c512=ET.SubElement(c51, "VALUE")
            c512.text="not collected"

            # c211= ET.SubElement(c21, "PLATFORM")
            # fileAttrib['filename']=gzFile # parse from tsv
            # fileAttrib['filetype']='fastq'
            # fileAttrib['checksum_method']='MD5'
            # fileAttrib['checksum']=md5 # parse from tsv
            # c211.attrib=fileAttrib




    tree = ET.ElementTree(root) #set the root to 1st element i.e. SAMPLE_SET
    indent(root) #make it PRETTY

    # name for the output XML file
    xmlOutFile=tsvInFile[:-3] + 'xml'

    # Insert the XML version and encoding
    with open (xmlOutFile, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')

    # ElementTree needs to write XML in binary mode; use append option
    with open (xmlOutFile, 'ab') as file:
        tree.write(file)


if __name__ == '__main__':
    inFile = sys.argv[1]
    outFile=inFile[:-3] + 'xml' # name for the output XML file

    tsv2XML(inFile,outFile)

    # replace ' /' with '/' in the XML file
    subprocess.call(["sed", "-i", "-e", 's/ \//\//g', outFile])
