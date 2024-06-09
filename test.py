#!/usr/bin/env python3
# VIM: let b:airline_whitespace_disabled=1
"""
Charcoal's test module.

Contains unit tests, and runs them when invoked.

"""

from charcoal import Run
import unittest
import sys

# test string+int split
# test auto-input
# test e.g. random("abc"); "+" keeps separator
# look throught all wolfram pages again to see what isn't implemented

class CharcoalTest(unittest.TestCase):
    def test_print(self):
        self.assertEqual(Run("abc"), "abc")
        self.assertEqual(Run("abc←←Ｍ←abc"), "abc")
        self.assertEqual(Run("→abc"), "abc")
        self.assertEqual(Run("↓abc"), "a\nb\nc")
        self.assertEqual(Run("←abc¶def"), "fed\ncba")
        self.assertEqual(Run("←abc"), "cba")
        self.assertEqual(Run("↑abc"), "c\nb\na")
        self.assertEqual(Run("↖abc"), "c  \n b \n  a")
        self.assertEqual(Run("↗abc"), "  c\n b \na  ")
        self.assertEqual(Run("↘abc"), "a  \n b \n  c")
        self.assertEqual(Run("↙abc"), "  a\n b \nc  ")
        self.assertEqual(Run("↓abc←def"), "  a\n  b\n  c\nfed")
        self.assertEqual(Run("Print('abc')", verbose=True), "abc")
        self.assertEqual(
            Run(
                """\
Print('abc');Move(:Left);Move(:Left);Move(:Left);Print('abc')""",
                verbose=True
            ),
            "abc"
        )
        self.assertEqual(Run("Print(:Right, 'abc')", verbose=True), "abc")
        self.assertEqual(Run("Print(:Down, 'abc')", verbose=True), "a\nb\nc")
        self.assertEqual(Run("Print(:Left, 'abc')", verbose=True), "cba")
        self.assertEqual(Run("Print(:Up, 'abc')", verbose=True), "c\nb\na")
        self.assertEqual(
            Run("Print(:UpLeft, 'abc')", verbose=True),
            "c  \n b \n  a"
        )
        self.assertEqual(
            Run("Print(:UpRight, 'abc')", verbose=True),
            "  c\n b \na  "
        )
        self.assertEqual(
            Run("Print(:DownRight, 'abc')", verbose=True),
            "a  \n b \n  c"
        )
        self.assertEqual(
            Run("Print(:DownLeft, 'abc')", verbose=True),
            "  a\n b \nc  "
        )
        self.assertEqual(
            Run("Print(:Down, 'abc');Print(:Left, 'def')", verbose=True),
            "  a\n  b\n  c\nfed"
        )

    def test_multiprint(self):
        self.assertEqual(Run("Ｐabc"), "abc")
        self.assertEqual(Run("Ｐ→abc"), "abc")
        self.assertEqual(Run("Ｐ↓abc"), "a\nb\nc")
        self.assertEqual(Run("Ｐ←abc"), "cba")
        self.assertEqual(Run("Ｐ↑abc"), "c\nb\na")
        self.assertEqual(Run("Ｐ→↓abc"), "abc\nb  \nc  ")
        self.assertEqual(Run("Ｐ+abc"), "  c  \n  b  \ncbabc\n  b  \n  c  ")
        self.assertEqual(Run("ＰK´*****"), """\
*   *
*  * 
* *  
**   
*    
**   
* *  
*  * 
*   *""")
        self.assertEqual(Run("foo ¦bar⸿baz"), "foo bar\nbaz    ")
        self.assertEqual(Run("Multiprint('abc')", verbose=True), "abc")
        self.assertEqual(Run("Multiprint(:Right, 'abc')", verbose=True), "abc")
        self.assertEqual(
            Run("Multiprint(:Down, 'abc')", verbose=True),
            "a\nb\nc"
        )
        self.assertEqual(Run("Multiprint(:Left, 'abc')", verbose=True), "cba")
        self.assertEqual(
            Run("Multiprint(:Up, 'abc')", verbose=True),
            "c\nb\na"
        )
        self.assertEqual(
            Run("Multiprint(:Right, :Down, 'abc')", verbose=True),
            "abc\nb  \nc  "
        )
        self.assertEqual(
            Run("Multiprint(:+, 'abc')", verbose=True),
            "  c  \n  b  \ncbabc\n  b  \n  c  "
        )

    def test_jump(self):
        self.assertEqual(Run("aＭ³¦³a"), """\
a    
     
     
    a""")
        self.assertEqual(Run("abＪ³¦³a"), """\
ab  
    
    
   a""")
        self.assertEqual(
            Run("Print(\"a\");Move(3, 3);Print(\"a\");", verbose=True),
            """\
a    
     
     
    a""")
        self.assertEqual(
            Run("Print(\"ab\");JumpTo(3, 3);Print(\"a\");", verbose=True),
            """\
ab  
    
    
   a""")

    def test_eval(self):
        self.assertEqual(Run("ＶＳ", "abc←←Ｍ←abc"), "abc")
        self.assertEqual(Run("↓ＶＳ", "⁺⁵¦⁵"), ("|\n" * 10)[:-1])
        self.assertEqual(Run("ＵＶ'foobar'"), "foobar")
        self.assertEqual(
            Run("Evaluate(InputString())", "abc←←Ｍ←abc", verbose=True),
            "abc"
        )
        self.assertEqual(
            Run(
                "Print(:Down, Evaluate(InputString()))",
                "⁺⁵¦⁵",
                verbose=True
            ),
            ("|\n" * 10)[:-1]
        )

    def test_box(self):
        self.assertEqual(Run("Ｂ⁵¦⁵*"), """\
*****
*   *
*   *
*   *
*****""")
        self.assertEqual(Run("Ｂ⁵¦⁵123"), """\
12312
1   3
3   1
2   2
13213""")
        self.assertEqual(Run("Box(5, 5, '*')", verbose=True), """\
*****
*   *
*   *
*   *
*****""")
        self.assertEqual(Run("Box(5, 5, '123')", verbose=True), """\
12312
1   3
3   1
2   2
13213""")
        self.assertEqual(Run("Box(5.999, 5.999, '123')", verbose=True), """\
12312
1   3
3   1
2   2
13213""")
        self.assertEqual(Run("\
Box(Times(2.999, 1.999), 5.999, '123')", verbose=True), """\
12312
1   3
3   1
2   2
13213""")
        self.assertEqual(Run("\
Box(10, 1, 'charcoal'); Print('a')", verbose=True), "aharcoalch")
        self.assertEqual(Run("\
Box(10, Negate(1), 'charcoal'); Print('a')", verbose=True), "aharcoalch")
        self.assertEqual(Run("\
Box(Negate(10), 1, 'charcoal'); Print('a')", verbose=True), "hclaocraha")
        self.assertEqual(Run("\
Box(Negate(10), Negate(10), 'charcoal');", verbose=True), """\
arcoalchar
h        c
c        o
l        a
a        l
o        c
c        h
r        a
a        r
hclaocrahc""")

    def test_rectangle(self):
        self.assertEqual(Run("ＵＲ⁵¦⁵"), """\
+---+
|   |
|   |
|   |
+---+""")
        self.assertEqual(Run("ＵＲ±⁵¦±⁵"), """\
+---+
|   |
|   |
|   |
+---+""")
        self.assertEqual(Run("Rectangle(5, 5)", verbose=True), """\
+---+
|   |
|   |
|   |
+---+""")

    def test_oblong(self):
        self.assertEqual(Run("ＵＯ⁵¦⁵a"), """\
aaaaa
aaaaa
aaaaa
aaaaa
aaaaa""")
        self.assertEqual(Run("ＵＯ±⁵¦±⁵a"), """\
aaaaa
aaaaa
aaaaa
aaaaa
aaaaa""")
        self.assertEqual(Run("\
ＮθＮηＮζＵＯθ#Ｍ÷⁻θη²↘ＵＯη*Ｍ÷⁻ηζ²↘ＵＯζ@", "[12,6,2]"), """\
############
############
############
###******###
###******###
###**@@**###
###**@@**###
###******###
###******###
############
############
############""")

    def test_background(self):
        self.assertEqual(Run("Ｐ+abcＵＢ*"), """\
**c**
**b**
cbabc
**b**
**c**""")
        self.assertEqual(Run("Ｐ+abcＵＢ*#"), """\
*#c#*
*#b#*
cbabc
*#b#*
*#c#*""")
        self.assertEqual(Run("Ｐ+abcＵＢ*#¶#*"), """\
*#c#*
#*b*#
cbabc
#*b*#
*#c#*""")
        self.assertEqual(Run("Ｂ⁵¦⁵*ＵＢ#"), """\
*****
*###*
*###*
*###*
*****""")
        self.assertEqual(Run("Ｂ⁵¦⁵*ＵＢ#-"), """\
*****
*-#-*
*-#-*
*-#-*
*****""")
        self.assertEqual(Run("Ｂ⁵¦⁵*ＵＢ#-¶-#"), """\
*****
*#-#*
*-#-*
*#-#*
*****""")
        self.assertEqual(Run("Ｆ⁶«Ｍ→_»ＵＢ| "), "_|_|_|_|_|_")
        self.assertEqual(Run("ＵＢ#@↗³⟲"), "/@#\n#/#\n#@/")
        # TODO: weird, why does Charcoal escape asterisks???
        self.assertEqual(
            Run("Multiprint(:+, 'abc');SetBackground('*')", verbose=True),
            """\
**c**
**b**
cbabc
**b**
**c**"""
        )
        self.assertEqual(
            Run("Multiprint(:+, 'abc');SetBackground('*#')", verbose=True),
            """\
*#c#*
*#b#*
cbabc
*#b#*
*#c#*"""
        )
        self.assertEqual(
            Run(
                "Multiprint(:+, 'abc');SetBackground('*#\\n#*')",
                verbose=True
            ),
            """\
*#c#*
#*b*#
cbabc
#*b*#
*#c#*"""
        )
        self.assertEqual(
            Run("Box(5, 5, '*');SetBackground('#')", verbose=True),
            """\
*****
*###*
*###*
*###*
*****"""
        )
        self.assertEqual(
            Run("Box(5, 5, '*');SetBackground('#-')", verbose=True),
            """\
*****
*-#-*
*-#-*
*-#-*
*****"""
        )
        self.assertEqual(
            Run("Box(5, 5, '*');SetBackground('#-\\n-#')", verbose=True),
            """\
*****
*#-#*
*-#-*
*#-#*
*****"""
        )

    def test_copy(self):
        self.assertEqual(Run("Ｇ+⁵*Ｃ³¦³"), """\
*****   
*****   
*****   
********
********
   *****
   *****
   *****""")
        self.assertEqual(Run("Ｇ→⁵↓⁶*Ｃ³¦³"), """\
*****   
    *   
    *   
   *****
    *  *
    *  *
       *
       *
       *""")
        self.assertEqual(Run("***¶  *¶  *Ｃ¹¦¹"), """\
*** 
 ***
   *
   *""")
        self.assertEqual(
            Run("Polygon(:+, 5, '*');Copy(3, 3)", verbose=True),
            """\
*****   
*****   
*****   
********
********
   *****
   *****
   *****"""
        )
        self.assertEqual(
            Run("Polygon(:Right, 5, :Down, 6, '*');Copy(3, 3)", verbose=True),
            """\
*****   
    *   
    *   
   *****
    *  *
    *  *
       *
       *
       *"""
        )
        self.assertEqual(
            Run("Print('***\\n  *\\n  *');Copy(1, 1)", verbose=True),
            """\
*** 
 ***
   *
   *"""
        )

    def test_for(self):
        self.assertEqual(Run("Ｆ⁵a"), "aaaaa")
        self.assertEqual(Run("ＦabcιＦdefι"), "abcdef")
        self.assertEqual(Run("≔⁵ιＦＳκ", "foobar"), "foobar")
        self.assertEqual(Run("≔i«ικλ»▶i⟦a¦bc¦d⟧"), "abcd")
        self.assertEqual(Run("for(5)Print('a')", verbose=True), "aaaaa")
        self.assertEqual(Run("for(1)Assign('a',k);Print(k)", verbose=True), "a")
        self.assertEqual(
            Run(
                "Assign(5,i);for(InputString())Print(k)",
                "foobar",
                verbose=True
            ),
            "foobar"
        )

    def test_while(self):
        self.assertEqual(Run("≔⁵βＷβ«ab≔⁻β¹β»"), "ababababab")
        self.assertEqual(
            Run("""\
Assign(5, b);
while (b) {
    Print('ab');
    Assign(Subtract(b, 1), b);
}""", verbose=True),
            "ababababab"
        )

    def test_if(self):
        self.assertEqual(Run("¿¹asdf"), "asdf")
        self.assertEqual(Run("¿⁰asdf"), "")
        self.assertEqual(Run("¿⁰«asdf»ghjk"), "ghjk")
        self.assertEqual(Run("if(1)Print('asdf')", verbose=True), "asdf")
        self.assertEqual(Run("if(0)Print('asdf')", verbose=True), "")
        self.assertEqual(Run("""\
if (0) {
    Print('asdf')
} //else
    Print('ghjk')""", verbose=True), "ghjk")

    def test_switch(self):
        self.assertEqual(Run("≡§abc⁰⁺¹¦¹ω§abc⁰"), "a")
        self.assertEqual(Run("≡«§abc⁰⁺¹¦¹ω§abc⁰"), "a")
        self.assertEqual(Run("≡«§abc⁰⁺¹¦¹ω§abc⁰»"), "a")

    def test_slice(self):
        self.assertEqual(Run("✂abc"), "abc")
        self.assertEqual(Run("✂abcd²"), "cd")
        self.assertEqual(Run("✂abcd²·²"), "cd")
        self.assertEqual(Run("✂abcd¦2"), "cd")
        self.assertEqual(Run("✂abcd¦2.2"), "cd")
        self.assertEqual(Run("✂abc⁰¦²"), "ab")
        self.assertEqual(Run("✂abcdefg⁰¦⁹¦²"), "aceg")
        self.assertEqual(Run("\
Print(Slice('asdf')); Print(1);", verbose=True), "asdf-")

    def test_pivot(self):
        self.assertEqual(Run("↶¹asdf"), "   f\n  d \n s  \na   ")
        self.assertEqual(Run("↶²asdf"), "f\nd\ns\na")
        self.assertEqual(
            Run("PivotLeft(1);Print('asdf')", verbose=True),
            "   f\n  d \n s  \na   "
        )
        self.assertEqual(
            Run("PivotLeft(2);Print('asdf')", verbose=True),
            "f\nd\ns\na"
        )
        self.assertEqual(
            Run("PivotLeft(2);Print('asdf\\rghjk')", verbose=True),
            "fk\ndj\nsh\nag"
        )
        self.assertEqual(
            Run("PivotLeft(1);Print('asdf\\rghjk')", verbose=True),
            "   f \n  d k\n s j \na h  \n g   "
        )

    def test_reflect_transform(self):
        self.assertEqual(Run("(({{[[<<‖Ｔ→"), ">>]]}}))")
        self.assertEqual(Run("(({{¶  [[<<‖Ｔ→"), "  }}))\n>>]]  ")
        self.assertEqual(Run("´⎛´⎞‖Ｔ↑"), "⎝⎠")
        self.assertEqual(Run("---‖Ｔ↖"), "|\n|\n|")

    def test_rotate_transform(self):
        self.assertEqual(Run("|¶-¶/¶\\¶v¶^¶<¶>⟲Ｔ²"), "-|\\/v^<>")
        # TODO: should v^<> be rotated

    def test_rotate_prism(self):
        self.assertEqual(Run("|----⟲Ｐ²⁴⁶"), """\
     -    
     |    
     |    
     |    
|----|    
    |----|
    |     
    |     
    |     
    -     """)

    def test_reflect_mirror(self):
        self.assertEqual(Run("(({{[[<<‖Ｍ→"), "(({{[[<<>>]]}}))")
        self.assertEqual(Run("(({{¶  [[<<‖Ｍ→"), "(({{    }}))\n  [[<<>>]]  ")
        self.assertEqual(Run("´⎛´⎞‖Ｍ↓"), "⎛⎞\n⎝⎠")
        self.assertEqual(Run("---‖Ｍ↖"), "|   \n|   \n|   \n ---")
        for dir in "↖↗↘↙":
            self.assertEqual(
                Run("\\/↘²‖Ｍ%s" % dir), Run("\\/↘²‖Ｃ%s" % dir), dir
            )

    def test_rotate_copy(self):
        self.assertEqual(Run("abc¶de⟲Ｃ²"), """\
abc
de 
 c 
 be
 ad""")
        self.assertEqual(Run("abc¶de⟲Ｃ⁴"), """\
abc   
de    
    ed
   cba""")
        self.assertEqual(Run("abc¶de⟲Ｃ⁶"), """\
   da
abceb
de  c""")
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｃ↙²"), """\
ce   
bdabc
a  de""")
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｃ↙⁴"), """\
   abc
    de
