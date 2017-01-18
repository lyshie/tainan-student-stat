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
