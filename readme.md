這個專案在實作 sic/xe 的 assembler，以下為各檔案之概述：
- sicxe.py 內含 OPTAB, DIRECTIVE, registerOP
- sicxeasmparser.py 內含讀檔的相關操作
- objfile.py 有輸出至 object file 的各種函式
- assembler.py 中有 pass1 和 pass2
    - pass1 先建立 SYMTAB (symbol table)
    - pass2 則產生 object program
- textbooksicxe.obj 是 textbooksicxe.asm 的 object program
- sample.obj 是 textbooksicxe.asm 的 object program 參考解答
