#!/usr/bin/env python
import mechanize
from getpass import getpass
import lxml.html, os

def login(user, password):
	agent = mechanize.Browser()
	page = agent.open('https://pointcarre.vub.ac.be')
	loginForm = list(agent.forms())[0]
	loginForm.find_control("username").value = user
	loginForm.find_control("password").value = password
	agent.select_form(nr = 0)
	page = agent.submit()
	return agent

# Scrapet de "Department"-pagina voor de verschillende "Total Program" nummers.
def scrapeDepartment(agent, url):
        print url
        agent.open(url)
        rawResponse = agent.response().read()
        html = lxml.html.fromstring(rawResponse)
        rows = html.xpath('//table[@id="curriculum_total_program_browser_table"]/tbody/tr')
        
        total_program_ids = []
        for row in rows:
                departement = row.xpath('td[1]/text()')
                row = row.xpath('td[2]/div/ul/li/a/@href')
                if len(row) > 0:
                        index = row[0].rfind('=')
                        print departement, row[0][index+1:]
                        total_program_ids.append(row[0][index+1:])
        
        return total_program_ids

# Scrape de "Total Program"-pagina voor de verschillende "Programs".
def scrapeTotalProgram(agent, url):
        agent.open(url)
        rawResponse = agent.response().read()
        html = lxml.html.fromstring(rawResponse)
        rows = html.xpath('//table[@id="curriculum_program_browser_table"]/tbody/tr')

        program_ids = []
        for row in rows:
                row = row.xpath('td[1]/a/@href')
                if len(row) > 0:
                        index = row[0].rfind('=')
                        program_ids.append(row[0][index+1:])

        return program_ids

# 
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

## standard_url = "http://pointcarre.vub.ac.be/index.php?curriculum_student_browser_table_direction=4&curriculum_student_browser_table_page_nr=1&curriculum_student_browser_table_column=1&application=curriculum&go=curriculum_program_viewer&curriculum_student_browser_table_per_page=all&curriculum_program="
 
## trajecten = [494, 605, 496]
## urls = [standard_url + str(num) for num in trajecten]

## We beslissen welke departementen we willen scrapen.
## Dit is voorlopig manueel.
departments = [5] # 5 = WE; 7 = IR
standard_url_dep = "http://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_total_programs_browser&curriculum_department="
departments_urls = [standard_url_dep + str(num) for num in departments] # URL's Genereren voor de agent.

agent = login(raw_input('Username: '), getpass())

## Total Programs ophalen van elk departement.
total_programs = set()
for url in departments_urls:
        total_programs.update(scrapeDepartment(agent, url))

print "TOTAL PROGRAMS:"
for p in total_programs:
        print p

#standard_url_tprogram = "https://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_programs_browser&curriculum_total_program="
#standard_url_tprogram = "http://pointcarre.vub.ac.be/index.php?curriculum_total_program_browser_table_direction=4&curriculum_total_program_browser_table_page_nr=1&curriculum_total_program_browser_table_column=1&application=curriculum&go=curriculum_total_programs_browser&curriculum_total_program_browser_table_per_page=all&curriculum_department="
#Kwintens Fix
standard_url_tprogram = "http://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_programs_browser&curriculum_total_program_browser_table_per_page=all&curriculum_total_program="

total_program_urls = [standard_url_tprogram + str(num) for num in total_programs]

## Programs ophalen voor elk Total Program
programs = set()
for url in total_program_urls:
        print url
        programs.update(scrapeTotalProgram(agent, url))

print "PROGRAMS:"
for tp in programs:
        print tp

# standard_url_program = "http://pointcarre.vub.ac.be/index.php?application=curriculum&go=curriculum_program_viewer&curriculum_program="
standard_url_program = "http://pointcarre.vub.ac.be/index.php?curriculum_student_browser_table_direction=4&curriculum_student_browser_table_page_nr=1&curriculum_student_browser_table_column=1&application=curriculum&go=curriculum_program_viewer&curriculum_student_browser_table_per_page=all&curriculum_program="
program_urls = [standard_url_program + str(num) for num in programs]

emails = set()
for url in program_urls:
        # print "Trying: " + url
        emails.update(scrapeRichting(agent, url))

print "E-MAILS:"
for e in emails:
        print e

#--------------

##emails = set()
##master_emails = set()
##schakel_emails = set()
##
##print "trajecten"
##for t in trajecten:
##        print t
##
##print "programs"
##for p in programs:
##        print p
##
####for url in urls:
####        emails.update(scrapeRichting(agent, url))
####
####print "\n### EMAILS ###"
####for email in emails:
####	print email
