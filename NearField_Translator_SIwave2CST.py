# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import os
import pandas as pd
import MakeXML

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

DAT_Ex_Xmin = pd.DataFrame()
DAT_Ey_Xmin = pd.DataFrame()
DAT_Ez_Xmin = pd.DataFrame()
DAT_Hx_Xmin = pd.DataFrame()
DAT_Hy_Xmin = pd.DataFrame()
DAT_Hz_Xmin = pd.DataFrame()

DAT_Ex_Xmax = pd.DataFrame()
DAT_Ey_Xmax = pd.DataFrame()
DAT_Ez_Xmax = pd.DataFrame()
DAT_Hx_Xmax = pd.DataFrame()
DAT_Hy_Xmax = pd.DataFrame()
DAT_Hz_Xmax = pd.DataFrame()

DAT_Ex_Ymin = pd.DataFrame()
DAT_Ey_Ymin = pd.DataFrame()
DAT_Ez_Ymin = pd.DataFrame()
DAT_Hx_Ymin = pd.DataFrame()
DAT_Hy_Ymin = pd.DataFrame()
DAT_Hz_Ymin = pd.DataFrame()

DAT_Ex_Ymax = pd.DataFrame()
DAT_Ey_Ymax = pd.DataFrame()
DAT_Ez_Ymax = pd.DataFrame()
DAT_Hx_Ymax = pd.DataFrame()
DAT_Hy_Ymax = pd.DataFrame()
DAT_Hz_Ymax = pd.DataFrame()

DAT_Ex_Zmin = pd.DataFrame()
DAT_Ey_Zmin = pd.DataFrame()
DAT_Ez_Zmin = pd.DataFrame()
DAT_Hx_Zmin = pd.DataFrame()
DAT_Hy_Zmin = pd.DataFrame()
DAT_Hz_Zmin = pd.DataFrame()

DAT_Ex_Zmax = pd.DataFrame()
DAT_Ey_Zmax = pd.DataFrame()
DAT_Ez_Zmax = pd.DataFrame()
DAT_Hx_Zmax = pd.DataFrame()
DAT_Hy_Zmax = pd.DataFrame()
DAT_Hz_Zmax = pd.DataFrame()

