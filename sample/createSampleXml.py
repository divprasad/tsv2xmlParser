#!/usr/bin/env python3
import sys
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

def tsv2XML(tsvInFile, xmlOutFile):
    root = ET.Element("SAMPLE_SET")
    #samAttrib={}

    # Loop to read input tsv file and parse each line as a SAMPLE in the Sample_SET XML
    with open(tsvInFile, 'r') as f:
        for line in f:
            line=line.rstrip()
            alias, date, province, isolate, gid = line.split('\t')
            #samAttrib['alias']=alias
            # print(alias,date)
            #samAttrib['center_name']='Dutch COVID-19 response team'

            r1 = ET.SubElement(root, "SAMPLE")
            r1.attrib['alias']=alias # parse from tsv
            r1.attrib['center_name']="ERASMUS MC, UNIVERISTY MEDICAL CENTER"
            r1.attrib['broker_name']="Submission account for department of Viroscience’s Research Teams, ErasmusMC"
            #r1.attrib['center_name']='Dutch COVID-19 response team'
            #root.append (r1)

            # r1 = ET.Element("SAMPLE")
            # r1.attrib=samAttrib # parse from tsv
            # root.append (r1)

            c1 = ET.SubElement(r1, "TITLE")
            c1.text = "Dutch COVID-19 response sample sequencing"

            c2 = ET.SubElement(r1, "SAMPLE_NAME")

            c21= ET.SubElement(c2, "TAXON_ID")
            c21.text= "2697049"

            c22= ET.SubElement(c2, "SCIENTIFIC_NAME")
            c22.text="Severe acute respiratory syndrome coronavirus 2"

            c22= ET.SubElement(c2, "COMMON_NAME")
            c22.text="Human coronavirus 2019"

            c3 = ET.SubElement(r1, "DESCRIPTION")
            c3.text = "A SARS-CoV-2 specfic multiplex PCR for Nanopore sequencing was performed, similar to amplicon-based approaches as previously described. In short, primers for 86 overlapping amplicons spanning the entire genome were designed using primal. The amplicon length was set to 500bp with 75bp overlap between the different amplicons. The libraries were generated using the native barcode kits from Nanopore (EXP-NBD104 and EXP-NBD114 and SQK-LSK109) and sequenced on a R9.4 flow cell multiplexing up to 24 samples per sequence run. Raw data was demultiplexed, amplicon primers were trimmed and human data was removed by mapping against the human reference genome."

            c4 = ET.SubElement(r1, "SAMPLE_ATTRIBUTES")

            c41= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c411=ET.SubElement(c41, "TAG")
            c411.text="collecting institution"
            c412=ET.SubElement(c41, "VALUE")
            c412.text="not provided"

            c42= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c421=ET.SubElement(c42, "TAG")
            c421.text="collection date"
            c422=ET.SubElement(c42, "VALUE")
            c422.text=str(date) #parse from tsv

            c43= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c431=ET.SubElement(c43, "TAG")
            c431.text="collector name"
            c432=ET.SubElement(c43, "VALUE")
            c432.text="Dutch COVID-19 response team"

            c44= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c441=ET.SubElement(c44, "TAG")
            c441.text="geographic location (country and/or sea)"
            c442=ET.SubElement(c44, "VALUE")
            c442.text="Netherlands"

            c45= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c451=ET.SubElement(c45, "TAG")
            c451.text="geographic location (region and locality)"
            c452=ET.SubElement(c45, "VALUE")
            c452.text=str(province) #parse from tsv

            c46= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c461=ET.SubElement(c46, "TAG")
            c461.text="GISAID Accession ID"
            c462=ET.SubElement(c46, "VALUE")
            c462.text=str(gid) #parse from tsv

            c47= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c471=ET.SubElement(c47, "TAG")
            c471.text="host common name"
            c472=ET.SubElement(c47, "VALUE")
            c472.text="Human"

            c48= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c481=ET.SubElement(c48, "TAG")
            c481.text="host health state"
            c482=ET.SubElement(c48, "VALUE")
            c482.text="not collected"

            c49= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c491=ET.SubElement(c49, "TAG")
            c491.text="host scientific name"
            c492=ET.SubElement(c49, "VALUE")
            c492.text="Homo sapiens"

            c410= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4101=ET.SubElement(c410, "TAG")
            c4101.text="host sex"
            c4102=ET.SubElement(c410, "VALUE")
            c4102.text="not provided"

            c411= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4111=ET.SubElement(c411, "TAG")
            c4111.text="host subject id"
            c4112=ET.SubElement(c411, "VALUE")
            c4112.text="restricted access"

            c412= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4121=ET.SubElement(c412, "TAG")
            c4121.text="isolate"
            c4122=ET.SubElement(c412, "VALUE")
            c4122.text=str(isolate) #parse from tsv

            c413= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4131=ET.SubElement(c413, "TAG")
            c4131.text="isolation source host-associated"
            c4132=ET.SubElement(c413, "VALUE")
            c4132.text="not collected"

            c414= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4141=ET.SubElement(c414, "TAG")
            c4141.text="sample capture status"
            c4142=ET.SubElement(c414, "VALUE")
            c4142.text="active surveillance in response to outbreak"

            c415= ET.SubElement(c4, "SAMPLE_ATTRIBUTE")
            c4151=ET.SubElement(c415, "TAG")
            c4151.text="ENA-CHECKLIST"
            c4152=ET.SubElement(c415, "VALUE")
            c4152.text="ERC000033"


    indent(root) #make it PRETTY
    xmlstr = ET.tostring(root, encoding='utf8').decode('utf8')
    #xmlstr = ET.tostring(root).decode('utf8')
    #prettify(root)

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
