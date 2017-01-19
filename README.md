# tainan-student-stat
臺南市班級男女生人數統計(含折抵)

## 1. Python modules
  * [bs4](https://pypi.python.org/pypi/beautifulsoup4): Beautiful Soup 4
  * [mechanizeh](https://pypi.python.org/pypi/mechanize/)
  * [Jinja2](https://pypi.python.org/pypi/Jinja2)
  * [percache](https://pypi.python.org/pypi/percache)

```bash
# apt-get install python-bs4
# apt-get install python-mechanize
# apt-get install python-jinja2
# pip install --upgrade percache
```

## 2. Nginx
```bash
# vim /etc/nginx/sites-enabled/001-myweb
```
```nginx
        location /python {
                include uwsgi_params;
                uwsgi_modifier1 9;
                uwsgi_pass 127.0.0.1:9001;
        }
```

## 3. uWSGI
```bash
# vim /etc/uwsgi/apps-enabled/python.ini
```
```ini
[uwsgi]
plugins = cgi
socket = 127.0.0.1:9001
cgi = /python=/var/www/python
module = pyindex
cgi-allowed-ext = .py
cgi-helper = .py=python
```

## 4. Credit
  * Author: HSIEH, Li-Yi
  * All programs are released under the GPL.