ed    
cba   """)
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｃ↙⁶"), """\
abc
 de
 a 
db 
ec """)
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｃ↖²"), """\
ec 
db 
 a 
 de
abc""")
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｃ↖⁴"), """\
cba   
ed    
    de
   abc""")
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｃ↖⁶"), """\
a  de
bdabc
ce   """)
        self.assertEqual(Run("de¶abc⟲Ｃ↗²"), """\
de  c
abceb
   da""")
        self.assertEqual(Run("de¶abc⟲Ｃ↗⁴"), """\
   cba
    ed
de    
abc   """)
        self.assertEqual(Run("de¶abc⟲Ｃ↗⁶"), """\
 ad
 be
 c 
de 
abc""")
        self.assertEqual(
            Run("Print('abc\\nde');RotateCopy(2)", verbose=True),
            """\
abc
de 
 c 
 be
 ad"""
        )
        self.assertEqual(
            Run("Print('abc\\nde');RotateCopy(4)", verbose=True),
            """\
abc   
de    
    ed
   cba"""
        )
        self.assertEqual(
            Run("Print('abc\\nde');RotateCopy(6)", verbose=True),
            """\
   da
abceb
de  c"""
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateCopy(:DownLeft, 2)""",
                verbose=True
            ),
            """\
ce   
bdabc
a  de"""
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateCopy(:DownLeft, 4)""",
                verbose=True
            ),
            """\
   abc
    de
ed    
cba   """
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateCopy(:DownLeft, 6)""",
                verbose=True
            ),
            """\
abc
 de
 a 
db 
ec """
        )

    def test_rotate_overlap(self):
        self.assertEqual(Run("abc¶de⟲Ｏ²"), """\
abc
de 
 be
 ad""")
        self.assertEqual(Run("abc¶de⟲Ｏ⁴"), """\
abc  
de ed
  cba""")
        self.assertEqual(Run("abc¶de⟲Ｏ⁶"), """\
  da
abcb
de c""")
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｏ↙²"), """\
ce  
babc
a de""")
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｏ↙⁴"), """\
  abc
ed de
cba  """)
        self.assertEqual(Run("abc↙Ｍ←de⟲Ｏ↙⁶"), """\
abc
 de
db 
ec """)
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｏ↖²"), """\
ec 
db 
 de
abc""")
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｏ↖⁴"), """\
cba  
ed de
  abc""")
        self.assertEqual(Run("abc↖Ｍ←de⟲Ｏ↖⁶"), """\
a de
babc
ce  """)
        self.assertEqual(Run("de¶abc⟲Ｏ↗²"), """\
de c
abcb
  da""")
        self.assertEqual(Run("de¶abc⟲Ｏ↗⁴"), """\
  cba
de ed
abc  """)
        self.assertEqual(Run("de¶abc⟲Ｏ↗⁶"), """\
 ad
 be
de 
abc""")
        self.assertEqual(
            Run("Print('abc\\nde');RotateOverlap(2)", verbose=True),
            """\
abc
de 
 be
 ad"""
        )
        self.assertEqual(
            Run("Print('abc\\nde');RotateOverlap(4)", verbose=True),
            """\
abc  
de ed
  cba"""
        )
        self.assertEqual(
            Run("Print('abc\\nde');RotateOverlap(6)", verbose=True),
            """\
  da
abcb
de c"""
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateOverlap(:DownLeft, 2)""",
                verbose=True
            ),
            """\
ce  
babc
a de"""
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateOverlap(:DownLeft, 4)""",
                verbose=True
            ),
            """\
  abc
ed de
cba  """
        )
        self.assertEqual(
            Run(
                """
Print('abc');
Move(:DownLeft);
Move(:Left);
Print('de');
RotateOverlap(:DownLeft, 6)""",
                verbose=True
            ),
            """\
abc
 de
db 
ec """
        )
        self.assertEqual(Run("abcＭ↓def⟲Ｃ↖²⁴⁶"), """\
       f    
       e    
       d    
      c     
fed   b     
   cbaa     
     aabc   
     b   def
     c      
    d       
    e       
    f       """)
        self.assertEqual(Run("abcＭ↓def⟲Ｏ↖²⁴⁶"), """\
      f    
      e    
      d    
     c     
fed  b     
   cbabc   
     b  def
     c     
    d      
    e      
    f      """)

    def test_rotate_shutter(self):
        self.assertEqual(Run("⁴+⟲Ｓ²⁴⁶"), """\
    |    
    |    
    |    
    |    
----+----
    |    
    |    
    |    
    |    """)

    def test_reflect_copy(self):
        self.assertEqual(Run("abc¶def¶ghi‖Ｃ←"), "cbaabc\nfeddef\nihgghi")
        self.assertEqual(Run("abc¶d¶gh‖Ｃ←"), "cbaabc\n  dd  \n hggh ")
        self.assertEqual(Run("abc¶d¶gh‖Ｃ→"), "abccba\nd    d\ngh  hg")
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｃ↖a"), """\
 a    
ifc   
heb   
gda   
   abc
   def
   ghi""")
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｃ↗a"), """\
   adg
   beh
   cfi
abc a 
def   
ghi   """)
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｃ↙a"), """\
   abc
   def
   ghi
adg   
beh   
cfi   
 a    """)
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｃ↘a"), """\
abc   
def   
ghi a 
   ifc
   heb
   gda""")
        self.assertEqual(Run("abc¶  d¶ gh‖Ｃ←"), "cbaabc\nd    d\nhg  gh")
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↑"), "ghi\nd  \na c\na c\nd  \nghi")
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↓"), "a c\nd  \nghi\nghi\nd  \na c")
        self.assertEqual(Run("a↓↓↓↓↓→→→a‖Ｃ↙"), """\
   a   
       
       
a      
       
      a
     a """)
        self.assertEqual(Run("a↓↓↓↓↓←←←←←a‖Ｃ↘"), """\
   a   
       
       
      a
       
a      
 a     """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↖"), """\
i c   
h     
gda   
   a c
   d  
   ghi""")
        self.assertEqual(Run("a c¶ d¶ghi‖Ｃ↖"), """\
i c   
hd    
g a   
   a c
    d 
   ghi""")
        self.assertEqual(Run("  a¶ d¶ghi‖Ｃ↖"), """\
i a   
hd    
g     
     a
    d 
   ghi""")
        self.assertEqual(Run("a¶bcd‖Ｃ↖"), """\
d    
c    
ba   
  a  
  bcd""")
        self.assertEqual(Run("abc¶d‖Ｃ↖"), """\
 c   
 b   
da   
  abc
  d  """)
        self.assertEqual(Run("a¶d¶ghi‖Ｃ↖"), """\
i     
h     
gda   
   a  
   d  
   ghi""")
        self.assertEqual(Run("cdeＭ↖bＭ↖a‖Ｃ↖"), """\
eba 
d  a
c  b
 cde""")
        self.assertEqual(Run("abcＭ↖d‖Ｃ↖"), """\
cd  
b   
a  d
 abc""")
        self.assertEqual(Run("a¶d¶ghi‖Ｃ↗"), """\
 adg
a  h
d  i
ghi """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↗"), """\
   adg
     h
   c i
a c   
d     
ghi   """)
        self.assertEqual(Run("a c¶ d¶ghi‖Ｃ↗"), """\
   a g
    dh
   c i
a c   
 d    
ghi   """)
        self.assertEqual(Run("  a¶ d¶ghi‖Ｃ↗"), """\
     g
    dh
   a i
  a   
 d    
