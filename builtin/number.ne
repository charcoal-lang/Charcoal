unsigned_int -> [0-9]:+ {% parseInt("".join(d[0])) %}

int -> ("-"|"+"):? [0-9]:+ {% parseInt(d[0][0] + "".join(d[1])) if d[0] else parseInt("".join(d[1])) %}

unsigned_decimal -> [0-9]:+ ("." [0-9]:+):? {% parseFloat("".join(d[0]) + ("." + d[1][1].join("") if d[1] else "") %}

decimal -> "-":? [0-9]:+ ("." [0-9]:+):? {% parseFloat((d[0] or "") + "".join(d[1]) + ("." + "".join(d[2][1]) if d[2] else "") %}

percentage -> decimal "%" {% d[0] / 100 %}

jsonfloat -> "-":? [0-9]:+ ("." [0-9]:+):? ([eE] [+-]:? [0-9]:+):? {% parseFloat((d[0] or "") + "".join(d[1]) + (("." + "".join(d[2][1])) if d[2] else "") + (("e" + (d[3][1] or "+") + "".join(d[3][2])) if d[3] else "") %}