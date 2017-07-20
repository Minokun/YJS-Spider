# 用于md5加密
# @param str 字符串
# @return str 字符串
# @author WuXiaokun
def md5(src):
    import hashlib
    hash = hashlib.md5()
    hash.update(src.encode('utf-8'))
    return hash.hexdigest()