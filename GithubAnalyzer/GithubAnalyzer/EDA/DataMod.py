import pandas as pd

links = pd.read_csv('urlsDebugProcessed.csv')
#links.loc[:,'id'] = 0
# links.to_csv('urlsDebugProcessed.csv', index=False)
#urls = links.loc[links['id'] < 0, 'url'].tolist()
#print(urls)
projects = pd.read_csv('ProjectData.csv')
print len(projects.index)


