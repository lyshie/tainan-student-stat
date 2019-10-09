#!/bin/sh

grep -oP '(?<=<span id="ctl00_ContentPlaceHolder1_txtsch_ch_name">).*?(?=</span>)' pages/*
