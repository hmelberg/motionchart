# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 15:33:33 2014

@author: Hans
"""
# This module is a wrapper which makes it possible to create Google Motion Charts in from a Pandas dataframe in Python
# You have to be online for the chart to work (bexause it loads a javascript module from google)

import os
import webbrowser
import pandas as pd
from IPython.display import HTML
import pyperclip
import datetime as datetime

class GoogleMotionChart(object):
    def __init__(self,
        df = df, 
        title = "Google Motion Chart",
        url = r"""https://www.google.com/jsapi""",
        time = 1,
        x = 2,
        y = 3,
        size = 6, 
        color = 2,
        category = 2,
        xscale='linear',
        yscale='linear',
        play = 'true',
        loop = 'false',
        width = 800,
        height = 600,
        varLabels=None):
            self.df = df               # specifies the name of the pandas dataframe used to create the motion chart, default is df
            self.title = title         # the title of the chart (text, string) 
            self.url = url             # url to folder with js and css files; can be local, default is external which requires wireless connection
            self.key = key             # the column number of the time variable (does not have to be time, can be any variable which you want to use to determine the motion)
            self.x = x                 # number or name (text, string) of the x-variable in the chart. Can later be changed by clicking on the varibale in the chart. Number starts from 0 which is the outer index of the dataframe
            self.y = y
            self.size = size           # name (text, string) or column number (integer) of the variable used to determine the size of the circles
            self.color = color         # name (text, string) or column number (integer) variable used to determine the color of the circles
            self.category = category   # name (text, string) or column number (integer) variable used to descripbe the category the observation belongs to. Example Mid-West, South. Often the same variable as color.  
            self.xscale= xscale        # Scale for x-variable, string, default 'linear'. Possible values 'linear', 'log', 'sqrt', 'log', 'quadnomial', 'ordinal'
            self.yscale= yscale
            self.play = play           # string: 'true' or 'false' (default, false). Determines whether the motion starts right away or if you have to click play first. 
            self.loop = loop           # string: 'true' or 'false' (default, false). Determines whether the motion keeps repeating after one loop over the series, or stops.
            self.width = width         # width of chart in pixels, default 800
            self.height = height       # height of chart in pixels, default 400
            self.varLabels = varLabels # list of labels for columns (default is column headers of dataframe, if specified, must be of same length as the number of columns in the dataframe, including - and starting with - the index columns)
    
    def test(self):
        fruitdf = pd.DataFrame([
          ['Apples',  '1988-0-1', 1000, 300, 'East'],
          ['Oranges', '1988-0-1', 1150, 200, 'West'],
          ['Bananas', '1988-0-1', 300,  250, 'West'],
          ['Apples',  '1989-6-1', 1200, 400, 'East'],
          ['Oranges', '1989-6-1', 750,  150, 'West'],
          ['Bananas', '1989-6-1', 788,  617, 'West']])
        fruitdf.columns = ['fruit', 'time', 'sales', 'price', 'location']
        fruitdf['time2'] =  pd.to_datetime(fruitdf['time'])

   def htmlString(self):
        gTemplate = """
        <html>
          <head>
            <script type="text/javascript" src="https://www.google.com/jsapi"></script>
            <script type="text/javascript">
              google.load("visualization", "1", {packages:["motionchart"]});
              google.setOnLoadCallback(drawChart);
              function drawChart() {
                var data = new google.visualization.DataTable();
                """ + jColumns + "data.addRows(" + jRowString2 + """
                );
                var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));
        
                chart.draw(data, {width: 600, height:300});
              }
            </script>
          </head>
          <body>
            <div id="chart_div" style="width: 600px; height: 300px;"></div>
          </body>
        </html>
        """
        tempdf = df.reset_index()
