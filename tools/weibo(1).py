import time
import requests
from requests.adapters import HTTPAdapter
# from bs4 import BeautifulSoup
from pandas import DataFrame as df
import emoji

queue_list = Queue()

class weibo:
    def __init__(self):
        self.headers_list = [#{'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36',
                             # 'cookie':'_T_WM=13900148534; SUB=_2A25ze0yUDeRhGeBK71MU9S7LyDuIHXVQhFTcrDV6PUJbkdAKLUXVkW1NR9Zyhy3zGsDUnkBaFOwvRM-CeBkAMPgs; SUHB=0S7yLu3tZw9gj2; SCF=ArBMGSMh5xDqDUocWgkGlcbd5qj9MftgNqsiQ5nWdW-q7DM0czvEC4-0vTglLybXwf6xPq17Utvi7eFS1_ntqdY.; SSOLoginState=1585396932; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; WEIBOCN_FROM=1110106030'}]
                            {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                              'cookie':'_T_WM=ab0eb50bb8323851d8573a562b2565e0; SUB=_2A25zeGmaDeRhGeBK6FMY-SjFzDyIHXVQg3fSrDV6PUJbkdAKLWr1kW1NR8Sw9zWVMFPdKV2ZehMH7A6UO8_f5YJm; SUHB=0KABpeaMBUK2-H; SCF=AntTcSbwL33mAxZLom3fUqKOqazVX8oPi3rHkWONatD4FZZeDB3BnSug3-8ZXJCtAKTOLHvnW7BHdL96dhvSh3A.; SSOLoginState=1585191371'}]
                            # {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                            #  'cookie':'_T_WM=531dd56c1cf7cf416325d73101868315; SUB=_2A25zfw8TDeRhGeBK6FMY-SjFzDyIHXVQg5FbrDV6PUJbkdAKLVjwkW1NR8Sw94IGClw2qabbSVWaOk44q0XNVWA3; SUHB=0V5VzXM0HL488U; SCF=Ah3dKslr_VJtg8KidPScW8el0kOQaNxQ1-B81bydF-otB_VvryydbNn1wGbhh0t1hhzNUNPnHWz7x2a2wF5fj0s.; SSOLoginState=1585151811'},
                            # {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                            #  'cookie': '_T_WM=531dd56c1cf7cf416325d73101868315; SUB=_2A25zfw8TDeRhGeBK6FMY-SjFzDyIHXVQg5FbrDV6PUJbkdAKLVjwkW1NR8Sw94IGClw2qabbSVWaOk44q0XNVWA3; SUHB=0V5VzXM0HL488U; SCF=Ah3dKslr_VJtg8KidPScW8el0kOQaNxQ1-B81bydF-otB_VvryydbNn1wGbhh0t1hhzNUNPnHWz7x2a2wF5fj0s.'}]
                           #  {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCW48cVg58tnDzcbYhhert4p1r51cX20Xb6dgCLwayCTc.; SUB=_2A25ze9-MDeRhGeFK61oY8S7KyzSIHXVQh-HErDV6PUJbktANLXLRkW1NQ44DJTcOTo0UwOFbR-jQBGZNoAnPKiui; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh6yOvjU..lNh_kuvN-AAzI5JpX5KzhUgL.FoMXehn4eK5cehn2dJLoI7vAIs8Vi--4iK.EiK.EUgQt; SUHB=0KAx4U2xIKR5Bq; SSOLoginState=1585426396; M_WEIBOCN_PARAMS=lfid%3D106003type%253D1%26luicode%3D20000174'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCyOU1D3hTbKk8pq8GAC-u5lhBXGkQ2G8Wg0CxTJF0Bhw.; SUB=_2A25ze8AEDeRhGeFK61oZ8irJzjuIHXVQh-BMrDV6PUJbktANLVj1kW1NQ45EYQ_tvgPjH_hTHgbTlOauZvAICCS6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZd2kTaDaNk.-4MTm8DQID5JpX5KzhUgL.FoMXehnReoBfSKM2dJLoIpWVIg8VMgLVi--Ri-i8iKLF; SUHB=0V5lidx9eVjzD5; SSOLoginState=1585426516; M_WEIBOCN_PARAMS=lfid%3D106003type%253D1%26luicode%3D20000174'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                              #'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCD8m4W3_iBGI5x1-U-DQZbY1wvTrD8oV8HUAqFFfNxIQ.; SUB=_2A25ze8CYDeRhGeFK61oS-C_KwjuIHXVQh-DQrDV6PUJbktANLWXwkW1NQ44D6SBwVOqt7Mo9-A0R35ZdNvgfPS0h; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5d.3EW4Q6IGLCbJWrJ0N9Z5JpX5KzhUgL.FoMXehn01h2c1KM2dJLoI08xSfeXi--ciKyFiK.Xi--4i-iFiK.pi--ciKyhi-8Wi--fiK.piK.7i--fi-zRi-i2; SUHB=0ebtnJQUgT2xjK; SSOLoginState=1585426632; M_WEIBOCN_PARAMS=lfid%3D106003type%253D1%26luicode%3D20000174'},
                             #{'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                            #  'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCxkzFzz069_yG8ilp314M0tTck4ZOXb7PZ7VIttmS2yM.; SUB=_2A25ze8FPDeRhGeFK61oS-C_Lzj6IHXVQh-8HrDV6PUJbktANLWbWkW1NQ44D90NielNX0Onp5kP4k46qb-tHf466; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W51UUAGnzPTokhAnB_YFe5C5JpX5KzhUgL.FoMXehn01h2NSKz2dJLoIE7LxK-L1KeL1hLbqCH8SEHWBEHWBcSQUg8V9EH8SFHFBb-RxCH8SC-RxF-4S7tt; SUHB=0y0ZLmb_ZjmVgy; SSOLoginState=1585426719; M_WEIBOCN_PARAMS=lfid%3D106003type%253D1%26luicode%3D20000174'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCRfLBX6hcek-WyVNEeM0MQXGKMd4eTBa1DEqUlGB_5Ho.; SUB=_2A25ze8EiDeRhGeFK61oT-SvLzjSIHXVQh-9qrDV6PUJbktANLVnRkW1NQ45EFUqEy9ZdCLgpuJ1xsQpMJAkQ3Zh3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFZr1BiJHp5s.dViazIl0Ms5JpX5KzhUgL.FoMXehnE1K-NSKn2dJLoI7D7qgLXUgR7ShqR; SUHB=0jBIOfHSTcZiOF; SSOLoginState=1585426802; M_WEIBOCN_PARAMS=lfid%3D106003type%253D1%26luicode%3D20000174'},
                             #{'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                            #  'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCRfLBX6hcek-WyVNEeM0MQXGKMd4eTBa1DEqUlGB_5Ho.; SUB=_2A25ze8EiDeRhGeFK61oT-SvLzjSIHXVQh-9qrDV6PUJbktANLVnRkW1NQ45EFUqEy9ZdCLgpuJ1xsQpMJAkQ3Zh3; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFZr1BiJHp5s.dViazIl0Ms5JpX5KzhUgL.FoMXehnE1K-NSKn2dJLoI7D7qgLXUgR7ShqR; SUHB=0jBIOfHSTcZiOF; SSOLoginState=1585426802; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D106003type%253D1'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SSOLoginState=1585427087; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfC6LSc0FlGK6oqoLPcm2yaFVUfejS2VbmfUT42DSsGkLc.; SUB=_2A25ze8LfDeRhGeFN7FAV-C_OzDyIHXVQh-6XrDV6PUJbktAKLUbmkW1NQ_VrUGL7pxuL04EMppxAyZbdf6euNb1K; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhCPgNbcPyjn5mAGZ9PO_aM5JpX5KzhUgL.FoM0S0zX1h2ES052dJLoI7LV9Px4Ig4rSKMt; SUHB=010GdwTp-A-zOR; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26fid%3D106003type%253D1%26uicode%3D10000011'},
                             #{'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfC_zpPWYHHLiquwoCodb3m4DhGVbDHjvdhFlrrIuoM5p0.; SUB=_2A25ze8NhDeRhGeFN7FMW9irLyj-IHXVQh-0prDV6PUJbktAKLWLakW1NQ_fJ3RRH9p4NQ1f-gUqRqDLNuHG2eIFo; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFcZuGDdU8E.z9xV-TfBL365JpX5KzhUgL.FoM0S02NSoBNeKe2dJLoIEXLxKBLB.eLB-2LxKqLBoML1K2LxK-LBK-LBoeLxK-LBo.LBonLxKBLB.2L1K2t; SUHB=0laFJVcwgF5Yvm; SSOLoginState=1585427249; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCKVvBvI7YADsBDJud9xlsaq6yCBwgewTi6A16gZRhfmc.; SUB=_2A25ze8PHDeRhGeFN7FAT9yrEwz-IHXVQh-2PrDV6PUJbktANLVankW1NQ_VaTJCEtPU10AQ7w82T9nSMWZhWL3s1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFbG555UUDEkB_pB984.xR75JpX5KzhUgL.FoM0S0zES0BR1he2dJLoI07LxK-LBKBL1K-LxK.LBKzL1-eLxKnL12zLBK-LxKqLBozL1K5LxK-L1h.LBo-LxKBLB.qLBoyXMJLJUgRt; SUHB=0qj08njJrhT3cq; SSOLoginState=1585427351; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; WEIBOCN_FROM=1110106030'},
                          #   {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCWL03yvpGYK5pqShnzUlN-IdeEObnUTHTiRtYQDaS60g.; SUB=_2A25ze8R4DeRhGeFN7FAR9SzMwz2IHXVQh-wwrDV6PUJbktAKLVLBkW1NQ_Z0_pAibMosCwGeo7kgyJzrrhSx4d8z; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5CPboJV.bZLFDw8H7ESAWC5JpX5KzhUgL.FoM0S0z7SKz71h22dJLoIEjLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1heL1h-LxK-LBo5L1h8KC281CHSS; SUHB=02MvpoSV6QYvsK; SSOLoginState=1585427497; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                           #  {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                           #   'cookie': '_T_WM=12164679619; MLOGIN=1; SSOLoginState=1585427580; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCeXTFQyrSk0m_dMId0AYy4b0jE0j5A8_AeWJEwrfs4gg.; SUB=_2A25ze8QsDeRhGeFN7FAT9yzEyTuIHXVQh-xkrDV6PUJbktANLWbCkW1NQ_VdIzVPY7OX6757QhvCp5J6LACvVwIh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhcLuyGJjDyEEJS2KNu9BmJ5JpX5KzhUgL.FoM0S0zES0zReoM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNe0MEeoME1hzN; SUHB=0HThh-OEzD1jBB; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                          #   {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                             # 'cookie': '_T_WM=12164679619; MLOGIN=1; SSOLoginState=1585427658; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCRiijSVE-0t3CcDnXRHPbH_ZyIJ-sxeZONej-k3Uqx0Q.; SUB=_2A25ze8SaDeRhGeFN7FAT9ifEzzmIHXVQh-zSrDV6PUJbktANLWz_kW1NQ_VWcnjcdF2nfkBiCteegCQn_vmd5VDn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhuahdOiJZ1O0d8mJmfxuCF5JpX5KzhUgL.FoM0S0zESo.RSh-2dJLoIpRLxK-LB.qL1hqLxK-LBo5L1KnLxKBLBonLBo9jqPMt; SUHB=0BLokINhuSUaVY; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                           #  {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                           #   'cookie': '_T_WM=12164679619; MLOGIN=1; SUHB=0z1Aw7pJmQCXXR; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCzd7XnqOw6fEKfGuTPiu7ji9yD1wnm9Lw_ALnlJ2KxJk.; SUB=_2A25ze8V-DeRhGeFN7FAR8y_NwjWIHXVQh-s2rDV6PUJbktANLXngkW1NQ_e41nABgQh7zFgemFgdWsmC3NcNIr2-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWouwkSimn2R7hs24TzppT65JpX5KzhUgL.FoM0S0z7e02p1K.2dJLoI7HkUc2EeBtt; SSOLoginState=1585427758; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                          #   {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                            #  'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfC--kkExIxJHmDM79mpQcqIlFSdbn49jwPfvr2hgnz8E0.; SUB=_2A25ze8UmDeRhGeFN7FAS8SjOzTyIHXVQh-turDV6PUJbktCOLRfXkW1NQ_UdG2ZeiSRMxhtZ8FxDPuWj_8oDKNcK; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWB9R7HX5d4vo.xXMo5eHm35JpX5KzhUgL.FoM0S0z0eKqESo52dJLoIEBLxKMLB.BL1KnLxKnL12qLBo5LxKnL12-LB-zLxKqLB-qL1K-t; SUHB=02MvprILuQYvsK; SSOLoginState=1585427830; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; WEIBOCN_FROM=1110106030'},
                           #  {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                           #   'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCbDSIzVhn1uIKgMLgchWiEL_RLgCT94Sq-AMeay0UbJI.; SUB=_2A25ze8WXDeRhGeFN7FAT9i3EzzSIHXVQh-vfrDV6PUJbktANLWTGkW1NQ_VBKiK-Svy3mY0xY3ppd6uFxhYjW418; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5hf0Mv5MS1S0_voqwKlm1v5JpX5KzhUgL.FoM0S0zESoeRShn2dJLoIEHSwHvk-cvKi--Xi-zRi-2Ei--Xi-zRi-2Ei--Xi-zRi-zcds8N; SUHB=0auAAXRGl0iY4E; SSOLoginState=1585427912; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},
                            # {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Mobile Safari/537.36',
                            #  'cookie': '_T_WM=12164679619; MLOGIN=1; SCF=AngUhlfziZsUSdMRTV1SesE8ZF3GbFJM1OblpevMJnfCuK9FxJpIILsMI5feWsQbo_bJbuR4M6ShmLnlyxjfDH8.; SUB=_2A25ze8ZcDeRhGeFN7FAT9ifIzjiIHXVQh-oUrDV6PUJbktANLXLBkW1NQ_VVekXC82i9ehAGRUV2fAeJjKAJqvOD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhsozF5AeIbK8y8wSYUxc1M5JpX5KzhUgL.FoM0S0zESo.XSKB2dJLoIE.LxK-L12BL1KMLxK-LBoMLBoMLxKqL1KMLBKMLxKBLB.2LB.8CKhHrBBtt; SUHB=0TPVOaXO4ijujw; SSOLoginState=1585427980; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803'},

        self.keywords = ""
        self.final_data = df()
        self.proxs = ['218.95.50.148', '219.146.127.6', '117.69.12.26', '117.69.13.65', '182.35.80.6',
                      '113.121.39.49', '183.209.23.41', '117.85.166.36', '180.118.128.222', '110.243.14.218',
                      '58.18.133.101', '125.108.109.117', '182.35.85.215', '113.124.87.65', '113.195.20.143',
                      '183.166.97.166', '180.118.128.112', '60.13.42.151', '182.149.83.194', '60.205.132.71'
                      ]

    def get_weibo(self):
        self.keywords = input("请输入关键词：")
        self.date = input("请输入查询日期（例如：20200328）：")
        print("正在爬取...")
        rs = requests.Session()
        rs.mount('http://', HTTPAdapter(max_retries=5))
        rs.mount('https://', HTTPAdapter(max_retries=5))
        content_list = []
        name_list = []
        gender_list = []
        loc_list =[]
        count = 0
        cnt = 0
        c_cnt = 0
        for i in range(1, 100):
            if cnt == 500:
                break
            rs.proxies = {'HTTP': str(self.proxs[count % 1]) + ': HTTP'}
            res = rs.get(
                "https://weibo.cn/search/mblog?hideSearchFrame=&keyword="
                + self.keywords + "&advancedfilter=1&starttime=" + self.date + "&endtime=" + self.date + "&sort=hot&page="
                + str(i), headers=self.headers_list[count % 1])
            count = count + 1
            res.encoding = "UTF-8"
            bs = BeautifulSoup(res.text, "html.parser")
            contents = bs.find_all('span', class_='ctt')
            href_list = bs.find_all('a', class_='nk')

            for content in contents:
                c_cnt += 1
                content_list.append(emoji.demojize(content.text[1:]))

                if c_cnt == 500:
                    break

            for href in href_list:
                name = href.text
                name_list.append(name)
                cnt += 1

                rs.proxies = {'HTTP': str(self.proxs[count % 1]) + ': HTTP'}
                info_res = rs.get(href.get('href'), headers=self.headers_list[count % 1])
                count = count + 1
                info_res.encoding = "UTF-8"
                info_bs = BeautifulSoup(info_res.text, "html.parser")
                ctt = info_bs.find('span', class_='ctt')
                print(cnt, ctt)
                district = ctt.text[:-8].split("/")[1]
                gender = ctt.text[:-8].split("/")[0][-1]
                gender_list.append(gender)
                loc_list.append(district)
                time.sleep(1)

                if cnt == 500:
                    break

            print("\n 已完成 %-4.1f" % (cnt * 100 / 500) + '%\n', end="")

        final_dict = {
            "name": name_list,
            "gender": gender_list,
            "location": loc_list,
            "content": content_list
        }

        csvname = self.keywords + "_" + self.date
        self.final_data = df(final_dict)
        self.final_data.to_csv(csvname + '.csv')


def main():
    a = weibo()
    a.get_weibo()


if __name__ == "__main__":
    main()
