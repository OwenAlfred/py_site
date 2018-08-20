# coding=gbk

# coding=utf-8

#-*- coding: UTF-8 -*-

from .CCPRestSDK import REST
# import ConfigParser
try:
    import configparser
except:
    from six.moves import configparser


# Ö÷ÕÊºÅ
accountSid = '8aaf07086521916801652828c5a7054a'

# Ö÷ÕÊºÅToken
accountToken = 'c1f723b195d348f6ae6d610ff18fe105'

# Ó¦ÓÃId
appId = '8aaf07086521916801652828c5f80550'

# ÇëÇóµØÖ·£¬¸ñÊ½ÈçÏÂ£¬²»ÐèÒªÐ´http://
serverIP = 'sandboxapp.cloopen.com'

# ÇëÇó¶Ë¿Ú
serverPort = '8883'

# REST°æ±¾ºÅ
softVersion = '2013-12-26'

# ·¢ËÍÄ£°å¶ÌÐÅ
# @param to ÊÖ»úºÅÂë
# @param datas ÄÚÈÝÊý¾Ý ¸ñÊ½ÎªÊý×é ÀýÈç£º{'12','34'}£¬Èç²»ÐèÌæ»»ÇëÌî ''
# @param $tempId Ä£°åId

# def sendTemplateSMS(to,datas,tempId):


#     #³õÊ¼»¯REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)

#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():

#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print ('%s:%s' % (k, s))
#         else:
#             print ('%s:%s' % (k, v))


# sendTemplateSMS(ÊÖ»úºÅÂë,ÄÚÈÝÊý¾Ý,Ä£°åId)

class CCP(object):
    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, '_instance'):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):

        # ³õÊ¼»¯REST SDK
        result = self.rest.sendTemplateSMS(to, datas, tempId)

        # for k, v in result.items():
        #     if k == 'templateSMS':
        #         for k, s in v.items():
        #             print ('%s:%s' % (k, s))
        #     else:
        #         print ('%s:%s' % (k, v))

        if '000000' == result['statusCode']:
            return True
        return False


ccp = CCP.instance()

if __name__ == '__main__':
    ccp.sendTemplateSMS('173xxxx1782', ['666666', 3], 1)
