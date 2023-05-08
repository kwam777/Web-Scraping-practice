#!/usr/bin/env python
# coding: utf-8

# Scrape Premier League Stats 

# In[2]:


import requests


# Nach Requests Import wird mithilfe Requests URL-Daten gescrapet

# In[3]:


standings_url = "https://fbref.com/de/wettbewerbe/9/Premier-League-Statistiken"


# In[4]:


data = requests.get(standings_url)


# In[5]:


data.text


# Import Beautiful Soup um Daten zu parsen

# In[6]:


from bs4 import BeautifulSoup


# In[7]:


soup = BeautifulSoup(data.text)


# In[8]:


standings_table = soup.select('table.stats_table')[0]


# In[17]:


standings_table


# Filtern nach allen Elementen mit 'a'

# In[18]:


links = standings_table.find_all('a')


# Nun lassen wir uns nur den "href"-Teil ausgeben weil nur dieser für uns relevant ist. 

# In[64]:


links = [l.get("href") for l in links]


# Ausgabe der Teams

# In[65]:


links = [l for l in links if '/mannschaften/' in l]


# Daten geben nur Mannschaftsnamen aus, wir wollen aber einen Link erstellen so wie es im HTML vorhanden ist für den direkten zugriff Also fügen wir den notwendigen link an den Anfang hinzu.

# In[66]:


mannschafts_urls = [f"https://fbref.com{l}" for l in links]


# In[67]:


mannschafts_urls


# Beginn mit der Extrahierung der Spiel Statistiken 

# In[69]:


mannschafts_url = mannschafts_urls[11]


# In[71]:


data = requests.get(mannschafts_url)


# In[72]:


data.text


# Gewünschten Tabelle bzgl. der Spiele mit pandas in ein Dataframe speichern

# In[73]:


import pandas as pd 



# In[74]:


Spiele = pd.read_html(data.text, match="Ergebnisse & Spiele")


# In[75]:


Spiele[0].head


# ziehen uns die Schuss-statistiken, zuerst wieder alle Links die 'a' beinhalten ziehen und dann sortieren

# In[76]:


soup = BeautifulSoup(data.text)


# In[77]:


links = soup.find_all('a')


# erneuter listenvergleich um unsere Wunschdaten einzugrenzen

# In[78]:


links = [l.get("href") for l in links]


# In[79]:


links = [l for l in links if l and 'all_comps/shooting/' in l]


# In[80]:


links


# Link ist auf der Website viermal vorhanden weswegen wir einen anderen Lösungsansatz versuchen mit einem requests-Befehl

# In[81]:


data = requests.get(f"https://fbref.com{links[0]}")


# In[82]:


import pandas as pd


# Ausgabe der Torschuss-Statistiken

# In[83]:


torschuesse = pd.read_html(data.text, match="Torschüsse")[0]


# In[84]:


torschuesse.head()


# In[86]:


torschuesse.columns = torschuesse.columns.droplevel()


# In[87]:


torschuesse.head()


# In[88]:


torschuesse["Datum"]


# Wir "mergen"die beiden Dataframes also wir verbinden sie (Übernehmen bestimmte Statistiken)  

# In[89]:


team_daten = Spiele[0].merge(shooting[["Datum","Sc", "SaT", "Entf.", "FS", "Elf", "VeElf" ]], on="Datum")


# In[90]:


team_daten.head()


# wir haben im Prinzip nur das Spiele-Dataframe übernommen und um einige Statistiken ergänzt. 

# In[91]:


team_daten


# In[92]:


Jahre = list(range(2022,2020, -1))


# In[93]:


Jahre


# In[94]:


alle_spiele = []


# In[227]:


platzierungen_url  = "https://fbref.com/de/wettbewerbe/9/Premier-League-Statistiken"


# Scrapen der Vor-Saison, wir scrapen die Platzierungen mit BeautifulSoup(parsen),wir wollen die Statistik-Tabelle, um die einzelnen Team-Links zu erhalten und filtern nach diesen. 
# Letzendlich werden diese Links zu Absoluten Links umgewandelt. 
# Als letzter Schritt werden wir eine Schleife(Loop) verwenden um mehrere Jahre an Daten zu erhalten.

# In[1]:


import time
for Jahr in Jahre: 
    data = requests.get(platzierungen_url)
    soup = BeautifulSoup(data.text)
    tabelle_platzierungen = soup.select('table.stats_table')[0]
    
    
    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if '/mannschaften/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Statistiken","").replace("-", " ")
        
        
        data = requests.get(team_url)
        spiele = pd.read_html(data.text, match="Ergebnisse & Spiele")[0]
        
        soup = BeautifulSoup(data.text)
        links = [l.get("href") for l in soup.find_all('a')]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        data = requests.get(f"https:fbref.com{links[0]}")
        torschuesse = pd.read_html(data.text, match="Torschüsse")[0]
        torschuesse.columns = torschuesse.columns.droplevel()
        
        
        try:
            team_daten = Spiele[0].merge(shooting[["Datum","Sc", "SaT", "Entf.", "FS", "Elf", "VeElf" ]]),
        except ValueError:
            continue 
            
            
            
       


# In[ ]:





# In[ ]:




