# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import os
import pandas
from lxml import etree
#폴더 설정
Current_Dir = os.getcwd() #현재폴더로 설정함
file_list = os.listdir(Current_Dir)
#파일 정리
NFD_list=[]
NFD_num=[]
for file_name in file_list:
    fileName, fileExtension = os.path.splitext(file_name)
#    print(fileExtension)
    if fileExtension == '.and':
        AND_fileName=fileName
        print(fileName)
    if fileExtension == '.nfd':
        NFD_num.append(int(fileName.split(AND_fileName+'_')[-1]))
        NFD_list.append((fileName, int(fileName.split(AND_fileName+'_')[-1])))
#        NFD_list.append(fileName+fileExtension)
#        print(fileName + fileExtension)
NFD_list_Sorted=sorted(NFD_list, key=lambda file: file[1]) # *.nfd 파일, 정렬됨
NFD_list=[]
for (name, num) in NFD_list_Sorted:
    path=os.path.join(Current_Dir, name+'.nfd')
    NFD_list.append(path)
#파일 정리 결과물
AND_file = os.path.join(Current_Dir, AND_fileName+'.and')  # *.and 파일
NFD_list
#결과물 이외의 필요없어진 변수들 삭제
del NFD_list_Sorted, NFD_num, fileExtension, fileName, file_list, file_name, name, num, path
#sorted(range(len(NFD_num)), key=lambda D: NFD_num[D])
f_AND = open(AND_file, 'r')
lines = f_AND.readlines()
FreqData=0
for line in lines:
    line=line.replace('\t','')
    line=line.split('=')
    if line[0]=='created_by':
        version=line[1].replace('\n','')
    elif line[0]=='fsweep':
        frequency=line[1].replace('\'','')
        frequency=frequency.split(',')
    else:
        pass
#        if line[0]=="$begin 'NearFieldData'\n":
#             FreqData==1
#        elif line[0]=="$end 'NearFieldData'\n":
#            break
#        elif FreqData==1:
#            pass
f_AND.close()

# read csv file
df = pandas.read_csv(NFD_list[0], skiprows=5, names=['Index', 'X', 'Y', 'Z', 'Ex_real', 'Ex_imag', 'Ey_real', 'Ey_imag', 'Ez_real', 'Ez_imag', 'Hx_real', 'Hx_imag', 'Hy_real', 'Hy_imag', 'Hz_real', 'Hz_imag'])
# df is pandas.DataFrame
CSV_data = df.set_index("Index")
CSV_data['Y']
EmissionType_list=["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"]
root = etree.Element("EmissionScan")
NFS_ver = etree.Element("Nfs_ver")
NFS_ver.text = "1.0"
File_name = etree.Element("Filename")
File_name.text = AND_fileName+EmissionType_list[0]+".xml"
File_ver = etree.Element("File_ver")
File_ver.text = "1"
ProbeType1 = etree.Element("Probe")
ProbeType2 = etree.SubElement("Field")
ProbeType2.text = EmissionType_list[0]
Data_elem = etree.Element("Data")
Coordi_elem = etree.SubElement("Coordinates")
Coordi_elem.text="xyz"
Freq_elem = etree.SubElement("Frequencies")
Freq_elem.tex