ghi   """)
        self.assertEqual(Run("a¶bcd‖Ｃ↗"), """\
  ab
   c
a  d
bcd """)
        self.assertEqual(Run("abc¶d‖Ｃ↗"), """\
   ad
   b 
   c 
abc  
d    """)
        self.assertEqual(Run("a¶d¶ghi‖Ｃ↗"), """\
 adg
a  h
d  i
ghi """)
        self.assertEqual(Run("abcＭ↖d‖Ｃ↗"), """\
    a
    b
   dc
  d  
abc  """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↙"), """\
   a c
   d  
   ghi
adg   
  h   
c i   """)
        self.assertEqual(Run("a c¶ d¶ghi‖Ｃ↙"), """\
   a c
    d 
   ghi
a g   
 dh   
c i   """)
        self.assertEqual(Run("  a¶ d¶ghi‖Ｃ↙"), """\
     a
    d 
   ghi
  g   
 dh   
a i   """)
        self.assertEqual(Run("a¶bcd‖Ｃ↙"), """\
  a  
  bcd
ab   
 c   
 d   """)
        self.assertEqual(Run("abc¶d‖Ｃ↙"), """\
  abc
  d  
ad   
b    
c    """)
        self.assertEqual(Run("a¶d¶ghi‖Ｃ↙"), """\
   a  
   d  
   ghi
adg   
  h   
  i   """)
        self.assertEqual(Run("abcＭ↖d‖Ｃ↙"), """\
    d
  abc
 a   
 b   
dc   """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↘"), """\
a c   
d     
ghi   
   i c
   h  
   gda""")
        self.assertEqual(Run("a c¶ d¶ghi‖Ｃ↘"), """\
a c   
 d    
ghi   
   i c
   hd 
   g a""")
        self.assertEqual(Run("  a¶ d¶ghi‖Ｃ↘"), """\
  a   
 d    
ghi   
   i a
   hd 
   g  """)
        self.assertEqual(Run("a¶bcd‖Ｃ↘"), """\
a    
bcd  
   d 
   c 
   ba""")
        self.assertEqual(Run("abc¶d‖Ｃ↘"), """\
abc 
d  c
   b
  da""")
        self.assertEqual(Run("a¶d¶ghi‖Ｃ↘"), """\
a     
d     
ghi   
   i  
   h  
   gda""")
        self.assertEqual(Run("↗⁶‖Ｃ↓a"), """\
     / 
    /  
   /   
  /    
 /     
/      
/      
 /     
  /    
   /   
    /  
     / 
      a""")
        self.assertEqual(Run("↘⁶‖Ｃ↑a"), """\
      a
     \\ 
    \\  
   \\   
  \\    
 \\     
\\      
\\      
 \\     
  \\    
   \\   
    \\  
     \\ """)
        self.assertEqual(Run("↗²↖↙⁴‖Ｃa"), """\
   //    
  /  /   
 / // /  
/ /  / / 
        a""")
        self.assertEqual(Run("↗²↖↙⁴‖Ｃ←a"), """\
/      /
 /    / 
/ /  / /
 / // / 
    a   """)

    def test_reflect_overlap(self):
        self.assertEqual(Run("abc¶def¶ghi‖Ｏ←"), "cbabc\nfedef\nihghi")
        self.assertEqual(Run("abc¶def¶ghi‖Ｏ←a"), " cbabc\n fedef\naihghi")
        self.assertEqual(Run("abc¶def¶ghi‖Ｏ→a"), "abcba\ndefed\ngaihg")
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｏ↖a"), """\
 a   
ifc  
heb  
gdabc
  def
  ghi""")
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｏ↗a"), """\
  adg
  beh
abcfi
defa 
ghi  """)
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｏ↙a"), """\
  abc
  def
adghi
beh  
cfi  
 a   """)
        self.assertEqual(Run("abc¶def¶ghi↑‖Ｏ↘a"), """\
abc  
defa 
ghifc
  heb
  gda""")
        self.assertEqual(Run("abc¶d¶gh‖Ｏ←"), "cbabc\n  d  \n hgh ")
        self.assertEqual(Run("abc¶d¶gh‖Ｏ→"), "abcba\nd   d\ngh hg")
        self.assertEqual(Run("abc¶  d¶ gh‖Ｏ←"), "cbabc\nd   d\nhg gh")
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↑"), "ghi\nd  \na c\nd  \nghi")
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↓"), "a c\nd  \nghi\nd  \na c")
        self.assertEqual(Run("a c¶d¶ghi¶jkl‖Ｏ↓"), """\
a c
d  
ghi
jkl
ghi
d  
a c""")
        self.assertEqual(Run("a↓↓↓↓↓→→→a‖Ｏ↙"), """\
  a   
      
a     
      
      
     a""")
        self.assertEqual(Run("a↓↓↓↓↓←←←←←a‖Ｏ↘"), """\
   a  
      
     a
      
      
a     """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↖"), """\
i c  
h    
gda c
  d  
  ghi""")
        self.assertEqual(Run("a c¶ d¶ghi‖Ｏ↖"), """\
i c  
hd   
g a c
   d 
  ghi""")
        self.assertEqual(Run("  a¶ d¶ghi‖Ｏ↖"), """\
i a  
hd   
g   a
   d 
  ghi""")
        self.assertEqual(Run("a¶bcd‖Ｏ↖"), """\
d   
c   
ba  
 bcd""")
        self.assertEqual(Run("abc¶d‖Ｏ↖"), """\
 c  
 b  
dabc
 d  """)
        self.assertEqual(Run("a¶d¶ghi‖Ｏ↖"), """\
i    
h    
gda  
  d  
  ghi""")
        self.assertEqual(Run("cdeＭ↖bＭ↖a‖Ｏ↖"), """\
eba
d b
cde""")
        self.assertEqual(Run("abcＭ↖d‖Ｏ↖"), """\
cd 
b d
abc""")
        self.assertEqual(Run("a¶d¶ghi‖Ｏ↗"), """\
adg
d h
ghi""")
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↗"), """\
  adg
    h
a c i
d    
ghi  """)
        self.assertEqual(Run("a c¶ d¶ghi‖Ｏ↗"), """\
  a g
   dh
a c i
 d   
ghi  """)
        self.assertEqual(Run("  a¶ d¶ghi‖Ｏ↗"), """\
    g
   dh
  a i
 d   
ghi  """)
        self.assertEqual(Run("a¶bcd‖Ｏ↗"), """\
 ab
a c
bcd""")
        self.assertEqual(Run("abc¶d‖Ｏ↗"), """\
  ad
  b 
abc 
d   """)
        self.assertEqual(Run("a¶d¶ghi‖Ｏ↗"), """\
adg
d h
ghi""")
        self.assertEqual(Run("abcＭ↖d‖Ｏ↗"), """\
   a
   b
  dc
abc """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↙"), """\
  a c
  d  
adghi
  h  
c i  """)
        self.assertEqual(Run("a c¶ d¶ghi‖Ｏ↙"), """\
  a c
   d 
a ghi
 dh  
c i  """)
        self.assertEqual(Run("  a¶ d¶ghi‖Ｏ↙"), """\
    a
   d 
  ghi
 dh  
a i  """)
        self.assertEqual(Run("a¶bcd‖Ｏ↙"), """\
 a  
abcd
 c  
 d  """)
        self.assertEqual(Run("abc¶d‖Ｏ↙"), """\
 abc
ad  
b   
c   """)
        self.assertEqual(Run("a¶d¶ghi‖Ｏ↙"), """\
  a  
  d  
adghi
  h  
  i  """)
        self.assertEqual(Run("abcＭ↖d‖Ｏ↙"), """\
   d
 abc
 b  
dc  """)
        self.assertEqual(Run("a c¶d¶ghi‖Ｏ↘"), """\
a c  
d    
ghi c
  h  
  gda""")
        self.assertEqual(Run("a c¶ d¶ghi‖Ｏ↘"), """\
a c  
 d   
ghi c
  hd 
  g a""")
        self.assertEqual(Run("  a¶ d¶ghi‖Ｏ↘"), """\
  a  
 d   
ghi a
  hd 
  g  """)
        self.assertEqual(Run("a¶bcd‖Ｏ↘"), """\
a   
bcd 
  c 
  ba""")
        self.assertEqual(Run("abc¶d‖Ｏ↘"), """\
abc
d b
 da""")
        self.assertEqual(Run("a¶d¶ghi‖Ｏ↘"), """\
a    
d    
ghi  
  h  
  gda""")
        self.assertEqual(Run("a¶d¶ghi‖ＯＯ↘²"), """\
a   
di  
ghi 
 gda""")
        self.assertEqual(Run("abcＭ↖d‖ＯＯ↖²"), """\
 cd
abc
 a """)
        self.assertEqual(Run("abc‖ＯＯ→⁰"), """\
abccba""")
        self.assertEqual(Run("""\
Print('a\\nbc\\ndef\\nghij\\nklmno');
ReflectOverlapOverlap(:UpRight, 2);
Print('-');""", verbose=True), """\
 a    
abcgk 
 defl 
 ghij 
 klmno
    o 
    - """)
        self.assertEqual(Run("""\
polygon :d :r 5 '*'
reflectoverlapoverlap :d 5
print 'a'""", verbose=True), """\
****a
**** 
***  
**** 
*****""")
        self.assertEqual(Run("""\
polygon :u :r 5 '*'
reflectoverlapoverlap :u 5
print 'a'""", verbose=True), """\
*****
**** 
***  
**** 
****a""")
        self.assertEqual(Run("""\
polygon :u :le 5 '*'
reflectoverlapoverlap :le 5
print 'a'""", verbose=True), """\
****a
*****
*****
** **
*   *""")
        self.assertEqual(Run("""\
polygon :u :r 5 '*'
reflectoverlapoverlap :r 5
print 'a'""", verbose=True), """\
a****
*****
*****
** **
*   *""")

    def test_reflect_butterfly(self):
        self.assertEqual(Run("<<|\\‖Ｂ→"), "<<|\\|>>")
        self.assertEqual(Run("foobar¶‖Ｂ↓a"), """\
foobar
a     
foopar""")

    def test_rotate(self):
        self.assertEqual(Run("abc¶def¶ghi⟲²"), "cfi\nbeh\nadg")
        self.assertEqual(Run("abc¶def¶ghi⟲¹"), """\
  c  
 b f 
a e i
 d h 
  g  """)
        self.assertEqual(Run("abc¶def¶ghi↑⟲¹a"), """\
  c a
 b f 
a e i
 d h 
  g  """)
        self.assertEqual(Run("abc¶def¶ghi↑⟲³a"), """\
a i  
 f h 
c e g
 b d 
  a  """)
        self.assertEqual(Run("a c¶d¶g⟲²a"), "c  \n  a\nadg")
        self.assertEqual(Run("a c¶d¶g⟲⁶a"), "gda\na  \n  c")
        self.assertEqual(Run("a c¶d¶g⟲⁴a"), " ag\n  d\nc a")
        self.assertEqual(Run("↘asdf⟲²↘asdf"), """\
    a   
   f s  
  d   d 
 s     f
a       """)

    def test_reflect(self):
        self.assertEqual(Run("a c¶d¶ghi‖←a"), " c a\n   d\naihg")
        self.assertEqual(Run("a c¶d¶ghi‖→a"), " c a\n   d\naihg")
        self.assertEqual(Run("a c¶d¶ghi‖↑a"), "ghia\nd   \na c ")
        self.assertEqual(Run("a c¶d¶ghi‖↓a"), "ghia\nd   \na c ")
        self.assertEqual(Run("a c¶d¶ghi‖↖a"), "a  \ni c\nh  \ngda")
        self.assertEqual(Run("a c¶d¶ghi‖↗a"), "adg\n  h\nc i\n  a")
        self.assertEqual(Run("a c¶d¶ghi‖↙a"), "adg\n  h\nc i\n  a")
        self.assertEqual(Run("a c¶d¶ghi‖↘a"), "a  \ni c\nh  \ngda")

    def test_polygon(self):
        self.assertEqual(Run("Ｇ+⁵a"), """\
aaaaa
aaaaa
aaaaa
aaaaa
aaaaa""")
        self.assertEqual(Run("Ｇ↗↘←⁴*#Ｍ↓*"), """\
   #   
  *#*  
 #*#*# 
