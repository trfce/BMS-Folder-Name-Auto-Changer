import os

BMS_Path = "C:/BMS/Insane BMS"
BMS_list = []
BMS_Error = []
#BMS_Folderlist = []
BMS_Needcheck = []
BMS_Success = 0
BMS_Failed = 0
for (path, dir, files) in os.walk(BMS_Path): # BMS 폴더 속 BMS 파일을 읽어옴.
    for filename in files:
        ext = os.path.splitext(filename)[-1]
#        BMS_Folderlist.append(path)
#        BMS_Folderlist_set = set(BMS_Folderlist)
#        BMS_Folderlist = list(BMS_Folderlist_set)
        if ext in ['.bms', '.bme', '.bml', '.pms', 'bmx']:
            BMS_Filename = "%s/%s" % (path, filename)
            BMS_list.append(BMS_Filename)

    if BMS_list == []: # 맨 처음 BMS_list가 0인 상황을 무시.
        continue
    
    for i in range(0, len(BMS_list)): #모은 BMS를 오래된 날짜 순으로 정렬.
        for j in range(0, len(BMS_list)):
            if os.path.getmtime(BMS_list[i]) < os.path.getmtime(BMS_list[j]):
                (BMS_list[i], BMS_list[j]) = (BMS_list[j], BMS_list[i])

    print(BMS_list[0]+"의 Title로 폴더명을 변경합니다.")
    
    try:
        f = open(BMS_list[0], 'r', encoding='shift_jisx0213') # 제일 오래된 BMS 파일을 open.
        BMS_reading = f.readlines()
    except UnicodeDecodeError:
        BMS_Error.append(BMS_list[0])
        print("%s을 읽는데 실패하였습니다. 나중에 직접 확인해주세요." % BMS_list[0])
        
    f.close()
                                    
    for a in BMS_reading: 
        
        if a[0:6].upper() == '#TITLE': # BMS에서 TITLE, ARTIST를 가져옴
            BMS_title = a[7:-1]
        if a[0:7].upper() == '#ARTIST':
            BMS_artist = a[8:-1]
            BMS_filename = BMS_list[0].rsplit(BMS_list[0].split('/')[-1])[0].strip("/").strip()
            
            if BMS_title[-3:].upper() in ('AL)', 'YS)', 'ER)', 'R7)', 'L7)', 'R5)', 'L5)', 'S)-', 'RD)'): # 차분명을 폴더에 넣지 않기 위한 작업
                BMSfolderNameBefore = "%s/%s (by %s)" % (BMS_Path, BMS_title.rsplit('(', 1)[0].strip(), BMS_artist.rsplit('/')[0]strip()))
            elif BMS_title[-3:].upper() in ('AL-', 'YS-', 'ER-', 'R7-', 'L7-', 'R5-', 'L5-', 'SY-', 'RD-'):
                BMSfolderNameBefore = "%s/%s (by %s)" % (BMS_Path, BMS_title.rsplit('-', 2)[-3].strip(), BMS_artist.rsplit('/')[0]strip())
            elif BMS_title[-3:].upper() in ('AL]', 'YS]', 'ER]', 'R7]', 'L7]', 'R5]', 'L5]', 'SY]', 'RD]'):
                BMSfolderNameBefore = "%s/%s (by %s)" % (BMS_Path, BMS_title.rsplit('[', 1)[0].strip(), BMS_artist.rsplit('/')[0]strip())
            else:
                BMSfolderNameBefore = "%s/%s (by %s)" % (BMS_Path, BMS_title.rsplit('[', 1)[0].strip(), BMS_artist.rsplit('/')[0]strip())
                
            BMStranslate = BMSfolderNameBefore.maketrans({"*":"","?":"","\"":"","<":"",">":"","|":""})
            try:  # 폴더명 변경 및 예외 발생 시 예외처리
                os.rename(BMS_filename, BMSfolderNameBefore.translate(BMStranslate))
                BMS_Success += 1

            except:
                BMS_Error.append(BMS_filename)
                print(BMS_filename + "의 폴더변경에 실패했습니다. 나중에 직접 변경해주세요.")
                BMS_Failed += 1
                
    BMS_list = [] # BMS List를 초기화
print("변경 성공 :" + str(BMS_Success))
print("변경 실패 :" + str(BMS_Failed))
print("------------------------------변경 실패한 곡 목록------------------------------")
for i in range(0, len(BMS_Error)):
    print("%s. %s" % (i+1, BMS_Error[i]))