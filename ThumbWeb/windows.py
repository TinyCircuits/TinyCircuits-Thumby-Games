import serial
import serial.tools.list_ports
import time
import requests
from requests.exceptions import Timeout, ConnectionError
from bs4 import BeautifulSoup
import textwrap
import re
from urllib.parse import urljoin

BAUD_RATE = 115200

def find_thumby_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if p.vid == 0x2E8A: 
            return p.device
    for p in ports:
        if "COM" in p.device:
            return p.device
    return None

def process_search(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        titles = soup.find_all('a', class_='result__url', limit=5)
        snippets = soup.find_all('a', class_='result__snippet', limit=5)
        
        out = ["T:RESULTS", "T:-------------"]
        
        for i in range(min(len(titles), len(snippets))):
            raw_title = titles[i].get_text(strip=True)[:24]
            desc = snippets[i].get_text(strip=True)[:45]
            
            link = titles[i].get('href', '')
            if "uddg=" in link:
                link = link.split('uddg=')[1].split('&')[0]
                link = requests.utils.unquote(link)
                
            out.append(f"T:🔗 {raw_title}")
            out.append(f"L:{link}")
            
            for line in textwrap.wrap(desc, width=12):
                out.append(f"T:{line}")
            out.append("T:-------------")
            
        return out
    except Timeout:
        return ["T:ERROR", "T:Connection", "T:Timed Out!", "T:-----------", "T:Press B to", "T:go back."]
    except ConnectionError:
        return ["T:ERROR", "T:No Internet", "T:Connection!", "T:-----------", "T:Press B to", "T:go back."]
    except Exception as e:
        return ["T:ERROR", "T:Search Failed", f"T:{str(e)[:12]}", "T:Press B."]

def process_webpage(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for junk in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'button', 'svg', 'img', 'iframe']):
            junk.decompose()
            
        out = ["T:BROWSER", "T:-------------"]
        line_count = 0
        max_lines = 150
        
        body = soup.body if soup.body else soup
        
        for element in body.find_all(['p', 'h1', 'h2', 'h3', 'a']):
            if line_count >= max_lines:
                break
                
            text = element.get_text(strip=True)
            if not text or len(text) < 2:
                continue
                
            if element.name == 'a':
                href = element.get('href', '')
                if href:
                    resolved_url = urljoin(url, href)
                    if resolved_url.startswith('http'):
                        wrapped = textwrap.wrap(f"LNK:{text}", width=12)
                        for w_line in wrapped:
                            out.append(f"T:{w_line}")
                            out.append(f"L:{resolved_url}")
                            line_count += 1
            else:
                wrapped = textwrap.wrap(text, width=12)
                for w_line in wrapped:
                    out.append(f"T:{w_line}")
                    line_count += 1
                    
        if len(out) <= 1:
            out.append("T:No text found.")
            
        return out[:max_lines]
    except Timeout:
        return ["T:ERROR", "T:Site is too", "T:slow to load.", "T:-----------", "T:Press B to", "T:go back."]
    except ConnectionError:
        return ["T:ERROR", "T:No Internet", "T:Connection!", "T:-----------", "T:Press B to", "T:go back."]
    except Exception as e:
        return ["T:ERROR", "T:Page Failed", f"T:{str(e)[:12]}", "T:Press B."]

ser = None
while True:
    if ser is None:
        target_port = find_thumby_port()
        if target_port:
            print(f"Connecting on {target_port}...")
            try:
                ser = serial.Serial(target_port, BAUD_RATE, timeout=0.1)
                print("Connected!")
            except Exception as e:
                print(f"Failed: {e}")
                time.sleep(2)
                continue
        else:
            print("Searching for Thumby...")
            time.sleep(2)
            continue

    try:
        if ser.in_waiting > 0:
            raw_req = ser.readline().decode('utf-8', errors='ignore').strip()
            if raw_req:
                print(f"Request: {raw_req}")
                
                payload_lines = []
                if raw_req.startswith("SEARCH:"):
                    payload_lines = process_search(raw_req[7:])
                elif raw_req.startswith("GET:"):
                    payload_lines = process_webpage(raw_req[4:])
                
                if payload_lines:
                    ser.write(b"RESET\n")
                    time.sleep(0.01)
                    
                    for payload_line in payload_lines:
                        ser.write((payload_line + "\n").encode('utf-8'))
                        time.sleep(0.01)
                    print("Page updated.")
                    
    except (serial.SerialException, OSError):
        print("Connection lost.")
        if ser:
            try: ser.close()
            except: pass
        ser = None
        time.sleep(2)