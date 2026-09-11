#!/bin/sh
# assemble style + corps en un fichier .dc.html
name=$1; body=$2
{
  printf '<!doctype html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n'
  cat _style.html
  printf '</helmet>\n'
  cat "$body"
  printf '</x-dc>\n</body>\n</html>\n'
} > "$name"
