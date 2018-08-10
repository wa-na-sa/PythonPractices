#将图片转化为字符画，用法：
#python "01 pic2char.py" 1.jpg -o 1.txt --width 100 --height 100
from PIL import Image
import argparse

#命令行参数处理
parser = argparse.ArgumentParser()

parser.add_argument("file")
parser.add_argument("-o", "--output")
parser.add_argument("--width", type = int, default = 80)
parser.add_argument("--height", type = int, default = 80)

args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output
#字符列表
char_list = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
#RGB到字符
def rgb2char(r, g, b, aplha = 256):
    if aplha == 0:
        return " "
    length = len(char_list)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)#灰度值公式
    
    unit = (256.0 + 1) / length
    return char_list[int(gray / unit)]

im = Image.open(IMG)
im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

text = ""
for i in range(HEIGHT):
    for j in range(WIDTH):
        text += rgb2char(*im.getpixel((j, i)))
    text += '\n'
print(text)
#输出字符画到文件
if OUTPUT:
    with open(OUTPUT, "w") as f:
        f.write(text)
else:
    with open("output.txt", "w") as f:
        f.write(text)
        
            #                         ...        .             ..                                     
            #                        ... :_(/\/\////tttttftfj\<. ..                                   
            #                      .. "xYunvvuuuvvvvvvccczczzzz0C! ..                                 
            #                         \YruXxxXvnvvvvccccczzzzXXzQJ:                                   
            #                        ;vnuc-''_zcvvvvccccczXXXXXXXOf    .                              
            #                   ...  ?Yuv: .. :cccccccczzzzzXXXXYYO]                                  
            #                    ... ]Yucl '. ;zcvccczzzzzXXXXXYYYO)                                  
            #                   . .. ]XnX\    |UccccczzzzXXXXXYYYYO)                                  
            #             ..    .....]YuuuYYYUcccccczzzzXXXXYYYUUUO)                                  
            #              .... . .. ]YuuuuvcvvccczzzzXXXXXXYYYYUUZ) .. ...  ...                      
            #             .. .  ..   {OYUUJJJJCCCCLQUzXXXXYYYUUUUUZ) ... ... ...                      
            #             ..                   .    ?QXXYYYYYUUUJJm)          ..                      
            #               `!_??]]]]]??]]]]]]]]]][-fJXXYYYYYUJJJJm) `"^^^^^^'.                       
            #         ... ^]rzXXYYYYUUUJJJCCCCLLLLLQJXXYYYUUUUJUJJm).,lII;;;II,.   .                  
            #        .. !XcxnnuuuuuvvvvvcccczzzzXXXXYYYYUYUJJJJJCCm( ";:::;;;;;l:.   .                
            #          "ucxnnnnuuuvvvvvccccczzzzXXXYYYYYUUUJJJJJCCm) ";:::;;;;;Il^....                
            #          (XrnnnnunuuvvvvvccccczzzXXXXYYYYUYUJJJJJJJCm( ";;;:;;;;;Il:...                 
            #       . ;cnnnnuuuuuvvvvvccccczzXXXXXXYYUUUUJJJJJJJJCm) "I:;;;;;;IIIl'...                
            #         (zxnnnuuuvvvvvcccczzzXXXXXXXXzzzXYUUJJJJCJCJw} ,I;;;;;IIIII!:.                  
            #        'fcnnnuuuuvvvvcccccczXXXYXzcccunuvzXYUJJCCJJLO! :;;;;;IIIIIllI.                  
            #        ;vunnuuuuvvvvccccczzzXXXXzcvnxjfjrnvXYJCCCCUmu .;I;;IIIIIIIl!!'                  
            #        _XuuuuvvvvvccccccXzzcvvvuxj/()[_[)|fnzUCJJZp] 'IlIIIIIlIllll!!"                  
            #        [YuuuvvvvvccczzzzXzcvunnnj/(1]]xn}1/nYQZmqJ+.';Ill;IlIllllll!i:                  
            #        1XnnuvvvvvcczzzzXzczzx\{}]-+~;}qzi~]1/xvr]` 'IlI;IIllIllllll!i;..                
            #        -/(\/tfjrrxnnnunvz}' . .+}... >qu .....'`":;;:::::::;;IIlII;I;:.                 
            #        >1}{1)|\//tfrrrxv?  ''.-aY .. <qu..''^",:::::,,,"",:::;:;;;:::".  .              
            #       .;__-?][}{1)|\//r]  `^' ]bx .. >wu..''`^""^",""""^^""",,:,:,,,"`    .             
            # ... .>|ncj?":i!!_/{_]{I ;{~..>fZc?]" >wn  >{)+'.`^`'.;)uv\!.'^^^'.,}rvr{: .             
            # .  !XpQvcwq|.""lUm]i_+. ]*X  vmUJ0Z> >mr_CZ0pdx`.'. ]wdYXpq{..`.'|Z0cvOkQ~              
            #   +bL>  .!Jd} `;UQ_l+l  _pn.  ]pn'`' >QLZf;'Ickj . ]kY;..:Yh( .^zp)'  .rpC^             
            #   }k/ . ``:Xq- "YQ<,i,  _qu   -dn  . >qx  .' "UZ> {kj .''' fk\ ,LJ"..  .cm>             
            #   }k/   ."`xd( ^YQ>"!". _qn   -px .. >wn. .. ^XZ! rb{ .''..}pu "LJ,.    vmi             
            #   }b/   .'.fdt ^YQi`l"  _pn   -pn .. >wu. .'.^YZl up] '''' _qz ^LJ"     cmi             
            #   }b/      jdf ^YQi';^ ._pn.  -dn .. >qu..'' "Yml nd[ '''' -wz ^LJ"     cmi             
            #   }k/     ^Xp} "YQl.:`  _pu   -dx... >wu'.''."YZi [dx .''' /h) :LJ^     cmi             
            #   }b/     _mQ; ^Yw- ^'  +pn . ?bx .. >wu'.``."YOi "Qm! .' ,Cw! :LJ^     cmi             
            #   }mC?.  ;Jk(  ./kU!   !zmn.. >qJ, ..<qn  .. `YZi  ]hY'   j*(  :LJ^     cmi             
            #   }k(.(cXr+  ... .?jvx(:!mu .'..+xX!.I|]^^""^,}(I.^'.!/YXj!    ^{}`    .?),             
            #   }k/         ..        >qx..'^`...^"`.'::::;,''^,""^.             .                    
            #   }k/                 . +b\.'`^","",,,::;;;;;;I;::::;^.                                 
            #   }b/                  ?bU`.",:;;;;II;;Il!!!!^  "!!l!,                                  
            #   )#t              ;-1Ubz;.",:;IIlllll!!!!ii"   .:<i>:                                  
            #   iCf              ]bOc?..^,,;Illl!!!!!iiiii^....^><<:                                  
            #                         ,::IIll!!!!i!iiii>><l...'l>>i'                                  
            #                         `I;lll!!!!ii!iiii>>>>!:,!<<<"   .                               
            #                        . ^!!!!!!!!!!iiii>ii>><~~><~: .                                  
            #                         ...',l>>>>>>><<><<<<<<<!:'....                                  
            #                         ...  .^;lllllllllllll;". .....                                  