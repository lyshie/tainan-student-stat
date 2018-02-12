#!/bin/sh

grep -oP '(?<=<span id="ctl00_ContentPlaceHolder1_txtsch_en_name">).*?(?=</span>)' pages/*
