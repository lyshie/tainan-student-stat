#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import cgi
from bs4 import BeautifulSoup
import mechanize
#import percache
from jinja2 import Template

HTML = u"""<!DOCTYPE html>
<html>

    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1">
        <title>班級男女生人數統計(含折抵)</title>

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/flatly/bootstrap.min.css">

        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
            <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
            <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>

    <body>
        <!-- Page Content -->
        <div class="container">
            <div class="row">

                <div id="content">
                    <div class="table-responsive">
                        <table class="table table-bordered table-striped table-hover text-right">
                            <thead>
                                    <th>年級</th>
                                    <th>合計</th>
                                    {% for i in range(width) -%}
                                    <th>{{ i + 1 }}</th>
                                    {% endfor -%}
                            </thead>
                            <tbody>
                                {% set total = [0] -%}
                                {% set total_m = [0] -%}
                                {% set total_f = [0] -%}
                                {% for i in range(6) -%}
                                <tr>
                                    <td>{{ i + 1 }}</td>
                                    <td>
                                        <table class="table">
                                            <tr>
                                                {% set sum = [0] -%}
                                                {% for cell in result[i] -%}
                                                    {% set _ = sum.append(sum.pop() + cell[2] | int) -%}
                                                {% endfor -%}
                                                <td class="info">{{ sum[0] }}</td>
                                                {% set _ = total_m.append(total_m.pop() + sum[0]) -%}

                                                {% set sum = [0] -%}
                                                {% for cell in result[i] -%}
                                                    {% set _ = sum.append(sum.pop() + cell[3] | int) -%}
                                                {% endfor -%}
                                                <td class="danger">{{ sum[0] }}</td>
                                                {% set _ = total_f.append(total_f.pop() + sum[0]) -%}
                                            </tr>
                                            <tr class="success">
                                                {% set sum = [0] -%}
                                                {% for cell in result[i] -%}
                                                    {% set _ = sum.append(sum.pop() + cell[4] | int) -%}
                                                {% endfor -%}
                                                <td colspan="2">{{ sum[0] }}</td>
                                                {% set _ = total.append(total.pop() + sum[0]) -%}
                                            </tr>
                                        </table>
                                    </td>
                                    {% for cell in result[i] -%}
                                    <td>
                                        <table class="table">
                                            <tr>
                                                <td class="info">{{ cell[2] }}</td>
                                                <td class="danger">{{ cell[3] }}</td>
                                            </tr>
                                            <tr class="success">
                                                <td colspan="2">{{ cell[4] }} ({{ cell[5] | default('0', true) }}, {{ cell[6] | default('0', true) }}) / {{ cell[7] }}</td>
                                            </tr>
                                        </table>
                                    </td>
                                    {% endfor -%}
                                </tr>
                                {% endfor -%}
                                <tr>
                                    <td>合計</td>
                                    <td>
                                        <table class="table text-right">
                                            <tr>
                                                <td class="info">{{ total_m[0] }}</td>
                                                <td class="danger">{{ total_f[0] }}</td>
                                            </tr>
                                        </table>
                                    </td>
                                    <td colspan="{{ width }}">
                                        <table class="table text-left">
                                            <tr>
                                                <td class="warning">{{ total[0] }}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>

            <div class="row">
                <div class="col-lg-3">
                    <select id="schoolid" class="form-control form-inline">
                        <option value="114681">七股</option>
                        <option value="114726">二溪</option>
                        <option value="114625">三村</option>
                        <option value="114684">三股</option>
                        <option value="114705">三慈</option>
                        <option value="114711">下營</option>
                        <option value="114632">口埤</option>
                        <option value="213630">土城</option>
                        <option value="114735">土庫</option>
                        <option value="114662">大山</option>
                        <option value="114724">大內</option>
                        <option value="114691">大文</option>
                        <option value="114605">大甲</option>
                        <option value="213619">大光</option>
                        <option value="213603">大同</option>
                        <option value="114650">大成</option>
                        <option value="114756">大竹</option>
                        <option value="114655">大社</option>
                        <option value="213637">大港</option>
                        <option value="114633">大新</option>
                        <option value="114612">大潭</option>
                        <option value="114629">大橋</option>
                        <option value="114624">大灣</option>
                        <option value="114672">子龍</option>
                        <option value="114653">小新</option>
                        <option value="114635">山上</option>
                        <option value="114707">中洲</option>
                        <option value="114712">中營</option>
                        <option value="114777">五王</option>
                        <option value="114614">五甲</option>
                        <option value="114743">仁光</option>
                        <option value="114606">仁和</option>
                        <option value="114673">仁愛</option>
                        <option value="114601">仁德</option>
                        <option value="114751">內角</option>
                        <option value="114717">六甲</option>
                        <option value="213697">六溪分校</option>
                        <option value="213617">公園</option>
                        <option value="114736">公誠</option>
                        <option value="114761">太康</option>
                        <option value="114701">文山</option>
                        <option value="213642">文元</option>
                        <option value="114778">文化</option>
                        <option value="114661">文正</option>
                        <option value="114617">文和</option>
                        <option value="114747">文昌</option>
                        <option value="114602">文賢</option>
                        <option value="213612">日新</option>
                        <option value="114740">月津</option>
                        <option value="114753">仙草</option>
                        <option value="114699">北門</option>
                        <option value="114664">北勢</option>
                        <option value="114640">北寮</option>
                        <option value="114644">左鎮</option>
                        <option value="114779">正新</option>
                        <option value="114767">永安</option>
                        <option value="114782">永信</option>
                        <option value="114623">永康</option>
                        <option value="114784">永康勝利</option>
                        <option value="114627">永康復興</option>
                        <option value="213613">永華</option>
                        <option value="213621">永福</option>
                        <option value="114642">玉山</option>
                        <option value="114636">玉井</option>
                        <option value="213693">玉湖分校</option>
                        <option value="114749">玉豐</option>
                        <option value="114714">甲中</option>
                        <option value="114748">白河</option>
                        <option value="213624">石門</option>
                        <option value="213616">立人</option>
                        <option value="114685">光復</option>
                        <option value="114646">光榮</option>
                        <option value="114775">吉貝耍</option>
                        <option value="114708">宅港</option>
                        <option value="213641">安平</option>
                        <option value="213636">安佃</option>
                        <option value="114656">安定</option>
                        <option value="114658">安定南興</option>
                        <option value="213626">安順</option>
                        <option value="114663">安業</option>
                        <option value="114765">安溪</option>
                        <option value="213629">安慶</option>
                        <option value="213620">成功</option>
                        <option value="114750">竹門</option>
                        <option value="114742">竹埔</option>
                        <option value="114683">竹橋</option>
                        <option value="213625">西門</option>
                        <option value="114641">西埔</option>
                        <option value="114675">西港</option>
                        <option value="114677">西港成功</option>
                        <option value="114626">西勢</option>
                        <option value="213607">志開</option>
                        <option value="114631">那拔</option>
                        <option value="114604">依仁</option>
                        <option value="114668">佳里</option>
                        <option value="114669">佳興</option>
                        <option value="213614">協進</option>
                        <option value="213627">和順</option>
                        <option value="114720">官田</option>
                        <option value="114744">岸內</option>
                        <option value="114670">延平</option>
                        <option value="213622">忠義</option>
                        <option value="114770">東山</option>
                        <option value="213604">東光</option>
                        <option value="114772">東原</option>
                        <option value="114710">東陽</option>
                        <option value="114716">東興</option>
                        <option value="114759">果毅</option>
                        <option value="114718">林鳳</option>
                        <option value="114680">松林</option>
                        <option value="114755">河東</option>
                        <option value="114608">虎山</option>
                        <option value="213694">金砂分校</option>
                        <option value="114697">長平</option>
                        <option value="213634">長安</option>
                        <option value="114603">長興</option>
                        <option value="114774">青山</option>
                        <option value="213631">青草</option>
                        <option value="114780">信義</option>
                        <option value="114611">保西</option>
                        <option value="114615">保東</option>
                        <option value="210601">南大附小</option>
                        <option value="114639">南化</option>
                        <option value="114657">南安</option>
                        <option value="114799">南科實小</option>
                        <option value="114733">南梓</option>
                        <option value="213635">南興</option>
                        <option value="114689">建功</option>
                        <option value="114682">後港</option>
                        <option value="114763">後壁</option>
                        <option value="114678">後營</option>
                        <option value="114758">柳營</option>
                        <option value="213609">省躬</option>
                        <option value="114785">紅瓦厝</option>
                        <option value="114667">紀安</option>
                        <option value="114648">茄拔</option>
                        <option value="114695">苓和</option>
                        <option value="114760">重溪</option>
                        <option value="213638">海佃</option>
                        <option value="213628">海東</option>
                        <option value="114660">培文</option>
                        <option value="114693">將軍</option>
                        <option value="114616">崇和</option>
                        <option value="213640">崇明</option>
                        <option value="213606">崇學</option>
                        <option value="114776">崑山</option>
                        <option value="114618">深坑</option>
                        <option value="114700">蚵寮</option>
                        <option value="114674">通興</option>
                        <option value="114709">頂洲</option>
                        <option value="114659">麻豆</option>
                        <option value="213601">勝利</option>
                        <option value="213602">博愛</option>
                        <option value="213610">喜樹</option>
                        <option value="213639">復興</option>
                        <option value="114665">港尾</option>
                        <option value="114676">港東</option>
                        <option value="114723">渡拔</option>
                        <option value="213696">湖東分校</option>
                        <option value="114647">善化</option>
                        <option value="114649">善化大同</option>
                        <option value="114652">善糖</option>
                        <option value="114764">菁寮</option>
                        <option value="114713">賀建</option>
                        <option value="213623">進學</option>
                        <option value="213618">開元</option>
                        <option value="114651">陽明</option>
                        <option value="114721">隆田</option>
                        <option value="114671">塭內</option>
                        <option value="211602">慈濟</option>
                        <option value="114762">新山</option>
                        <option value="114630">新化</option>
                        <option value="114654">新市</option>
                        <option value="114729">新民</option>
                        <option value="114734">新生</option>
                        <option value="114619">新光</option>
                        <option value="114766">新東</option>
                        <option value="213615">新南</option>
                        <option value="114781">新泰</option>
                        <option value="114732">新進</option>
                        <option value="114768">新嘉</option>
                        <option value="114730">新橋</option>
                        <option value="213608">新興</option>
                        <option value="114728">新營</option>
                        <option value="114731">新營新興</option>
                        <option value="114638">楠西</option>
                        <option value="114643">瑞峰</option>
                        <option value="114771">聖賢</option>
                        <option value="213646">裕文</option>
                        <option value="114722">嘉南</option>
                        <option value="213699">漁光分校</option>
                        <option value="114694">漚汪</option>
                        <option value="213644">億載</option>
                        <option value="114637">層林</option>
                        <option value="114607">德南</option>
                        <option value="213605">德高</option>
                        <option value="213645">賢北</option>
                        <option value="114706">學甲</option>
                        <option value="213643">學東</option>
                        <option value="114769">樹人</option>
                        <option value="114692">樹林</option>
                        <option value="114686">篤加</option>
                        <option value="114702">錦湖</option>
                        <option value="213695">頭社分校</option>
                        <option value="114688">龍山</option>
                        <option value="114620">龍崎</option>
                        <option value="213611">龍崗</option>
                        <option value="213692">龍船分校</option>
                        <option value="114628">龍潭</option>
                        <option value="114609">歸仁</option>
                        <option value="114610">歸南</option>
                        <option value="213632">鎮海</option>
                        <option value="114703">雙春</option>
                        <option value="114613">關廟</option>
                        <option value="213698">關嶺分校</option>
                        <option value="114696">鯤鯓</option>
                        <option value="211601">寶仁</option>
                        <option value="114738">歡雅</option>
                        <option value="213633">顯宮</option>
                        <option value="114737">鹽水</option>
                        <option value="114739">坔頭港</option>
                    </select>
                    <script type="text/javascript">
                        jQuery.noConflict();
                        (function($) {
                            $(function() {
                                var schoolid = window.location.search;
                                schoolid = schoolid.replace(/\D/g, '');
                                $('select#schoolid').val(schoolid);
                                $('select#schoolid').on('change', function() {
                                    var schoolid = $('select#schoolid').val();
                                    window.location.href = 'student2.py?id=' + schoolid;
                                });
                            });
                        })(jQuery);
                    </script>
                </div>
            <div>
        </div>
    </body>

</html>
"""

