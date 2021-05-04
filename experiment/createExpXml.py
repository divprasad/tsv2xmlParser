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
    root = ET.Element("EXPERIMENT_SET")

    # Loop to read input tsv file and parse each line as a SAMPLE in the Sample_SET XML
    with open(tsvInFile, 'r') as f:
        for line in f:
            line=line.rstrip()
            samAlias, expAlias, _, _ = line.split('\t')
            r1=ET.SubElement(root,"EXPERIMENT")
            r1.attrib['alias']=expAlias # parse from tsv

            c1=ET.SubElement(r1, "TITLE")
            c1.text="GridION sequencing"

            c2=ET.SubElement(r1, "STUDY_REF")
            c2.attrib['accession']="PRJEB39014"

            c3=ET.SubElement(r1, "DESIGN")
            c31=ET.SubElement(c3, "DESIGN_DESCRIPTION")
            c32=ET.SubElement(c3, "SAMPLE_DESCRIPTOR")
            c32.attrib['accession']=samAlias # parse from tsv

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

    indent(root) #make it PRETTY
    xmlstr = ET.tostring(root, encoding='utf8').decode('utf8')

    # Insert the XML version and encoding
    with open (xmlOutFile, 'w') as file:
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

    # minor esthetic fix
    # replace ' /' with '/' in the XML file
    subprocess.call(["sed", "-i", "-e", 's/ \//\//g', outFile])