*#*#*#*
   *   """)
        self.assertEqual(Run("Ｇ↗↘←⁴*#¶#*Ｍ↓*"), """\
   *   
  *#*  
 *#*#* 
*#*#*#*
   *   """)
        self.assertEqual(Run("Ｇ↘↗↙↙⁵#"), """\
#########
######## 
#######  
######   
#####    
####     
###      
##       
#        """)
        self.assertEqual(Run("Ｇ*⁵#"), """\
    #####    
   #######   
  #########  
 ########### 
#############
#############
#############
#############
#############
 ########### 
  #########  
   #######   
    #####    """)
        self.assertEqual(Run("ＧＨ↙→→↖⊕÷Ｌθ⁴θ", "\
thisrepresentationisnotatriangle"), """\
        t        
       h e       
      i   l      
     s     g     
    r       n    
   e         a   
  p           i  
 r             r 
esentationisnotat""")

    def test_cycle_chop(self):
        self.assertEqual(Run("…abc¹⁰"), "abcabcabca")

    def test_crop(self):
        self.assertEqual(Run("abcddd¶d¶ghi¶j¶j¶jjjＭ³↖Ｔ³¦³"), """\
ghi
j  
j  """)
        self.assertEqual(Run("Ｍ⁵↑ＵＯχ*Ｍ⁵↘Ｔ³¦³#"), """\
#**
***
***""")

    def test_extend(self):
        self.assertEqual(Run("foobarＵＥ¹"), "f o o b a r")
        self.assertEqual(Run("foobar¶baz¶→→quuxＵＥ³¦³"), """\
f   o   o   b   a   r
                     
                     
                     
b   a   z            
                     
                     
                     
    q   u   u   x    """)

    def test_clear(self):
        self.assertEqual(Run("foobar⎚bazquux"), "bazquux")

    def test_exponentiate(self):
        self.assertEqual(Run("Ｘ²¦³"), "--------")

    def test_index(self):
        self.assertEqual(Run("§abc²"), "c")
        self.assertEqual(Run("§⟦¹a²b³⟧²"), "--")
        self.assertEqual(Run("§⦃c¹b²a³⦄a"), "---")
        self.assertEqual(Run("Ｌ§ψ⁰"), "-")

    def test_ternary(self):
        self.assertEqual(Run("⎇¹¦¹÷¹¦⁰"), "-")

    def test_plus(self):
        self.assertEqual(Run("⁺¹a"), "1a")
        self.assertEqual(Run("⁺¹⟦a⟧"), "1a")
        self.assertEqual(Run("⁺¹⟦⟦a⟧⟧"), "1a")
        self.assertEqual(Run("⁺¹¦¹"), "--")
        self.assertEqual(Run("⁺””a"), "a")

    def test_minus(self):
        self.assertEqual(Run("⁻²¦¹"), "-")

    def test_multiply(self):
        self.assertEqual(Run("×²¦³"), "------")
        self.assertEqual(Run("×⟦²⟧³"), "------")
        self.assertEqual(Run("×⟦⟦²⟧⟧³"), "------")
        self.assertEqual(Run("×⟦²⟧⟦³⟧"), "------")
        self.assertEqual(Run("×⟦⟦²⟧⟧⟦⟦³⟧⟧"), "------")
        self.assertEqual(Run("×²abc"), "abcabc")
        self.assertEqual(Run("×²⟦abc⟧"), "abcabc")
        self.assertEqual(Run("×²⟦⟦abc⟧⟧"), "abcabc")

    def test_divide(self):
        self.assertEqual(Run("÷⁵¦²"), "--")
        self.assertEqual(Run("÷abcabcab³"), "ab")
        self.assertEqual(Run("÷⟦abcabcab⟧³"), "ab")
        self.assertEqual(Run("÷⟦⟦abcabcab⟧⟧³"), "ab")
        # self.assertEqual(Run("÷⟦a¹a²b²c³⟧³"), "a\n-")

    def test_and(self):
        self.assertEqual(Run("∧⁰¦÷¹¦⁰"), "")

    def test_or(self):
        self.assertEqual(Run("∨¹¦÷¹¦⁰"), "-")

    def test_not(self):
        self.assertEqual(Run("¬⁰"), "-")

    def test_comparison(self):
        self.assertEqual(Run("⁼¹¦¹"), "-")
        self.assertEqual(Run("‹⁰¦¹"), "-")
        self.assertEqual(Run("›¹¦⁰"), "-")
        self.assertEqual(Run("⁼⁰¦¹"), "")
        self.assertEqual(Run("‹²¦¹"), "")
        self.assertEqual(Run("›¹¦²"), "")

    def test_cast(self):
        self.assertEqual(Run("Ｉ¹¹¹"), "111")
        self.assertEqual(Run("Ｉ5"), "-----")

    def test_minimum(self):
        self.assertEqual(Run("Ｉ⌊⟦¹¦²¦³¦±¹⟧"), "-1")
        self.assertEqual(Run("Ｉ⌊⁹⁹·⁵"), "99")
        self.assertEqual(Run("⌊foobar"), "a")
        self.assertEqual(Run("⌊ω"), "")

    def test_maximum(self):
        self.assertEqual(Run("⌈⟦¹¦²¦³¦±¹⟧"), "---")
        self.assertEqual(Run("Ｉ⌈⁹⁹·⁵"), "100")
        self.assertEqual(Run("⌈foobar"), "r")
        self.assertEqual(Run("⌈ω"), "")

    def test_join(self):
        self.assertEqual(Run("⪫⟦a¦b¦c⟧foo"), "afoobfooc")

    def test_split(self):
        self.assertEqual(Run("⪪afoobfooc¦foo"), "a\nb\nc")
        self.assertEqual(Run("Ｉ⪪Ｘ²¦³²¦⁹"), "42 \n4  \n672\n6  ")
        self.assertEqual(Run("⪪β⪪aeiou¹"), "     \nbcd  \nfgh  \njklmn\npqrst\nvwxyz")

    def test_lowercase(self):
        self.assertEqual(Run("↧FOOBAR"), "foobar")
        self.assertEqual(Run("↧⟦"), "")

    def test_uppercase(self):
        self.assertEqual(Run("↥foobar"), "FOOBAR")
        self.assertEqual(Run("↥⟦"), "")

    def test_power(self):
        self.assertEqual(Run("Ｘ²¦³"), "--------")

    def test_push(self):
        self.assertEqual(Run("≔⟦¹¦²¦³⟧α⊞Ｏα¦⁴"), "-   \n--  \n--- \n----")
        self.assertEqual(Run("≔⟦¹¦²¦³⟧α⊞α¦⁴α"), "-   \n--  \n--- \n----")

    def test_pop(self):
        self.assertEqual(Run("≔⟦¹¦²¦³⟧α⊟α"), "---")

    def test_negate(self):
        self.assertEqual(Run("±±¹"), "-")
        self.assertEqual(Run("±⟦ω"), "-")

    def test_ranges(self):
        self.assertEqual(Run("…¹¦¹⁰"), """\
-        
--       
---      
----     
-----    
------   
-------  
-------- 
---------""")
        self.assertEqual(Run("…a¦e"), "a\nb\nc\nd")
        self.assertEqual(Run("…·¹¦¹⁰"), """\
-         
--        
---       
----      
-----     
------    
-------   
--------  
--------- 
----------""")
        self.assertEqual(Run("…·a¦e"), "a\nb\nc\nd\ne")

    def test_find(self):
        self.assertEqual(Run("⌕abcd¦c"), "--")
        self.assertEqual(Run("⌕⟦¹a²b³c⁴d⟧¦³"), "----")
        self.assertEqual(Run("⌕Ａabcdc¦c"), "--  \n----")
        self.assertEqual(Run("⌕Ａ⟦a³a¹a²b³c⁴d⟧¦³"), "-      \n-------")

    def test_pad(self):
        self.assertEqual(Run("◧foo⁵"), "  foo")
        self.assertEqual(Run("◨foo⁵"), "foo  ")

    def test_chr_ord(self):
        self.assertEqual(Run("℅⁶⁵"), "A")
        self.assertEqual(Run("Ｉ℅A"), "65")

    def test_reverse(self):
        self.assertEqual(Run("⮌foobar"), "raboof")
        self.assertEqual(Run("⮌⟦¹a²b⟧"), "b \n--\na \n- ")
        self.assertEqual(Run("Ｉ⮌¹·²"), "2.1")
        self.assertEqual(Run("Ｉ⮌±¹²"), "-21")

    def test_toggle_trim(self):
        self.assertEqual(Run("↓foo×⪫ＫＡω⁵ＵＴ"), """\
f
o
o
foofoofoofoofoo""")

    def test_peek(self):
        # TODO: test manipulation
        self.assertEqual(Run("barＭ←×ＫＫ⁵"), "barrrrr")
        self.assertEqual(Run("barＭ←⪫ＫＤ³←ω"), "barab")
        self.assertEqual(Run("↓foo×⪫ＫＡω⁵"), """\
f              
o              
o              
foofoofoofoofoo""")
        self.assertEqual(Run("baz←Ｍ←×⪫ＫＭω⁵"), "bzbzbzbzbzb")
        self.assertEqual(Run("quux←Ｍ←×⪫ＫＶω⁵"), "quxuxuxuxuxu")
        self.assertEqual(Run(
            "quux``4`M``4`*``j`K`V`w`5",
            grave=True
        ), "quxuxuxuxuxu")
        self.assertEqual(Run(
            "Multiprint('a');Print(Times(Peek(),2));",
            verbose=True
        ), "aa")

    def test_count(self):
        self.assertEqual(Run("№foo¦o"), "--")
        self.assertEqual(Run("№⟦¹a¹⟧¦¹"), "--")

    def test_map(self):
        self.assertEqual(Run("Ｅ⟦¹1²⟧Ｉι"), "1\n-\n2")
        self.assertEqual(Run("map 6 times '🐐' i ", verbose=True), """\
     
🐐    
🐐🐐   
🐐🐐🐐  
🐐🐐🐐🐐 
🐐🐐🐐🐐🐐""")

    def test_string_map(self):
        self.assertEqual(Run("⭆Ｓ⎇﹪κＩηι×ιＩη", "['Hello, World!', '3']"), "\
HHHellllo,   Worrrld!!!")
        self.assertEqual(Run("⭆χι"), "0123456789")

    def test_base(self):
        self.assertEqual(Run("\
cast basestring 'asdf' 62", verbose=True), "2491733")
        self.assertEqual(Run("cast base [1,2,3,4] 62", verbose=True), "246206")
        self.assertEqual(Run("basestring 2491733, 62", verbose=True), "asdf")
        self.assertEqual(Run("base 246206, 62", verbose=True), """\
-   
--  
--- 
----""")

    def test_sqrt(self):
        self.assertEqual(Run("sqrt 9", verbose=True), "---")
        self.assertEqual(Run("sqrt 10", verbose=True), "---")
        self.assertEqual(Run("₂⟦10"), "---")

    def test_abs(self):
        self.assertEqual(Run("abs negate 9", verbose=True), "---------")
        self.assertEqual(Run("↔-9"), "9")
        self.assertEqual(Run("↔⟦"), "")

    def test_filter(self):
        self.assertEqual(Run("filter 5 i", verbose=True), """\
-   
--  
--- 
----""")
        self.assertEqual(Run("filter [1,2,3,4,0] (--i)", verbose=True), """\
--  
--- 
----
    """)

    def test_reduce(self):
        self.assertEqual(Run("\
Print(Cast(Reduce([1,2,3,4,5,6,7],{Plus(i,k)})))", verbose=True), "28")

    def test_any(self):
        self.assertEqual(Run("Print(Any([0,0,1,0],i))", verbose=True), "-")
        self.assertEqual(Run("Print(Any([0,0,0,0],i))", verbose=True), "")
        self.assertEqual(Run("Print(Any(2,i))", verbose=True), "-")

    def test_all(self):
        self.assertEqual(Run("Print(All([1,2,3,1],i))", verbose=True), "-")
        self.assertEqual(Run("Print(All([1,2,0,1],i))", verbose=True), "")
        self.assertEqual(Run("Print(All(2,i))", verbose=True), "")

    def test_direction(self):
        self.assertEqual(Run("ＦＮ✳§⟦↘→↗→⟧ι⁻θ¹O", "5"), """\
\\           ----\\    
 \\         /     \\   
  \\       /       \\  
   \\     /         \\ 
    ----/           O""")
        self.assertEqual(Run("ＦＮＰ✳✳⟦dr¦r¦ur¦r⟧⁻θ¹O", "5"), """\
   /
  / 
 /  
O---
 \\  
  \\ 
   \\""")
        self.assertEqual(Run("ＦＮＰ✳✳⟦d¦r¹r⟧⁻θ¹O", "5"), """\
   /
  / 
 /  
O---
|   
|   
|   """)
        self.assertEqual(Run("ＦＮＰ✳✳⟦d¦r¦1¦r⟧⁻θ¹O", "5"), """\
   /
  / 
 /  
O---
|   
|   
|   """)

    def test_ij(self):
        self.assertEqual(Run("→→→ⅈ"), "--")
        self.assertEqual(Run("↓↓↓ⅉ"), " \n \n|\n|")
        
    def test_incremented_decremented_halved_doubled(self):
        self.assertEqual(Run("Ｉ⊕2.25"), "3.25")
        self.assertEqual(Run("Ｉ⊕⟦2.25³·²⁵4.25⟧"), "3.25\n4.25\n5.25")
        self.assertEqual(Run("Ｉ⊕²·²⁵"), "3.25")
        self.assertEqual(Run("Ｉ⊕⟦"), "")
        self.assertEqual(Run("Ｉ⊖2.25"), "1.25")
        self.assertEqual(Run("Ｉ⊖²·²⁵"), "1.25")
        self.assertEqual(Run("Ｉ⊖⟦"), "")
        self.assertEqual(Run("Ｉ⊗¹·²⁵"), "2.5")
        self.assertEqual(Run("Ｉ⊗1.25"), "2.5")
        self.assertEqual(Run("Ｉ⊗⟦"), "")
        self.assertEqual(Run("Ｉ⊘¹·²⁵"), "0.625")
        self.assertEqual(Run("Ｉ⊘1.25"), "0.625")
        self.assertEqual(Run("Ｉ⊘⟦"), "")
        self.assertEqual(Run("cast halved 1.25", verbose="True"), "0.625")

    def test_sum_product(self):
        self.assertEqual(Run("ＩΣ⟦³¦²¦¹⟧"), "6")
        self.assertEqual(Run("ＩΣ⟦⟦¹¦²¦³⟧⟦⁴¦⁵⟧⟦⁶⟧⟧"), "1\n2\n3\n4\n5\n6")
        self.assertEqual(Run("ＩΣ3 2 1 4"), "10")
        self.assertEqual(Run("ＩΣ5..4"), "5.4")
        self.assertEqual(Run("ＩΣ⁰¹²³⁴⁵⁶⁷⁸⁹⁰¹²³⁴⁵⁶⁷⁸⁹"), "90")
        self.assertEqual(Run("ＩΣ01234567890123456789"), "90")
        self.assertEqual(Run("ＩΣ¹·²⁵"), "8")
        self.assertEqual(Run("ＩΠ⟦³¦²¦¹⟧"), "6")
        self.assertEqual(Run("ＩΠ3 2 1 4"), "24")
        self.assertEqual(Run("ＩΠ3 2 1 4"), "24")
        self.assertEqual(Run("ＩΠ5..4"), "2")
        self.assertEqual(Run("ＩΠ12345"), "120")
        self.assertEqual(Run("ＩΠ¹²³⁴⁵"), "120")
        self.assertEqual(Run("ＩΠ⟦"), "1")
        self.assertEqual(Run("ＩΠ¹·²⁵"), "10")

    def test_map_assign(self):
        self.assertEqual(Run("≔⟦³¦²¦¹⟧β≧×²ββ"), "------\n----  \n--    ")
        self.assertEqual(Run("≔⟦³¦²¦¹⟧β≧⁻¹ββ"), "--\n- \n  ")
        self.assertEqual(Run("≔⟦³¦²¦¹⟧β≦⁻³ββ"), "  \n- \n--")

    def test_lambda(self):
        self.assertEqual(Run("«a"), "a")
        self.assertEqual(Run("↓«abc"), "a\nb\nc")

    def test_dictionary_verbose(self):
        self.assertEqual(Run("""\
Print({".": "e"});""", verbose=True), "{'.': 'e'}")

    def test_compression(self):
        self.assertEqual(Run("”y≔⟦³¦²¦¹⟧β▷sβ”"), "≔⟦³¦²¦¹⟧β▷sβ")
        self.assertEqual(Run("”y≔⟦³¦²¦¹⟧β▷sβ"), "≔⟦³¦²¦¹⟧β▷sβ")
        self.assertEqual(Run("Print('´⸿¶')", verbose=True), "´⸿¶")
        self.assertEqual(Run("\
Print('zzyzyzyzyzyzyzyzzzzzzzzyzyz')", verbose=True), "\
zzyzyzyzyzyzyzyzzzzzzzzyzyz")
        self.assertEqual(
            Run(
                "\
Print('aaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccc')",
                verbose=True
            ),
            "aaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccc"
        )
        self.assertEqual(
            Run(
                "\
Print('yyyyyyyyyyyyyyyyyyeeeeeeeeeeeeeeeeeeqqqqqqqqqqqqqqqqqqqqbbbbbbbb')",
                verbose=True
            ),
            "yyyyyyyyyyyyyyyyyyeeeeeeeeeeeeeeeeeeqqqqqqqqqqqqqqqqqqqqbbbbbbbb"
        )
        self.assertEqual(
            Run(
                "\
Print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')",
                verbose=True
            ),
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        )
        self.assertEqual(
            Run(
                r"Print('\\\\\n \\\\              //\\\\\n  \\\\            \
//  \\\\            //\n   \\\\          //    \\\\          //\n    \
\\\\        //      \\\\        //\n     \\\\      //        \\\\      //\
\n      \\\\    //          \\\\    //\n       \\\\  //    //\\\\    \\\\  //\
\n        \\\\//    //  \\\\    \\\\//\n         //    //    \\\\    \\\\\
\n        //\\\\  //      \\\\  //\\\\\n           \\\\//        \\\\//  \
\\\\\n                              \\\\')",
                verbose=True
            ),
            __import__("re").sub(r"\\", r"\\\\", """\
\\                                  
 \\              //\\               
  \\            //  \\            //
   \\          //    \\          // 
    \\        //      \\        //  
     \\      //        \\      //   
      \\    //          \\    //    
       \\  //    //\\    \\  //     
        \\//    //  \\    \\//      
         //    //    \\    \\       
        //\\  //      \\  //\\      
           \\//        \\//  \\     
                              \\    """)
        )

    def test_python(self):
        self.assertEqual(Run("▷min⟦¹¦²⟧"), "-")
        self.assertEqual(Run("▶random.seed⟦⁰⟧Ｉ▷random.random"), "\
0.8444218515250481")
        self.assertEqual(Run("≔⟦³¦²¦¹⟧β▷Sβ"), "-  \n-- \n---")

    def test_shunt(self):
        self.assertEqual(Run("cast 1 + 2 * 3", verbose=True), "7")
        self.assertEqual(Run("cast -1 + 2 * 3", verbose=True), "5")
        self.assertEqual(Run("cast 9 * (2 + 3)", verbose=True), "45")
        self.assertEqual(Run("i = 100; cast i", verbose=True), "100")
        self.assertEqual(Run("\
i = 10; cast ((i + 2) * (i + 3))", verbose=True), "156")

    def test_wolfram(self):
        # TODO: official examples for number things
        self.assertEqual(Run("▷IntegerQ⟦¹⟧"), "True")
        self.assertEqual(Run("▷IntegerQ⟦¹·¹⟧"), "False")
        self.assertEqual(Run("▷OddQ⟦¹⟧"), "True")
        self.assertEqual(Run("▷OddQ⟦²⟧"), "False")
        self.assertEqual(Run("▷EvenQ⟦²⟧"), "True")
        self.assertEqual(Run("▷EvenQ⟦¹⟧"), "False")
        # not actually wolfram
        self.assertEqual(Run("▷Log10⟦¹²³⁸¹⁹⟧"), "-----")
        self.assertEqual(Run("Ｉ▷N⟦≕Piχ⟧"), "3.141592653")
        self.assertEqual(Run("Ｉ▷N⟦≕Pi⟧"), "3.141592653")
        self.assertEqual(Run("Ｉ▷N⟦≕Degree⟧"), "0.01745329251")
        self.assertEqual(Run("▷StringJoin⟦⟦ab¦cd⟧xy⟧"), "\
abcdxy")
        self.assertEqual(Run("▷StringLength⟦tiger⟧"), "5")
        self.assertEqual(Run("\
▷StringLength⟦⟦cat¦dog¦fish¦coelenterate⟧⟧"), "\
3 \n3 \n4 \n12")
        self.assertEqual(Run("▷StringLength⟦◆´α´β´γ⟷ℬ↵⟧"), "9")
        self.assertEqual(Run("▷StringLength⟦ab¶cd⟧"), "5")
        self.assertEqual(Run("▷StringLength⟦ω⟧"), "0")
        self.assertEqual(Run("▷StringLength⟦´α´β´γ⟧"), "3")
        self.assertEqual(Run("▷StringSplit⟦a bbb cccc aa d⟧"), "\
a   \nbbb \ncccc\naa  \nd   ")
        self.assertEqual(Run("▷StringSplit⟦a--bbb---ccc--dddd¦--⟧"), "\
a   \nbbb \n-ccc\ndddd")
        self.assertEqual(Run("▷StringSplit⟦the cat in the hat⟧"), "\
the\ncat\nin \nthe\nhat")
        self.assertEqual(Run("▷StringSplit⟦192.168.0.1¦.⟧"), "\
192\n168\n0  \n1  ")
        self.assertEqual(Run("\
▷StringSplit⟦123 2.3 4 6″≕WhitespaceCharacter⟧"), "\
123\n2.3\n4  \n6  ")
        self.assertEqual(Run("\
▷StringSplit⟦11a22b3？≕_≕LetterQ⟧"), "11\n22\n3 ")
        self.assertEqual(Run("\
▷StringSplit⟦A tree, an apple, four pears. And more: two sacks\
▷RegularExpression⟦\\W+⟧⟧"), "\
A    \ntree \nan   \napple\nfour \npears\nAnd  \nmore \ntwo  \nsacks")
        self.assertEqual(Run("\
▷StringSplit⟦primes: 2 two 3 three 5 five ...\
⁺⁺≕Whitespace▷RegularExpression⟦\\d⟧≕Whitespace⟧"), "\
primes: \ntwo     \nthree   \nfive ...")
        self.assertEqual(Run("▷StringSplit⟦a-b:c-d:e-f-g¦⟦:¦-⟧⟧"), "\
a\nb\nc\nd\ne\nf\ng")
        self.assertEqual(Run("▷StringSplit⟦a-b:c-d:e-f-g¦｜:¦-⟧"), "\
a\nb\nc\nd\ne\nf\ng")
        self.assertEqual(Run("▷StringSplit⟦a b::c d::e f g➙::¦--⟧"), "\
a b  \n--   \nc d  \n--   \ne f g")
# TODO: DelayedRule, naming etc
#         self.assertEqual(Run("▷StringSplit⟦a--b c--d e«➙--ι»⟧"), """\
# a  \n-- \nb c\n-- \nd e""")
        self.assertEqual(Run("\
▷StringSplit⟦⟦a:b:c:d¦listable:element⟧:⟧"), "\
a       \nb       \nc       \nd       \n        \nlistable\nelement ")
        self.assertEqual(Run("▷StringSplit⟦:a:b:c:¦:≕All⟧"), " \na\nb\nc\n ")
        self.assertEqual(Run("\
▷StringSplit⟦▷StringSplit⟦11:12:13//21:22:23//31:32:33¦//⟧:⟧"), "\
11 12 13\n21 22 23\n31 32 33")
        self.assertEqual(Run("▷StringTake⟦abcdefghijklm⁶⟧"), "abcdef")
        self.assertEqual(Run("▷StringTake⟦abcdefghijklm±⁴⟧"), "jklm")
        self.assertEqual(Run("▷StringTake⟦abcdefghijklm⟦⁵¦¹⁰⟧⟧"), "efghij")
        self.assertEqual(Run("▷StringTake⟦abcdefghijklm⟦⁶⟧⟧"), "f")
        self.assertEqual(Run("▷StringTake⟦abcdefghijklm⟦¹±¹¦²⟧⟧"), "acegikm")
        self.assertEqual(Run("▷StringTake⟦⟦abcdef¦stuv¦xyzw⟧±²⟧"), "\
ef\nuv\nzw")
        self.assertEqual(Run("▷StringTake⟦◆´α´β´γ⟷ℬ↵±⁴⟧"), "ℬ↵")
        self.assertEqual(Run("▷StringTake⟦abc▷UpTo⟦⁴⟧⟧"), "abc")
        self.assertEqual(Run("▷StringTake⟦abc¶def⁵⟧"), "abc\nd  ")
        self.assertEqual(Run("▷StringDrop⟦abcdefghijklm⁴⟧"), "efghijklm")
        self.assertEqual(Run("▷StringDrop⟦abcdefghijklm±⁴⟧"), "abcdefghi")
        self.assertEqual(Run("▷StringDrop⟦abcdefghijklm⟦⁵¦¹⁰⟧⟧"), "abcdklm")
        self.assertEqual(Run("▷StringDrop⟦abcdefghijklm⟦³⟧⟧"), "\
abdefghijklm")
        self.assertEqual(Run("▷StringDrop⟦abcdefghijklm⟦¹±¹¦²⟧⟧"), "bdfhjl")
        self.assertEqual(Run("▷StringDrop⟦⟦abcdef¦xyzw¦stuv⟧±²⟧"), "\
abcd\nxy  \nst  ")
        self.assertEqual(Run("▷StringDrop⟦◆´α´β´γ⟷ℬ↵±⁴⟧"), "◆αβγ⟷")
        self.assertEqual(Run("▷StringDrop⟦abc▷UpTo⟦⁴⟧⟧"), "")
        self.assertEqual(Run("▷StringDrop⟦abc¶def⁴⟧"), "def")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm⁶⟧"), "f")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm⟦¹¦³¦⁵⟧⟧"), "a\nc\ne")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm±⁴⟧"), "j")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm¹；⁶⟧"), "\
a\nb\nc\nd\ne\nf")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm¹；±¹；²⟧"), "\
a\nc\ne\ng\ni\nk\nm")
        self.assertEqual(Run("▷StringPart⟦abcdefghijklm±¹；¹；±²⟧"), "\
m\nk\ni\ng\ne\nc\na")
        self.assertEqual(Run("▷StringPart⟦⟦abcd¦efgh¦ijklm⟧¹⟧"), "\
a\ne\ni")
        self.assertEqual(Run("▷StringPart⟦◆´α´β´γ⟷ℬ↵±⁴⟧"), "")
        self.assertEqual(Run("▷StringPart⟦abcde⟦⟧⟧"), "")
        self.assertEqual(Run("▷StringReplace⟦abbaabbaa➙ab¦X⟧"), "XbaXbaa")
        self.assertEqual(Run("▷StringReplace⟦ababbabbaaababa➙″ab¦X⟧"), "\
XbXbaaXa")
        self.assertEqual(Run("▷▷StringReplace⟦➙″ab¦X⟧⟦ababbabbaaababa⟧"), "\
XbXbaaXa")
        self.assertEqual(Run("▷StringReplace⟦abc abcb abdc➙⁺ab≕_¦X⟧"), "\
X Xb Xc")
        self.assertEqual(Run("\
▷StringReplace⟦abc abcd abcd➙⁺⁺≕WordBoundary¦abc≕WordBoundary¦XX⟧"), "\
XX abcd abcd")
        self.assertEqual(Run("\
▷StringReplace⟦abcd acbd➙▷RegularExpression⟦[ab]⟧¦XX⟧"), "\
XXXXcd XXcXXd")
# TODO: datepattern but i need mathematica for that
        self.assertEqual(Run("\
▷StringReplace⟦abcd acbd➙⁺▷RegularExpression⟦[ab]⟧≕_¦YY⟧"), "\
YYcd YYYY")
# TODO: delayedrule
        self.assertEqual(Run("▷StringReplace⟦abcddbbcbbbacbbaa➙bb¦X²⟧"), "\
abcddXcXbacbbaa")
        self.assertEqual(Run("\
▷StringReplace⟦abcdabcdaabcabcd⟦➙abc¦Y➙d¦XXX⟧⟧"), "YXXXYXXXaYYXXX")
        self.assertEqual(Run("▷StringReplace⟦product: A ´⊕ B➙´⊕¦x⟧"), "\
product: A x B")
        self.assertEqual(Run("\
▷StringReplace⟦The cat in the hat.➙the¦a➙≕IgnoreCase≕True⟧"), "\
a cat in a hat.")
        self.assertEqual(Run("▷StringReplace⟦ Have a nice day. \
➙｜⁺≕StartOfString≕Whitespace⁺≕Whitespace≕EndOfStringω⟧"), "\
Have a nice day.")
        self.assertEqual(Run("\
▷StringReplace⟦this (*comment1*) is a test (*comment2*)\
➙⁺⁺(*▷Shortest⟦≕___⟧¦*)ω⟧"), "this  is a test ")
        self.assertEqual(Run("\
▷StringReplace⟦<title>The Title</title>¶<h1>The <a href='link'>head</a></h1>\
¶<p>Some text follows here...</p>➙⁺⁺<″▷Except⟦>⟧>ω⟧"), """\
The Title                
The head                 
Some text follows here...""")
        self.assertEqual(Run("▷StringCases⟦abcadcacb⁺⁺a≕_¦c⟧"), "abc\nadc")
        self.assertEqual(Run("▷▷StringCases⟦⁺⁺a≕_¦c⟧⟦abcadcacb⟧"), "abc\nadc")
        self.assertEqual(Run("\
▷StringCases⟦the cat in the hat⁺⁺a≕__¦e⟧"), "at in the")
        self.assertEqual(Run("\
▷StringCases⟦11a22b3″≕DigitCharacter⟧"), "11\n22\n3 ")
        self.assertEqual(Run("\
▷StringCases⟦11a22b3？≕_≕LetterQ⟧"), "a\nb")
        self.assertEqual(Run("\
▷StringCases⟦a1b22c333▷RegularExpression⟦..2⟧⟧"), "1b2")
        self.assertEqual(Run("\
▷StringCases⟦On 31/12/2003 we left, and on 5/3/2004 we came back\
▷DatePattern⟦⟦Day¦Month¦Year⟧⟧⟧"), "31/12/2003\n5/3/2004  ")
        self.assertEqual(Run("\
▷StringCases⟦the cat in the hat\
⁺▷RegularExpression⟦(?<=the )⟧″≕WordCharacter⟧"), "cat\nhat")
        self.assertEqual(Run("▷StringCases⟦abcddbbbacbbaa″｜a¦bb²⟧"), "a \nbb")
        self.assertEqual(Run("\
▷StringCases⟦abcdabcdcd⟦abc¦cd⟧⟧"), "abc\nabc\ncd ")
        self.assertEqual(Run("\
▷StringCases⟦abcdabcdcd｜abc¦cd⟧"), "abc\nabc\ncd ")
        self.assertEqual(Run("\
▷StringCases⟦⟦ability¦argument¦listable⟧⁺⁺a≕___¦l⟧"), "\
abil\n    \n    \n    \nabl ")
        self.assertEqual(Run("\
▷StringCases⟦cat Cat hat CAT¦cat➙≕IgnoreCase≕True⟧"), "cat\nCat\nCAT")
        self.assertEqual(Run("\
▷StringCases⟦ab bac adaf⁺a″≕LetterCharacter⟧"), "ab  \nac  \nadaf")
        self.assertEqual(Run("▷StringCases⟦ab bac adaf\
⁺a″≕LetterCharacter➙≕Overlaps≕True⟧⟧"), "ab  \nac  \nadaf\naf  ")
        # TODO Overlaps -> All
        self.assertEqual(Run("≔message¦This is a text with 3 phones numbers: \
(800)965-3726, (217)398-6500 and (217)398-5151.\
▷StringCases⟦≕message⁺⁺⁺⁺⁺\
(″≕DigitCharacter¦)″≕DigitCharacter¦-″≕DigitCharacter⟧"), """\
(800)965-3726
(217)398-6500
(217)398-5151""")
        self.assertEqual(Run("\
▷StringReplace⟦⟦aaabbbbaaaa¦bbbaaaab¦aaabab⟧➙ab¦X⟧"), "\
aaXbbbaaaa\nbbbaaaX   \naaXX      ")
        self.assertEqual(Run("▷StringCount⟦abbaabbaa¦bb⟧"), "2")
        self.assertEqual(Run("▷StringCount⟦abcadcadcbaac⁺⁺a≕_¦c⟧"), "4")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat¦cat⟧"), "1")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat⁺⁺a≕__¦e⟧"), "1")
        self.assertEqual(Run("▷StringCount⟦11a22b3″≕DigitCharacter⟧"), "3")
        self.assertEqual(Run("▷StringCount⟦11a22b3？≕_≕LetterQ⟧"), "2")
        self.assertEqual(Run("\
▷StringCount⟦a1b22c333▷RegularExpression⟦..2⟧⟧"), "1")
        self.assertEqual(Run("\
▷StringCount⟦the cat in the hat\
⁺▷RegularExpression⟦(?<=the )⟧″≕WordCharacter⟧"), "2")
        self.assertEqual(Run("▷StringCount⟦abcdabcdcd⟦abc¦cd⟧⟧"), "3")
        self.assertEqual(Run("▷StringCount⟦abcdabcdcd｜abc¦cd⟧"), "3")
        self.assertEqual(Run("\
▷StringCount⟦⟦ability¦argument¦listable⟧⁺⁺a≕___¦l⟧"), "1\n0\n1")
        self.assertEqual(Run("▷StringCount⟦abAB¦a⟧"), "1")
        self.assertEqual(Run("▷StringCount⟦abAB¦a➙≕IgnoreCase≕True⟧"), "2")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat⁺⁺t≕__¦t⟧"), "1")
        self.assertEqual(Run("\
▷StringCount⟦the cat in the hat⁺⁺t≕__¦t➙≕Overlaps≕True⟧"), "3")
        self.assertEqual(Run("\
▷StringPosition⟦abXYZaaabXYZaaaaXYZXYZ¦XYZ⟧"), "\
 3  5\n10 12\n17 19\n20 22")
        self.assertEqual(Run("\
▷▷StringPosition⟦XYZ⟧⟦abXYZaaabXYZaaaaXYZXYZ⟧"), "\
 3  5\n10 12\n17 19\n20 22")
        self.assertEqual(Run("▷StringPosition⟦XYZabc¦XYZ⟧"), "1 3")
        self.assertEqual(Run("\
▷StringPosition⟦abXYZaaabXYZaaaaXYZXYZ¦XYZ¹⟧"), "3 5")
        self.assertEqual(Run("\
▷StringPosition⟦AAAAA¦AA⟧"), "1 2\n2 3\n3 4\n4 5")
        self.assertEqual(Run("\
▷StringPosition⟦AAAAA¦AA➙≕Overlaps≕False⟧"), "1 2\n3 4")
        self.assertEqual(Run("▷StringPosition⟦ABAABBAABABB⟦ABA¦AA⟧⟧"), "\
 1  3\n 3  4\n 7  8\n 8 10")
        self.assertEqual(Run("\
▷StringPosition⟦ABAABBAABABB⟦ABA¦AA⟧➙≕Overlaps≕False⟧"), "1 3\n7 8")
        self.assertEqual(Run("\
▷StringPosition⟦abAB¦a➙≕IgnoreCase≕True⟧"), "1 1\n3 3")
        self.assertEqual(Run("\
▷StringPosition⟦abAB¦a➙≕IgnoreCase≕False⟧"), "1 1")
        self.assertEqual(Run("▷StringRepeat⟦a⁵⁰⟧"), "a" * 50)
        self.assertEqual(Run("▷StringRepeat⟦abc¹⁰⟧"), "abc" * 10)
        self.assertEqual(Run("▷StringRepeat⟦TTAGGG¹⁰⁰⟧"), "TTAGGG" * 100)
        self.assertEqual(Run("▷StringRepeat⟦ab¹⁰¦¹⁹⟧"), ("ab" * 10)[:19])
        self.assertEqual(Run("▷StringDelete⟦1 2 3 4 5 6 7 8 9¦ ⟧"), "\
123456789")
        self.assertEqual(Run("▷StringDelete⟦CACACGTCGACT¦CAC⟧"), "\
ACGTCGACT")
        self.assertEqual(Run("\
▷StringDelete⟦abcde12345abcde″≕DigitCharacter⟧"), "abcdeabcde")
        self.assertEqual(Run("▷▷StringDelete⟦ ⟧⟦1 2 3 4 5 6 7 8 9⟧"), "\
123456789")
        self.assertEqual(Run("\
▷StringDelete⟦ABCDE12345abcde¦AB➙≕IgnoreCase≕False⟧⟧"), "\
CDE12345abcde")
        self.assertEqual(Run("\
▷StringDelete⟦ABCDE12345abcde¦AB➙≕IgnoreCase≕True⟧⟧"), "\
CDE12345cde")
        self.assertEqual(Run("▷RemoveDiacritics⟦ḥ⟧"), "h")
        self.assertEqual(Run("▷RemoveDiacritics⟦ā⟧"), "a")
        self.assertEqual(Run("▷RemoveDiacritics⟦ï⟧"), "i")
        self.assertEqual(Run("▷RemoveDiacritics⟦naïve⟧"), "naive")
        self.assertEqual(Run("▷RemoveDiacritics⟦haček⟧"), "hacek")
        self.assertEqual(Run("▷RemoveDiacritics⟦⟦ā¦ḥ¦ï⟧⟧"), "a\nh\ni")
        self.assertEqual(Run("▷RemoveDiacritics⟦Ε´υ´ρώ´π´η⟧"), "Ευρωπη")
        # TODO: break ligatures
        # TODO: StringTemplate
        self.assertEqual(Run("▷StringRiffle⟦⟦a¦b¦c¦d¦e⟧⟧"), "a b c d e")
        self.assertEqual(Run("▷StringRiffle⟦⟦a¦b¦c¦d¦e⟧, ⟧"), "a, b, c, d, e")
        self.assertEqual(Run("▷StringRiffle⟦⟦a¦b¦c¦d¦e⟧⟦(¦, ¦)⟧⟧"), "\
(a, b, c, d, e)")
        self.assertEqual(Run("\
▷StringRiffle⟦⟦⟦a¦b¦c⟧⟦d¦e¦f⟧⟧⟧"), "a b c\nd e f")
        self.assertEqual(Run("▷StringRiffle⟦⟦⟦a¦b¦c⟧⟦d¦e¦f⟧⟧¶¦	⟧"), "\
a	b	c\nd	e	f")
        self.assertEqual(Run("\
▷StringRiffle⟦⟦⟦a¦27⟧⟦b¦28⟧⟦c¦29⟧⟧⟦{¦, ¦}⟧: ⟧"), "\
{a: 27, b: 28, c: 29}")
        self.assertEqual(Run("▷StringStartsQ⟦abcd¦a⟧"), "True")
        self.assertEqual(Run("▷StringStartsQ⟦quickSort¦quick⟧"), "True")
        self.assertEqual(Run("▷StringStartsQ⟦United States¦United⟧"), "True")
        self.assertEqual(Run("\
▷StringStartsQ⟦⟦int1¦int2¦int3¦float1¦float2¦longint1⟧¦int⟧"), "\
True \nTrue \nTrue \nFalse\nFalse\nFalse")
        self.assertEqual(Run("▷StringStartsQ⟦Abcd¦a➙≕IgnoreCase≕False⟧"), "\
False")
        self.assertEqual(Run("▷StringStartsQ⟦Abcd¦a➙≕IgnoreCase≕True⟧"), "\
True")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦d⟧"), "True")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦a⟧"), "False")
        self.assertEqual(Run("▷StringEndsQ⟦quickSort¦Sort⟧"), "True")
        self.assertEqual(Run("▷StringEndsQ⟦Great Dane¦Dane⟧"), "True")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦D➙≕IgnoreCase≕False⟧"), "\
