from flask import Flask, redirect, url_for, render_template, request
import scraper
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == 'POST':
        search_String = request.form['searchString']
        radioButton = request.form['flexRadioDefault']
        
        if radioButton == 'BS': resultsDic, number = BSsearch(search_String)

        try:
            numPages = request.form['numPages'] 
        except:
            numPages = 1

        if radioButton == 'API': resultsDic, number = APIsearch(search_String, numPages)
        print(search_String)
        return render_template("index.html", resultsDic = resultsDic, radioButton = radioButton, search_String = search_String, number = number, numPages = numPages)
        
    else:      
        return render_template("index.html", radioButton = 'BS', search_String = '')

def BSsearch(search_String):
    results = scraper.scrape_github(search_String)
    number = len(results)
    return results, number

def APIsearch(search_String, pages):
    results = scraper.github_api(search_String, pages)
    number = len(results)
    return results, number



if __name__ == '__main__':
    app.run(debug=True)