NORMAL = {'url': 'https://std.tn.edu.tw/sis/AnonyQuery/StatGradeClassSex.aspx',
          'selectid': 'ctl00$ContentPlaceHolder1$ddlSchool1$School',
          'tableid': 'ContentPlaceHolder1_gvStat'}
SPECIAL = {'url': 'https://std.tn.edu.tw/sis/AnonyQuery/SchoolStat.aspx',
           'selectid': 'ctl00$ContentPlaceHolder1$DdlSchool1$School',
           'tableid': 'ContentPlaceHolder1_gv1'}

template = Template(HTML)

#cache = percache.Cache('/tmp/my-cache')


#@cache
def getTableData(schoolid='213623', url='', selectid='', tableid=''):
    br = mechanize.Browser()

    br.open(url)
    form = list(br.forms())[0]

    form[selectid] = [schoolid]
    response = mechanize.urlopen(form.click(
        id='ContentPlaceHolder1_btnSearch')).read()

    soup = BeautifulSoup(response, 'html.parser')

    table = soup.find(id=tableid)

    table_data = [[toDigit(cell.text) for cell in row('td')]
                  for row in table('tr')]

    return table_data


def toDigit(text):
    text = re.sub(r'\D', '', text)
    text = re.sub(r'^0*', '', text)

    return text