False")
        self.assertEqual(Run("▷StringEndsQ⟦abcD¦d➙≕IgnoreCase≕True⟧"), "True")
        # TODO: select
        self.assertEqual(Run("▷StringContainsQ⟦bcde⁺⁺c≕__¦t⟧"), "False")
        self.assertEqual(Run("▷StringContainsQ⟦bcde⁺⁺b≕__¦e⟧"), "True")
        self.assertEqual(Run("\
▷StringContainsQ⟦⟦a¦b¦ab¦abcd¦bcde⟧¦a⟧"), "True \nFalse\nTrue \nTrue \nFalse")
        self.assertEqual(Run("\
▷StringContainsQ⟦abcd¦BC➙≕IgnoreCase≕False⟧"), "False")
        self.assertEqual(Run("\
▷StringContainsQ⟦abcd¦BC➙≕IgnoreCase≕True⟧"), "True")
        self.assertEqual(Run("▷FromDigits⟦⟦⁵¦¹¦²¦⁸⟧⟧"), "5128")
        self.assertEqual(Run("▷FromDigits⟦⟦¹¦⁰¦¹¦¹¦⁰¦¹¦¹⟧²⟧"), "91")
        self.assertEqual(Run("▷FromDigits⟦1923⟧"), "1923")
        self.assertEqual(Run("▷FromDigits⟦1011011²⟧"), "91")
        self.assertEqual(Run("\
▷FromDigits⟦⟦¹¦⁴¦²⁵¦⁴¹⟧▷MixedRadix⟦⟦²⁴¦⁶⁰¦⁶⁰⟧⟧⟧"), "102341")
        self.assertEqual(Run("▷FromDigits⟦⟦≕a≕b≕c≕d≕e⟧≕x⟧"), "\
a x ^ 4 + b x ^ 3 + c x ^ 2 + d x + e")
        # TODO: Expand
        self.assertEqual(Run("▷FromDigits⟦⟦⁷¦¹¹¦⁰¦⁰¦⁰¦¹²²⟧⟧"), "810122")
        # TODO: RealDigits
        self.assertEqual(Run("▷FromDigits⟦⟦⟦¹⟦⁵¦⁷¦¹¦⁴¦²¦⁸⟧⟧¹⟧"), "11/7")
        self.assertEqual(Run("\
▷FromDigits⟦⟦³¦²¦⁵⟧▷MixedRadix⟦⟦³¦¹²⟧⟧⟧"), "137")
        self.assertEqual(Run("▷FromDigits⟦XVII¦Roman⟧"), "17")
        self.assertEqual(Run("▷FromDigits⟦⟦¹¦²¦³≕Indeterminate⟧⟧"), "123")
        # TODO: scientific notation for reals
        self.assertEqual(Run("▷N⟦▷FromDigits⟦⟦⟦⟦¹¦²¦³⟧⟧⁰⟧⟧³⁰⟧"), "\
0.123123123123123123123123123123")
        # TODO: Array
        self.assertEqual(Run("Ｅ▷Tuples⟦⟦⁰¦¹⟧⁴⟧▷FromDigits⟦⟦⟦ι⟧⁰⟧²⟧"), """\
0    \n1/15 \n2/15 \n1/5  \n4/15 \n1/3  \n2/5  \n7/15 \n8/15 \n3/5  \n1/15 
11/15\n4/5  \n13/15\n14/15\n1    """)
        self.assertEqual(Run("▷FromDigits⟦⟦⟦⟦¹¦²¦³⟧⟧⁰⟧⟧"), "41/333")
        # TODO: tuples, array
        self.assertEqual(Run("\
▷FromDigits⟦⟦¹¦³¦²²¦¹⁴⟧▷MixedRadix⟦⟦²⁴¦⁶⁰¦⁶⁰⟧⟧"), "98534")
        # TODO: NumberCompose, Quantity, UnitConvert

        #Range
        self.assertEqual(Run("▷Range⟦⁴⟧"), "1\n2\n3\n4")
        self.assertEqual(Run("▷Range⟦¹·²¦²·²¦·¹⁵⟧"), "\
1.2 \n1.35\n1.50\n1.65\n1.80\n1.95\n2.10")
        # TODO: symbolic comparison
        self.assertEqual(Run("▷Range⟦¹¦¹⁰¦²⟧"), "1\n3\n5\n7\n9")
        self.assertEqual(Run("▷Range⟦¹⁰¦¹¦±¹⟧"), "\
10\n9 \n8 \n7 \n6 \n5 \n4 \n3 \n2 \n1 ")
        # TODO: symbolic comparison, irrational comparison
        self.assertEqual(Run("▷Range⟦Ｘ²¦²²⁵⁺⁵Ｘ²¦²²⁵⟧"), """\
53919893334301279589334030174039261347274288845081144962207220498432
53919893334301279589334030174039261347274288845081144962207220498433
53919893334301279589334030174039261347274288845081144962207220498434
53919893334301279589334030174039261347274288845081144962207220498435
53919893334301279589334030174039261347274288845081144962207220498436
53919893334301279589334030174039261347274288845081144962207220498437""")
        self.assertEqual(Run("▷Range⟦⟦⁵¦²¦⁶¦³⟧⟧"), "\
1\n2\n3\n4\n5\n \n1\n2\n \n1\n2\n3\n4\n5\n6\n \n1\n2\n3")
        self.assertEqual(Run("Ｘ≕q▷Range⟦⁵⟧"), "\
q    \nq ^ 2\nq ^ 3\nq ^ 4\nq ^ 5")
        # TODO: even more things
