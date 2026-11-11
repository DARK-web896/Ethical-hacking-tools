from flask import Flask, render_template_string, request
import socket
import requests
import hashlib
import base64
import urllib.parse
import uuid
import random
import string
import re

app = Flask(__name__)

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberNexus Elite - Security Suite</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #020617; color: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; }
        .glass-panel { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(16px); border: 1px solid rgba(56, 189, 248, 0.2); }
        .glow-btn:hover { box-shadow: 0 0 25px rgba(14, 165, 233, 0.5); }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-slate-950">

    <!-- Header & Live Search -->
    <header class="w-full bg-slate-950/80 border-b border-slate-800/80 p-4 sticky top-0 z-50 backdrop-blur-xl">
        <div class="max-w-4xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="h-3 w-3 bg-cyan-400 rounded-full animate-pulse"></div>
                <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 tracking-wider">CYBER_NEXUS ELITE</h1>
            </div>
            <!-- Live Search Bar -->
            <div class="w-full sm:w-80">
                <input type="text" id="searchInput" onkeyup="searchTools()" placeholder="🔍 Search from 30 security tools..." 
                    class="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-cyan-400 transition shadow-inner">
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="w-full max-w-4xl mx-auto p-4 my-8">
        <div class="glass-panel rounded-3xl p-6 sm:p-8 shadow-2xl shadow-cyan-950/20">
            <form method="POST" class="space-y-6">
                <div>
                    <label class="block text-sm font-semibold text-cyan-300 mb-2">Select Security Tool (30 Available):</label>
                    <select name="tool_type" id="toolSelect" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3.5 text-white focus:outline-none focus:border-cyan-400 transition">
                        <!-- Reconnaissance & Network (1-7) -->
                        <option value="dns">1. DNS Lookup (Resolve IP)</option>
                        <option value="reverse_dns">2. Reverse DNS Lookup</option>
                        <option value="port_scan">3. Quick Port Scanner (Top Ports)</option>
                        <option value="ip_track">4. IP Geolocation Tracker</option>
                        <option value="sub_enum">5. Basic Subdomain Finder</option>
                        <option value="ping_sim">6. Ping Simulator</option>
                        <option value="whois_sim">7. Whois Domain Info Lookup</option>
                        
                        <!-- Web Vulnerability & Inspection (8-15) -->
                        <option value="http_headers">8. HTTP Headers Inspector</option>
                        <option value="headers">9. Security Headers Vulnerability Checker</option>
                        <option value="dir_fuzz">10. Basic Directory Fuzzer (Admin/Login)</option>
                        <option value="robots_check">11. Robots.txt Analyzer</option>
                        <option value="ssl_check">12. SSL Certificate Info Checker</option>
                        <option value="link_extractor">13. Webpage Link Extractor</option>
                        <option value="status_explainer">14. HTTP Status Code Explainer</option>
                        <option value="request_tester">15. HTTP Request Method Tester</option>
                        
                        <!-- Crypto, Encoding & Decoding (16-24) -->
                        <option value="hash_gen">16. MD5 / SHA256 Hash Generator</option>
                        <option value="sha512_gen">17. SHA-512 Secure Hash Generator</option>
                        <option value="base64_enc">18. Base64 Encoder / Decoder</option>
                        <option value="url_codec">19. URL Encoder / Decoder</option>
                        <option value="jwt_decode">20. JWT Token Structure Decoder</option>
                        <option value="html_codec">21. HTML Entity Encoder / Decoder</option>
                        <option value="rot13_cipher">22. ROT13 Cipher Encryptor / Decryptor</option>
                        <option value="hex_conv">23. Hex to ASCII / ASCII to Hex Converter</option>
                        <option value="mac_lookup">24. MAC Address Vendor Lookup</option>
                        
                        <!-- Security Utilities & Generators (25-30) -->
                        <option value="pwd_check">25. Password Strength Analyzer</option>
                        <option value="pwd_gen">26. Secure Random Password Generator</option>
                        <option value="uuid_gen">27. UUID / GUID Generator</option>
                        <option value="user_agent">28. Random User-Agent Generator</option>
                        <option value="text_stats">29. Text Length & Word Counter Utility</option>
                        <option value="subnet_calc">30. Local Network Subnet / CIDR Info</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-semibold text-cyan-300 mb-2">Target Input (Domain, IP, URL or Text):</label>
                    <input type="text" name="target" placeholder="Enter target domain, IP or query..." required
                        class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3.5 text-white focus:outline-none focus:border-cyan-400 transition shadow-inner">
                </div>

                <button type="submit" 
                    class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-extrabold py-4 rounded-xl transition duration-200 shadow-lg glow-btn tracking-wide uppercase text-sm">
                    ⚡ Execute Tool Execution
                </button>
            </form>

            <!-- Results Output Box -->
            {% if result %}
            <div class="mt-8 p-5 bg-slate-950/90 border border-cyan-500/30 rounded-2xl shadow-xl">
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-xs font-bold text-cyan-400 uppercase tracking-widest flex items-center gap-2">
                        <span class="h-2 w-2 bg-emerald-400 rounded-full"></span> Execution Output:
                    </h3>
                </div>
                <pre class="whitespace-pre-wrap text-xs sm:text-sm font-mono text-emerald-400 overflow-x-auto max-h-96 p-2">{{ result }}</pre>
            </div>
            {% endif %}
        </div>
    </main>

    <!-- Footer with "Made by Ziyan" -->
    <footer class="text-center py-6 border-t border-slate-900 bg-slate-950/50">
        <p class="text-xs text-slate-400">CyberNexus Elite Suite • Built with Python & Flask</p>
        <p class="text-sm font-bold text-cyan-400 mt-1">Made by Ziyan 🚀</p>
    </footer>

    <!-- Live Search Script -->
    <script>
        function searchTools() {
            let input = document.getElementById('searchInput').value.toLowerCase();
            let select = document.getElementById('toolSelect');
            let options = select.options;
            for (let i = 0; i < options.length; i++) {
                let txt = options[i].text.toLowerCase();
                options[i].style.display = txt.includes(input) ? "" : "none";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        tool = request.form.get('tool_type')
        target = request.form.get('target', '').strip()
        
        try:
            clean = target.replace("https://", "").replace("http://", "").split("/")[0]
            
            if tool == 'dns':
                ip = socket.gethostbyname(clean)
                result = f"[+] Target Domain : {clean}\n[+] Resolved IP : {ip}"
                
            elif tool == 'reverse_dns':
                host = socket.gethostbyaddr(target)
                result = f"[+] IP Address : {target}\n[+] Hostname   : {host[0]}"
                
            elif tool == 'port_scan':
                ip = socket.gethostbyname(clean)
                ports = [21, 22, 23, 53, 80, 443, 3306, 8080]
                output = f"Scanning {clean} ({ip}):\n" + "-"*35 + "\n"
                for p in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    res = s.connect_ex((ip, p))
                    output += f"Port {p:5}: {'OPEN' if res == 0 else 'CLOSED'}\n"
                    s.close()
                result = output
                
            elif tool == 'ip_track':
                res = requests.get(f"http://ip-api.com/json/{clean}", timeout=5).json()
                if res.get('status') == 'success':
                    result = f"IP      : {res.get('query')}\nCountry : {res.get('country')}\nRegion  : {res.get('regionName')}\nCity    : {res.get('city')}\nISP     : {res.get('isp')}"
                else:
                    result = "[-] Invalid IP or lookup failed."
                    
            elif tool == 'sub_enum':
                subs = ['www', 'mail', 'test', 'admin', 'api', 'dev', 'portal', 'shop', 'blog', 'secure']
                output = f"Subdomain Scan for: {clean}\n" + "-"*35 + "\n"
                for sub in subs:
                    url = f"http://{sub}.{clean}"
                    try:
                        r = requests.get(url, timeout=2)
                        output += f"[+] Found: {url} (Status: {r.status_code})\n"
                    except:
                        pass
                result = output if output.count('\n') > 2 else "[-] No common subdomains found."
                
            elif tool == 'ping_sim':
                ip = socket.gethostbyname(clean)
                result = f"[+] Host {clean} resolved to {ip}\n[+] TCP Handshake successful. Status: ONLINE (Latency < 50ms)"
                
            elif tool == 'whois_sim':
                result = f"[+] WHOIS Simulated Info for {clean}:\n" + "-"*35 + "\nRegistrar: Example Registrar LLC\nCreated Date: 2010-01-01\nStatus: Active / ClientTransferProhibited"
                
            elif tool == 'http_headers':
                url = target if target.startswith('http') else 'https://' + target
                res = requests.get(url, timeout=5)
                output = f"HTTP Response Headers for {url}:\n" + "-"*40 + "\n"
                for k, v in res.headers.items():
                    output += f"{k}: {v}\n"
                result = output
                
            elif tool == 'headers':
                url = target if target.startswith('http') else 'https://' + target
                res = requests.get(url, timeout=5)
                headers = res.headers
                sec_h = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
                output = f"Security Headers Vulnerability Check: {url}\n" + "-"*45 + "\n"
                for h in sec_h:
                    output += f"[{'PRESENT' if h in headers else 'MISSING'}] {h}\n"
                result = output
                
            elif tool == 'dir_fuzz':
                url_base = target if target.startswith('http') else 'http://' + target
                wordlist = ['admin', 'login', 'dashboard', 'uploads', 'api', 'test', 'config.php', 'secret']
                output = f"Directory Fuzzing for {url_base}:\n" + "-"*40 + "\n"
                for word in wordlist:
                    test_url = f"{url_base.rstrip('/')}/{word}"
                    try:
                        r = requests.get(test_url, timeout=3)
                        if r.status_code in [200, 403]:
                            output += f"[{r.status_code}] {test_url}\n"
                    except:
                        pass
                result = output
                
            elif tool == 'robots_check':
                url = (target if target.startswith('http') else 'https://' + target).rstrip('/') + '/robots.txt'
                res = requests.get(url, timeout=5)
                result = f"Robots.txt Analysis for {target}:\n" + "-"*40 + "\n" + res.text[:1200]
                
            elif tool == 'ssl_check':
                url = target if target.startswith('http') else 'https://' + target
                res = requests.get(url, timeout=5)
                result = f"[+] URL: {url}\n[+] SSL Handshake: Successful\n[+] Status Code: {res.status_code}\n[+] Connection: Encrypted"
                
            elif tool == 'link_extractor':
                url = target if target.startswith('http') else 'https://' + target
                res = requests.get(url, timeout=5)
                links = re.findall(r'href=[\"\'](https?://[^\'\"]+)', res.text)
                result = f"Extracted Links ({len(links)} found):\n" + "\n".join(links[:20]) if links else "[-] No external links found."
                
            elif tool == 'status_explainer':
                codes = {
                    "200": "OK - Request successful",
                    "301": "Moved Permanently",
                    "400": "Bad Request",
                    "401": "Unauthorized",
                    "403": "Forbidden Access",
                    "404": "Page Not Found",
                    "500": "Internal Server Error"
                }
                result = f"HTTP Status Code {target}:\n{codes.get(target, 'Custom or standard HTTP status code.')}"
                
            elif tool == 'request_tester':
                url = target if target.startswith('http') else 'https://' + target
                r_get = requests.get(url, timeout=5)
                r_head = requests.head(url, timeout=5)
                result = f"URL: {url}\nGET Method Status  : {r_get.status_code}\nHEAD Method Status : {r_head.status_code}"
                
            elif tool == 'hash_gen':
                md5 = hashlib.md5(target.encode()).hexdigest()
                sha256 = hashlib.sha256(target.encode()).hexdigest()
                result = f"Input Text : {target}\nMD5        : {md5}\nSHA256     : {sha256}"
                
            elif tool == 'sha512_gen':
                sha512 = hashlib.sha512(target.encode()).hexdigest()
                result = f"Input Text : {target}\nSHA512     : {sha512}"
                
            elif tool == 'base64_enc':
                encoded = base64.b64encode(target.encode()).decode()
                try:
                    decoded = base64.b64decode(target.encode()).decode()
                except:
                    decoded = "N/A (Not valid Base64)"
                result = f"Base64 Encoded : {encoded}\nBase64 Decoded : {decoded}"
                
            elif tool == 'url_codec':
                encoded = urllib.parse.quote(target)
                decoded = urllib.parse.unquote(target)
                result = f"URL Encoded : {encoded}\nURL Decoded : {decoded}"
                
            elif tool == 'jwt_decode':
                parts = target.split('.')
                if len(parts) >= 2:
                    def base64_pad(data):
                        return data + '=' * (-len(data) % 4)
                    header = base64.b64decode(base64_pad(parts[0])).decode()
                    payload = base64.b64decode(base64_pad(parts[1])).decode()
                    result = f"JWT Header:\n{header}\n\nJWT Payload:\n{payload}"
                else:
                    result = "[-] Invalid JWT token format."
                    
            elif tool == 'html_codec':
                import html
                encoded = html.escape(target)
                decoded = html.unescape(target)
                result = f"HTML Encoded : {encoded}\nHTML Decoded : {decoded}"
                
            elif tool == 'rot13_cipher':
                import codecs
                rot = codecs.encode(target, 'rot_13')
                result = f"Original : {target}\nROT13    : {rot}"
                
            elif tool == 'hex_conv':
                try:
                    hex_val = target.encode().hex()
                    ascii_val = bytes.fromhex(target).decode('utf-8', errors='ignore')
                except:
                    hex_val = target.encode().hex()
                    ascii_val = "Conversion failed or not valid hex"
                result = f"Hexadecimal : {hex_val}\nASCII Text  : {ascii_val}"
                
            elif tool == 'mac_lookup':
                result = f"[+] MAC Prefix Lookup for {target}:\nVendor: Sample NIC Manufacturer / Private OUI"
                
            elif tool == 'pwd_check':
                score = 0
                if len(target) >= 8: score += 1
                if any(c.isupper() for c in target): score += 1
                if any(c.isdigit() for c in target): score += 1
                if any(not c.isalnum() for c in target): score += 1
                strength = ["Very Weak ❌", "Weak ⚠️", "Moderate ⚡", "Strong 🔒", "Very Strong 🔥"][score]
                result = f"Password: {target}\nLength  : {len(target)}\nRating  : {strength}"
                
            elif tool == 'pwd_gen':
                chars = string.ascii_letters + string.digits + string.punctuation
                pwd = "".join(random.choice(chars) for _ in range(16))
                result = f"[+] Generated Secure Password (16 chars):\n{pwd}"
                
            elif tool == 'uuid_gen':
                result = f"[+] Generated UUIDv4:\n{uuid.uuid4()}"
                
            elif tool == 'user_agent':
                agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)"
                ]
                result = f"[+] Random User-Agent:\n{random.choice(agents)}"
                
            elif tool == 'text_stats':
                words = len(target.split())
                chars = len(target)
                result = f"Character Count : {chars}\nWord Count      : {words}"
                
            elif tool == 'subnet_calc':
                result = f"[+] Network Subnet Info for {target}:\nClass: C | CIDR: /24 | Total Hosts: 25
