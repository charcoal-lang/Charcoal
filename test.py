#!/usr/bin/env python3
# VIM: let b:airline_whitespace_disabled=1
"""
Charcoal's test module.

Contains unit tests, and runs them when invoked.

"""

# TODO: test capitalum (crlf)

from charcoal import Run
import unittest
import sys

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
        self.assertEqual(Run("ＰK¦*****"), """\
*   *
*  * 
* *  
**   
*    
**   
* *  
*  * 
*   *""")
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
        self.assertEqual(Run("""
Box(Times(2.999, 1.999), 5.999, '123')""", verbose=True), """\
12312
1   3
3   1
2   2
13213""")

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
        self.assertEqual(Run("Ａ⁵ιＦＳκ", "foobar"), "foobar")
        self.assertEqual(Run("≔i«ικλ»▶i⟦a¦bc¦d⟧"), "abcd")
        self.assertEqual(Run("for(5)Print('a')", verbose=True), "aaaaa")
        self.assertEqual(
            Run(
                "Assign(5,i);for(InputString())Print(k)",
                "foobar",
                verbose=True
            ),
            "foobar"
        )

    def test_while(self):
        self.assertEqual(Run("Ａ⁵βＷβ«abＡ⁻β¹β»"), "ababababab")
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

    def test_slice(self):
        self.assertEqual(Run("✂abc"), "abc")
        self.assertEqual(Run("✂abcd²"), "cd")
        self.assertEqual(Run("✂abc⁰¦²"), "ab")
        self.assertEqual(Run("✂abcdefg⁰¦⁹¦²"), "aceg")

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
        self.assertEqual(Run("|¶-¶/¶\¶v¶^¶<¶>⟲Ｔ²"), "-|\/v^<>")
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
        self.assertEqual(Run("a¶¶¶¶¶→→→→a‖Ｃ↙"), """\
   a   
       
       
a      
       
      a
     a """)
        self.assertEqual(Run("a¶¶¶¶¶←←←←a‖Ｃ↘"), """\
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
        self.assertEqual(Run("a¶¶¶¶¶→→→→a‖Ｏ↙"), """\
  a   
      
a     
      
      
     a""")
        self.assertEqual(Run("a¶¶¶¶¶←←←←a‖Ｏ↘"), """\
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

    def test_reflect_butterfly(self):
        self.assertEqual(Run("<<|\\‖Ｂ→"), "<<|\|>>")

    def test_rotate(self):
        self.assertEqual(Run("abc¶def¶ghi⟲²"), "cfi\nbeh\nadg")
        self.assertEqual(Run("abc¶def¶ghi⟲¹"), """\
  c  
 b f 
a e i
 d h 
  g  """)
        self.assertEqual(Run("abc¶def¶ghi⟲¹a"), """\
  c   
 b f a
a e i 
 d h  
  g   """)
        self.assertEqual(Run("abc¶def¶ghi⟲³a"), """\
 a   
  i  
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

    def test_cycle_chop(self):
        self.assertEqual(Run("…abc¹⁰"), "abcabcabca")

    def test_crop(self):
        self.assertEqual(Run("abcddd¶d¶ghi¶j¶j¶jjjＭ³↖Ｔ³¦³"), """\
ghi
j  
j  """)

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

    def test_ternary(self):
        self.assertEqual(Run("⎇¹¦¹÷¹¦⁰"), "-")

    def test_plus(self):
        self.assertEqual(Run("⁺¹a"), "1a")
        self.assertEqual(Run("⁺¹¦¹"), "--")
        self.assertEqual(Run("⁺””a"), "a")

    def test_minus(self):
        self.assertEqual(Run("⁻²¦¹"), "-")

    def test_multiply(self):
        self.assertEqual(Run("×²¦³"), "------")
        self.assertEqual(Run("×²¦abc"), "abcabc")
        self.assertEqual(Run("×²¦⟦abc⟧"), "abc\nabc")

    def test_divide(self):
        self.assertEqual(Run("÷⁵¦²"), "--")
        self.assertEqual(Run("÷abcabcab¦³"), "ab")
        self.assertEqual(Run("÷⟦a¹a²b²c³⟧¦³"), "a\n-")

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

    def test_maximum(self):
        self.assertEqual(Run("⌈⟦¹¦²¦³¦±¹⟧"), "---")

    def test_join(self):
        self.assertEqual(Run("⪫⟦a¦b¦c⟧foo"), "afoobfooc")

    def test_split(self):
        self.assertEqual(Run("⪪afoobfooc¦foo"), "a\nb\nc")

    def test_lowercase(self):
        self.assertEqual(Run("↧FOOBAR"), "foobar")

    def test_uppercase(self):
        self.assertEqual(Run("↥foobar"), "FOOBAR")

    def test_power(self):
        self.assertEqual(Run("Ｘ²¦³"), "--------")

    def test_push(self):
        self.assertEqual(Run("Ａ⟦¹¦²¦³⟧α⊞Ｏα¦⁴"), "-   \n--  \n--- \n----")
        self.assertEqual(Run("Ａ⟦¹¦²¦³⟧α⊞α¦⁴α"), "-   \n--  \n--- \n----")

    def test_pop(self):
        self.assertEqual(Run("Ａ⟦¹¦²¦³⟧α⊟α"), "---")

    def test_negate(self):
        self.assertEqual(Run("±±¹"), "-")

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
            "Multiprint('a');Print(*(Peek(),2));",
            verbose=True
        ), "aa")

    def test_count(self):
        self.assertEqual(Run("№foo¦o"), "--")
        self.assertEqual(Run("№⟦¹a¹⟧¦¹"), "--")

    def test_map(self):
        self.assertEqual(Run("Ｅ⟦¹1²⟧Ｉι"), "1\n-\n2")

    def test_reduce(self):
        self.assertEqual(Run("\
Print(Cast(/([1,2,3,4,5,6,7],{Print(+(i,k))})))", verbose=True), "28")

    def test_any(self):
        self.assertEqual(
            Run("Print(Any([0,0,1,0],{Print(i)}))", verbose=True),
            "-"
        )
        self.assertEqual(
            Run("Print(Any([0,0,0,0],{Print(i)}))", verbose=True),
            ""
        )
        pass

    def test_all(self):
        self.assertEqual(
            Run("Print(All([1,2,3,1],{Print(i)}))", verbose=True),
            "-"
        )
        self.assertEqual(
            Run("Print(All([1,2,0,1],{Print(i)}))", verbose=True),
            ""
        )
        pass

    def test_python(self):
        self.assertEqual(Run("ＵＰmin⟦¹¦²⟧"), "-")
        self.assertEqual(
            Run("ＵＰrandom.seed⟦⁰⟧ＩＵＰrandom.random"), "0.8444218515250481"
        )
        self.assertEqual(Run("Ａ⟦³¦²¦¹⟧βＵＰsβ"), "-  \n-- \n---")
        self.assertEqual(Run("Ａ⟦³¦²¦¹⟧β▷sβ"), "-  \n-- \n---")

    def test_wolfram(self):
        # TODO: official examples for number things
        self.assertEqual(Run("▷IntegerQ⟦¹⟧"), "-")
        self.assertEqual(Run("▷IntegerQ⟦¹·¹⟧"), "")
        self.assertEqual(Run("▷OddQ⟦¹⟧"), "-")
        self.assertEqual(Run("▷OddQ⟦²⟧"), "")
        self.assertEqual(Run("▷EvenQ⟦²⟧"), "-")
        self.assertEqual(Run("▷EvenQ⟦¹⟧"), "")
        self.assertEqual(Run("▷Log10⟦¹²³⁸¹⁹⟧"), "-----")
        self.assertEqual(Run("Ｉ▷N⟦≕Piχ⟧"), "3.141592653")
        self.assertEqual(Run("Ｉ▷N⟦≕Pi⟧"), "3.141592653")
        self.assertEqual(Run("Ｉ▷N⟦≕Degree⟧"), "0.01745329251")
        self.assertEqual(Run("▷StringJoin⟦⟦ab¦cd⟧xy⟧"), """\
abcdxy""")
        self.assertEqual(Run("▷StringLength⟦tiger⟧"), "-----")
        self.assertEqual(Run("\
▷StringLength⟦⟦cat¦dog¦fish¦coelenterate⟧⟧"), "\
---         \n---         \n----        \n------------")
        self.assertEqual(Run("▷StringLength⟦◆´α´β´γ⟷ℬ↵⟧"), "---------")
        self.assertEqual(Run("▷StringLength⟦ab¶cd⟧"), "-----")
        self.assertEqual(Run("▷StringLength⟦ω⟧"), "")
        self.assertEqual(Run("▷StringLength⟦´α´β´γ⟧"), "---")
        self.assertEqual(Run("▷StringSplit⟦a bbb cccc aa d⟧"), "\
a   \nbbb \ncccc\naa  \nd   ")
        self.assertEqual(Run("▷StringSplit⟦a--bbb---ccc--dddd¦--⟧"), "\
a   \nbbb \n-ccc\ndddd")
        self.assertEqual(Run("▷StringSplit⟦the cat in the hat⟧"), "\
the\ncat\nin \nthe\nhat")
        self.assertEqual(Run("▷StringSplit⟦192.168.0.1¦.⟧"), "\
192\n168\n0  \n1  ")
        self.assertEqual(Run("\
▷StringSplit⟦123 2.3 4 6‴≕WhitespaceCharacter⟧"), "\
123\n2.3\n4  \n6  ")
        self.assertEqual(Run("\
▷StringSplit⟦11a22b3？≕_≕LetterQ⟧"), "11\n22\n3 ")
        self.assertEqual(Run("\
▷StringSplit⟦A tree, an apple, four pears. And more: two sacks\
▷RegularExpression⟦\W+⟧⟧"), "\
A    \ntree \nan   \napple\nfour \npears\nAnd  \nmore \ntwo  \nsacks")
        self.assertEqual(Run("\
▷StringSplit⟦primes: 2 two 3 three 5 five ...\
⁺⁺≕Whitespace▷RegularExpression⟦\d⟧≕Whitespace⟧"), "\
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
        self.assertEqual(Run("▷StringSplit⟦:a:b:c:¦:≕All⟧"), " \na\nb\nc")
        self.assertEqual(Run("\
▷StringSplit⟦▷StringSplit⟦11:12:13//21:22:23//31:32:33¦//⟧:⟧"), "\
11\n12\n13\n  \n21\n22\n23\n  \n31\n32\n33")
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
▷StringReplace⟦abcdabcdaabcabcd⟦➙abc¦Y➙d¦XXX⟧⟧"), "\
YXXXYXXXaYYXXX")
        self.assertEqual(Run("▷StringReplace⟦product: A ⊕ B➙⊕¦x⟧"), "\
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
▷StringCases⟦⟦ability¦argument¦listable⟧⁺⁺a≕___¦l⟧"), "abil\n    \n    \nabl ")
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
        self.assertEqual(Run("▷StringCount⟦abbaabbaa¦bb⟧"), "--")
        self.assertEqual(Run("▷StringCount⟦abcadcadcbaac⁺⁺a≕_¦c⟧"), "----")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat¦cat⟧"), "-")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat⁺⁺a≕__¦e⟧"), "-")
        self.assertEqual(Run("▷StringCount⟦11a22b3″≕DigitCharacter⟧"), "---")
        self.assertEqual(Run("▷StringCount⟦11a22b3？≕_≕LetterQ⟧"), "--")
        self.assertEqual(Run("\
▷StringCount⟦a1b22c333▷RegularExpression⟦..2⟧⟧"), "-")
        self.assertEqual(Run("\
▷StringCount⟦the cat in the hat\
⁺▷RegularExpression⟦(?<=the )⟧″≕WordCharacter⟧"), "--")
        self.assertEqual(Run("▷StringCount⟦abcdabcdcd⟦abc¦cd⟧⟧"), "---")
        self.assertEqual(Run("▷StringCount⟦abcdabcdcd｜abc¦cd⟧"), "---")
        self.assertEqual(Run("\
▷StringCount⟦⟦ability¦argument¦listable⟧⁺⁺a≕___¦l⟧"), "-\n \n-")
        self.assertEqual(Run("▷StringCount⟦abAB¦a⟧"), "-")
        self.assertEqual(Run("▷StringCount⟦abAB¦a➙≕IgnoreCase≕True⟧"), "--")
        self.assertEqual(Run("▷StringCount⟦the cat in the hat⁺⁺t≕__¦t⟧"), "-")
        self.assertEqual(Run("\
▷StringCount⟦the cat in the hat⁺⁺t≕__¦t➙≕Overlaps≕True⟧"), "---")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦abXYZaaabXYZaaaaXYZXYZ¦XYZ⟧ＥιＩλ"), "\
3 \n5 \n  \n10\n12\n  \n17\n19\n  \n20\n22")
        self.assertEqual(Run("\
Ｅ▷▷StringPosition⟦XYZ⟧⟦abXYZaaabXYZaaaaXYZXYZ⟧ＥιＩλ"), "\
3 \n5 \n  \n10\n12\n  \n17\n19\n  \n20\n22")
        self.assertEqual(Run("Ｅ▷StringPosition⟦XYZabc¦XYZ⟧ＥιＩλ"), "1\n3")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦abXYZaaabXYZaaaaXYZXYZ¦XYZ¹⟧ＥιＩλ"), "3\n5")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦AAAAA¦AA⟧ＥιＩλ"), "1\n2\n \n2\n3\n \n3\n4\n \n4\n5")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦AAAAA¦AA➙≕Overlaps≕False⟧ＥιＩλ"), "1\n2\n \n3\n4")
        self.assertEqual(Run("Ｅ▷StringPosition⟦ABAABBAABABB⟦ABA¦AA⟧⟧ＥιＩλ"), "\
1 \n3 \n  \n3 \n4 \n  \n7 \n8 \n  \n8 \n10")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦ABAABBAABABB⟦ABA¦AA⟧➙≕Overlaps≕False⟧ＥιＩλ"), "\
1\n3\n \n7\n8")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦abAB¦a➙≕IgnoreCase≕True⟧ＥιＩλ"), "1\n1\n \n3\n3")
        self.assertEqual(Run("\
Ｅ▷StringPosition⟦abAB¦a➙≕IgnoreCase≕False⟧ＥιＩλ"), "1\n1")
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
        self.assertEqual(Run("▷StringRiffle⟦⟦⟦a¦b¦c⟧⟦d¦e¦f⟧⟧⟧"), "a b c\nd e f")
        self.assertEqual(Run("▷StringRiffle⟦⟦⟦a¦b¦c⟧⟦d¦e¦f⟧⟧¶¦	⟧"), "\
a	b	c\nd	e	f")
        self.assertEqual(Run("▷StringRiffle⟦⟦⟦a¦27⟧⟦b¦28⟧⟦c¦29⟧⟧⟦{¦, ¦}⟧: ⟧"), "\
{a: 27, b: 28, c: 29}")
        self.assertEqual(Run("▷StringStartsQ⟦abcd¦a⟧"), "-")
        self.assertEqual(Run("▷StringStartsQ⟦quickSort¦quick⟧"), "-")
        self.assertEqual(Run("▷StringStartsQ⟦United States¦United⟧"), "-")
        self.assertEqual(Run("\
▷StringStartsQ⟦⟦int1¦int2¦int3¦float1¦float2¦longint1⟧¦int⟧"), "-\n-\n-")
        self.assertEqual(Run("▷StringStartsQ⟦Abcd¦a➙≕IgnoreCase≕False⟧"), "")
        self.assertEqual(Run("▷StringStartsQ⟦Abcd¦a➙≕IgnoreCase≕True⟧"), "-")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦d⟧"), "-")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦a⟧"), "")
        self.assertEqual(Run("▷StringEndsQ⟦quickSort¦Sort⟧"), "-")
        self.assertEqual(Run("▷StringEndsQ⟦Great Dane¦Dane⟧"), "-")
        self.assertEqual(Run("▷StringEndsQ⟦abcd¦D➙≕IgnoreCase≕False⟧"), "")
        self.assertEqual(Run("▷StringEndsQ⟦abcD¦d➙≕IgnoreCase≕True⟧"), "-")
        self.assertEqual(Run("▷StringContainsQ⟦bcde⁺⁺c≕__¦t⟧"), "")
        self.assertEqual(Run("▷StringContainsQ⟦bcde⁺⁺b≕__¦e⟧"), "-")
        self.assertEqual(Run("\
▷StringContainsQ⟦⟦a¦b¦ab¦abcd¦bcde⟧¦a⟧"), "-\n \n-\n-")
        self.assertEqual(Run("\
▷StringContainsQ⟦⟦a¦b¦ab¦abcd¦bcde⟧¦a⟧"), "-\n \n-\n-")
        self.assertEqual(Run("\
▷StringContainsQ⟦abcd¦BC➙≕IgnoreCase≕False⟧"), "")
        self.assertEqual(Run("\
▷StringContainsQ⟦abcd¦BC➙≕IgnoreCase≕True⟧"), "-")

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
        self.assertEqual(Run("ψ"), "") # null byte
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
        self.assertEqual(Run("Ａp....Pβrnbkqbnr↙↷²×⁺β¶⁷β↶²RNBKQBNR"), """\
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
\____/"""
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
ＮβＡ-~-¶θ¿‹β⁰Ｆ³θ¿β«θＦβ⁺-~-|$¶θ»↓\
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

CharcoalTests = unittest.TestLoader().loadTestsFromTestCase(CharcoalTest)


def RunTests():
    unittest.main(defaultTest="CharcoalTests", argv=[sys.argv[0]])

if __name__ == "__main__":
    RunTests()