#        self.assertEqual(Run("\
#≔⟦±²¦⁹¦⁵¦³¦±³¦±⁶¦±⁷¦±⁴¦⁸¦³⟧χ¦×χＸ≕x▷Range⟦⁰¦⁻Ｌχ¹⟧"), "-2 + 9 x + 5 x ^ 2 + \
#3 x ^ 3 - 3 x ^ 4 - 6 x ^ 5 - 7 x ^ 6 - 4 x ^ 7 + 8 x ^ 8 + 3 x ^ 9")
        self.assertEqual(Run("▷Range⟦±⁴¦⁹¦³⟧"), "-4\n-1\n2 \n5 \n8 ")
        self.assertEqual(Run("▷Range⟦▷Range⟦⁵⟧⟧"), "1\n \n1\n2\n \n1\n2\n3\n \
\n1\n2\n3\n4\n \n1\n2\n3\n4\n5")
        self.assertEqual(Run("▷Range⟦▷Range⟦▷Range⟦³⟧⟧⟧"), "1\n \n \n1\n \n1\n\
2\n \n \n1\n \n1\n2\n \n1\n2\n3")

        # Tuples
        self.assertEqual(Run("▷Tuples⟦⟦⁰¦¹⟧³⟧"), "\
0 0 0\n0 0 1\n0 1 0\n0 1 1\n1 0 0\n1 0 1\n1 1 0\n1 1 1")
        self.assertEqual(Run("▷Tuples⟦⟦¹¦⁰⟧³⟧"), "\
1 1 1\n1 1 0\n1 0 1\n1 0 0\n0 1 1\n0 1 0\n0 0 1\n0 0 0")
        self.assertEqual(Run("▷Tuples⟦⟦⟦≕a≕b⟧⟦¹¦²¦³¦⁴⟧⟦≕x⟧⟧⟧"), "\
a 1 x\na 2 x\na 3 x\na 4 x\nb 1 x\nb 2 x\nb 3 x\nb 4 x")
        self.assertEqual(Run("▷Tuples⟦⟦≕a≕b⟧²⟧"), "a a\na b\nb a\nb b")
        self.assertEqual(Run("▷Tuples⟦⟦≕a≕a≕b⟧²⟧"), "\
a a\na a\na b\na a\na a\na b\nb a\nb a\nb b")
        self.assertEqual(Run("▷Tuples⟦⟦≕a≕b⟧⟦²¦²⟧⟧"), """\
a a\na a\n   \na a\na b\n   \na a\nb a\n   \na a\nb b\n   \na b\na a\n   \n\
a b\na b\n   \na b\nb a\n   \na b\nb b\n   \nb a\na a\n   \nb a\na b\n   \n\
b a\nb a\n   \nb a\nb b\n   \nb b\na a\n   \nb b\na b\n   \nb b\nb a\n   \n\
b b\nb b""")
        self.assertEqual(Run("▷Tuples⟦▷f⟦≕x≕y≕z⟧²⟧"), "\
f[x, x]\nf[x, y]\nf[x, z]\nf[y, x]\nf[y, y]\nf[y, z]\nf[z, x]\nf[z, y]\n\
f[z, z]")
        # TODO: a lot of stuff
        self.assertEqual(Run("▷Tuples⟦⟦⁰¦¹⟧³⟧"), "\
0 0 0\n0 0 1\n0 1 0\n0 1 1\n1 0 0\n1 0 1\n1 1 0\n1 1 1")
        self.assertEqual(Run("Ｅ▷Tuples⟦⟦⁰¦¹⟧³⟧▷FromDigits⟦ι²⟧"), "\
0\n1\n2\n3\n4\n5\n6\n7")
        self.assertEqual(Run("Ｅ▷Tuples⟦⟦A¦B⟧³⟧▷StringJoinι"), "\
AAA\nAAB\nABA\nABB\nBAA\nBAB\nBBA\nBBB")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c⟧⟧"), "\
 \n \na\n \nb\n \nc\n \na\nb\n \na\nc\n \nb\nc\n \na\nb\nc")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d⟧²⟧"), "\
 \n \na\n \nb\n \nc\n \nd\n \na\nb\n \na\nc\n \na\nd\n \nb\nc\n \nb\nd\n \nc\nd")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d⟧⟦²⟧⟧"), "\
