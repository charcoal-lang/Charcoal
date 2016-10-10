from charcoal import Run
import unittest
import sys


class CharcoalTest(unittest.TestCase):
    def test_print(self):
        self.assertEqual(Run("abc"), "abc")
        self.assertEqual(Run("abc←←Ｍ←abc"), "abc")
        self.assertEqual(Run("→abc"), "abc")
        self.assertEqual(Run("↓abc"), "a\nb\nc")
        self.assertEqual(Run("←abc"), "cba")
        self.assertEqual(Run("↑abc"), "c\nb\na")
        self.assertEqual(Run("↖abc"), "c  \n b \n  a")
        self.assertEqual(Run("↗abc"), "  c\n b \na  ")
        self.assertEqual(Run("↘abc"), "a  \n b \n  c")
        self.assertEqual(Run("↙abc"), "  a\n b \nc  ")
        self.assertEqual(Run("↓abc←def"), "  a\n  b\n  c\nfed")

    def test_multiprint(self):
        self.assertEqual(Run("Ｐabc"), "abc")
        self.assertEqual(Run("Ｐ→abc"), "abc")
        self.assertEqual(Run("Ｐ↓abc"), "a\nb\nc")
        self.assertEqual(Run("Ｐ←abc"), "cba")
        self.assertEqual(Run("Ｐ↑abc"), "c\nb\na")
        self.assertEqual(Run("Ｐ→↓abc"), "abc\nb  \nc  ")
        self.assertEqual(Run("Ｐ+abc"), "  c  \n  b  \ncbabc\n  b  \n  c  ")

    def test_jump(self):
        self.assertEqual(Run("aＪ³¦³a"), """\
a    
     
     
    a""")

    def test_eval(self):
        self.assertEqual(Run("ＶＳ", ["abc←←Ｍ←abc"]), "abc")
        self.assertEqual(Run("↓ＶＳ", ["⁺⁵¦⁵"]), ("|\n" * 10)[:-1])

    def test_box(self):
        self.assertEqual(Run("Ｂ⁵¦⁵*"), """\
*****
*   *
*   *
*   *
*****""")

    def test_rectangle(self):
        self.assertEqual(Run("Ｒ⁵¦⁵"), """\
+---+
|   |
|   |
|   |
+---+""")

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

    def test_for(self):
        self.assertEqual(Run("Ｆ⁵a"), "aaaaa")
        self.assertEqual(Run("Ａ⁵ιＦＳκ", ["foobar"]), "foobar")

    def test_while(self):
        self.assertEqual(Run("Ａ⁵βＷβ«abＡ⁻β¹β»"), "ababababab")

    def test_if(self):
        self.assertEqual(Run("¿¹asdf"), "asdf")
        self.assertEqual(Run("¿⁰asdf"), "")
        self.assertEqual(Run("¿⁰«asdf»ghjk"), "ghjk")

    def test_pivot(self):
        self.assertEqual(Run("↶¹asdf"), "   f\n  d \n s  \na   ")
        self.assertEqual(Run("↶²asdf"), "f\nd\ns\na")

    def test_rotate_copy(self):
        pass

    def test_reflect_copy(self):
        self.assertEqual(Run("abc¶def¶ghi‖Ｃ←"), "cbaabc\nfeddef\nihgghi")
        self.assertEqual(Run("abc¶d¶gh‖Ｃ←"), "cbaabc\n  dd  \n hggh ")
        self.assertEqual(Run("abc¶d¶gh‖Ｃ→"), "abccba\nd    d\ngh  hg")
        self.assertEqual(Run("abc¶  d¶ gh‖Ｃ←"), "cbaabc\nd    d\nhg  gh")
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↑"), "ghi\nd  \na c\na c\nd  \nghi")
        self.assertEqual(Run("a c¶d¶ghi‖Ｃ↓"), "a c\nd  \nghi\nghi\nd  \na c")
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

    def test_rotate_overlap(self):
        pass

    def test_reflect_overlap(self):
        self.assertEqual(Run("abc¶def¶ghi‖Ｏ←"), "cbabc\nfedef\nihghi")
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

    def test_rotate(self):
        self.assertEqual(Run("abc¶def¶ghi⟲²"), "cfi\nbeh\nadg")
        self.assertEqual(Run("abc¶def¶ghi⟲¹"), """\
  c  
 b f 
a e i
 d h 
  g  """)

    def test_reflect(self):
        self.assertEqual(Run("abc¶def¶ghi‖←"), "cba\nfed\nihg")
        self.assertEqual(Run("abc¶d¶gh‖←"), "cba\n  d\n hg")
        self.assertEqual(Run("abc¶d¶gh‖→"), "cba\n  d\n hg")
        self.assertEqual(Run("a c¶d¶ghi‖↑"), "ghi\nd  \na c")
        self.assertEqual(Run("a c¶d¶ghi‖↓"), "ghi\nd  \na c")
        self.assertEqual(Run("a c¶d¶ghi‖↖"), "i c\nh  \ngda")
        self.assertEqual(Run("a c¶d¶ghi‖↗"), "adg\n  h\nc i")
        self.assertEqual(Run("a c¶d¶ghi‖↘"), "i c\nh  \ngda")
        self.assertEqual(Run("a c¶d¶ghi‖↙"), "adg\n  h\nc i")

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

    def test_escape(self):
        self.assertEqual(Run("Ｇ+⁵a´¶´‖"), """\
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
        self.assertEqual(Run("""\
×⁶()↙↓¹⁰↖↖¹⁰↓↓²↘⁸Ｍ↑__↖←¤:↗¤\
3.141592653589793238462643383279502884197169"""), """\
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
       \\__\\|""")
        self.assertEqual(
            Run(
                "ＦＳ¿⁼ι(«(↓»«Ｍ↑)",
                ["(()(()())()((())))(())"]
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
                ["4"]
            ), """\
 $ $ $ $  
 | | | |  
--------- 
~~~~~~~~~ 
--------- """
        )
        self.assertEqual(Run("Ｇ↗↘←Ｎ*Ｍ↓*", ["4"]), """\
   *   
  ***  
 ***** 
*******
   *   """)


CharcoalTests = unittest.TestLoader().loadTestsFromTestCase(CharcoalTest)


def RunTests():
    unittest.main(defaultTest="CharcoalTests", argv=[sys.argv[0]])

if __name__ == "__main__":
    RunTests()
