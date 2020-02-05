import pandas as pd
import numpy as np

links = pd.read_csv('../urlsDebugProcessed.csv')
projects = pd.read_csv('../ProjectData (3rd run).csv')

libraries = {
'TensorFlow': ['Tensor Flow', 'TensorFlow'],
'scikit-learn' : ['scikit', 'scikit-learn'],
'Microsoft Cognitive Toolkit' : ['Microsoft Cognitive Toolkit', 'MCT'],
'Theano' : ['Theano'],
'Pylearn2' : ['Pylearn', 'Pylearn2'],
'Pyevolve' : ['Pyevolve'],
'NuPIC' : ['NuPIC'],
'Caffe' : ['Caffe'],
'Keras' : ['Keras'],
'XG Boost' : ['XGBoost', 'XG Boost'],
'StatsModels' : ['StatsModels'],
'LightGBM' : ['LGBM', 'LightGBM', 'Light GBM'],
'CatBoost' : ['CatBoost'],
'PyTorch' : ['PyTorch'],
'Chainer' : ['Chainer'],
'numpy' : ['Numpy'],
'scipy' : ['Scipy'],
'pandas' : ['Pandas'],
'MDP' : ['MDP']
}

def removeOutliers(df, columnName):
    return df.loc( df[columnName].apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1), columnName)

def removeEmptyProjects(df):
    newDF = df[~df['readme'].isnull()]
    print (str(len(df.index) - len(newDF.index)) + ' of ' + str(len(df.index)) + ' are empty.' )
    return newDF


def getLibraries(df):
    newDF = pd.DataFrame(columns=projects.columns)
    #newDF = projects[0:0]
    for index, row in projects.iterrows():
        lib = []
        for key, value in libraries.iteritems():

            for v in value:
                if v.lower() in str(row['readme']).lower():
                    lib.append(key)
                    break
        #print('libsUsed: ' + str(lib))
        #print('readme: '+ row['readme'])
        for l in lib:
            newRow = row.copy()
            newRow['readmeLength'] = len(newRow['readme'])
            newRow['readme'] = l

            newDF = newDF.append(newRow, ignore_index=True)
            #print(newDF)


    return newDF






#def comparePageHeads(df):


def licenseTypes(df):
    return df.groupby(['license']).size().reset_index(name='counts')

def processProjectData(df):
    readmes = removeEmptyProjects(projects)
    newDF = getLibraries(readmes)
    newDF.rename(columns = {'readme': 'library'}, inplace=True)
    newDF.to_csv('ProjectDataProcessed.csv')
    print(newDF.columns)

processProjectData(projects)

#data = pd.read_csv('ProjectDataProcessed.csv')
#print(data.head(20))

