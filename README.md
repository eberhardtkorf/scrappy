# WebDev Project 1, Scrappy

### Overview

This repository contains two main .py files, namely `scraper.py` and `scrappy.py`.

#### `scraper.py` contains two functions that will retrieve information about repositories from GitHub. 

The function `scrape_github(search_term, num_pages = 1)` will use the `BeautifulSoup` library to scrape the GitHub website and return a list of     dictionaries containing information regarding the repositories.

The function `github_api(search_term, num_pages=1)` will use the `GitHub API` to return a list of dictionaries containing information regarding the repositories. This function also has functionality that allows you te retrieve more than 10 results, you can do this by setting the argument, `num_pages`, to more than `1`.

#### `scrappy.py` contains a Flask web app that allows you to interactively use the functions contained in `scraper.py`.

### How to run the Flask web app

After you have cloned the repository to your machine and activated a virtual environment, follow these steps:

Install the necessary libraries by running the following `pip` command:

    `pip install -r requirements.txt`

Run the `scrappy.py` by using the following command:

    `python scrappy.py`

You should now be able to access the website by opening the following URL in your chosen browser:

    `localhost:5000`

The Flask web app does not display any information from the `github_api(search_term, num_pages=1)` or `scrape_github(search_term, num_pages = 1)` functions that has a return value of `None`. This is to mimic the functionality you would see on `github.com`.
