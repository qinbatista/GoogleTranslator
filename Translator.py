# -*- coding: utf-8 -*-
import urllib.request
import random, execjs, requests
import json, hashlib, time
import xml.dom.minidom
# import unicodedata
import os
from fake_useragent import UserAgent
import re
import argparse
import xlwings as xw
import shutil
UA = UserAgent()


class GoogleTranslator:
    def __init__(self, timeout=30, oringal = '', target = ''):
        self.js = """
            // a:你要翻译的内容
            // uq:tkk值
            function vq(a,uq='422388.3876711001') {
                if (null !== uq)
                    var b = uq;
                else {
                    b = sq('T');
                    var c = sq('K');
                    b = [b(), c()];
                    b = (uq = window[b.join(c())] || "") || "";
                }
                var d = sq('t');
                c = sq('k');
                d = [d(), c()];
                c = "&" + d.join("") + "=";
                d = b.split(".");
                b = Number(d[0]) || 0;
                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var l = a.charCodeAt(g);
                    128 > l ? e[f++] = l : (2048 > l ? e[f++] = l >> 6 | 192 : (55296 == (l & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (l = 65536 + ((l & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = l >> 18 | 240,
                    e[f++] = l >> 12 & 63 | 128) : e[f++] = l >> 12 | 224,
                    e[f++] = l >> 6 & 63 | 128),
                    e[f++] = l & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++)
                    a += e[f],
                    a = tq(a, "+-a^+6");
                a = tq(a, "+-3^+b+-f");
                a ^= Number(d[1]) || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1000000;
                return c + (a.toString() + "." + (a ^ b))
            };

            /*--------------------------------------------------------------------------------
            参数：a 为你要翻译的原文
            其他外部函数：
            --------------------------------------------------------------------------------*/
            function sq(a) {
                return function() {
                    return a
                }
            }
            function tq(a, b) {
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2);
                    d = "a" <= d ? d.charCodeAt(0) - 87 : Number(d);
                    d = "+" == b.charAt(c + 1) ? a >>> d : a << d;
                    a = "+" == b.charAt(c) ? a + d & 4294967295 : a ^ d
                }
                return a
            }"""
        self.exec = execjs.compile(self.js)
        self.tkk = None
        self.url = 'https://translate.google.cn/'
        self.timeout = timeout
        self.headers = {
            'User-Agent': UA.random,
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'translate.google.cn'
        }
        self.session = requests.Session()
        self.oringal = oringal
        self.target = target

    def register(self):
        res = self.session.get(url=self.url, headers=self.headers, timeout=self.timeout)
        content = res.content.decode(encoding='utf-8')
        self.tkk = re.search("tkk:'(.*?)'", content).groups()[0]

    def build(self, key):
        self.tkk or self.register()
        tk = self.exec.call('vq', key, self.tkk)
        url = f'https://translate.google.cn/translate_a/single?' \
                f'client=webapp&sl=auto&hl={self.oringal}&tl={self.target}&dt=at&dt=bd&dt=ex&' \
                f'dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=gt&otf=1&' \
                f'ssel=0&tsel=3&kc=1&q={key}{tk}'
        self.headers['User-Agent'] = UA.random
        return url

    def translate(self, key):
        translate_back = -1
        modified_text = key
        using_symble = ''
        replaced_list = []
        symble_list = []
        if key.find('¬#252525FF¬TRAIT¬s¬')!=-1:
            using_symble = '¬#252525FF¬TRAIT¬s¬'
            replaced_list.append('[28]')
            symble_list.append('¬#252525FF¬TRAIT¬s¬')
        if key.find('$playername')!=-1:
            using_symble = '$playername'
            replaced_list.append('[1]')
            symble_list.append('$playername')
        if key.find('¬#A61214FF¬¬o:#A61214FF¬')!=-1:
            using_symble = '¬#A61214FF¬¬o:#A61214FF¬'
            replaced_list.append('[2]')
            symble_list.append('¬#A61214FF¬¬o:#A61214FF¬')
        if key.find('¬s¬')!=-1:
            using_symble = '¬s¬'
            replaced_list.append('[3]')
            symble_list.append('¬s¬')
        if key.find('<assistant><pause>')!=-1:
            using_symble = '<assistant><pause>'
            replaced_list.append('[4]')
            symble_list.append('<assistant><pause>')
        if key.find('$playername and $playername2')!=-1:
            using_symble = '$playername and $playername2'
            replaced_list.append('[5]')
            symble_list.append('$playername and $playername2')
        if key.find('<!crowdgoal>')!=-1:
            using_symble = '<!crowdgoal>'
            replaced_list.append('[6]')
            symble_list.append('<!crowdgoal>')
        if key.find('<col_a><+TRAIT>')!=-1:
            using_symble = '<col_a><+TRAIT>'
            replaced_list.append('[7]')
            symble_list.append('<col_a><+TRAIT>')
        if key.find('<+TRAIT>$playername')!=-1:
            using_symble = '<+TRAIT>$playername'
            replaced_list.append('[8]')
            symble_list.append('<+TRAIT>$playername')
        if key.find('<!whistledelayed>')!=-1:
            using_symble = '<!whistledelayed>'
            replaced_list.append('[9]')
            symble_list.append('<!whistledelayed>')
        if key.find('<!crowdoh>')!=-1:
            using_symble = '<!crowdoh>'
            replaced_list.append('[10]')
            symble_list.append('<!crowdoh>')
        if key.find('<+TRAIT>')!=-1:
            using_symble = '<+TRAIT>'
            replaced_list.append('[11]')
            symble_list.append('<+TRAIT>')
        if key.find('<assistant><-EXP><col_d>')!=-1:
            using_symble = '<assistant><-EXP><col_d>'
            replaced_list.append('[12]')
            symble_list.append('<assistant><-EXP><col_d>')
        if key.find('+1')!=-1:
            using_symble = '+1'
            replaced_list.append('[13]')
            symble_list.append('+1')
        if key.find('#')!=-1:
            using_symble = '#'
            replaced_list.append('[14]')
            symble_list.append('#')
        if key.find('&')!=-1:
            using_symble = '&'
            replaced_list.append('[15]')
            symble_list.append('&')
        if key.find('+')!=-1:
            using_symble = '+'
            replaced_list.append('[16]')
            symble_list.append('+')
        if key.find('.')!=-1:
            using_symble = '.'
            replaced_list.append('[17]')
            symble_list.append('.')
        if key.find('!')!=-1:
            using_symble = '!'
            replaced_list.append('[18]')
            symble_list.append('!')
        if key.find('?')!=-1:
            using_symble = '?'
            replaced_list.append('[19]')
            symble_list.append('?')
        if key.find('<assistant><EXP><col_a>')!=-1:
            using_symble = '<assistant><EXP><col_a>'
            replaced_list.append('[20]')
            symble_list.append('<assistant><EXP><col_a>')
        if key.find('<assistant><col_d><UNHAPPY>')!=-1:
            using_symble = '<assistant><col_d><UNHAPPY>'
            replaced_list.append('[20]')
            symble_list.append('<assistant><col_d><UNHAPPY>')
        if key.find('<+TRAIT>')!=-1:
            using_symble = '<+TRAIT>'
            replaced_list.append('[21]')
            symble_list.append('<+TRAIT>')
        if key.find('<!crowdgoal>')!=-1:
            using_symble = '<!crowdgoal>'
            replaced_list.append('[22]')
            symble_list.append('<!crowdgoal>')
        if key.find('<assistant>')!=-1:
            using_symble = '<assistant>'
            replaced_list.append('[23]')
            symble_list.append('<assistant>')
        if key.find('<col_d><-PAC>')!=-1:
            using_symble = '<col_d><-PAC>'
            replaced_list.append('[23]')
            symble_list.append('<col_d><-PAC>')
        if key.find('<col_a><-STR>')!=-1:
            using_symble = '<col_a><-STR>'
            replaced_list.append('[24]')
            symble_list.append('<col_a><-STR>')
        if key.find('<col_d><-TCK>')!=-1:
            using_symble = '<col_d><-TCK>'
            replaced_list.append('[25]')
            symble_list.append('<col_d><-TCK>')
        if key.find('<playername> <position>')!=-1:
            using_symble = '<playername> <position>'
            replaced_list.append('[26]')
            symble_list.append('<playername> <position>')
        if key.find('<nation>')!=-1:
            using_symble = '<nation>'
            replaced_list.append('[27]')
            symble_list.append('<nation>')




        if using_symble!='':
            # modified_text = key.replace(using_symble,'>>>')
            for index, replace_string in enumerate(replaced_list):
                modified_text = modified_text.replace(symble_list[index], replaced_list[index])
        #$relationship
        """hl -> tl"""
        url = self.build(modified_text)
        res = self.session.post(url=url, headers=self.headers, timeout=self.timeout)
        results = json.loads(res.content.decode(encoding='utf-8'))
        translated_string = results[0][0][0]
        if using_symble!='':
            # modified_text = translated_string.replace('>>>',using_symble)
            for index, replace_string in enumerate(replaced_list):
                translated_string = translated_string.replace(replaced_list[index], symble_list[index])
        print(f'{key}->{translated_string}')
        return translated_string

    def xml_doc(self,_path):
        print("Translate xml Started:"+_path)
        target_content = []
        with open(_path, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            for content in contents:
                if content.find("lang=\"en\"")!=-1:#找到需要翻译的特征符合lang="en"
                    key_word = content[content.find(">")+1:content.rfind("</")]
                    new_content = content.replace(key_word,self.translate(key_word))

                    target_content.append(new_content.replace("lang=\"en\"","lang=\"zh-cn\""))#添加中文特征符合
                    print("translated text:"+new_content)
                else:
                    target_content.append(content)
        with open(_path+".xml", 'w', encoding='utf-8') as f:
            f.writelines(target_content)

    def txt_doc(self, _path):
        print("Translate txt Started:"+_path)
        new_content = []
        with open(_path, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            for content in contents:
                new_content.append(content.replace(content,self.translate(content))+'\n')
        with open(_path+".txt", 'w', encoding='utf-8') as f:
            f.writelines(new_content)

    def txt_doc_giveitup3(self, _path):
        print("Translate txt Started:"+_path)
        new_content = []
        with open(_path, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            for content in contents:
                if content.find("		<value>")!=-1:
                    print(content)
                    start_text = content.find("		<value>")
                    end_text = content.find("</value>")
                    translate_string = content[start_text+len('		<value>'):end_text]
                    translate_back = False
                    if translate_string.find('#')!=-1:
                        translate_string = translate_string.replace("#",'..')
                        translate_back=True
                        modified_text = content.replace(translate_string.replace("..",'#'),self.translate(translate_string))+'\n'
                    elif translate_string.find('&')!=-1:
                        translate_string = translate_string.replace("&",'..')
                        translate_back=True
                        modified_text = content.replace(translate_string.replace("..",'&'),self.translate(translate_string))+'\n'
                    elif translate_string.find('+')!=-1:
                        translate_string = translate_string.replace("+",'..')
                        translate_back=True
                        modified_text = content.replace(translate_string.replace("..",'+'),self.translate(translate_string))+'\n'
                    #<assistant><col_d><UNHAPPY>
                    #<assistant><EXP><col_a>
                    else:
                        modified_text = content.replace(translate_string,self.translate(translate_string))+'\n'
                    if translate_back == True:
                        modified_text = modified_text.replace('..','#')
                        translate_back = False
                    new_content.append(modified_text)
                    print(modified_text)
                    time.sleep(2)
                else:
                    new_content.append(content+'\n')
        with open(_path+"."+self.target, 'w', encoding='utf-8') as f:
            f.writelines(new_content)

    def excel_manager_new_star(self, _path):
        for sheet_number in range(0,1):
            if os.path.exists(os.path.splitext(_path)[0]+'_translated'+os.path.splitext(_path)[-1])==False:
                shutil.copy(_path,os.path.splitext(_path)[0]+'_translated'+os.path.splitext(_path)[-1])
            modifying_file = os.path.splitext(_path)[0]+'_translated'+os.path.splitext(_path)[-1]
            app=xw.App(visible=False,add_book=False)
            wb=app.books.open(modifying_file)
            sheet=wb.sheets[sheet_number]
            ori_list = []
            tran_list = []
            if sheet_number == 0:#Core Text
                lines = 6000
                orignal_index = 6
                translate_index = 7

            elif sheet_number == 1:#Countries
                lines = 220
                orignal_index = 3
                translate_index = 4

            elif sheet_number == 2:#Continents
                lines = 10
                orignal_index = 2
                translate_index = 3

            elif sheet_number == 3:#Store MetaData
                lines = 60
                orignal_index = 3
                translate_index = 4

            elif sheet_number == 4:#Purchase MetaData
                lines = 70
                orignal_index = 3
                translate_index = 4

            elif sheet_number == 5:#Fake Ads
                lines = 15
                orignal_index = 3
                translate_index = 4

            elif sheet_number == 6:#Push Notifications
                lines = 10
                orignal_index = 3
                translate_index = 4

            elif sheet_number == 7:#Steam Specific
                lines = 320
                orignal_index = 2
                translate_index = 3

            elif sheet_number == 8:#Nintendo Specific
                lines = 380
                orignal_index = 2
                translate_index = 3

            elif sheet_number == 9:#PlayStation Specific
                lines = 380
                orignal_index = 2
                translate_index = 3

            for i in range(0,lines):
                ori_list.append(sheet[i,orignal_index].value)
                tran_list.append(sheet[i,translate_index].value)
            wb.save()
            wb.close()
            app.quit()
            # with open(os.path.dirname(os.path.realpath(__file__)) + "/ori_list.txt", "a") as f:
            #     for ori in ori_list:
            #         if ori == None:
            #             ori = ''
            #         f.writelines(str(ori)+'\n')
            # with open(os.path.dirname(os.path.realpath(__file__)) + "/tran_list.txt", "a") as f:
            #     for tran in tran_list:
            #         if ori == None:
            #             ori = ''
            #         f.writelines(str(tran)+'\n')
            # with open(os.path.dirname(os.path.realpath(__file__)) + "/ori_list.txt", "r") as f:
            #     context_ori = f.readlines()
            # with open(os.path.dirname(os.path.realpath(__file__)) + "/tran_list.txt", "r") as f:
            #     context_tran = f.readlines()
            # ori_list = []
            # tran_list = []
            # for i in context_ori:
            #     ori_list.append(i)
            # for i in context_tran:
            #     tran_list.append(i)
            is_file_open = False
            # wb就是新建的工作簿(workbook)，下面则对wb的sheet1的A1单元格赋值
            basic_line = 200 if lines>=200  else lines
            for loop in range(0, int(lines/basic_line)):
                app=xw.App(visible=True,add_book=False)
                wb=app.books.open(modifying_file)
                is_file_open = True
                for i in range(0,basic_line):
                    # if tran_list[i+loop*basic_line] =='None\n' and ori_list[i+loop*basic_line]!= '\n':
                    if tran_list[i+loop*basic_line] ==None and ori_list[i+loop*basic_line]!= None:
                        text = self.translate(ori_list[i+loop*basic_line])
                        print(f'{(i+loop*basic_line,translate_index+1)}:{ori_list[i+loop*basic_line]}->{text}')
                        wb.sheets[sheet_number].range((i+loop*basic_line+1,translate_index+1)).value = text
                if int(lines/basic_line) == loop+1:
                    for i in range(0,lines%200):
                    # if tran_list[i+loop*basic_line] =='None\n' and ori_list[i+loop*basic_line]!= '\n':
                        if tran_list[i+(loop+1)*basic_line] ==None and ori_list[i+(loop+1)*basic_line]!= None:
                            text = self.translate(ori_list[i+(loop+1)*basic_line])
                            print(f'{(i+(loop+1)*basic_line,translate_index+1)}:{ori_list[i+(loop+1)*basic_line]}->{text}')
                            wb.sheets[sheet_number].range((i+(loop+1)*basic_line+1,translate_index+1)).value = text
                wb.save()
                wb.close()
                app.quit()
    def brick_royal(self,_path):
        print("Translate txt Started:"+_path)
        new_content = []
        with open(_path, 'r', encoding='utf-8') as f:
            contents = f.readlines()
            for content in contents:
                translating_text = content[content.find(",")+1:]
                if translating_text!="":
                    new_content.append(content.replace(translating_text,self.translate(translating_text))+"\n")
                time.sleep(1)
        with open(_path+"."+self.target, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
def comparefiles(_path1, _path2):
    _path1_content = []
    _path2_content = []
    with open(_path1, 'r', encoding='utf-8') as f:
        _path1_content = f.readlines()
    with open(_path2, 'r', encoding='utf-8') as f:
        _path2_content = f.readlines()

    for thisindex , content1 in enumerate(_path1_content):
        content1_first_symbol_position = content1.find("\"")
        content1_next_symbol_position = content1.find("\"",content1_first_symbol_position+1)
        content1_keyword = content1[content1_first_symbol_position+1:content1_next_symbol_position]
        if content1_keyword=="":continue
        for index, content2 in enumerate(_path2_content):
            content2_first_symbol_position = content2.find("\"")
            content2_next_symbol_position = content2.find("\"",content2_first_symbol_position+1)
            content2_keyword = content2[content2_first_symbol_position+1:content2_next_symbol_position]
            if content1_keyword == content2_keyword:
                # print("found:"+content1_keyword)
                break
            # if index==len(_path2_content):
            # print("index="+str(index))
            # print("index="+str(index))
            # print("_path2_content="+str(len(_path2_content)))
            if index+1==len(_path2_content) and content1_keyword != content2_keyword:
                print("Missing["+str(thisindex)+"]:"+content1_keyword)
if __name__ == '__main__':
    comparefiles("/Users/batista/Desktop/English.txt", "/Users/batista/Desktop/chinese.txt")
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'zh-CN',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # mylist = os.listdir('./TranslateDoc/brick_royal')
    # for file_name in mylist:
    #     print(file_name)
    #     if file_name!=".DS_Store":
    #         gt.brick_royal('./TranslateDoc/brick_royal/'+file_name)



    #newstarmanager
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'zh-CN',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # # print(gt.translate(f"MISTER DOPEY!¦$clubname player $playername has received a $banlength match ban after testing positive for performance enhancing drugs! #BAN"))
    # gt.excel_manager_new_star('./Manager Translation Package 16680 INCLUDING CONVERTER_translated_V5.xlsx')






    # main()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'zh-CN',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # gt.txt_doc_giveitup3('/Users/batista/Desktop/demo/Language.en.txt')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'zh_TW',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # gt.txt_doc_giveitup3('/Users/batista/Desktop/demo/Language.en.txt')


    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'zh_HK',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # gt.txt_doc_giveitup3('/Users/batista/Desktop/demo/Language.en.txt')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'ja',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # gt.txt_doc_giveitup3('/Users/batista/Desktop/demo/Language.en.txt')

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-orgin', '--o'  , type = str, default = 'en', help = 'orginal text, 中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # parser.add_argument('-target','--t'  , type = str, default = 'ko',    help = 'target text,  中文:zh-CN, 英语:en, 繁体中文台湾:zh_TW, 繁体中文香港:zh_HK, 繁体中文新加坡:zh_HK, 俄语:ru, 日语:ja, 德语:de, 法语:fr, 韩语:ko, 泰语:th, 意大利语言:it')
    # args = parser.parse_args()
    # gt = GoogleTranslator(oringal= args.o, target=args.t)
    # gt.txt_doc_giveitup3('/Users/batista/Desktop/demo/Language.en.txt')
    # gt_en_to_zhCN = GoogleTranslator(oringal= 'en', target='zh-CN')
    # gt_en_to_zhCN.xml_doc('./demo_translate_files/demo.xml')

    # gt_znCN_to_en = GoogleTranslator(oringal= 'zh-CN', target='en')
    # gt_znCN_to_en.txt_doc('./demo_translate_files/demo.txt')