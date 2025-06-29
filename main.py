import os
import whois
import re
from datetime import datetime


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

def format_value(value):
    # Format lists and datetimes nicely
    
    if isinstance(value, list):
        # Remove duplicates and None values, flatten nested lists
        value = [v for v in value if v is not None]
        
        if all(isinstance(v, datetime) for v in value):
            return '\n  - '.join(dt.strftime('%Y-%m-%d %H:%M:%S') for dt in value)
        return '\n  - '.join(str(v) for v in value)
        
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
        
    elif value is None:
        return 'None'
        
    else:
        return str(value)
    
def is_valid_domain(domain):
    pattern = r"^(?!\-)([a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None

def run_whois(domain):
    try:
        info = whois.whois(domain)
        print(f"\n[ WHOIS Information for {domain} ]\n")

        keys = sorted(k for k in info.keys() if info.get(k) is not None)
        label_width = max(len(k) for k in keys) + 1  # +1 for space before ":"

        for key in keys:
            value = info.get(key)
            key_label = f"{key.replace('_', ' ').capitalize():<{label_width}}: "
            indent = ' ' * len(key_label)

            if isinstance(value, list):
                cleaned_list = list(dict.fromkeys(str(v).strip() for v in value if v))
                
                if not cleaned_list:
                    continue
                print(f"{key_label}{cleaned_list[0]}")
                for item in cleaned_list[1:]:
                    print(f"{indent}{item}")
                print()

            elif isinstance(value, datetime):
                print(f"{key_label}{value.strftime('%Y-%m-%d %H:%M:%S')}\n")

            else:
                print(f"{key_label}{str(value).strip()}\n")

    except Exception as e:
        print(f"[!] Error during WHOIS lookup: {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def help_chart():
    print("""
Available commands:
  w    whois    Domain name registration info   
  h    help     Show this help message
  c    clear    Clear the screen
  e    exit     Quit Aladdin
""")

def main():
    wc_banner()
    while True:
        command = input("> ").strip().lower()
        
        if command == "":
            print()
            continue

        if command in ("h", "help"):
            help_chart()
            
        elif command in ("clear", "c"):
            clear_screen()
            wc_banner()
            
        elif command.startswith("w") or command.startswith("whois"):
            parts = command.split()
            
            if len(parts) == 2:
                domain = parts[1]
                
                if is_valid_domain(domain):
                    run_whois(domain)
                    
                else:
                    print("[!] Invalid domain format. Example: example.com")
                    
            else:
                print("[!] Usage: whois [domain]")

        elif command in ("e", "exit"):
            print("Goodbye!")
            break
            
        else:
            print(f"Unknown command: '{command}' (type 'h' to see commands)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
