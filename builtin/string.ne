# Matches various kinds of string literals

# Double-quoted string
dqstring -> "\"" dstrchar:* "\"" {% "".join(d[1]) %}
sqstring -> "'"  sstrchar:* "'"  {% "".join(d[1]) %}
btstring -> "`"  [^`]:*    "`"  {% "".join(d[1]) %}

dstrchar -> [^\\"\n] {% d[0] %}
    | "\\" strescape {% JSON.parse("\"" + "".join(d) + "\"") %}

sstrchar -> [^\\\n] {% d[0] %}
    | "\\" strescape {% JSON.parse("\""+d.join("")+"\"") %}
    | "\\'" {% "'" %}

strescape -> ["\\/bfnrt] {% d[0] %}
    | "u" [a-fA-F0-9] [a-fA-F0-9] [a-fA-F0-9] [a-fA-F0-9] {% "".join(d) %}