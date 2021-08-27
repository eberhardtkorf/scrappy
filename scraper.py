import sys
import requests
import json
from bs4 import BeautifulSoup

#Functions
def scrape_github(search_term, num_pages = 1):

	resultList = []

	#Define URL and fetch HTML
	webPage = requests.get('https://github.com/search?q=' + search_term)
	soup = BeautifulSoup(webPage.content, 'html.parser')

	#Retrieve List of Repository and Check if search yielded any results
	try:
		repoListClass = soup.find('ul', {'class': 'repo-list'})
		repoList = repoListClass.findChildren('li', recursive=False)
	except:
		return resultList #no results thus return empty list

	#Go through Repository List and look for Applicable Results
	for repository in repoList:

		resultDic = {}

		repoContentClass = repository.findChildren('div', recursive = False)[1]

		#repo_name
		name = repoContentClass.findChildren('div', recursive = False)[0]
		name = name.findChildren('a', recursive = False)[0].text.strip()
		resultDic['repo_name'] = name

		#description
		try:
			description = repoContentClass.findChildren('p', recursive = False)[0].text.strip()
			resultDic['description'] = description
		except:
			resultDic['description'] = None

		tagsAndInfoClass = repoContentClass.findChildren('div', recursive = False)[1]

		#tags
		if len(tagsAndInfoClass.findChildren('div', recursive = False)) > 1:

			infoClass = tagsAndInfoClass.findChildren('div')[1]
			tagsClass = tagsAndInfoClass.findChildren('div', recursive = False)[0]
			tagsDivList = tagsClass.findChildren('a', recursive = False)
			tagsList = []

			for tag in tagsDivList:
				tagsList.append(tag.text.strip())

			resultDic['tags'] = tagsList
		else:
			resultDic['tags'] = None
			infoClass = tagsAndInfoClass.findChildren('div')[0]

		#num_stars
		try:
			stars = infoClass.findChildren('div', recursive = False)[0]
			if stars.findChildren('a'):
				resultDic['num_stars'] = stars.text.strip()
			else:
				resultDic['num_stars'] = None
		except:
			resultDic['num_stars'] = None

		#stars = infoClass.findChildren('div', recursive = False)[0].text.strip()
		#resultDic['num_stars'] = stars

		#language 
		try:
			language = infoClass.find('span', {'itemprop': 'programmingLanguage'}).text.strip()
			resultDic['language'] = language
		except:
			resultDic['language'] = None

		#license
		license = None
		infoClassDivs = infoClass.findChildren('div', recursive = False)
		for div in infoClassDivs:
			if div.text.strip().find('license') != -1:
				license = div.text.strip()
		resultDic['license'] = license

		#last_updated
		updated = infoClass.findChildren('relative-time')[0]['datetime']
		resultDic['last_updated'] = updated

		#num_issues
		try:
			issues = infoClass.findChildren('a', recursive=False)[0]
			resultDic['num_issues'] = issues.text.strip().split()[0]
		except:
			resultDic['num_issues'] = None

		resultList.append(resultDic)

	return resultList

def github_api(search_term, num_pages=1):

	resultsList = []

	numResults = int(num_pages)*10

	query = 'q=' + search_term.replace(' ','+') + '+&per_page=' + str(numResults) + '&in:name' + '&in:description'

	results = requests.get('https://api.github.com/search/repositories?'+ query)
	
	try:
		repoList = results.json()['items']
	except:
		return resultsList

	for repository in repoList:

		result = {}

		if repository['full_name']:
			result['repo_name'] = repository['full_name']
		else:
			result['repo_name'] = None

		if repository['description']:
			result['description'] = repository['description']
		else:
			result['description'] = None

		if repository['stargazers_count']:
			result['num_stars'] = repository['stargazers_count']
		else:
			result['num_stars'] = None

		if repository['language']:
			result['language'] = repository['language']
		else:
			result['language'] = None

		if repository['license']:
			result['license'] = repository['license']['name']
			if result['license'] == 'Other': result['license'] = None
		else:
			result['license'] = None

		result['last_updated'] = repository['updated_at']

		if repository['has_issues']:
			result['has_issues'] = True
		else:
			result['has_issues'] = False
			
		resultsList.append(result)

	return resultsList







