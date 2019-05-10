1.	build_dict.py

path為所有公然侮辱案件的位置
對每一案件，搜尋『』中的文字，再將頓號(、)之間的ZH分開。dict_raw輸出格式為:
日期, 是否有罪, ZH

2.	analyze_dict.py

list_swear為所有ZH所構成的list
list_guilty為對應ZH有罪的次數與總判決數
list_date為該ZH出現的日期所構成的list
(對index為i的ZH，該document frequency為list_guilty[i][1])
dict輸出的格式為:
ZH, 有罪次數, 總次數, 所有出現過ZH的日期

tf輸出的格式為:
ZH, 案件的檔名, ZH在該檔中出現的次數