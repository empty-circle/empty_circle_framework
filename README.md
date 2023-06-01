# The Empty Circle Reconnaissance Framework
___
Developed by David Kuszmar & Nikita Kotlyarov
2023 v`0.3`

```
 The Empty Circle is a recon framework for pentesters and redteamers.
 It is meant to be simple, easy to use, and easy to modify. 
 Check the readme for exact instructions and a walkthrough.
```
___
  
  
A couple of important notes!  
* Scrappy_Badger.py - the Darkweb Scraper - requires you to have entered the cleartext version of your torrc password and the appropriate ports set and matched as well.  
* Scrappy_Badger.py requires your tor service to be running!  
* Pastebin_Scraper.py requires the Pastebin API in order to work.  
* The nmap scanning involved here requires the use of sudo when launching the framework.  

Basic Tutorials for each module of the framework are below.

1) Basker: 
  This is a scanner that utilizes the incredible power of nmap to conduct stealthy, large-scale IP research. It works off of IPs in CIDR notation (ex: 0.0.0.0/24).
  
2) Hiss:  
  This is a scanner that works great when precision and accuracy are more important than stealth. The nmap command is formulated off of NMAPs own research to return the most precise and accurate data in the least amount of time.
  
4) Automated Service and Version Scanner:  
  This pulls data from the parsed results of Basker to automatically scan lists of vulnerable IPs. Select your list, sit back, and let it run.
  
5) Clearweb Scraper : aka `Scrappy_Pup.py`  
  The framework will launch this and automatically include universal variables like workspace location, etc. All you have to do is identify the keywords you want to search for.
  
6) Darkweb Scraper : aka `Scrappy_Badger.py`  
  As noted above, this requires password, listening port, and control port for your Tor service, which must be running. Be cautious, though there is some safety in scraping the darkweb in a fashion that keeps things plaintext, it's not perfect and it's not engineered to be as Secure As Possible. Consider yourself warned.
  
7) Script Scan Hub:  
  This is pretty simple and it will walk you through the process. Select your target, select the type of script scan you want to use, determine if you'd like it to be safe or aggressive, and let it rip.
  
8) Pastebin Crawler:  
  This is a crawler, so make sure you keep it open as long as you want it to run. Don't forget, you need a valid pastebin API.
  
