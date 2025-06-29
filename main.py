import os
import whois
import re
from datetime import datetime
import concurrent.futures
import dns.resolver
import requests


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

def load_wordlist(filepath="subdomains.txt"):
    try:
        with open(filepath, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist '{filepath}' not found.")
        return []
        
def dns_bruteforce(domain, wordlist):
    found = []

    def resolve_sub(sub):
        full_domain = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(full_domain, "A")
            return full_domain
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(resolve_sub, wordlist)

    for result in results:
        if result:
            found.append(result)

    return found
    
def query_public_sources(domain):
    found = set()

    try:
        response = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name_value = entry.get("name_value", "")
                for sub in name_value.splitlines():
                
                    if domain in sub:
                        found.add(sub.strip())
    except:
        pass

    try:
        response = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                sub = line.split(",")[0].strip()
                if domain in sub:
                    found.add(sub)
    except:
        pass

    return list(found)
    
def find_subdomains(domain, wordlist_path="subdomains.txt"):
    print(f"\n[ Subdomain Enumeration for {domain} ]\n")

    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        return

    brute_results = dns_bruteforce(domain, wordlist)
    api_results = query_public_sources(domain)

    all_found = sorted(set(brute_results + api_results))

    if all_found:
        for sub in all_found:
            print(f"[+] {sub}")
        print(f"\n[✓] Total found: {len(all_found)}")
    else:
        print("[!] No subdomains found.")
        
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
            
        elif cmd in ["s", "sub"]:
    
            if len(args) != 1:
                print("[!] Usage: sub [domain]")
            
            elif not is_valid_domain(args[0]):
                print("[!] Invalid domain format. Example: example.com")
            
            else:
                find_subdomains(args[0])

            
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
