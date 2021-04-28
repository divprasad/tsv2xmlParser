# tsv2xmlParser

parser for (programmatic) read submission to https://www.ebi.ac.uk/ena/browser/home 

accepts one tsv file of the format:

Run3zz_BC01	2020-11-19	somewhere	north hCoV-19/Netherlands/xy-ZZZ-1001/2020	EPI_ISL_xyyxzz
Run3zz_BC02	2020-10-14	somewhere south	hCoV-19/Netherlands/xy-ZZZ-1002/2020	EPI_ISL_xyyxzz
Run3zz_BC03	2020-11-18	somewhere south	hCoV-19/Netherlands/xy-ZZZ-1003/2020	EPI_ISL_xyyxzz
Run3zz_BC04	2020-11-19	somewhere north	hCoV-19/Netherlands/xy-ZZZ-1004/2020	EPI_ISL_xyyxzz

and converts to XML file
