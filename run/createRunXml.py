#!/usr/bin/env python3
import sys, subprocess
import xml.etree.ElementTree as ET

# make XML pretty
# source: https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
# source: https://stackoverflow.com/a/33956544
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

# https://stackoverflow.com/a/38573964/146633
def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  # for child open
            if queue:
                element.tail = '\n' + indent * queue[0][0]  # for sibling open
            else:
                element.tail = '\n' + indent * (level-1)  # for parent close
                queue[0:0] = children  # prepend so children come before siblings

# another source: https://stackoverflow.com/a/12940014  # ARCHIVED

def tsv2XML(tsvInFile,xmlOutFile):
    root = ET.Element("RUN_SET")

    # Loop to read input tsv file and parse each line as a SAMPLE in the Sample_SET XML
    with open(tsvInFile, 'r') as f:
        for line in f:
            line=line.rstrip()
            samAlias, expAlias, gzFile, md5 = line.split('\t')

            r1 = ET.SubElement(root, "RUN")
            r1.attrib['alias']=str(samAlias) # parse from tsv
            r1.attrib['center_name']='Dutch COVID-19 response team'
            # r1.attrib['center_name']="ERASMUS MC, UNIVERISTY MEDICAL CENTER"
            # r1.attrib['broker_name']="Submission account for department of Viroscience’s Research Teams, ErasmusMC"

            # root.append (r1)

            c1 = ET.SubElement(r1,"EXPERIMENT_REF")
            c1.attrib['refname']=str(expAlias) # parse from tsv

            c2 = ET.SubElement(r1,"DATA_BLOCK")
            c21= ET.SubElement(c2,"FILES")

            c211= ET.SubElement(c21,"FILE")
            c211.attrib['filename']=str(gzFile) # parse from tsv
            c211.attrib['filetype']='fastq'
            c211.attrib['checksum_method']='MD5'
            c211.attrib['checksum']=str(md5) # parse from tsv

    indent(root) #make it PRETTY
    #prettify(root)
    xmlstr = ET.tostring(root, encoding='utf8').decode('utf8')
    #xmlstr = ET.tostring(root).decode('utf8')

    # Insert the XML version and encoding
    with open (xmlOutFile, 'w') as file:
        #file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write(xmlstr)

    # NOTE - this step caused strange bug.
    # All the attrib key value pairs got set as if it were the last record (in the tsv file)
    #tree = ET.ElementTree(root) #set the root to 1st element i.e. SAMPLE_SET

    # ElementTree needs to write XML in binary mode; use append option
    # with open (xmlOutFile, 'ab') as file:
    #     tree.write(file,encoding='UTF-8', xml_declaration=True)

if __name__ == '__main__':
    inFile = sys.argv[1]
    outFile=inFile[:-3] + 'xml' # name for the output XML file

    tsv2XML(inFile,outFile) # run parser function and create XML

    # minor esthetic HOT FIX
    # replace ' /' with '/' in the XML file
    subprocess.call(["sed", "-i", "-e", 's/ \//\//g', outFile])
