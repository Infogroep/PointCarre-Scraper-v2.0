#!/usr/bin/env python
import mechanize
from getpass import getpass
import lxml.html
import os

def login(user, password):
	agent = mechanize.Browser()
	page = agent.open('https://pointcarre.vub.ac.be')
	loginForm = list(agent.forms())[0]
	loginForm.find_control("username").value = user
	loginForm.find_control("password").value = password
	agent.select_form(nr = 0)
	page = agent.submit()
	return agent

def scrapeRichting(agent, url):
	agent.open(url)
	rawResponse = agent.response().read()
	html = lxml.html.fromstring(rawResponse)
	rows = html.xpath('//table[@id="curriculum_student_browser_table"]/tbody/tr')

	netids = []
	for row in rows:
		row = row.xpath('td[4]/text()')
		if len(row) > 0:
			netids.append(row[0] + '@vub.ac.be')
	
	return netids

standard_url = "http://pointcarre.vub.ac.be/index.php?curriculum_student_browser_table_direction=4&curriculum_student_browser_table_page_nr=1&curriculum_student_browser_table_column=1&application=curriculum&go=curriculum_program_viewer&curriculum_student_browser_table_per_page=all&curriculum_program="

# 166: Ingenieurswetenschappen Toegepaste Computerwetenschappen.
# 
trajecten = [494, 605, 496]
urls = [standard_url + str(num) for num in trajecten]

faculteiten = [5]
faculteit_url = "http://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_total_programs_browser&curriculum_department="
fac_urls = [faculteit_url + str(num) for num in faculteiten]

# Scrape de faculteit pagina voor de verschillende trajecten.
def scrapeFaculteiten(agent, url):
        print url
        agent.open(url)
        rawResponse = agent.response().read()
        html = lxml.html.fromstring(rawResponse)
        rows = html.xpath('//table[@id="curriculum_total_program_browser_table"]/tbody/tr')
        
        traject_ids = []
        for row in rows:
                row = row.xpath('td[2]/div/ul/li/a/@href')
                if len(row) > 0:
                        index = row[0].rfind('=')
                        traject_ids.append(row[0][index+1:])
        
        return traject_ids

agent = login(raw_input('Username: '), getpass())

trajecten = set()
for url in fac_urls:
        trajecten.update(scrapeFaculteiten(agent, url))

traject_url = "https://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_programs_browser&curriculum_total_program="
traj_urls = [traject_url + str(num) for num in trajecten]

# Scrape de trajecten pagina voor de verschillende programma's.
def scrapeTrajecten(agent, url):
        print url
        agent.open(url)
        rawResponse = agent.response().read()
        html = lxml.html.fromstring(rawResponse)
        rows = html.xpath('')

for url in traj_urls:
        scrapeTrajecten(agent, url)

emails = set()
master_emails = set()
schakel_emails = set()

for t in trajecten:
        print t

##for url in urls:
##        emails.update(scrapeRichting(agent, url))
##
##print "\n### EMAILS ###"
##for email in emails:
##	print email
