Github is one of the most popular version control systems in use today, with over 100 million projects available to users. Because of this, it is one of the best sources to check on the current state of Computer Science. My Github Analyzer application scrapes thousands of machine learning projects in order to determine which machine learning libraries are most commonly used, and analyze various statistics about machine learning projects as a whole.

 
## Data Collection

The Python library Scrapy was used to get data from Github. The web scraping consisted of two spiders:

    GithubLinksSpider.py - Use search terms to get project links
    GithubProjectsSpider.py - Use project links to get data for each project

Each search term on Github allows the user to view 100 pages of information with 10 project links per page. I used 5 search terms classified by language to find projects:

    Python
    Jupyter Notebook
    Java
    Javascript
    All languages

Each search term produced 1000 links, although the final result produced around 4235 unique results. Getting project links was difficult due to Github servers timing out requests unless the rate of requests per second was low. Fortunately, the scraping for individual projects was much more forgiving in that regard.

 
## Results

The following data was obtained by analyzing the readme of each project and searching for references to each library, as well as their common aliases. 

 ![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Single%20Var/Library%20Count.png)

    
This plot shows the popularity of each library. It demonstrates that most libraries aren’t used much, and the top 5 libraries have by far the most usage.

![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Single%20Var/Commit%20Count.png)

![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Single%20Var/Commit%20Histogram.png)


These 2 plots demonstrate the number of total commits the scraped projects have for each library. They demonstrate that the libraries with the most commits are very different than their base popularity would suggest. The Histogram shows that most libraries have under 10000 commits, although there are significant outliers that may influence the results of the bar plot.

![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Single%20Var/Star%20Count.png)


This plot demonstrates that the libraries whose projects have the most stars are Pyevolve and NuPIC, while the rest have very few stars. 

![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Single%20Var/License%20Count.png)


This plot groups the projects by license. It reveals that the vast majority of projects have no license, although mit, apache, and gpl have a few uses. 

 ![](https://github.com/sethmjackson/GithubAnalyzer/blob/master/Images/Commit%20VS.%20Release.png)


This plot graphs the relationship between commits and releases. It shows that a lot of projects have 0 or 1 releases, but once the number of releases is greater than 1, there seems to be a positive correlation between commits and releases.

 
## Conclusion

The common pattern in the data is that the vast majority of projects on Github are small and don’t have any significant number of commits, stars, or other indicators of influence. The same seems to be true for different libraries, which have a few that most people use, but the rest have very little use. As a whole, Github seems to have a few big projects that get most of the activity from users, and the rest are small and inconsequential.

 
## Future work

One of the difficulties of using Scrapy on Github is that Github uses Javascript rendering on some html tags, such as the number of contributors and the date of each project. I attempted to use scrapy-splash to render these tags, but it didn’t work. If I were to redo this project, I would use Selenium instead of Scrapy, since it was built with Javascript support as a primary feature.

Another feature I would  add is to scrape the commit history for each project in order to see how machine learning projects have changed over time and which contributors are the most active.