a b\na c\na d\nb c\nb d\nc d")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d≕e⟧⟦³⟧⁵⟧"), "\
a b c\na b d\na b e\na c d\na c e")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d≕e⟧⟦⁰¦⁵¦²⟧⟧"), "\
 \n \na\nb\n \na\nc\n \na\nd\n \na\ne\n \nb\nc\n \nb\nd\n \nb\ne\n \nc\nd\n \n\
c\ne\n \nd\ne\n \na\nb\nc\nd\n \na\nb\nc\ne\n \na\nb\nd\ne\n \na\nc\nd\ne\n \n\
b\nc\nd\ne")
        self.assertEqual(Run("▷Subsets⟦▷Range⟦²⁰⟧¦≕All¦⟦⁶⁹³⁸¹⟧⟧"), "\
 1  3  4  5 11 14 17")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d⟧⟧"), "\
 \n \na\n \nb\n \nc\n \nd\n \na\nb\n \na\nc\n \na\nd\n \nb\nc\n \nb\nd\n \n\
c\nd\n \na\nb\nc\n \na\nb\nd\n \na\nc\nd\n \nb\nc\nd\n \na\nb\nc\nd")
        self.assertEqual(Run("▷Subsets⟦⟦≕a≕b≕c≕d⟧≕All⟦¹⁵¦¹¦±²⟧⟧"), "\
b\nc\nd\n \na\nb\nd\n \nc\nd\n \nb\nc\n \na\nc\n \nd\n \nb\n \n ")
        self.assertEqual(Run("▷Subsets⟦▷f⟦≕a≕b≕c⟧⟧"), "\
          \n          \nf[a]      \n          \nf[b]      \n          \n\
f[c]      \n          \nf[a, b]   \n          \nf[a, c]   \n          \n\
f[b, c]   \n          \nf[a, b, c]")
        # TODO: modify SymbolicOperation into heads (subclasses)

    def test_preinitialized(self):
        self.assertEqual(Run("θ", "a b c d e"), "a")
        self.assertEqual(Run("η", "a b c d e"), "b")
        self.assertEqual(Run("ζ", "a b c d e"), "c")
        self.assertEqual(Run("ε", "a b c d e"), "d")
        self.assertEqual(Run("δ", "a b c d e"), "e")
        self.assertEqual(Run("γ"), " !\"#$%&'()*+,-./0123456789:;<=>?@\
ABCDEFGHIJKLMNOPQRSTUVWXYZ\
[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~")
        self.assertEqual(Run("β"), "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(Run("α"), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.assertEqual(Run("ω"), "")
        self.assertEqual(Run("aψcＵＢb"), "abc")
        self.assertEqual(Run("χ"), "----------")
        self.assertEqual(Run("φ"), "-" * 1000)

    def test_input(self):
        self.assertEqual(
            Run("ＷＳι", "[\"abc\", 5, \"foobar\"]"),
            "abc5foobar"
        )
        self.assertEqual(
            Run("ＷＳι", "abc\n5\nfoobar"),
            "abc5foobar"
        )
        self.assertEqual(
            Run("ＷＳι", "abc 5 foobar"),
            "abc5foobar"
        )
        self.assertEqual(
            Run("ＷＮι", "[1, 2, \"3\"]"),
            "------"
        )
        self.assertEqual(
            Run("ＷＮι", "1\n2\n3"),
            "------"
        )
        self.assertEqual(
            Run("ＷＮι", "1 2 3"),
            "------"
        )
        self.assertEqual(Run("Ａ", "[[1, 2, 3]]"), "-  \n-- \n---")
        self.assertEqual(Run("Ａ", "[{\"foo\": \"bar\"}]"), "{'foo': 'bar'}")

    def test_escape(self):
        self.assertEqual(Run("Ｇ+⁵a´¶´‖"), """\
a¶‖a¶
a¶‖a¶
a¶‖a¶
a¶‖a¶
a¶‖a¶""")
        self.assertEqual(Run("`G+`5a`` `\n`` `;", grave=True), """\
a¶‖a¶
a¶‖a¶
a¶‖a¶
a¶‖a¶
a¶‖a¶""")

    def test_whitespace(self):
        self.assertEqual(Run("""\
Ｇ
 +
  ⁵
   a´ """, whitespace=True), """\
a a a
a a a
a a a
a a a
a a a""")

    def test_codepage(self):
        self.assertEqual(Run("\xC7+\xB5a\xE0 ", normal_encoding=True), """\
a a a
a a a
a a a
a a a
a a a""")
        self.assertEqual(Run("\xFF\xA4\xEC", normal_encoding=True), "╬")

    def test_challenges(self):
        self.assertEqual(Run("≔p....Pβrnbkqbnr↙↷²×⁺β¶⁷β↶²RNBKQBNR"), """\
rnbkqbnr
pppppppp
........
........
........
........
PPPPPPPP
RNBKQBNR""")
        pi_slice = """\
()()()()()()
|\\3.1415926|
|:\\53589793|
\\::\\2384626|
 \\::\\433832|
  \\::\\79502|
   \\::\\8841|
    \\::\\971|
     \\::\\69|
      \\::\\3|
       \\__\\|"""
        self.assertEqual(Run("""\
×⁶()↙↓¹⁰↖↖¹⁰↓↓²↘⁸Ｍ↑__↖←¤:↗¤\
3.141592653589793238462643383279502884197169"""), pi_slice)
        self.assertEqual(
            Run("""\
Print(Multiply(6, '()'));
Move(:DownLeft);
Print(:Down, 10);
Move(:UpLeft);
Print(:UpLeft, 10);
Move(:Down);
Print(:Down, 2);
Print(:DownRight, 8);
Move(:Up);
Print('__');
Move(:UpLeft);
Move(:Left);
Fill(':');
Move(:UpRight);
Fill('3.141592653589793238462643383279502884197169')""", verbose=True),
            pi_slice
        )
        self.assertEqual(Run("""\
×⁶()↙↓¹⁰↖↖¹⁰↓↓²↘⁸Ｍ↑__↖←¤:↗¤≕Pi"""), pi_slice)
        self.assertEqual(
            Run("__↗¹←↑¹↖²←_↘‖Ｍ←¤Ｓ", "#"), """\
  __  
 /##\\ 
/####\\
|####|
\\____/"""
        )
        self.assertEqual(
            Run(
                "ＦＳ¿⁼ι(«(↓»«Ｍ↑)",
                "(()(()())()((())))(())"
            ), """\
(                )(  )
 ()(    )()(    )  () 
    ()()    (  )      
             ()       """)
        self.assertEqual(
            Run(
                """\
Ｎβ≔-~-¶θ¿‹β⁰Ｆ³θ¿β«θＦβ⁺-~-|$¶θ»↓\
Congratulations on your new baby! :D⟲²""",
                "4"
            ), """\
 $ $ $ $ 
 | | | | 
---------
~~~~~~~~~
---------"""
        )
        self.assertEqual(Run("Ｇ↗↘←Ｎ*Ｍ↓*", "4"), """\
   *   
  ***  
 ***** 
*******
   *   """)
        self.assertEqual(Run("Ｅ…⁰⁻Ｌθ¹⪫θ× ι‖Ｏ←↑", "star"), """\
r  a  t  s  t  a  r
   r a t s t a r   
      ratstar      
   r a t s t a r   
r  a  t  s  t  a  r""")
        self.assertEqual(Run("Ｉ▷N⟦≕Eφ⟧"), "\
2.7182818284590452353602874713526624977572470936999595749669676277240766303535\
475945713821785251664274274663919320030599218174135966290435729003342952605956\
307381323286279434907632338298807531952510190115738341879307021540891499348841\
675092447614606680822648001684774118537423454424371075390777449920695517027618\
386062613313845830007520449338265602976067371132007093287091274437470472306969\
772093101416928368190255151086574637721112523897844250569536967707854499699679\
468644549059879316368892300987931277361782154249992295763514822082698951936680\
331825288693984964651058209392398294887933203625094431173012381970684161403970\
198376793206832823764648042953118023287825098194558153017567173613320698112509\
961818815930416903515988885193458072738667385894228792284998920868058257492796\
104841984443634632449684875602336248270419786232090021609902353043699418491463\
140934317381436405462531520961836908887070167683964243781405927145635490613031\
07208510383750510115747704171898610687396965521267154688957035035")
        self.assertEqual(Run("""\
while (InputString()) {
	Assign(Cast(Split(i, " ")), i);
	for (Range(AtIndex(i, 0), AtIndex(i, 2))) {
		JumpTo(k, AtIndex(i, 1));
		MapCommand(
		    PeekDirection(Minus(AtIndex(i, 3), AtIndex(i, 1)), :Down),
		    AtIndex("10", Sum(l))
		);
	}
}""", """\
0 0 9 9
1 1 10 10
2 2 11 11
""", verbose=True), """\
111111111  
1000000001 
10111111101
10111111101
10111111101
10111111101
10111111101
10111111101
10111111101
 1000000001
  111111111""")
        self.assertEqual(Run("""\
atindex '↙↓↘' 0""", verbose=True), "↙")
        self.assertEqual(Run("""\
if (InputNumber()) Print(1)
else print("|");
if (InputNumber()) Print(1);
else print("|");""", "1 0", verbose=True), "-|")
        self.assertEqual(Run("""\
for (10) {
	switch (i) {
		case 7: Print(">");
		case 8: Print("=");
		case 9: Print(">");
		default: Print("-");
	}
}""", verbose=True), "------->=>")
        # TODO: document switch correctly

    def test_grammars(self):
        from charcoaltoken import CharcoalTokenNames
        from unicodegrammars import UnicodeGrammars
        from verbosegrammars import VerboseGrammars
        from astprocessor import ASTProcessor
        from interpreterprocessor import InterpreterProcessor
        from stringifierprocessor import StringifierProcessor
        result = ""
        for key in UnicodeGrammars:
            if (
                key in ASTProcessor and
                len(UnicodeGrammars[key]) != len(ASTProcessor[key])
            ):
                result += "Unicode != AST " + CharcoalTokenNames[key] + "\n"
            if (
                key in InterpreterProcessor and
                len(UnicodeGrammars[key]) != len(InterpreterProcessor[key])
            ):
                result += (
                    "Unicode != Interpreter " + CharcoalTokenNames[key] + "\n"
                )
        for key in VerboseGrammars:
            if (
                key in StringifierProcessor and
                len(VerboseGrammars[key]) != len(StringifierProcessor[key])
            ):
                result += (
                    "Verbose != Stringifier " + CharcoalTokenNames[key] + "\n"
                )
        self.assertEqual(result[:-1], "")

CharcoalTests = unittest.TestLoader().loadTestsFromTestCase(CharcoalTest)


def RunTests():
    unittest.main(defaultTest="CharcoalTests", argv=[sys.argv[0]])

if __name__ == "__main__":
    RunTests()