#        timeVar = 'date'
#        categoryVar = 'thing'
        df['between'] = "new_Date"
        between = 'between'
        df['after'] = "after"
        after = 'after'
        df['date'] = df['date'].astype(datetime)
        df['date'].apply(str)
        df['date'].apply()
        
        df['date'] = pd.to_datetime(str(date)) 
        d = ts.strftime('%Y.%m.%d')
        
        #df['testtimevar2'] = df['testtimevar'].astype(np.int64) // 10*9
        df[timeVar] = pd.to_datetime(df[timeVar])
        df = df.set_index([categoryVar, between, timeVar, after])
        df = df.reset_index()
        df
        gData = df.to_json(orient = 'values', date_format = 'epoch')
        
        #http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
        #changeText = '"' + timeVar + '":'
        gData = gData.replace(',"new_Date",', ', new Date (')
        gData = gData.replace(',"after"', ')')
        gData = gData.replace('"', "'")
        varLabels = df.columns.tolist()
        del varLabels[1]
        del varLabels[2]
        print gData
        
        varTypesDict = {}
        for col in df.columns:
            if df[col].dtype == np.object:
                  varTypesDict[col] = 'string'
            else:
                  varTypesDict[col] = 'number'
        varTypesDict['date'] = 'date'
        
        a = ""
        for var in varLabels:
            a = a + "data.addColumn('" + str(varTypesDict[var]) + "' , '" + var + "');"
            


        
        df = self.df.reset_index()
        
        if self.varLabels == None:
            self.varLabels = df.columns.tolist()                



        
        dataValuesString = df.to_json(orient = 'values')
        varNamesString = ",".join(['"' + str(var) + '"' for var in self.varLabels])
        varNamesString = "[[" + varNamesString + "], ["
        dataValuesString = dataValuesString.lstrip("[")
        socrDataString = varNamesString + dataValuesString
        
        htmlString1 = socrTemplateStart.format(
                    data = socrDataString,
                    url = self.url
                    )
        return htmlString1            
           
   
        # Rename variables to avoid changing the properties of the object when changing strings to numbers which must be used in the js script
        # (Want to keep text description of variables and not change these to less understandavle numbers in the properties, sp only use numbers under the hood)
        # Also, what if one of the keys are in the index, what should the user then input?
        # check if this works in Python 3, str is unicode in Py3, so is also unicode str in this test            
        kkey   = self.key
        xx     = self.x
        yy     = self.y
        ssize  = self.size
        ccolor = self.color
        ccategory = self.category
        
        # find and replace with column numer if the variable is specified as a string (note: variable labels must be unique)
          
        if type(kkey) is str:
             kkey=self.varLabels.index(kkey)
        if type(xx) is str:
            xx=self.varLabels.index(xx)
        if type(yy) is str:            
            yy=self.varLabels.index(yy)
        if type(ssize) is str:
            ssize=self.varLabels.index(ssize)
        if type(ccolor) is str:
            ccolor=self.varLabels.index(ccolor)
        if type(ccategory) is str:
            ccategory=self.varLabels.index(ccategory)

        htmlString2 = socrTemplateEnd.format(
                    title = self.title,
                    key = kkey, x = xx, y = yy, size = ssize, color = ccolor, category = ccategory,
                    xscale= self.xscale , yscale= self.yscale,
                    play = self.play, loop = self.loop,
                    width = self.width, height = self.height)
        return htmlString2
        
    def to_browser(self):           # Use show()?
       htmlString = self.htmlStringStart() + self.htmlStringEnd()
       path = os.path.abspath('temp.html')
       url = 'file://' + path
        
       with open(path, 'w') as f:
           f.write(htmlString)
       webbrowser.open(url)

    def to_notebook(self):          # Use display()?
        htmlString = self.htmlStringStart() + self.htmlStringEnd()       
        htmlEncoded = htmlString.encode('base64')
        HTML('<iframe src="data:text/html;base64,{0}" width="800" height="400"></iframe>'.format(htmlEncoded))

    def to_clipboard(self):
        htmlString = self.htmlStringStart() + self.htmlStringEnd() 
        pyperclip.copy(self.htmlString)

    def to_htmlfile(self, path_and_name):
        htmlString = self.htmlStringStart() + self.htmlStringEnd()     
        fileName = path_and_name + ".html"
        try:                         # encode will not (need not!) work in Python 3 since it is unicode already
           fileName = fileName.encode('string-escape')
           with open(fileName, 'w') as f:
               f.write(htmlString)
        except:
           with open(fileName, 'w') as f:
               f.write(htmlString)

