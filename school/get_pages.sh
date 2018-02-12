#!/bin/sh

page_url="http://163.26.2.28/sch_data/sch_detail.aspx?sch_code="
ids=$(cut -d',' -f1 tainan.txt | xargs)

for id in $ids; do
	url="${page_url}${id}"
	file="pages/${id}"
	echo "${url}"
	wget "${url}" -O "${file}"
done
