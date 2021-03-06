#!/usr/bin/python3
from classes import Opts, Strings, Versioning
from scanner import scan
from versioncheck import check_version

import argparse
from requests import get
from sys import argv
from colorama import init, Fore, Style

init()

if __name__ == '__main__':
    if len(argv) == 2:
        if "--version" in argv[1]:
            try:
                version_info = get(Versioning.URL).json()
            except:
                print("[-] Error checking for updates. (Could not connect to GitHub)")
                exit(1)
                
            if version_info['version_new'] != Versioning.VERSION:    
                print("[+] New version available: " + version_info['version_new'])
                print("[i] Current version: " + Versioning.VERSION)
                print("[i] Update at: " + version_info['update_url'])
                print("[i] Changelog: ")
                [print(">\t" + line) for line in version_info['changelog']]
                        
            print(f"{Fore.GREEN}[+] HTTPSCAN Version: " + Versioning.VERSION + Style.RESET_ALL)
            exit(0)

    argp = argparse.ArgumentParser(
        description='Scan a host for open HTTP ports and gain information about the services present.',
        epilog='Example: python3 httpscan.py example.com | python3 httpscan.py -h')
    argp.add_argument('host', help='[Host To Scan] The domain to scan. EX: example.com.', type=str)
    argp.add_argument('--json', help='[JSON Override] Print raw JSON output instead of shell presentation.', action='store_true', default=False)
    argp.add_argument('--all', help='[Save All] Print each port\'s status, not just open ones.', action='store_true', default=False)
    argp.add_argument('--print_headers', help='[Shell] Print HTTP response headers along with existing output.', action='store_true', default=False)
    argp.add_argument('--print_body', help='[Shell] Print HTTP response body along with existing output.', action='store_true', default=False)
    argp.add_argument('--user_agent', 
                      help='[Request Header] Arbitrarily set your user-agent request-header. EX: --user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36".', action='store', 
                      default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36")
    argp.add_argument('--origin',
                    help='[Request Header] Arbitrarily set the origin request-header. EX: --origin="https://example.com".', action='store',
                    default="https://google.com")
    argp.add_argument('--path', 
                        help='[Request Header] Arbitrarily set the path request-header. EX: --path="/".', action='store',
                        default="/")
    argp.add_argument('--http_ports_file', help='[Resource] File name of JSON array of HTTP ports to scan. Default: httpscan/resources/http_ports.json.', action='store', default="httpscan/resources/http_ports.json")
    argp.add_argument('--ssl_ports_file', help='[Resource] File name of JSON array of HTTPS ports to scan. Default: httpscan/resources/ssl_ports.json.', action='store', default="httpscan/resources/ssl_ports.json")        
    argp.add_argument('--headers_file', help='[Resource] File name of JSON array of HTTP request headers to use. Default: httpscan/resources/http_headers.json', action='store', default="httpscan/resources/http_headers.json")
    argp.add_argument('--add_headers_file', help='[Resource] File name of JSON array of HTTP request headers to add to existing headers. Default: httpscan/resources/add_http_headers.json', action='store', default="httpscan/resources/add_http_headers.json")
    argp.add_argument('--socket_timeout', help='[Tuning] Timeout in seconds (float) until socket connection establishment effort is aborted.', action='store', type=float, default=1.0)
    argp.add_argument('--response_timeout', help='[Tuning] Timeout in seconds (float) until current socket connection is aborted while waiting for response.', action='store', type=float, default=1.0)
    argp.add_argument('--threads', help='[Tuning] Number of threads to use for scanning. Default: 1.', action='store', type=int, default=1)
    argp.add_argument('--follow_redirects', help='[Tuning] Follow redirects; Default: False.', action='store_true', default=False)
    argp.add_argument('--max_redirects', help='[Tuning] Max amount of redirects. "--follow_redirects" must be enabled. Default: 5.', action='store', default=5)
    argp.add_argument('--silence_updates', help='[Overrides] Hides/ignores new update notifications. Default: False.', action='store_true', default=False)
    argp.add_argument('--check_version', help='[Utilities] Prints version + checks for updates then exits.', action='store_true', default=False)
    args, leftovers = argp.parse_known_args()
    
    # Set options
    Opts.setArgs(args)
    
    check_version()
    
    if not Opts.json:
        with open('httpscan/resources/httpscan.logo', 'r') as f:
            Strings.logo = Fore.GREEN + f.read() + Style.RESET_ALL
        print(Strings.logo)
   
    scan()

    

    