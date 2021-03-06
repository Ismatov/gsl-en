#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest,os
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.IncomeStatement import incomeStatement
from renumerate.CategoryHint import categoryHinter
from renumerate.PenaltyEngine import penaltyEngine
from StringIO import StringIO

'''
original 特定非営利活動法人オープンソースソフトウェア協会.
'''

example1 = '''
平成18年度 「特定二手構常和活動1二《県る事業」 収支計算書
平成18年4月 1 日から 平成19年3月3]日まで
特定非営利活動まま人 六位7>ン・）一）《￥）7 レ 「）二7億会
（単位 二 円×
料 月 金 額
1 収入の部
1 会費・入会金収入
会費収入（年会賃 47日） 534,000
会費収入（費助会賃 71]) 840,000
7）「一受△「,ま支,費費 0
入会金収入 0 1,374,000
2 事業収入
ン6一の地事業収入(書寄8会会費 3118) 103,000
7（の地事業収入（7タ「一受△会費 54構・) 181,000
ン（の地事業収入 （日支平二〈五千ル部会会費 154書,) 25,000 309,000
3 補助金等収入
地方公共団体補助金収入 0 0
4 寄[タ付金収入
0 0
5 受の地収入
雑収入 0
利息収入 723 723
6 一7（の地の事業会書十からの寄億入 0 0
当期収入合計 1,683,723
商年度賃1業道金 784,416 784,416
収 入 合   2,468,139

11 支出の部
1  
(1) 73・一7日ン・)一一入×）7 い717」8<,七て】支一での手11】書月し二開てタレ
る商事賃書）支ン,）2 8 る事業
七￥構八』書五事費 116,000
五・て一△』支一支 ・ )(・一・1）ンタ）)））〈 い道常費 58,000
  七三7レ一の開億 会ま品費 286,852
日9家×ン書一出度費 100,000
1七売7タ7055書講5賃7六・7△出度費 30,000
出度開7】寄二(タ一1「構成 84,000 674,852
(2) 方一76ン・）一一戻〈￥)7 賃×・)二7二子3』二（戻)定・の手[]）三月ら二開・9￥
る構講受の収業・ 書1「賃・ 費「講』て￥5上出,・計共道 8 る事業
（）1）611011五06,018書家て書動ン一ル11三成 35,700 35,700
(3) 六一7構ン7一7い)7 い）二7道上て返一での手・]開1二開てま
る金支体書4定道費貸< る事業
日受事1五千】レ五,千書売会会書書賃費 15,523
五)千書事講書受会会品費 0
支開会開億費 0 15,523
(4) 7「一7構ン7一二<・) 7 い7上7ま5,上て返子一の利】費]る二開て「
る手上会日（]二￥5<,七て]7ま日0講息書書の書月費 ・ 町受常 ・ ま定書）<費 賃< る
五】千賃事会会講費 0 0
(円) >「一7構ン7一）<・） 7 七三7二[71二開家)る人千1百成の「二
￥ のの町借・町開構上げ講定費×る事業
町書事会会書講費 0
七三ヶ一会書,書費 0 0
(6) 71一7>ン7一7×・） 7 1い 「7二7に開ま）る人村ま5」二五六団
体の活動支機構上げ支開商×る事業
7タ「一受△会支品費 267,750
7タ「一受上×講手賃料 0
771・受△支77定会開億費 265,650 533,400
事業費合計 1,259,475
2 書支事費
手>「費賃事度動1 0
  0
  31,500
け書書億品費 11,952
受1[三書事費7]〈費 0
構事道品費 16,409
道1書道機費 66,388
【三「1品り講4支費 81,901
手」月,手金書公書県 4,000
支道費 96,800
  28,655
雑費 4,932
書五品費合計 342,537
当期支出合計 1,602,012
当期収支書額 81,711
  866,127

平成18年度 「・での地事業に係る事業」 収支計算書
平成18年4月 1 日から 平成19年3月 31 日 まで
特定共常利活動￥費人 六一一）ン￥」一2料）7 い）・二71品会
（単位 3 円）
料 目 金 額
1 収入の部
1 六一7ンけ・入77い取二78まげるの利開に開賃る講
費・昭売の受講 0
2 六一7ン9一177料取二7定利月し方ン家子△開売8
上げ]ンけル千料ン三ンの受講 0
3 六一7ン収一入77い取二7に開方る八位ヶ一支構まげ
で二二7ルの販売 0 0
4 1構7ン7一197い百二7に開道しに助品の販売 0 0
当期収入合計 0
収 入 合 計 0
110 支出万）常一一 一0一一一 0 00 00    
1事業費
6)六一7ン7一277か方二7借まげ千の利円に開1
る講費・町開の受講 0 0
位)六一タン9一入97レ取二7費利開しにレ入子△開
売8上げ3ンけル子一レ三ンの受講 0 0
8)六一7ン7・×収7い取17に開方る六位ヶ一支構
・ まげて二二7ルの販売 0 0
雑）六一7ン7一197借取二7に開道し定助品の販売 0 0
2費部費
億賃額部 0
品料手当 0
付講億品費 0
売額販費 0
補雑品費 0
道億道機費 0
町町額事費 0
構機公講 0
支道費 0
会講費 0 0
2千億費
千億費 0
当期支出合計 0
当期収支講額 0
家期構道収支書額 0
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj,  [534000L, 840000L, 1374000L, 103000L, 181000L, 25000L, 309000L, 723L, 723L, 1683723L])

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

