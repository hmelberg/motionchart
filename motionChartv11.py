# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 15:33:33 2014

@author: Hans Olav Melberg
"""
# This is a wrapper which makes it possible to create motion charts easily from a pandas dataframe
#
# Acknowledgements and more information
# See https://github.com/RamyElkest/SocrMotionChartsHTML5 for more information about the javascript which builds the chart
# See also https://github.com/psychemedia/dataviz4development/tree/master/SocrMotionCharts
# For more bakcground, and java version, see http://www.amstat.org/publications/jse/v18n3/dinov.pdf

import os
import webbrowser
import pandas as pd
from IPython.display import HTML

class SocrMotionChart(object):
    ''' To create a Motion Chart object from a pandas dataframe:
            smc = SocrMotionChart(df = dataframe)
        To send the object to the Ipyton Notebook, to a browser, to the clipboard (the HTML string which generates the chart) and to a html file by writing:
            smc.to_notebook()
            smc.to_browser()
            smc.to_clipboard()
            smc.to_file()
            
         Options and defaults (specifying which variable you want to be x, y, etc):
            smc = SocrMotionChart(
                    df = df, 
                    title = "Motion Chart",
                    url = "http://socr.ucla.edu/htmls/HTML5/MotionChart",
                    key = 1,
                    x = 2,
                    y = 3,
                    size = 4, 
                    color = 5,
                    category = 1,
                    xscale='linear',
                    yscale='linear',
                    play = 'true',
                    loop = 'false',
                    width = 800,
                    height = 600,
                    varLabels=None)
                    
                    Explained:
                        df              # specifies the name of the pandas dataframe used to create the motion chart, default is df
                        title           # string. the title of the chart (text, string) 
                        url             # string. url to folder with js and css files; can be local, default is external which requires wireless connection
                        key             # string or integer. the column number of the time variable (does not have to be time, can be any variable which you want to use to determine the motion)
                        x               # string or integer. number (integer) or name (text, string) of the x-variable in the chart. Can later be changed by clicking on the varibale in the chart. Number starts from 0 which is the outer index of the dataframe
                        y               # 
                        size            # name (text, string) or column number (integer) of the variable used to determine the size of the circles
                        color           # name (text, string) or column number (integer) variable used to determine the color of the circles
                        category        # name (text, string) or column number (integer) variable used to descripbe the category the observation belongs to. Example Mid-West, South. Often the same variable as color.  
                        xscale          # string. Scale for x-variable, string, default 'linear'. Possible values 'linear', 'log', 'sqrt', 'log', 'quadnomial', 'ordinal'
                        yscale          # string. Scale for y-variable, string, default 'linear'. Possible values 'linear', 'log', 'sqrt', 'log', 'quadnomial', 'ordinal'
                        play            # string. 'true' or 'false' (default, false). Determines whether the motion starts right away or if you have to click play first. 
                        loop            # string. 'true' or 'false' (default, false). Determines whether the motion keeps repeating after one loop over the series, or stops.
                        width           # integer. width of chart in pixels, default 800
                        height          # integer. height of chart in pixels, default 400
                        varLabels       # list. list of labels for columns (default is column headers of dataframe, if specified, must be of same length as the number of columns in the dataframe, including - and starting with - the index columns)
                               
        '''
    # This defines the motion chart object. basically just holds the parameters used to create the chart: name of data source, which variables to use        
    def __init__(self,
        df = 'df', 
        title = "Motion Chart",
        url = "http://socr.ucla.edu/htmls/HTML5/MotionChart",
        key = 1,
        x = 2,
        y = 3,
        size = 4, 
        color = 5,
        category = 5,
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
    
    # The informaton from the object is used to generate the HTML string generating the chart (inserting the specific information in the object into the template string)
    # Note: The string is generated in two steps, not one, because future version might want to revise some properties without redoing the reformatting and creatingof the dataset from the dataframe
    # Note: Initially the string itself was saved in the object, but although useful sometimes it seems memory greedy and in this version the object does not store the whole string, only the definition of it
    # Note: The template string used here is just a revised version of a template somebody else has created (See Tony Hirst: https://github.com/psychemedia/dataviz4development/tree/master/SocrMotionCharts)
    def htmlStringStart(self):
        socrTemplateStart='''<!DOCTYPE html>
        <html>
        <head>
        <!-- Meta Needed to force IE out of Quirks mode -->
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <!--StyleSheets-->
        <link href="{url}/css/bootstrap/bootstrap.min.css" rel="stylesheet">  
        <link href="{url}/css/jquery-ui-1.8.20.custom.css" rel="stylesheet"> 
        <link href="{url}/css/jquery.handsontable.css" rel="stylesheet">
        <link href="{url}/css/jquery.motionchart.css" rel="stylesheet">
        <link href="{url}/css/jquery.contextMenu.css" rel="stylesheet">
        <!--Scripts-->
        <script src="{url}/js/jquery-1.7.2.min.js"></script>
        <script src="{url}/js/dependencies.min.js"></script>
        <script src="{url}/js/custom-bootstrap.js"></script>
        <script src="{url}/js/jquery.handsontable.js"></script>
        <script src="{url}/js/jquery.motionchart.js"></script>
        </head>
        <body>
        <script>
        
        var data = {data};
        </script>
        '''
        # In order to make it easy to use information in the index of the dataframe, the index is the passed dataframe is reset
        # For instance: If the time variable is in the index of the dataframe, say the outer index, then one would write
        # smc = SocrMotionChart(df, key = 0) when specifying the motion chart
        # Note that although the key often is time, it does not have to be so (unlike Google Motion Chart)
        # In SocrMotionCharts it is basically whatver variable you want to use to define the change 
        
        df = self.df.reset_index()
        
        # If variable labels are not specified, the column names of the dataframe is used
        # Note. variable levels are specified the list of labels to be used has to have the same number of elements as the columns in the reset dataframe (ie. original number of columns plus number of index levels)
        if self.varLabels == None:
            self.varLabels = df.columns.tolist()                
        
        # Here the data is converted from a pandas dataframe to the format which is accepted by the SocrMotion Chart (javascript)
        # The starting point is a json string of all the values in the dataframe, which is then modified to fit the string SocrMotionChart wants
        dataValuesString = df.to_json(orient = 'values')
        varNamesString = ",".join(['"' + str(var) + '"' for var in self.varLabels])
        varNamesString = "[[" + varNamesString + "], ["
        dataValuesString = dataValuesString.lstrip("[")
        socrDataString = varNamesString + dataValuesString
        
        # The generated string containing the data in the right format, is inserted into the template string
        htmlString1 = socrTemplateStart.format(
                    data = socrDataString,
                    url = self.url
                    )
        # Change reference to bootstrap.js file if the url is changed to  "custom-bootstrap.js"
        # The js available on SOCR's webpage which lists it as boostrap.js, but on GitHub version which many use
        # to install a local copy, the same file is referred to as custom-boostrap.js
        # The default value is to keep it as 'custom-boostrap.js', but if the url points to socr 
        # (which is default since we want the chart to work on the web), then the filename is changed to 'bootstrap.js'
        if self.url == "http://socr.ucla.edu/htmls/HTML5/MotionChart":
            htmlString1 = htmlString1.replace("custom-bootstrap.js", "bootstrap.js")
        return htmlString1            
    
    # Generating the last half of the html string which produces the motion chart
    def htmlStringEnd(self):
        socrTemplateEnd = '''<div id="content" align="center">
        <div class="motionchart" style="width:{width}px; height:{height}px;"></div>
        <script>     
        $('.motionchart').motionchart({{
                title: "{title}",
                'data': data,
                mappings: {{key: {key}, x: {x}, y: {y},
                    size: {size},  color: {color}, category: {category} }},
                scalings: {{ x: '{xscale}', y: '{yscale}' }},
                colorPalette: {{"Blue-Red": {{from: "rgb(0,0,255)", to: "rgb(255,0,0)"}}}},
                color: "Red-Blue",
                play: {play},
                loop: {loop}
            }});
        </script>
        </div>
        </body>
        </html>
        '''
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
        
        # The user is free to specify many variables either by location (an integer representing the column number) or by name (the column name in the dataframe(
        # This means we have to find and replace with column number if the variable is specified as a string since the javascript wants integers (note: variable labels must be unique)
        # The code below finds and replaces the specified column name (text) with the column number (numeric)
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
            
        # The properites are inserted into the last half of the template string
        htmlString2 = socrTemplateEnd.format(
                    title = self.title,
                    key = kkey, x = xx, y = yy, size = ssize, color = ccolor, category = ccategory,
                    xscale= self.xscale , yscale= self.yscale,
                    play = self.play, loop = self.loop,
                    width = self.width, height = self.height)
        return htmlString2
    
    # Display the motion chart in the browser (start the default browser)    
    def to_browser(self):           # Use show() instead?
       htmlString = self.htmlStringStart() + self.htmlStringEnd()
       path = os.path.abspath('temp.html')
       url = 'file://' + path
        
       with open(path, 'w') as f:
           f.write(htmlString)
       webbrowser.open(url)
       
    # Display the motion chart in the Ipython notebook  
    def to_notebook(self):          # Use display()?
        htmlString = self.htmlStringStart() + self.htmlStringEnd()       
        htmlEncoded = htmlString.encode('base64')
        HTML('<iframe src="data:text/html;base64,{0}" width="800" height="400"></iframe>'.format(htmlEncoded))
        
    # Copy the HTML string to the clipboard  
    def to_clipboard(self):
        htmlString = self.htmlStringStart() + self.htmlStringEnd() 
        pyperclip.copy(self.htmlString)
        
    # Save the motion chart as a HTML file  
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
               
def MotionChartDemo():
    fruitdf = pd.DataFrame([
      ['Apples',  '1988-0-1', 1000, 300, 44,'East'],
      ['Oranges', '1988-0-1', 1150, 200, 42, 'West'],
      ['Bananas', '1988-0-1', 300,  250, 35, 'West'],
      ['Apples',  '1989-6-1', 1200, 400, 48, 'East'],
      ['Oranges', '1989-6-1', 750,  150, 47, 'West'],
      ['Bananas', '1989-6-1', 788,  617, 45, 'West']])
    fruitdf.columns = ['fruit', 'time', 'sales', 'price', 'temperature', 'location']
    fruitdf['time'] =  pd.to_datetime(fruitdf['time'])
    smc = SocrMotionChart(
              df = fruitdf,
              url = "http://socr.ucla.edu/htmls/HTML5/MotionChart",
              key = 'time',
              x = 'price',
              y = 'sales',
              size = 'temperature',
              color = 'fruit',
              category = 'location')
    smc.to_browser()





