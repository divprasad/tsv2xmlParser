# tsv2xmlParser

Parsers for (programmatic) read submission to https://www.ebi.ac.uk/ena/browser/home

Parses a .tsv file & converts to the equivalent .xml file

## `createSampleXml.py`
takes one tsv file as the argument; tsv has the format:

  "alias"    "date"    "province"    "isolateName"    "GisaidID"

  Run3zz_BC01    2020-11-19    somewhere north    hCoV-19/Netherlands/xy-ZZZ-1001/2020    EPI_ISL_xyyxzz  
  Run3zz_BC02    2020-10-14    somewhere south    hCoV-19/Netherlands/xy-ZZZ-1002/2020    EPI_ISL_xyyxzz  
  Run3zz_BC03    2020-11-18    somewhere south    hCoV-19/Netherlands/xy-ZZZ-1003/2020    EPI_ISL_xyyxzz  
  Run3zz_BC04    2020-11-19    somewhere north    hCoV-19/Netherlands/xy-ZZZ-1004/2020    EPI_ISL_xyyxzz  
  ..  
  ..  

## `createRunXml.py` and `createExpXml.py`
takes one tsv file as the argument; tsv has the format:

  "samAlias"    "expAlias"    "gzFile"    "md5"

  Run3zz_BCyy    Exp_Run3zz_BCyy    path_to_folder/Run3zz_BCyy.fastq.gz    5bc7e43c01f76709b2c0d89b1f50264b  
  Run3zz_BCyy    Exp_Run3zz_BCyy    path_to_folder/Run3zz_BCyy.fastq.gz    acad7c8f729469556c58abd0f30c88cd  
  Run3zz_BCyy    Exp_Run3zz_BCyy    path_to_folder/Run3zz_BCyy.fastq.gz    6f7fed624f91cb4f8512b96c4d9b1dec  
  Run3zz_BCyy    Exp_Run3zz_BCyy    path_to_folder/Run3zz_BCyy.fastq.gz    b0f2ca8884b6ff7e35563d055e9c7d1a  
  ..  
  ..  
  
where path_to_folder/ is relative to the root user directory in the ENA ftp drop-box 

**Usage:** `python creatSample.py runxy-yz.tsv` produces the output runxy-yz.xml