smc = SocrMotionChart(df = df, url = r"C:\Users\Hans\Google Drive\python\motionchart")
smc.to_browser()

smc = SocrMotionChart(df = df, 
                      url = r"C:\Users\Hans\Google Drive\python\motionchart",
                      key = 'date',
                      x = 'x',
                      y = 'y',
                      size = 'z',
                      color = 'thing',
                      category = 'thing')


import pandas as pd
df = pd.read_csv(r"""C:\Users\hans\Google Drive\data\div/motion-chart.csv""", sep = ";", decimal = ",")
df.columns = [x.lower() for x in df.columns]
df.head()
df = df[['date', 'thing', 'key', 'x', 'y', 'z']]



df2 = pd.read_csv(r"""C:\Users\hans\Google Drive\data\div/motionchartsample.csv""", sep = ",", decimal = ".")
#df2.columns = [x.lower() for x in df.columns]
df2.head()
#df2 = df[['date', 'thing', 'key', 'x', 'y', 'z']]
df2.HPI

smc2 = SocrMotionChart(df2, 
                      url = r"C:\Users\Hans\Google Drive\python\motionchart",
                      key = 'Year',
                      x = 'HPI',
                      y = 'UR',
                      size = 'pop',
                      color = 'State',
                      category = 'State')
smc2.to_browser()
# In google

# This is the first modification - importing the library
import datetime as datetime

df.head()
df = df.reset_index()
timeVar = 'date'
categoryVar = 'thing'
df['between'] = "new_Date"
between = 'between'
df['after'] = "after"
after = 'after'
df['date'] = df['date'].astype(datetime)
df['date'].apply(str)
df['date'].apply()

df['date'] = pd.to_datetime(str(date)) 
d = ts.strftime('%Y.%m.%d')

#df['testtimevar2'] = df['testtimevar'].astype(np.int64) // 10*9
df[timeVar] = pd.to_datetime(df[timeVar])
df = df.set_index([categoryVar, between, timeVar, after])
df = df.reset_index()
df
gData = df.to_json(orient = 'values', date_format = 'epoch')

#http://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
#changeText = '"' + timeVar + '":'
gData = gData.replace(',"new_Date",', ', new Date (')
gData = gData.replace(',"after"', ')')
gData = gData.replace('"', "'")
varLabels = df.columns.tolist()
del varLabels[1]
del varLabels[2]
print gData

varTypesDict = {}
for col in df.columns:
    if df[col].dtype == np.object:
          varTypesDict[col] = 'string'
    else:
          varTypesDict[col] = 'number'
varTypesDict['date'] = 'date'

a = ""
for var in varLabels:
    a = a + "data.addColumn('" + str(varTypesDict[var]) + "' , '" + var + "');"
    

#http://stackoverflow.com/questions/5257923/how-to-load-local-script-files-as-fallback-in-cases-where-cdn-are-blocked-unavai?lq=1

#
#If you want a list of columns of a certain type, you can use groupby:
#
#>>> df = pd.DataFrame([[1, 2.3456, 'c', 'd', 78]], columns=list("ABCDE"))
#>>> df
#   A       B  C  D   E
#0  1  2.3456  c  d  78
#
#[1 rows x 5 columns]
#>>> df.dtypes
#A      int64
#B    float64
#C     object
#D     object
#E      int64
#dtype: object
#>>> g = df.columns.to_series().groupby(df.dtypes).groups
#>>> g
#{dtype('int64'): ['A', 'E'], dtype('float64'): ['B'], dtype('O'): ['C', 'D']}
#>>> {k.name: v for k, v in g.items()}
#{'object': ['C', 'D'], 'int64': ['A', 'E'], 'float64': ['B']}

# page_template stays the same
# ...

           
a = df.to_json(orient = "values")
a

jColumns = a
jRowString2 = gData

jAll ="""
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["motionchart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        """ + jColumns + "data.addRows(" + jRowString2 + """
        );

        var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

        chart.draw(data, {width: 600, height:300});
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 600px; height: 300px;"></div>
  </body>
</html>
"""

df.head()
gData
print (jAll)
import pyperclip

pyperclip.copy(jAll)