num=0
# read csv file
for freq in frequency:
    df = pd.read_csv(NFD_list[num], skiprows=5, names=['Index', 'X', 'Y', 'Z', 'Ex_real', 'Ex_imag', 'Ey_real', 'Ey_imag', 'Ez_real', 'Ez_imag', 'Hx_real', 'Hx_imag', 'Hy_real', 'Hy_imag', 'Hz_real', 'Hz_imag'])
    # df is pandas.DataFrame
    del df["Index"]
    for n in range(df.shape[0]):
        for m in range(3):
            df.iloc[n,m]=df.iloc[n,m].replace("mm", "")
            if "e+" in df.iloc[n,m]:
                (numb, power) = df.iloc[n,m].split('e+')
    #            power = str(int(power)-3)
                power = int(power)-3
                if power >= 0:
                    df.iloc[n,m] = numb +"e+"+ str(power)
                else:
                    df.iloc[n,m] = numb + "e" +str(power)
            elif "e-" in df.iloc[n,m]:
                (numb, power) = df.iloc[n,m].split('e-')
                power = str(int(power)+3)
                df.iloc[n,m] = numb + 'e-' + power
            else:
                continue
    df['X']=pd.to_numeric(df['X'])
    df['Y']=pd.to_numeric(df['Y'])
    df['Z']=pd.to_numeric(df['Z'])
    X_min = min(df['X'])
    X_max = max(df['X'])
    Y_min = min(df['Y'])
    Y_max = max(df['Y'])
    Z_min = min(df['Z'])
    Z_max = max(df['Z'])
    X_min_side = df[df.X==X_min]
    X_max_side = df[df.X==X_max]
    Y_min_side = df[df.Y==Y_min]
    Y_max_side = df[df.Y==Y_max]
    Z_min_side = df[df.Z==Z_min]
    Z_max_side = df[df.Z==Z_max]
    
    if num == 0:        
        DAT_Ex_Xmin = pd.concat([DAT_Ex_Xmin, X_min_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Xmax = pd.concat([DAT_Ex_Xmax, X_max_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Xmin = pd.concat([DAT_Ey_Xmin, X_min_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Xmax = pd.concat([DAT_Ey_Xmax, X_max_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Xmin = pd.concat([DAT_Ez_Xmin, X_min_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Xmax = pd.concat([DAT_Ez_Xmax, X_max_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Ex_Ymin = pd.concat([DAT_Ex_Ymin, Y_min_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Ymax = pd.concat([DAT_Ex_Ymax, Y_max_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Ymin = pd.concat([DAT_Ey_Ymin, Y_min_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Ymax = pd.concat([DAT_Ey_Ymax, Y_max_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Ymin = pd.concat([DAT_Ez_Ymin, Y_min_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Ymax = pd.concat([DAT_Ez_Ymax, Y_max_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Ex_Zmin = pd.concat([DAT_Ex_Zmin, Z_min_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Zmax = pd.concat([DAT_Ex_Zmax, Z_max_side[['X','Y','Z', 'Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Zmin = pd.concat([DAT_Ey_Zmin, Z_min_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Zmax = pd.concat([DAT_Ey_Zmax, Z_max_side[['X','Y','Z', 'Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Zmin = pd.concat([DAT_Ez_Zmin, Z_min_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Zmax = pd.concat([DAT_Ez_Zmax, Z_max_side[['X','Y','Z', 'Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Hx_Xmin = pd.concat([DAT_Hx_Xmin, X_min_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Xmax = pd.concat([DAT_Hx_Xmax, X_max_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Xmin = pd.concat([DAT_Hy_Xmin, X_min_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Xmax = pd.concat([DAT_Hy_Xmax, X_max_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Xmin = pd.concat([DAT_Hz_Xmin, X_min_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Xmax = pd.concat([DAT_Hz_Xmax, X_max_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)

        DAT_Hx_Ymin = pd.concat([DAT_Hx_Ymin, Y_min_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Ymax = pd.concat([DAT_Hx_Ymax, Y_max_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Ymin = pd.concat([DAT_Hy_Ymin, Y_min_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Ymax = pd.concat([DAT_Hy_Ymax, Y_max_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Ymin = pd.concat([DAT_Hz_Ymin, Y_min_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Ymax = pd.concat([DAT_Hz_Ymax, Y_max_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)

        DAT_Hx_Zmin = pd.concat([DAT_Hx_Zmin, Z_min_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Zmax = pd.concat([DAT_Hx_Zmax, Z_max_side[['X','Y','Z', 'Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Zmin = pd.concat([DAT_Hy_Zmin, Z_min_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Zmax = pd.concat([DAT_Hy_Zmax, Z_max_side[['X','Y','Z', 'Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Zmin = pd.concat([DAT_Hz_Zmin, Z_min_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Zmax = pd.concat([DAT_Hz_Zmax, Z_max_side[['X','Y','Z', 'Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)

    else:
        DAT_Ex_Xmin = pd.concat([DAT_Ex_Xmin, X_min_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Xmax = pd.concat([DAT_Ex_Xmax, X_max_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Xmin = pd.concat([DAT_Ey_Xmin, X_min_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Xmax = pd.concat([DAT_Ey_Xmax, X_max_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Xmin = pd.concat([DAT_Ez_Xmin, X_min_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Xmax = pd.concat([DAT_Ez_Xmax, X_max_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Ex_Ymin = pd.concat([DAT_Ex_Ymin, Y_min_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Ymax = pd.concat([DAT_Ex_Ymax, Y_max_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Ymin = pd.concat([DAT_Ey_Ymin, Y_min_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Ymax = pd.concat([DAT_Ey_Ymax, Y_max_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Ymin = pd.concat([DAT_Ez_Ymin, Y_min_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Ymax = pd.concat([DAT_Ez_Ymax, Y_max_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Ex_Zmin = pd.concat([DAT_Ex_Zmin, Z_min_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ex_Zmax = pd.concat([DAT_Ex_Zmax, Z_max_side[['Ex_real','Ex_imag']].rename(columns={"Ex_real":"Ex_real_"+str(num), "Ex_imag":"Ex_imag_"+str(num)})], axis=1)
        DAT_Ey_Zmin = pd.concat([DAT_Ey_Zmin, Z_min_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ey_Zmax = pd.concat([DAT_Ey_Zmax, Z_max_side[['Ey_real','Ey_imag']].rename(columns={"Ey_real":"Ey_real_"+str(num), "Ey_imag":"Ey_imag_"+str(num)})], axis=1)
        DAT_Ez_Zmin = pd.concat([DAT_Ez_Zmin, Z_min_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)
        DAT_Ez_Zmax = pd.concat([DAT_Ez_Zmax, Z_max_side[['Ez_real','Ez_imag']].rename(columns={"Ez_real":"Ez_real_"+str(num), "Ez_imag":"Ez_imag_"+str(num)})], axis=1)

        DAT_Hx_Xmin = pd.concat([DAT_Hx_Xmin, X_min_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Xmax = pd.concat([DAT_Hx_Xmax, X_max_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Xmin = pd.concat([DAT_Hy_Xmin, X_min_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Xmax = pd.concat([DAT_Hy_Xmax, X_max_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Xmin = pd.concat([DAT_Hz_Xmin, X_min_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Xmax = pd.concat([DAT_Hz_Xmax, X_max_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)

        DAT_Hx_Ymin = pd.concat([DAT_Hx_Ymin, Y_min_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Ymax = pd.concat([DAT_Hx_Ymax, Y_max_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Ymin = pd.concat([DAT_Hy_Ymin, Y_min_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Ymax = pd.concat([DAT_Hy_Ymax, Y_max_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Ymin = pd.concat([DAT_Hz_Ymin, Y_min_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Ymax = pd.concat([DAT_Hz_Ymax, Y_max_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)

        DAT_Hx_Zmin = pd.concat([DAT_Hx_Zmin, Z_min_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hx_Zmax = pd.concat([DAT_Hx_Zmax, Z_max_side[['Hx_real','Hx_imag']].rename(columns={"Hx_real":"Hx_real_"+str(num), "Hx_imag":"Hx_imag_"+str(num)})], axis=1)
        DAT_Hy_Zmin = pd.concat([DAT_Hy_Zmin, Z_min_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hy_Zmax = pd.concat([DAT_Hy_Zmax, Z_max_side[['Hy_real','Hy_imag']].rename(columns={"Hy_real":"Hy_real_"+str(num), "Hy_imag":"Hy_imag_"+str(num)})], axis=1)
        DAT_Hz_Zmin = pd.concat([DAT_Hz_Zmin, Z_min_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        DAT_Hz_Zmax = pd.concat([DAT_Hz_Zmax, Z_max_side[['Hz_real','Hz_imag']].rename(columns={"Hz_real":"Hz_real_"+str(num), "Hz_imag":"Hz_imag_"+str(num)})], axis=1)
        
    print(num)
    num=num+1

DAT_Ex_Xmin.to_csv('Ex_Xmin.dat', sep='\t', index=False, header=False)
DAT_Ex_Xmax.to_csv('Ex_Xmax.dat', sep='\t', index=False, header=False)
DAT_Ey_Xmin.to_csv('Ey_Xmin.dat', sep='\t', index=False, header=False)
DAT_Ey_Xmax.to_csv('Ey_Xmax.dat', sep='\t', index=False, header=False)
DAT_Ez_Xmin.to_csv('Ez_Xmin.dat', sep='\t', index=False, header=False)
DAT_Ez_Xmax.to_csv('Ez_Xmax.dat', sep='\t', index=False, header=False)
DAT_Hx_Xmin.to_csv('Hx_Xmin.dat', sep='\t', index=False, header=False)
DAT_Hx_Xmax.to_csv('Hx_Xmax.dat', sep='\t', index=False, header=False)
DAT_Hy_Xmin.to_csv('Hy_Xmin.dat', sep='\t', index=False, header=False)
DAT_Hy_Xmax.to_csv('Hy_Xmax.dat', sep='\t', index=False, header=False)
DAT_Hz_Xmin.to_csv('Hz_Xmin.dat', sep='\t', index=False, header=False)
DAT_Hz_Xmax.to_csv('Hz_Xmax.dat', sep='\t', index=False, header=False)

DAT_Ex_Ymin.to_csv('Ex_Ymin.dat', sep='\t', index=False, header=False)
DAT_Ex_Ymax.to_csv('Ex_Ymax.dat', sep='\t', index=False, header=False)
DAT_Ey_Ymin.to_csv('Ey_Ymin.dat', sep='\t', index=False, header=False)
DAT_Ey_Ymax.to_csv('Ey_Ymax.dat', sep='\t', index=False, header=False)
DAT_Ez_Ymin.to_csv('Ez_Ymin.dat', sep='\t', index=False, header=False)
DAT_Ez_Ymax.to_csv('Ez_Ymax.dat', sep='\t', index=False, header=False)
DAT_Hx_Ymin.to_csv('Hx_Ymin.dat', sep='\t', index=False, header=False)
DAT_Hx_Ymax.to_csv('Hx_Ymax.dat', sep='\t', index=False, header=False)
DAT_Hy_Ymin.to_csv('Hy_Ymin.dat', sep='\t', index=False, header=False)
DAT_Hy_Ymax.to_csv('Hy_Ymax.dat', sep='\t', index=False, header=False)
DAT_Hz_Ymin.to_csv('Hz_Ymin.dat', sep='\t', index=False, header=False)
DAT_Hz_Ymax.to_csv('Hz_Ymax.dat', sep='\t', index=False, header=False)

DAT_Ex_Zmin.to_csv('Ex_Zmin.dat', sep='\t', index=False, header=False)
DAT_Ex_Zmax.to_csv('Ex_Zmax.dat', sep='\t', index=False, header=False)
DAT_Ey_Zmin.to_csv('Ey_Zmin.dat', sep='\t', index=False, header=False)
DAT_Ey_Zmax.to_csv('Ey_Zmax.dat', sep='\t', index=False, header=False)
DAT_Ez_Zmin.to_csv('Ez_Zmin.dat', sep='\t', index=False, header=False)
DAT_Ez_Zmax.to_csv('Ez_Zmax.dat', sep='\t', index=False, header=False)
DAT_Hx_Zmin.to_csv('Hx_Zmin.dat', sep='\t', index=False, header=False)
DAT_Hx_Zmax.to_csv('Hx_Zmax.dat', sep='\t', index=False, header=False)
DAT_Hy_Zmin.to_csv('Hy_Zmin.dat', sep='\t', index=False, header=False)
DAT_Hy_Zmax.to_csv('Hy_Zmax.dat', sep='\t', index=False, header=False)
DAT_Hz_Zmin.to_csv('Hz_Zmin.dat', sep='\t', index=False, header=False)
DAT_Hz_Zmax.to_csv('Hz_Zmax.dat', sep='\t', index=False, header=False)

#    CSV_Data=CSV_data.rename(columns={"Ex_real":"Ex_real_"+str(n), "Ex_imag":"Ex_imag_"+str(n), "Ey_real":"Ey_real_"+str(n), "Ey_imag":"Ey_imag_"+str(n), "Ez_real":"Ez_real_"+str(n), "Ez_imag":"Ez_imag_"+str(n), "Hx_real":"Hx_real_"+str(n), "Hx_imag":"Hx_imag_"+str(n), "Hy_real":"Hy_real_"+str(n), "Hy_imag":"Hy_imag_"+str(n), "Hz_real":"Hz_real_"+str(n), "Hz_imag":"Hz_imag_"+str(n)})

EmissionType_list=["Ex_Xmin", "Ex_Xmax", "Ey_Xmin", "Ey_Xmax", "Ez_Xmin", "Ez_Xmax", "Hx_Xmin", "Hx_Xmax", "Hy_Xmin", "Hy_Xmax", "Hz_Xmin", "Hz_Xmax", \
                   "Ex_Ymin", "Ex_Ymax", "Ey_Ymin", "Ey_Ymax", "Ez_Ymin", "Ez_Ymax", "Hx_Ymin", "Hx_Ymax", "Hy_Ymin", "Hy_Ymax", "Hz_Ymin", "Hz_Ymax", \
                   "Ex_Zmin", "Ex_Zmax", "Ey_Zmin", "Ey_Zmax", "Ez_Zmin", "Ez_Zmax", "Hx_Zmin", "Hx_Zmax", "Hy_Zmin", "Hy_Zmax", "Hz_Zmin", "Hz_Zmax"]
for Field in EmissionType_list:
    MakeXML.MakeXML_CST(Field, frequency)
