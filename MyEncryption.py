class MyEncryption:
    encode_key = 'uldruldruldr'
    re_decode = False
    
    @staticmethod
    def reset():
        MyEncryption.encode_key = 'uldruldruldr'
        MyEncryption.re_decode = False
    
    @classmethod
    def decodeKeyGenerate(cls, en_keys):
        factory = {'u':'d','d':'u','l':'r','r':'l'}
        de_keys = ''
        for k in en_keys[::-1]:
            de_keys += factory[k]
        return de_keys
        
    @classmethod
    def __disorganize(cls, pre_list, keys):
        special_key = {
            'u':{2:12,3:20,4:28,8:4,9:11,10:19,11:27,12:33,16:3,17:10,18:18,19:26,20:32,24:2,25:9,26:17,27:25,28:31,31:8,32:16,33:24},
            'l':{0:9,1:17,2:25,5:2,6:8,7:16,8:24,9:31,13:1,14:7,15:15,16:23,17:30,21:0,22:6,23:14,24:22,25:29,29:5,30:13,31:21}
        }
        def inner(text,key):
            in_text = text + ['sample']
            for i, j in enumerate(text):
                target_pos = special_key[key].get(i, i)
                    
                in_text[target_pos] = j
            return in_text[:-1]
        # replace
        keys_rev = {'r':'lll', 'd':'uuu'}
        for tar, val in keys_rev.items():
            keys = keys.replace(tar, val)
            # del repeat
            keys = keys.replace('uuuu', '')
            keys = keys.replace('llll', '')
        # encode
        for k in keys:
            pre_list = inner(pre_list, k)
            
        return pre_list
        
    @classmethod
    def encode(cls, text):
        lst = list(map(int, list(''.join(map(lambda x: '0' * (8 - len(x)) + x, map(lambda x: str(bin(ord(x)))[2:], list(text)))))))
        # 补0（34n）
        lst = [0] * ((34 - len(lst)) % 34) + lst
        group = []
        for i in range(0, len(lst), 34):
            group.append(cls.__disorganize(lst[i : i + 34], MyEncryption.encode_key))
        group = ''.join(map(lambda x: ''.join(map(str, x)), group))
        group = '0' * (6 - len(group) % 6) + group
        return ''.join(chr(48 + int(group[i : i + 6], 2)) for i in range(0, len(group), 6))
        
    @classmethod
    def decode(cls, text):
        asc = ''.join(list(map(lambda x: '0' * (6 - len(x)) + x, list(map(lambda x: bin(ord(x) - 48)[2:], list(text))))))
        asc = asc[len(asc) % 34:]
        asc = [asc[i : i + 34] for i in range(0, len(asc), 34)]
        turning = []
        for i in asc:
            turning.append(cls.__disorganize(list(i), MyEncryption.decodeKeyGenerate(MyEncryption.encode_key) if MyEncryption.re_decode else MyEncryption.encode_key))
        asc = ''.join(map(''.join, turning))
        idx = asc.find('1')
        asc = asc[idx - (idx - len(asc)) % 8:]
        return ''.join(chr(int(asc[i : i + 8], 2)) for i in range(0, len(asc), 8))
    

m = 'Manners maketh man'
res = MyEncryption.encode(m)
print(res)

d = MyEncryption.decode(res)
print(d)
# ----------Others Example-------------
print('-'*50)
m = '114514'
MyEncryption.re_decode = True
MyEncryption.encode_key = 'uldrrdul'

res = MyEncryption.encode(m)
print(res)

d = MyEncryption.decode(res)
print(d)
MyEncryption.reset()