def combineTables(normal=[], special=[]):
    result = [[] for x in xrange(0, 6)]
    width = 0

    for row in special:
        g = int(row[0]) - 1
        result[g].append(row)

        width = max(width, len(result[g]))

    for row in normal:
        g = int(row[0]) - 1
        c = int(row[1])
        if len(result[g]) < c:
            row[2], row[3] = row[3], row[2]
            result[g].append(row)

        width = max(width, len(result[g]))

    return result, width


def main():
    form = cgi.FieldStorage()
    if form.has_key('id'):
        schoolid = form['id'].value
    else:
        schoolid = '213623'
    schoolid = re.sub(r'\D', '', schoolid)

    normal_data = filter(lambda x: x and x[0].isdigit() and x[1].isdigit(),  getTableData(schoolid=schoolid,
                                                                                          url=NORMAL['url'], selectid=NORMAL['selectid'], tableid=NORMAL['tableid']))
    special_data = filter(lambda x: x and x[0].isdigit() and x[1].isdigit(), getTableData(schoolid=schoolid,
                                                                                          url=SPECIAL['url'], selectid=SPECIAL['selectid'], tableid=SPECIAL['tableid']))

    result, width = combineTables(normal=normal_data, special=special_data)
    # pprint.pprint(result)

    print "Content-Type: text/html;charset=utf-8"
    print
    print template.render(result=result, width=width).encode("UTF-8")

    # cache.close()

if __name__ == '__main__':
    main()
