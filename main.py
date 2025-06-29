def wc_banner():
    print("""
                     ..    d$P              $$      `$b
                    z$"   $$F               4$$      $$L
                    $$   4$$                 $$.     4$$    ,z$P
                    $$   $$'                 $$F      $$   $$$P
                   $$$   $$                  $$f      $$   ""`
                  $'$$; 4$F      .,_         $$'      $$
                .$' ?$L 4$'   .d$" `?    zee $$   ,ec $F  d$F z$$   ,ce,.
              .d$ee. $$ 4$'  d$"   z$  $$"  .$f.d$"  4$  4$$ 4$$P z$P?$$$
             d$" "?$$d$,`$  $$F   z$f,$$    $$.$$    $P  $$% $$$4$"   4$$
.$"%.     ,p$"        $$ $ J$$  z$$$ $$"  .$$ $$"  .$$C 4$P  $$$"     $$f
`$.     ,d$b****q,     $.$ $$$$$P $$.$$b.$P4$ $$L.$P4$F $P  4$P     .$$"
 `?$$g$P"        "     `b' `??"   "?"^?F"   $$`?PF"  $$ "   P'     eF

        beginner-friendly reconnaissance tool | by acysecstudent
""")

def main():
    wc_banner()
    while True:
        command = input("> ").strip().lower()

        if command == "help":
            print("""
Available commands:
  help    Show this help message
  exit    Quit Aladdin
""")
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print(f"Unknown command: '{command}' (type 'help' to see commands)")

if __name__ == "__main__":
    main()
