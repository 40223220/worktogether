#@+leo-ver=5-thin
#@+node:2014fall.20141212095015.1775: * @file wsgi.py
# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝


#@@language python
#@@tabwidth -4

#@+<<declarations>>
#@+node:2014fall.20141212095015.1776: ** <<declarations>> (wsgi)
import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random
# 導入 gear 模組
import gear

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"

'''以下為近端 input() 與 for 迴圈應用的程式碼, 若要將程式送到 OpenShift 執行, 除了採用 CherryPy 網際框架外, 還要轉為 html 列印
# 利用 input() 取得的資料型別為字串
toprint = input("要印甚麼內容?")
# 若要將 input() 取得的字串轉為整數使用, 必須利用 int() 轉換
repeat_no = int(input("重複列印幾次?"))
for i in range(repeat_no):
    print(toprint)
'''
#@-<<declarations>>
#@+others
#@+node:2014fall.20141212095015.1777: ** class Hello
################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Hello(object):

    # Hello 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    #@+others
    #@+node:2014fall.20141212095015.2004: *3* __init__
    def __init__(self):
        # 配合透過案例啟始建立所需的目錄
        if not os.path.isdir(data_dir+'/tmp'):
            os.mkdir(data_dir+'/tmp')
        if not os.path.isdir(data_dir+"/downloads"):
            os.mkdir(data_dir+"/downloads")
        if not os.path.isdir(data_dir+"/images"):
            os.mkdir(data_dir+"/images")
    #@+node:2015.20150330144929.1713: *3* CheckGearSize
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def CheckGearSize(self, n_g1=15, n_g2=24,M=5, P=15):

         n_g1 = int(str(n_g1))
         n_g2 = int(str(n_g2))

         if n_g1 < 15:
            return "齒輪1 低於15" + self.DesignGear()
         elif n_g1 > 80:
            return "齒輪1 超過80 " + self.DesignGear()
         elif n_g2 < 15:
            return "齒輪2 低於15 " + self.DesignGear()
         elif n_g2 > 80:
            return "齒輪2 超過80 " + self.DesignGear()
         else:
            cherrypy.session['g1'] =  n_g1
            cherrypy.session['g2'] =  n_g2
            
            outstring = '''
                <!DOCTYPE html> 
                <html>
                <head>
                齒輪1='''+str(n_g1)+'''<br />
                齒輪2='''+str(n_g2)+'''<br />
                <br /><a href="\ShowGear\">繪製齒輪</a><br />
                <br /><a href="\DesignGear\">重新設計</a><br />
                <head>
                </html>
            '''
            return outstring
    #@+node:2015.20150627113431.1: *3* CheckGearSize1
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def CheckGearSize1(self, n_g1=15, n_g2=24,n_g3=24,n_g4=15,M=5, P=15):

         n_g1 = int(str(n_g1))
         n_g2 = int(str(n_g2))
         n_g3 = int(str(n_g3))
         n_g4 = int(str(n_g4))

         if n_g1 < 15:
            return "齒輪1 低於15" + self.DesignGear1()
         elif n_g1 > 80:
            return "齒輪1 超過80 " + self.DesignGear1()
         elif n_g2 < 15:
            return "齒輪2 低於15 " + self.DesignGear1()
         elif n_g2 > 80:
            return "齒輪2 超過80 " + self.DesignGear1()
         elif n_g3 < 15:
            return "齒輪3 低於15" + self.DesignGear1()
         elif n_g3 > 80:
            return "齒輪3 超過80 " + self.DesignGear1()
         elif n_g4 < 15:
            return "齒輪4 低於15 " + self.DesignGear1() 
         elif n_g4 > 80:
            return "齒輪4 超過80 " + self.DesignGear1()
         elif n_g2!=n_g3:
            return "齒輪2跟齒輪3齒數不同可能會有干涉的問題 " + self.DesignGear1()  
         else:
            cherrypy.session['g1'] =  n_g1
            cherrypy.session['g2'] =  n_g2
            cherrypy.session['g3'] =  n_g3
            cherrypy.session['g4'] =  n_g4
            
            outstring = '''
                <!DOCTYPE html> 
                <html>
                <head>
                齒輪1='''+str(n_g1)+'''<br />
                齒輪2='''+str(n_g2)+'''<br />
                齒輪3='''+str(n_g3)+'''<br />
                齒輪4='''+str(n_g4)+'''<br />
                <br /><a href="\ShowGear1\">繪製齒輪</a><br />
                <br /><a href="\DesignGear1\">重新設計</a><br />
                <head>
                </html>
            '''
            return outstring
    #@+node:2014fall.20141212095015.1778: *3* index_orig
    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index_orig(self, toprint="a_40223220"):
        return toprint
    #@+node:2014fall.20141212095015.1779: *3* hello
    @cherrypy.expose
    def hello(self, toprint="Hello World!"):
        return toprint
    #@+node:2014fall.20141215194146.1791: *3* index
    @cherrypy.expose
    def index(self, guess=None):
        # 將標準答案存入 answer session 對應區
        theanswer = random.randint(1, 100)
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        cherrypy.session['answer'] = theanswer
        cherrypy.session['count'] = thecount
        # 印出讓使用者輸入的超文件表單
        outstring = '''
    a_40223220
    '''

        return outstring
    #@+node:2015.20150615085301.1: *3* index1
    @cherrypy.expose
    def index1(self, guess=None):
        # 將標準答案存入 answer session 對應區
        theanswer = random.randint(1, 100)
        thecount = 0
        # 將答案與計算次數變數存進 session 對應變數
        cherrypy.session['answer'] = theanswer
        cherrypy.session['count'] = thecount
        # 印出讓使用者輸入的超文件表單
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=POST action=doCheck>
    請輸入您所猜的整數:<input type=text name=guess><br />
    <input type=submit value=send>
    </form>
    <hr>
    <!-- 以下在網頁內嵌 Brython 程式 -->
    <script type="text/python">
    from browser import document, alert

    def echo(ev):
        alert(document["zone"].value)

    # 將文件中名稱為 mybutton 的物件, 透過 click 事件與 echo 函式 bind 在一起
    document['mybutton'].bind('click',echo)
    </script>
    <input id="zone"><button id="mybutton">click !</button>
    <hr>
    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    import math

    # 畫布指定在名稱為 plotarea 的 canvas 上
    # 以下使用中文變數名稱
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    # 用紅色畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(0, 500)
    ctx.strokeStyle = "red"
    ctx.stroke()

    # 用藍色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 0)
    ctx.strokeStyle = "blue"
    ctx.stroke()

    # 用綠色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 500)
    ctx.strokeStyle = "green"
    ctx.stroke()

    # 用黑色畫一個圓
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.strokeStyle = "black"
    ctx.arc(250,250,50,0,2*math.pi)
    ctx.stroke()
    </script>
    <canvas id="plotarea" width="800" height="600"></canvas>
    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150331094055.1733: *3* DesignGear
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def DesignGear(self, n_g1=15, n_g2=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <form method=\"post\" action=\"CheckGearSize\">
    <fieldset>

    齒數1(範圍:15~80):<input type=text name=n_g1 value='''+str(n_g1)+'''><br />
    齒數2(範圍:15~80):<input type=text name=n_g2 value = '''+str(n_g2)+'''><br />

    <input type=\"submit\" value=\"繪製齒輪\">
    </form>
    </body>
    </html>
    '''
      
        return outstring
    #@+node:2015.20150622102244.1: *3* DesignGear1
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def DesignGear1(self, n_g1=15, n_g2=24,n_g3=24,n_g4=15,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=\"post\" action=\"CheckGearSize1\">
    <fieldset>
     <legend>齒輪2跟齒輪3齒數需相同不然可能會有干涉的問題:</legend>
     
    齒輪1(範圍:15~80):<input type=text name=n_g1 value='''+str(n_g1)+'''><br />
    齒輪2(範圍:15~80):<input type=text name=n_g2 value='''+str(n_g2)+'''><br />
    齒輪3(範圍:15~80):<input type=text name=n_g3 value='''+str(n_g3)+'''><br />
    齒輪4(範圍:15~80):<input type=text name=n_g4 value='''+str(n_g4)+'''><br />


    <input type=\"submit\" value=\"繪製齒輪\">
    </form>
    </body>
    </html>
    '''
      
        return outstring
    #@+node:2015.20150622011853.1: *3* threeDgear1
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def threeDgear1(self, N1=15, N2=24,N3=24,N4=24,N5=24,N6=24,N7=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
        
    <form method=\"post\" action=\"mygeartest3\">
    <fieldset>

    齒數1(範圍:15~80):<br /><input type=\"text\" name=\"N1\"><br />
    齒數2(範圍:15~80):<br /><input type=\"text\" name=\"N2\"><br />
    齒數3(範圍:15~80):<br /><input type=\"text\" name=\"N3\"><br />
    齒數4(範圍:15~80):<br /><input type=\"text\" name=\"N4\"><br />
    齒數5(範圍:15~80):<br /><input type=\"text\" name=\"N5\"><br />
    齒數6(範圍:15~80):<br /><input type=\"text\" name=\"N6\"><br />
    齒數7(範圍:15~80):<br /><input type=\"text\" name=\"N7\"><br />


    <input type=\"submit\" value=\"send\">
    </form>
    </body>
    </html>
    '''
      
        return outstring
    #@+node:2015.20150330144929.1762: *3* do2Dgear
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def do2Dgear(self, N=20, M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    import math

    # 畫布指定在名稱為 plotarea 的 canvas 上
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    # 用紅色畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    '''
        outstring += '''
    ctx.moveTo('''+str(N)+","+str(M)+")"
        outstring += '''
    ctx.lineTo(0, 500)
    ctx.strokeStyle = "red"
    ctx.stroke()

    # 用藍色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 0)
    ctx.strokeStyle = "blue"
    ctx.stroke()

    # 用綠色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 500)
    ctx.strokeStyle = "green"
    ctx.stroke()

    # 用黑色畫一個圓
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.strokeStyle = "black"
    ctx.arc(250,250,50,0,2*math.pi)
    ctx.stroke()
    </script>
    <canvas id="plotarea" width="800" height="600"></canvas>
    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150331094055.1735: *3* do3Dgear
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def do3Dgear(self, N=20, M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">
    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    import math

    # 畫布指定在名稱為 plotarea 的 canvas 上
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    # 用紅色畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    '''
        outstring += '''
    ctx.moveTo('''+str(N)+","+str(M)+")"
        outstring += '''
    ctx.lineTo(0, 500)
    ctx.strokeStyle = "red"
    ctx.stroke()

    # 用藍色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 0)
    ctx.strokeStyle = "blue"
    ctx.stroke()

    # 用綠色再畫一條直線
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.moveTo(0, 0)
    ctx.lineTo(500, 500)
    ctx.strokeStyle = "green"
    ctx.stroke()

    # 用黑色畫一個圓
    ctx.beginPath()
    ctx.lineWidth = 3
    ctx.strokeStyle = "black"
    ctx.arc(250,250,50,0,2*math.pi)
    ctx.stroke()
    </script>
    <canvas id="plotarea" width="800" height="600"></canvas>
    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150330144929.1765: *3* mygeartest
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest(self, N=20, M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    def create_line(x1, y1, x2, y2, width=3, fill="red"):
    	ctx.beginPath()
    	ctx.lineWidth = width
    	ctx.moveTo(x1, y1)
    	ctx.lineTo(x2, y2)
    	ctx.strokeStyle = fill
    	ctx.stroke()

    # 導入數學函式後, 圓周率為 pi
    # deg 為角度轉為徑度的轉換因子
    deg = pi/180.
    #
    # 以下分別為正齒輪繪圖與主 tkinter 畫布繪圖
    #
    # 定義一個繪正齒輪的繪圖函式
    # midx 為齒輪圓心 x 座標
    # midy 為齒輪圓心 y 座標
    # rp 為節圓半徑, n 為齒數
    def 齒輪(midx, midy, rp, n, 顏色):
        # 將角度轉換因子設為全域變數
        global deg
        # 齒輪漸開線分成 15 線段繪製
        imax = 15
        # 在輸入的畫布上繪製直線, 由圓心到節圓 y 軸頂點畫一直線
        create_line(midx, midy, midx, midy-rp)
        # 畫出 rp 圓, 畫圓函式尚未定義
        #create_oval(midx-rp, midy-rp, midx+rp, midy+rp, width=2)
        # a 為模數 (代表公制中齒的大小), 模數為節圓直徑(稱為節徑)除以齒數
        # 模數也就是齒冠大小
        a=2*rp/n
        # d 為齒根大小, 為模數的 1.157 或 1.25倍, 這裡採 1.25 倍
        d=2.5*rp/n
        # ra 為齒輪的外圍半徑
        ra=rp+a
        print("ra:", ra)
        # 畫出 ra 圓, 畫圓函式尚未定義
        #create_oval(midx-ra, midy-ra, midx+ra, midy+ra, width=1)
        # rb 則為齒輪的基圓半徑
        # 基圓為漸開線長齒之基準圓
        rb=rp*cos(20*deg)
        print("rp:", rp)
        print("rb:", rb)
        # 畫出 rb 圓 (基圓), 畫圓函式尚未定義
        #create_oval(midx-rb, midy-rb, midx+rb, midy+rb, width=1)
        # rd 為齒根圓半徑
        rd=rp-d
        # 當 rd 大於 rb 時
        print("rd:", rd)
        # 畫出 rd 圓 (齒根圓), 畫圓函式尚未定義
        #create_oval(midx-rd, midy-rd, midx+rd, midy+rd, width=1)
        # dr 則為基圓到齒頂圓半徑分成 imax 段後的每段半徑增量大小
        # 將圓弧分成 imax 段來繪製漸開線
        dr=(ra-rb)/imax
        # tan(20*deg)-20*deg 為漸開線函數
        sigma=pi/(2*n)+tan(20*deg)-20*deg
        for j in range(n):
            ang=-2.*j*pi/n+sigma
            ang2=2.*j*pi/n+sigma
            lxd=midx+rd*sin(ang2-2.*pi/n)
            lyd=midy-rd*cos(ang2-2.*pi/n)
            #for(i=0;i<=imax;i++):
            for i in range(imax+1):
                r=rb+i*dr
                theta=sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-atan(theta)
                xpt=r*sin(alpha-ang)
                ypt=r*cos(alpha-ang)
                xd=rd*sin(-ang)
                yd=rd*cos(-ang)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由左側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    lfx=midx+xpt
                    lfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # the line from last end of dedendum point to the recent
            # end of dedendum point
            # lxd 為齒根圓上的左側 x 座標, lyd 則為 y 座標
            # 下列為齒根圓上用來近似圓弧的直線
            create_line((lxd),(lyd),(midx+xd),(midy-yd),fill=顏色)
            #for(i=0;i<=imax;i++):
            for i in range(imax+1):
                r=rb+i*dr
                theta=sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-atan(theta)
                xpt=r*sin(ang2-alpha)
                ypt=r*cos(ang2-alpha)
                xd=rd*sin(ang2)
                yd=rd*cos(ang2)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由右側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    rfx=midx+xpt
                    rfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # lfx 為齒頂圓上的左側 x 座標, lfy 則為 y 座標
            # 下列為齒頂圓上用來近似圓弧的直線
            create_line(lfx,lfy,rfx,rfy,fill=顏色)

    齒輪(400,400,300,41,"blue")

    </script>
    <canvas id="plotarea" width="800" height="800"></canvas>
    </body>
    </html>
    '''

        return outstring
    #@+node:amd.20150415215023.1: *3* ShowGear
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def ShowGear(self, n_g1=15, n_g2=24,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        
        m_g1 = 10*g1/2
        m_g2 = 10*g2/2
        
        if m_g1>=m_g2:
            x=m_g1
        else:
            x=m_g2
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>

    <form method=\"post\" action=\"DesignGear\">

    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>


    <input type=\"submit\" value=\"重新繪製\">
    </form>


    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <fieldset>

     <legend>齒輪組合圖:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    x='''+str(x)+'''
    x=x+20

    pa = 10
    # m 為模數
    m = 10
    # 第1齒輪齒數
    n_g1 ='''+str( g1)+'''
    # 第2齒輪齒數
    n_g2 ='''+str( g2)+'''

    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2

    y=rp_g1+20


    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x,y)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-x,-y)
    spur.Spur(ctx).Gear(x,y,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x,y+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-x,-(y+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(x,y+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()


    </script>
    <canvas id="plotarea" width="3800" height="4000"></canvas>

    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150622011937.1: *3* mygeartest3
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def mygeartest3(self, N1=15, N2=24,N3=24,N4=24,N5=24,N6=24,N7=24,M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <form method=\"post\" action=\"threeDgear1\">
    <fieldset>

     <legend>最下面有返回按鈕:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 20
    # m 為模數
    m = 20

    # 第1齒輪齒數
    n_g1 = '''+str(N1)+'''
    # 第2齒輪齒數
    n_g2 = '''+str(N2)+'''
    # 第3齒輪齒數
    n_g3 = '''+str(N3)+'''
    # 第4齒輪齒數
    n_g4 = '''+str(N4)+'''
    # 第5齒輪齒數
    n_g5 = '''+str(N5)+'''
    # 第6齒輪齒數
    n_g6 = '''+str(N6)+'''
    # 第7齒輪齒數
    n_g7 = '''+str(N7)+'''

    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2
    rp_g5 = m*n_g5/2
    rp_g6 = m*n_g6/2
    rp_g7 = m*n_g7/2

    ##########################################################################

    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820)
    # rotate to engage
    ctx.rotate(pi)
    # put it back
    ctx.translate(-820,-820)
    spur.Spur(ctx).Gear(820,820,rp_g1,n_g1, pa, "blue")
    ctx.restore()

    ##########################################################################

    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-820,-(820+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(820,820+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    ##########################################################################

    # 將第3齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+2*rp_g2+rp_g3)
    # rotate to engage
    ctx.rotate(-pi/n_g3*(n_g2%2))
    # put it back
    ctx.translate(-820,-(820+rp_g1+2*rp_g2+rp_g3))
    spur.Spur(ctx).Gear(820,820+rp_g1+2*rp_g2+rp_g3,rp_g3,n_g3, pa, "black")
    ctx.restore()

    ##########################################################################

    # 將第4齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+2*rp_g2+2*rp_g3+rp_g4)
    # rotate to engage
    a=(n_g2%2)+(n_g3%2)-1
    ctx.rotate(-pi/n_g4*a)
    # put it back
    ctx.translate(-820,-(820+rp_g1+2*rp_g2+2*rp_g3+rp_g4))
    spur.Spur(ctx).Gear(820,820+rp_g1+2*rp_g2+2*rp_g3+rp_g4,rp_g4,n_g4, pa, "black")
    ctx.restore()

    ##########################################################################

    # 將第5齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+rp_g5)
    # rotate to engage
    b=(n_g2%2)+(n_g3%2)+(n_g4%2)-2
    ctx.rotate(-pi/n_g5*b)
    # put it back
    ctx.translate(-820,-(820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+rp_g5))
    spur.Spur(ctx).Gear(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+rp_g5,rp_g5,n_g5, pa, "black")
    ctx.restore()

    ##########################################################################

    # 將第6齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+rp_g6)
    # rotate to engage
    c=(n_g2%2)+(n_g3%2)+(n_g4%2)+(n_g5%2)-3
    ctx.rotate(-pi/n_g6*c)
    # put it back
    ctx.translate(-820,-(820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+rp_g6))
    spur.Spur(ctx).Gear(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+rp_g6,rp_g6,n_g6, pa, "black")
    ctx.restore()

    ##########################################################################

    # 將第7齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+2*rp_g6+rp_g7)
    # rotate to engage
    d=(n_g2%2)+(n_g3%2)+(n_g4%2)+(n_g5%2)+(n_g6%2)-4
    ctx.rotate(-pi/n_g7*d)
    # put it back
    ctx.translate(-820,-(820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+2*rp_g6+rp_g7))
    spur.Spur(ctx).Gear(820,820+rp_g1+2*rp_g2+2*rp_g3+2*rp_g4+2*rp_g5+2*rp_g6+rp_g7,rp_g7,n_g7, pa, "black")
    ctx.restore()

    ##########################################################################


    </script>
    <canvas id="plotarea" width="3800" height="12000"></canvas>

    <input type=\"submit\" value=\"return\">
    </form>

    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150622102228.1: *3* ShowGear1
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def ShowGear1(self, n_g1=15, n_g2=24,n_g3=24,n_g4=15,M=5, P=15):
        g1= int(cherrypy.session.get('g1'))
        g2= int(cherrypy.session.get('g2'))
        g3= int(cherrypy.session.get('g3'))
        g4= int(cherrypy.session.get('g4'))
         
        m_g1 = 10*g1/2
        m_g2 = 10*g2/2
        
        if m_g1>=m_g2:
            x=m_g1
        else:
            x=m_g2

        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>

    <form method=\"post\" action=\"DesignGear1\">
    <fieldset>

    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>

    <input type=\"submit\" value=\"重新繪製\">
    </form>

    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

     <legend>齒輪組和圖:</legend>

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *
    # 請注意, 這裡導入位於 Lib/site-packages 目錄下的 spur.py 檔案
    import spur

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")


    # 以下利用 spur.py 程式進行繪圖, 接下來的協同設計運算必須要配合使用者的需求進行設計運算與繪圖
    # 其中並將工作分配給其他組員建立類似 spur.py 的相關零件繪圖模組
    # midx, midy 為齒輪圓心座標, rp 為節圓半徑, n 為齒數, pa 為壓力角, color 為線的顏色
    # Gear(midx, midy, rp, n=20, pa=20, color="black"):
    # 模數決定齒的尺寸大小, 囓合齒輪組必須有相同的模數與壓力角
    # 壓力角 pa 單位為角度

    pa = 10
    # m 為模數
    m = 10

    x='''+str(x)+'''
    x=x+20

    # 第1齒輪齒數
    n_g1 = '''+str( g1)+'''
    # 第2齒輪齒數
    n_g2 = '''+str( g2)+'''
    # 第3齒輪齒數
    n_g3 = '''+str( g3)+'''
    # 第4齒輪齒數
    n_g4 = '''+str( g4)+'''


    # 計算兩齒輪的節圓半徑
    rp_g1 = m*n_g1/2
    rp_g2 = m*n_g2/2
    rp_g3 = m*n_g3/2
    rp_g4 = m*n_g4/2

    y=rp_g1+20

    # 將第1齒輪順時鐘轉 90 度
    # 使用 ctx.save() 與 ctx.restore() 以確保各齒輪以相對座標進行旋轉繪圖
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x,y)
    # rotate to engage
    ctx.rotate(-pi)
    # put it back
    ctx.translate(-x,-y)
    spur.Spur(ctx).Gear(x,y,rp_g1,n_g1, pa, "blue")
    ctx.restore()



    # 將第2齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x,y+rp_g1+rp_g2)
    # rotate to engage
    ctx.rotate(-pi/n_g2)
    # put it back
    ctx.translate(-x,-(y+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(x,y+rp_g1+rp_g2,rp_g2,n_g2, pa, "black")
    ctx.restore()

    # 將第3齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x+rp_g2+rp_g3,y+rp_g1+rp_g2)
    # rotate to engage

    ctx.rotate(-pi/2+(pi/n_g3*0.5)*(n_g2%4))

    # put it back
    ctx.translate(-(x+rp_g2+rp_g3),-(y+rp_g1+rp_g2))
    spur.Spur(ctx).Gear(x+rp_g2+rp_g3,y+rp_g1+rp_g2,rp_g3,n_g3, pa, "black")
    ctx.restore()


    # 將第4齒輪逆時鐘轉 90 度之後, 再多轉一齒, 以便與第1齒輪進行囓合
    ctx.save()
    # translate to the origin of second gear
    ctx.translate(x+rp_g2+rp_g3,y+rp_g1+rp_g2+rp_g3+rp_g4)

    # rotate to engage

    a=(n_g2%2)-1
    ctx.rotate(-pi/n_g4*a)

    # put it back
    ctx.translate(-(x+rp_g2+rp_g3),-(y+rp_g1+rp_g2+rp_g3+rp_g4))
    spur.Spur(ctx).Gear(x+rp_g2+rp_g3,y+rp_g1+rp_g2+rp_g3+rp_g4,rp_g4,n_g4, pa, "black")
    ctx.restore()

    </script>
    <canvas id="plotarea" width="3800" height="12000"></canvas>


    </body>
    </html>
    '''

        return outstring
    #@+node:2015.20150331094055.1737: *3* my3Dgeartest
    @cherrypy.expose
    # N 為齒數, M 為模數, P 為壓力角
    def my3Dgeartest(self, N=20, M=5, P=15):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <!-- 載入 brython.js -->
    <script type="text/javascript" src="/static/Brython3.1.1-20150328-091302/brython.js"></script>
    <script src="/static/Cango2D.js" type="text/javascript"></script>
    <script src="/static/gearUtils-04.js" type="text/javascript"></script>
    </head>
    <!-- 啟動 brython() -->
    <body onload="brython()">

    <!-- 以下為 canvas 畫圖程式 -->
    <script type="text/python">
    # 從 browser 導入 document
    from browser import document
    from math import *

    # 準備在 id="plotarea" 的 canvas 中繪圖
    canvas = document["plotarea"]
    ctx = canvas.getContext("2d")

    def create_line(x1, y1, x2, y2, width=3, fill="red"):
    	ctx.beginPath()
    	ctx.lineWidth = width
    	ctx.moveTo(x1, y1)
    	ctx.lineTo(x2, y2)
    	ctx.strokeStyle = fill
    	ctx.stroke()

    # 導入數學函式後, 圓周率為 pi
    # deg 為角度轉為徑度的轉換因子
    deg = pi/180.
    #
    # 以下分別為正齒輪繪圖與主 tkinter 畫布繪圖
    #
    # 定義一個繪正齒輪的繪圖函式
    # midx 為齒輪圓心 x 座標
    # midy 為齒輪圓心 y 座標
    # rp 為節圓半徑, n 為齒數
    def gear(midx, midy, rp, n, 顏色):
        # 將角度轉換因子設為全域變數
        global deg
        # 齒輪漸開線分成 15 線段繪製
        imax = 15
        # 在輸入的畫布上繪製直線, 由圓心到節圓 y 軸頂點畫一直線
        create_line(midx, midy, midx, midy-rp)
        # 畫出 rp 圓, 畫圓函式尚未定義
        #create_oval(midx-rp, midy-rp, midx+rp, midy+rp, width=2)
        # a 為模數 (代表公制中齒的大小), 模數為節圓直徑(稱為節徑)除以齒數
        # 模數也就是齒冠大小
        a=2*rp/n
        # d 為齒根大小, 為模數的 1.157 或 1.25倍, 這裡採 1.25 倍
        d=2.5*rp/n
        # ra 為齒輪的外圍半徑
        ra=rp+a
        print("ra:", ra)
        # 畫出 ra 圓, 畫圓函式尚未定義
        #create_oval(midx-ra, midy-ra, midx+ra, midy+ra, width=1)
        # rb 則為齒輪的基圓半徑
        # 基圓為漸開線長齒之基準圓
        rb=rp*cos(20*deg)
        print("rp:", rp)
        print("rb:", rb)
        # 畫出 rb 圓 (基圓), 畫圓函式尚未定義
        #create_oval(midx-rb, midy-rb, midx+rb, midy+rb, width=1)
        # rd 為齒根圓半徑
        rd=rp-d
        # 當 rd 大於 rb 時
        print("rd:", rd)
        # 畫出 rd 圓 (齒根圓), 畫圓函式尚未定義
        #create_oval(midx-rd, midy-rd, midx+rd, midy+rd, width=1)
        # dr 則為基圓到齒頂圓半徑分成 imax 段後的每段半徑增量大小
        # 將圓弧分成 imax 段來繪製漸開線
        dr=(ra-rb)/imax
        # tan(20*deg)-20*deg 為漸開線函數
        sigma=pi/(2*n)+tan(20*deg)-20*deg
        for j in range(n):
            ang=-2.*j*pi/n+sigma
            ang2=2.*j*pi/n+sigma
            lxd=midx+rd*sin(ang2-2.*pi/n)
            lyd=midy-rd*cos(ang2-2.*pi/n)
            #for(i=0;i<=imax;i++):
            for i in range(imax+1):
                r=rb+i*dr
                theta=sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-atan(theta)
                xpt=r*sin(alpha-ang)
                ypt=r*cos(alpha-ang)
                xd=rd*sin(-ang)
                yd=rd*cos(-ang)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由左側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    lfx=midx+xpt
                    lfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # the line from last end of dedendum point to the recent
            # end of dedendum point
            # lxd 為齒根圓上的左側 x 座標, lyd 則為 y 座標
            # 下列為齒根圓上用來近似圓弧的直線
            create_line((lxd),(lyd),(midx+xd),(midy-yd),fill=顏色)
            #for(i=0;i<=imax;i++):
            for i in range(imax+1):
                r=rb+i*dr
                theta=sqrt((r*r)/(rb*rb)-1.)
                alpha=theta-atan(theta)
                xpt=r*sin(ang2-alpha)
                ypt=r*cos(ang2-alpha)
                xd=rd*sin(ang2)
                yd=rd*cos(ang2)
                # i=0 時, 繪線起點由齒根圓上的點, 作為起點
                if(i==0):
                    last_x = midx+xd
                    last_y = midy-yd
                # 由右側齒根圓作為起點, 除第一點 (xd,yd) 齒根圓上的起點外, 其餘的 (xpt,ypt)則為漸開線上的分段點
                create_line((midx+xpt),(midy-ypt),(last_x),(last_y),fill=顏色)
                # 最後一點, 則為齒頂圓
                if(i==imax):
                    rfx=midx+xpt
                    rfy=midy-ypt
                last_x = midx+xpt
                last_y = midy-ypt
            # lfx 為齒頂圓上的左側 x 座標, lfy 則為 y 座標
            # 下列為齒頂圓上用來近似圓弧的直線
            create_line(lfx,lfy,rfx,rfy,fill=顏色)

    gear(400,400,300,41,"blue")
    </script>
    <canvas id="plotarea" width="800" height="800"></canvas>
    </body>
    </html>
    '''

        return outstring
    #@+node:2014fall.20141215194146.1793: *3* doCheck
    @cherrypy.expose
    def doCheck(self, guess=None):
        # 假如使用者直接執行 doCheck, 則設法轉回根方法
        if guess is None:
            raise cherrypy.HTTPRedirect("/")
        # 從 session 取出 answer 對應資料, 且處理直接執行 doCheck 時無法取 session 值情況
        try:
            theanswer = int(cherrypy.session.get('answer'))
        except:
            raise cherrypy.HTTPRedirect("/")
        # 經由表單所取得的 guess 資料型別為 string
        try:
            theguess = int(guess)
        except:
            return "error " + self.guessform()
        # 每執行 doCheck 一次,次數增量一次
        cherrypy.session['count']  += 1
        # 答案與所猜數字進行比對
        if theanswer < theguess:
            return "big " + self.guessform()
        elif theanswer > theguess:
            return "small " + self.guessform()
        else:
            # 已經猜對, 從 session 取出累計猜測次數
            thecount = cherrypy.session.get('count')
            return "exact: <a href=''>再猜</a>"
    #@+node:2014fall.20141215194146.1789: *3* guessform
    def guessform(self):
        # 印出讓使用者輸入的超文件表單
        outstring = str(cherrypy.session.get('answer')) + "/" + str(cherrypy.session.get('count')) + '''<form method=POST action=doCheck>
    請輸入您所猜的整數:<input type=text name=guess><br />
    <input type=submit value=send>
    </form>'''
        return outstring
    #@-others
#@-others
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
    
root = Hello()
root.gear = gear.Gear()
cherrypy.server.socket_port = 8081
cherrypy.server.socket_host = '127.0.0.1'

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(root, config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(root, config=application_conf)
#@-leo
