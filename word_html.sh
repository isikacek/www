#/bin/bash

head=$(cat <<EOF
{% extends "base.html" %}
{% block head %}
    <style>
        .Remove {
            display: none!important;
        }
        p {
            text-indent: 0pt!important;
        }
        td {
            vertical-align: top;
            width: 33%;
            max-width: 33rem;
        }
        .WordSection5 table:first-of-type {
            width: 100%;
            max-width: 43rem;
        }
        .WordSection5 table:first-of-type tr:nth-child(3n) > td {
            width: 100%;
        }
        @media (min-width: 550px) {
            .WordSection5 table:first-of-type tr {
                display: flex;
            }
            .WordSection5 table:first-of-type tr td {
                flex: 1;
            }
        }

        @media (max-width: 900px) {
            table, tr, th, td {
                display: block;
                height: fit-content!important;
                max-width: 33rem;
                width: 100%;
            }
        }
        @media (min-width: 550px) and (max-width: 900px) {
            tr {
                column-count: 2;
            }
            td {
                padding: 0rem!important;
            }
        }
        @media (max-width: 550px) {
            td {
                padding: 0rem!important;
            }
            p {
                text-align: left!important;
            }
        }
        #cv-table * {
            width: initial;
            padding-left: 2rem;
        }
        #cv-table tr {
            display: table-row;
        }
        #cv-table th, #cv-table td {
            display: table-cell;
        }
    <\/style>
{% endblock %}
{% block content %}
      {% include "_cv_head.html"  %}
      <div id="word">
EOF
)
head=$(echo "$head" | tr -d '\n\r')

iconv -f WINDOWS-1250 -t UTF-8 $1 |
tr -d '\n\r' |
sed\
  -e "s/^<html.*\(<div[^>]*WordSection3[^>]*>\)/$head\1/g"\
  -e 's/text-indent[^;]+;//'\
  -e 's/ *\xe2\x97\xA6 */ - /g'\
  -e 's/\(font-family:[^"'";]+;?\)\("'"?\)/\2/'\
  -e 's/<\/body.*$/<\/div>{% endblock %}/g'\
  -e 's/width[^;]*pt;//g'\
  -e 's/&nbsp;//g'
