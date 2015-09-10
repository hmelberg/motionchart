# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 15:33:33 2014

@author: Hans Olav Melberg
"""
# This module is a wrapper which makes it possible to create Motion Charts easily from a pandas dataframe
# Acknowledgements and more information
# See https://github.com/RamyElkest/SocrMotionChartsHTML5 for more information about the javascript which builds the chart
# See also https://github.com/psychemedia/dataviz4development/tree/master/SocrMotionCharts

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
                        y 
                        size            # name (text, string) or column number (integer) of the variable used to determine the size of the circles
                        color           # name (text, string) or column number (integer) variable used to determine the color of the circles
                        category        # name (text, string) or column number (integer) variable used to descripbe the category the observation belongs to. Example Mid-West, South. Often the same variable as color.  
                        xscale          # string. Scale for x-variable, string, default 'linear'. Possible values 'linear', 'log', 'sqrt', 'log', 'quadnomial', 'ordinal'
                        yscale          # string. Scale for x-variable, string, default 'linear'. Possible values 'linear', 'log', 'sqrt', 'log', 'quadnomial', 'ordinal'
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
            
     
  
# Some tests and examples
df = pd.read_csv("""motion-chart.csv""", sep = ";", decimal = ",")
df.columns = [x.lower() for x in df.columns]
df.head()
df = df[['date', 'thing', 'key', 'x', 'y', 'z']]

smc = SocrMotionChart(df = df, 
                      key = 'date',
                      x = 'x',
                      y = 'y',
                      size = 'z',
                      color = 'thing',
                      category = 'thing')
smc.to_browser()

# More examples and testing
smc2 = SocrMotionChart(df = df, 
                      key = 'Year',
                      x = 'Unemployment_rate',
                      y = 'Housing_price_index',
                      size = 'Unemployment_rate',
                      color = 'Region',
                      category = 'State')
smc2.to_browser()


def sampleData():
    house_prics_vs_income = r'''
    {"State":{"0":"Alabama","1":"Alaska","2":"Arizona","3":"Arkansas","4":"California","5":"Colorado","6":"Connecticut","7":"Delaware","8":"Washington DC","9":"Florida","10":"Georgia","11":"Hawaii","12":"Idaho","13":"Illinois","14":"Indiana","15":"Iowa","16":"Kansas","17":"Kentucky","18":"Louisiana","19":"Maine","20":"Maryland","21":"Massachusetts","22":"Michigan","23":"Minnesota","24":"Mississippi","25":"Missouri","26":"Montana","27":"Nebraska","28":"Nevada","29":"New Hampshire","30":"New Jersey","31":"New Mexico","32":"New York","33":"North Carolina","34":"North Dakota","35":"Ohio","36":"Oklahoma","37":"Oregon","38":"Pennsylvania","39":"Rhode Island","40":"South Carolina","41":"South Dakota","42":"Tennessee","43":"Texas","44":"Utah","45":"Vermont","46":"Virginia","47":"Washington","48":"West Virginia","49":"Wisconsin","50":"Wyoming","51":"Alabama","52":"Alaska","53":"Arizona","54":"Arkansas","55":"California","56":"Colorado","57":"Connecticut","58":"Delaware","59":"Washington DC","60":"Florida","61":"Georgia","62":"Hawaii","63":"Idaho","64":"Illinois","65":"Indiana","66":"Iowa","67":"Kansas","68":"Kentucky","69":"Louisiana","70":"Maine","71":"Maryland","72":"Massachusetts","73":"Michigan","74":"Minnesota","75":"Mississippi","76":"Missouri","77":"Montana","78":"Nebraska","79":"Nevada","80":"New Hampshire","81":"New Jersey","82":"New Mexico","83":"New York","84":"North Carolina","85":"North Dakota","86":"Ohio","87":"Oklahoma","88":"Oregon","89":"Pennsylvania","90":"Rhode Island","91":"South Carolina","92":"South Dakota","93":"Tennessee","94":"Texas","95":"Utah","96":"Vermont","97":"Virginia","98":"Washington","99":"West Virginia","100":"Wisconsin","101":"Wyoming","102":"Alabama","103":"Alaska","104":"Arizona","105":"Arkansas","106":"California","107":"Colorado","108":"Connecticut","109":"Delaware","110":"Washington DC","111":"Florida","112":"Georgia","113":"Hawaii","114":"Idaho","115":"Illinois","116":"Indiana","117":"Iowa","118":"Kansas","119":"Kentucky","120":"Louisiana","121":"Maine","122":"Maryland","123":"Massachusetts","124":"Michigan","125":"Minnesota","126":"Mississippi","127":"Missouri","128":"Montana","129":"Nebraska","130":"Nevada","131":"New Hampshire","132":"New Jersey","133":"New Mexico","134":"New York","135":"North Carolina","136":"North Dakota","137":"Ohio","138":"Oklahoma","139":"Oregon","140":"Pennsylvania","141":"Rhode Island","142":"South Carolina","143":"South Dakota","144":"Tennessee","145":"Texas","146":"Utah","147":"Vermont","148":"Virginia","149":"Washington","150":"West Virginia","151":"Wisconsin","152":"Wyoming","153":"Alabama","154":"Alaska","155":"Arizona","156":"Arkansas","157":"California","158":"Colorado","159":"Connecticut","160":"Delaware","161":"Washington DC","162":"Florida","163":"Georgia","164":"Hawaii","165":"Idaho","166":"Illinois","167":"Indiana","168":"Iowa","169":"Kansas","170":"Kentucky","171":"Louisiana","172":"Maine","173":"Maryland","174":"Massachusetts","175":"Michigan","176":"Minnesota","177":"Mississippi","178":"Missouri","179":"Montana","180":"Nebraska","181":"Nevada","182":"New Hampshire","183":"New Jersey","184":"New Mexico","185":"New York","186":"North Carolina","187":"North Dakota","188":"Ohio","189":"Oklahoma","190":"Oregon","191":"Pennsylvania","192":"Rhode Island","193":"South Carolina","194":"South Dakota","195":"Tennessee","196":"Texas","197":"Utah","198":"Vermont","199":"Virginia","200":"Washington","201":"West Virginia","202":"Wisconsin","203":"Wyoming","204":"Alabama","205":"Alaska","206":"Arizona","207":"Arkansas","208":"California","209":"Colorado","210":"Connecticut","211":"Delaware","212":"Washington DC","213":"Florida","214":"Georgia","215":"Hawaii","216":"Idaho","217":"Illinois","218":"Indiana","219":"Iowa","220":"Kansas","221":"Kentucky","222":"Louisiana","223":"Maine","224":"Maryland","225":"Massachusetts","226":"Michigan","227":"Minnesota","228":"Mississippi","229":"Missouri","230":"Montana","231":"Nebraska","232":"Nevada","233":"New Hampshire","234":"New Jersey","235":"New Mexico","236":"New York","237":"North Carolina","238":"North Dakota","239":"Ohio","240":"Oklahoma","241":"Oregon","242":"Pennsylvania","243":"Rhode Island","244":"South Carolina","245":"South Dakota","246":"Tennessee","247":"Texas","248":"Utah","249":"Vermont","250":"Virginia","251":"Washington","252":"West Virginia","253":"Wisconsin","254":"Wyoming","255":"Alabama","256":"Alaska","257":"Arizona","258":"Arkansas","259":"California","260":"Colorado","261":"Connecticut","262":"Delaware","263":"Washington DC","264":"Florida","265":"Georgia","266":"Hawaii","267":"Idaho","268":"Illinois","269":"Indiana","270":"Iowa","271":"Kansas","272":"Kentucky","273":"Louisiana","274":"Maine","275":"Maryland","276":"Massachusetts","277":"Michigan","278":"Minnesota","279":"Mississippi","280":"Missouri","281":"Montana","282":"Nebraska","283":"Nevada","284":"New Hampshire","285":"New Jersey","286":"New Mexico","287":"New York","288":"North Carolina","289":"North Dakota","290":"Ohio","291":"Oklahoma","292":"Oregon","293":"Pennsylvania","294":"Rhode Island","295":"South Carolina","296":"South Dakota","297":"Tennessee","298":"Texas","299":"Utah","300":"Vermont","301":"Virginia","302":"Washington","303":"West Virginia","304":"Wisconsin","305":"Wyoming","306":"Alabama","307":"Alaska","308":"Arizona","309":"Arkansas","310":"California","311":"Colorado","312":"Connecticut","313":"Delaware","314":"Washington DC","315":"Florida","316":"Georgia","317":"Hawaii","318":"Idaho","319":"Illinois","320":"Indiana","321":"Iowa","322":"Kansas","323":"Kentucky","324":"Louisiana","325":"Maine","326":"Maryland","327":"Massachusetts","328":"Michigan","329":"Minnesota","330":"Mississippi","331":"Missouri","332":"Montana","333":"Nebraska","334":"Nevada","335":"New Hampshire","336":"New Jersey","337":"New Mexico","338":"New York","339":"North Carolina","340":"North Dakota","341":"Ohio","342":"Oklahoma","343":"Oregon","344":"Pennsylvania","345":"Rhode Island","346":"South Carolina","347":"South Dakota","348":"Tennessee","349":"Texas","350":"Utah","351":"Vermont","352":"Virginia","353":"Washington","354":"West Virginia","355":"Wisconsin","356":"Wyoming"},"Year":{"0":2000,"1":2000,"2":2000,"3":2000,"4":2000,"5":2000,"6":2000,"7":2000,"8":2000,"9":2000,"10":2000,"11":2000,"12":2000,"13":2000,"14":2000,"15":2000,"16":2000,"17":2000,"18":2000,"19":2000,"20":2000,"21":2000,"22":2000,"23":2000,"24":2000,"25":2000,"26":2000,"27":2000,"28":2000,"29":2000,"30":2000,"31":2000,"32":2000,"33":2000,"34":2000,"35":2000,"36":2000,"37":2000,"38":2000,"39":2000,"40":2000,"41":2000,"42":2000,"43":2000,"44":2000,"45":2000,"46":2000,"47":2000,"48":2000,"49":2000,"50":2000,"51":2001,"52":2001,"53":2001,"54":2001,"55":2001,"56":2001,"57":2001,"58":2001,"59":2001,"60":2001,"61":2001,"62":2001,"63":2001,"64":2001,"65":2001,"66":2001,"67":2001,"68":2001,"69":2001,"70":2001,"71":2001,"72":2001,"73":2001,"74":2001,"75":2001,"76":2001,"77":2001,"78":2001,"79":2001,"80":2001,"81":2001,"82":2001,"83":2001,"84":2001,"85":2001,"86":2001,"87":2001,"88":2001,"89":2001,"90":2001,"91":2001,"92":2001,"93":2001,"94":2001,"95":2001,"96":2001,"97":2001,"98":2001,"99":2001,"100":2001,"101":2001,"102":2002,"103":2002,"104":2002,"105":2002,"106":2002,"107":2002,"108":2002,"109":2002,"110":2002,"111":2002,"112":2002,"113":2002,"114":2002,"115":2002,"116":2002,"117":2002,"118":2002,"119":2002,"120":2002,"121":2002,"122":2002,"123":2002,"124":2002,"125":2002,"126":2002,"127":2002,"128":2002,"129":2002,"130":2002,"131":2002,"132":2002,"133":2002,"134":2002,"135":2002,"136":2002,"137":2002,"138":2002,"139":2002,"140":2002,"141":2002,"142":2002,"143":2002,"144":2002,"145":2002,"146":2002,"147":2002,"148":2002,"149":2002,"150":2002,"151":2002,"152":2002,"153":2003,"154":2003,"155":2003,"156":2003,"157":2003,"158":2003,"159":2003,"160":2003,"161":2003,"162":2003,"163":2003,"164":2003,"165":2003,"166":2003,"167":2003,"168":2003,"169":2003,"170":2003,"171":2003,"172":2003,"173":2003,"174":2003,"175":2003,"176":2003,"177":2003,"178":2003,"179":2003,"180":2003,"181":2003,"182":2003,"183":2003,"184":2003,"185":2003,"186":2003,"187":2003,"188":2003,"189":2003,"190":2003,"191":2003,"192":2003,"193":2003,"194":2003,"195":2003,"196":2003,"197":2003,"198":2003,"199":2003,"200":2003,"201":2003,"202":2003,"203":2003,"204":2004,"205":2004,"206":2004,"207":2004,"208":2004,"209":2004,"210":2004,"211":2004,"212":2004,"213":2004,"214":2004,"215":2004,"216":2004,"217":2004,"218":2004,"219":2004,"220":2004,"221":2004,"222":2004,"223":2004,"224":2004,"225":2004,"226":2004,"227":2004,"228":2004,"229":2004,"230":2004,"231":2004,"232":2004,"233":2004,"234":2004,"235":2004,"236":2004,"237":2004,"238":2004,"239":2004,"240":2004,"241":2004,"242":2004,"243":2004,"244":2004,"245":2004,"246":2004,"247":2004,"248":2004,"249":2004,"250":2004,"251":2004,"252":2004,"253":2004,"254":2004,"255":2005,"256":2005,"257":2005,"258":2005,"259":2005,"260":2005,"261":2005,"262":2005,"263":2005,"264":2005,"265":2005,"266":2005,"267":2005,"268":2005,"269":2005,"270":2005,"271":2005,"272":2005,"273":2005,"274":2005,"275":2005,"276":2005,"277":2005,"278":2005,"279":2005,"280":2005,"281":2005,"282":2005,"283":2005,"284":2005,"285":2005,"286":2005,"287":2005,"288":2005,"289":2005,"290":2005,"291":2005,"292":2005,"293":2005,"294":2005,"295":2005,"296":2005,"297":2005,"298":2005,"299":2005,"300":2005,"301":2005,"302":2005,"303":2005,"304":2005,"305":2005,"306":2006,"307":2006,"308":2006,"309":2006,"310":2006,"311":2006,"312":2006,"313":2006,"314":2006,"315":2006,"316":2006,"317":2006,"318":2006,"319":2006,"320":2006,"321":2006,"322":2006,"323":2006,"324":2006,"325":2006,"326":2006,"327":2006,"328":2006,"329":2006,"330":2006,"331":2006,"332":2006,"333":2006,"334":2006,"335":2006,"336":2006,"337":2006,"338":2006,"339":2006,"340":2006,"341":2006,"342":2006,"343":2006,"344":2006,"345":2006,"346":2006,"347":2006,"348":2006,"349":2006,"350":2006,"351":2006,"352":2006,"353":2006,"354":2006,"355":2006,"356":2006},"Housing_price_index":{"0":203.6,"1":169.7,"2":207.2,"3":185.6,"4":283.6,"5":279.8,"6":279.0,"7":277.4,"8":265.9,"9":213.0,"10":247.8,"11":238.0,"12":204.0,"13":251.5,"14":211.3,"15":193.4,"16":186.2,"17":220.3,"18":163.8,"19":297.5,"20":247.3,"21":440.6,"22":261.6,"23":240.3,"24":181.6,"25":215.3,"26":219.9,"27":204.7,"28":194.4,"29":295.8,"30":295.5,"31":203.6,"32":361.8,"33":242.5,"34":167.1,"35":223.0,"36":150.6,"37":255.2,"38":246.0,"39":299.0,"40":223.1,"41":202.5,"42":220.7,"43":165.8,"44":240.7,"45":261.3,"46":239.4,"47":278.6,"48":162.3,"49":233.3,"50":156.0,"51":214.7,"52":179.2,"53":220.4,"54":195.6,"55":314.4,"56":302.0,"57":305.0,"58":298.4,"59":309.2,"60":235.2,"61":265.1,"62":257.8,"63":215.8,"64":266.7,"65":221.3,"66":203.4,"67":196.4,"68":230.8,"69":173.0,"70":326.7,"71":269.0,"72":492.0,"73":275.3,"74":264.7,"75":190.9,"76":227.9,"77":230.7,"78":213.4,"79":207.7,"80":329.9,"81":326.5,"82":212.9,"83":396.6,"84":254.7,"85":175.5,"86":234.1,"87":159.4,"88":269.3,"89":263.1,"90":335.2,"91":236.5,"92":213.2,"93":231.8,"94":176.1,"95":250.0,"96":281.9,"97":260.3,"98":294.5,"99":171.8,"100":245.3,"101":164.7,"102":222.1,"103":188.1,"104":233.2,"105":203.1,"106":356.0,"107":315.5,"108":336.0,"109":324.1,"110":354.4,"111":259.8,"112":277.2,"113":279.5,"114":223.2,"115":282.7,"116":227.4,"117":210.6,"118":204.7,"119":239.1,"120":181.1,"121":360.3,"122":299.4,"123":552.5,"124":286.4,"125":287.8,"126":196.3,"127":240.7,"128":245.4,"129":219.9,"130":221.3,"131":369.6,"132":367.9,"133":222.2,"134":441.3,"135":262.9,"136":185.4,"137":241.9,"138":165.7,"139":281.6,"140":282.2,"141":391.0,"142":245.2,"143":223.1,"144":239.0,"145":182.7,"146":253.8,"147":301.6,"148":283.7,"149":308.0,"150":179.0,"151":257.2,"152":175.0,"153":229.6,"154":204.0,"155":250.4,"156":211.8,"157":407.3,"158":323.6,"159":366.9,"160":357.5,"161":401.4,"162":290.0,"163":286.4,"164":320.9,"165":232.3,"166":301.6,"167":234.2,"168":219.9,"169":213.0,"170":248.8,"171":190.0,"172":397.9,"173":338.7,"174":607.9,"175":297.8,"176":312.9,"177":202.2,"178":253.6,"179":266.2,"180":228.5,"181":250.6,"182":406.5,"183":412.6,"184":235.6,"185":493.9,"186":271.2,"187":196.2,"188":250.9,"189":172.3,"190":299.1,"191":304.3,"192":456.9,"193":253.7,"194":235.6,"195":247.0,"196":186.9,"197":256.8,"198":334.9,"199":311.5,"200":325.1,"201":186.1,"202":274.8,"203":187.0,"204":241.9,"205":225.0,"206":291.3,"207":226.4,"208":508.9,"209":337.7,"210":413.7,"211":411.9,"212":494.1,"213":347.9,"214":302.8,"215":401.6,"216":257.1,"217":328.0,"218":243.0,"219":230.2,"220":223.7,"221":263.4,"222":201.4,"223":449.5,"224":404.9,"225":675.2,"226":311.2,"227":339.9,"228":212.3,"229":270.8,"230":295.2,"231":240.6,"232":335.4,"233":451.7,"234":475.1,"235":254.8,"236":559.7,"237":285.6,"238":214.2,"239":261.1,"240":181.2,"241":333.6,"242":340.1,"243":536.9,"244":268.8,"245":249.4,"246":259.5,"247":194.1,"248":270.8,"249":379.4,"250":365.7,"251":362.3,"252":200.0,"253":297.5,"254":208.2,"255":264.6,"256":258.4,"257":394.8,"258":244.2,"259":618.4,"260":358.7,"261":464.8,"262":477.2,"263":609.6,"264":444.7,"265":322.8,"266":499.5,"267":306.0,"268":359.9,"269":254.2,"270":245.0,"271":234.7,"272":277.5,"273":220.7,"274":498.2,"275":493.7,"276":731.7,"277":322.8,"278":367.4,"279":228.6,"280":290.8,"281":339.4,"282":251.2,"283":398.1,"284":496.7,"285":551.7,"286":294.9,"287":634.5,"288":309.8,"289":233.0,"290":271.2,"291":192.9,"292":400.7,"293":383.3,"294":595.8,"295":294.1,"296":270.5,"297":280.9,"298":205.0,"299":307.3,"300":432.0,"301":438.8,"302":430.3,"303":224.2,"304":323.0,"305":234.8,"306":284.4,"307":274.5,"308":432.7,"309":258.0,"310":646.7,"311":369.1,"312":481.9,"313":508.3,"314":660.2,"315":488.9,"316":340.0,"317":537.4,"318":348.0,"319":379.8,"320":258.6,"321":251.3,"322":243.3,"323":288.0,"324":244.4,"325":522.3,"326":536.7,"327":731.9,"328":321.5,"329":373.1,"330":251.8,"331":303.3,"332":374.1,"333":256.8,"334":414.0,"335":509.6,"336":585.1,"337":330.7,"338":662.0,"339":331.9,"340":244.3,"341":272.8,"342":201.0,"343":455.1,"344":409.0,"345":613.7,"346":317.4,"347":285.9,"348":301.9,"349":218.6,"350":359.8,"351":461.8,"352":469.3,"353":488.9,"354":234.8,"355":332.5,"356":268.8},"Unemployment_rate":{"0":4.5,"1":6.7,"2":4.0,"3":4.4,"4":4.9,"5":2.8,"6":2.2,"7":3.9,"8":5.7,"9":3.6,"10":3.7,"11":4.3,"12":4.9,"13":4.3,"14":3.2,"15":2.6,"16":3.7,"17":4.1,"18":5.4,"19":3.5,"20":3.8,"21":2.6,"22":3.5,"23":3.3,"24":5.6,"25":3.4,"26":5.0,"27":3.0,"28":4.0,"29":2.8,"30":3.7,"31":5.0,"32":4.6,"33":3.6,"34":3.0,"35":4.0,"36":3.1,"37":4.9,"38":4.1,"39":4.1,"40":3.8,"41":2.3,"42":3.9,"43":4.2,"44":3.3,"45":2.9,"46":2.2,"47":5.2,"48":5.5,"49":3.6,"50":3.9,"51":5.3,"52":6.4,"53":4.7,"54":5.0,"55":5.4,"56":3.7,"57":3.3,"58":3.4,"59":6.4,"60":4.8,"61":4.0,"62":4.6,"63":5.0,"64":5.4,"65":4.4,"66":3.3,"67":4.3,"68":5.4,"69":5.9,"70":3.9,"71":4.0,"72":3.7,"73":5.3,"74":3.7,"75":5.5,"76":4.7,"77":4.6,"78":3.1,"79":5.3,"80":3.5,"81":4.2,"82":4.8,"83":4.9,"84":5.5,"85":2.9,"86":4.2,"87":3.8,"88":6.3,"89":4.7,"90":4.7,"91":5.3,"92":3.4,"93":4.4,"94":4.8,"95":4.4,"96":3.6,"97":3.4,"98":6.4,"99":4.8,"100":4.5,"101":3.9,"102":5.4,"103":7.1,"104":6.1,"105":5.3,"106":6.7,"107":5.7,"108":4.4,"109":4.0,"110":6.7,"111":5.7,"112":4.9,"113":4.1,"114":5.4,"115":6.5,"116":5.2,"117":3.9,"118":5.1,"119":5.7,"120":5.9,"121":4.4,"122":4.5,"123":5.3,"124":6.2,"125":4.5,"126":6.7,"127":5.2,"128":4.5,"129":3.7,"130":5.7,"131":4.5,"132":5.8,"133":5.5,"134":6.2,"135":6.6,"136":3.5,"137":5.7,"138":4.8,"139":7.6,"140":5.6,"141":5.1,"142":5.9,"143":3.3,"144":5.3,"145":6.4,"146":5.8,"147":4.0,"148":4.2,"149":7.3,"150":5.9,"151":5.3,"152":4.1,"153":5.5,"154":7.7,"155":5.7,"156":5.8,"157":6.8,"158":6.1,"159":5.5,"160":4.2,"161":7.0,"162":5.3,"163":4.8,"164":3.9,"165":5.3,"166":6.7,"167":5.3,"168":4.4,"169":5.6,"170":6.2,"171":6.3,"172":5.0,"173":4.5,"174":5.8,"175":7.1,"176":4.8,"177":6.4,"178":5.6,"179":4.4,"180":4.0,"181":5.3,"182":4.4,"183":5.8,"184":5.9,"185":6.4,"186":6.4,"187":3.6,"188":6.2,"189":5.6,"190":8.1,"191":5.7,"192":5.4,"193":6.7,"194":3.6,"195":5.7,"196":6.7,"197":5.6,"198":4.5,"199":4.1,"200":7.4,"201":6.0,"202":5.6,"203":4.4,"204":5.2,"205":7.4,"206":5.0,"207":5.6,"208":6.2,"209":5.6,"210":4.9,"211":4.0,"212":7.5,"213":4.7,"214":4.8,"215":3.3,"216":4.7,"217":6.2,"218":5.3,"219":4.7,"220":5.6,"221":5.5,"222":5.7,"223":4.6,"224":4.3,"225":5.2,"226":7.0,"227":4.6,"228":6.3,"229":5.8,"230":4.3,"231":3.9,"232":4.6,"233":3.9,"234":4.9,"235":5.7,"236":5.8,"237":5.5,"238":3.5,"239":6.2,"240":4.9,"241":7.3,"242":5.4,"243":5.2,"244":6.8,"245":3.8,"246":5.5,"247":6.0,"248":5.0,"249":3.7,"250":3.7,"251":6.3,"252":5.3,"253":5.0,"254":3.9,"255":4.0,"256":6.8,"257":4.7,"258":4.9,"259":5.4,"260":5.0,"261":4.9,"262":4.2,"263":6.5,"264":3.8,"265":5.3,"266":2.8,"267":3.8,"268":5.7,"269":5.4,"270":4.6,"271":5.1,"272":6.1,"273":7.1,"274":4.8,"275":4.1,"276":4.8,"277":6.7,"278":4.0,"279":7.9,"280":5.4,"281":4.0,"282":3.8,"283":4.1,"284":3.6,"285":4.4,"286":5.3,"287":5.0,"288":5.2,"289":3.4,"290":5.9,"291":4.4,"292":6.1,"293":5.0,"294":5.0,"295":6.8,"296":3.9,"297":5.6,"298":5.3,"299":4.3,"300":3.5,"301":3.5,"302":5.5,"303":5.0,"304":4.7,"305":3.6,"306":3.5,"307":6.5,"308":4.1,"309":5.3,"310":4.9,"311":4.3,"312":4.4,"313":3.5,"314":5.9,"315":3.4,"316":4.6,"317":2.5,"318":3.2,"319":4.6,"320":4.9,"321":3.8,"322":4.3,"323":5.8,"324":3.9,"325":4.6,"326":3.8,"327":4.8,"328":6.9,"329":4.0,"330":6.7,"331":4.8,"332":3.3,"333":3.0,"334":4.2,"335":3.5,"336":4.7,"337":4.3,"338":4.6,"339":4.7,"340":3.2,"341":5.4,"342":4.1,"343":5.4,"344":4.6,"345":5.1,"346":6.4,"347":3.1,"348":5.1,"349":4.9,"350":3.0,"351":3.7,"352":3.0,"353":4.9,"354":4.7,"355":4.7,"356":3.3},"Region":{"0":"South","1":"West","2":"Southwest","3":"South","4":"West","5":"West","6":"New England","7":"Middle Atlantic","8":"South","9":"South","10":"South","11":"West","12":"West","13":"Midwest","14":"Midwest","15":"Midwest","16":"Midwest","17":"South","18":"South","19":"New England","20":"Middle Atlantic","21":"New England","22":"Midwest","23":"Midwest","24":"South","25":"South","26":"West","27":"Midwest","28":"West","29":"New England","30":"Middle Atlantic","31":"Southwest","32":"Middle Atlantic","33":"South","34":"Midwest","35":"Midwest","36":"Southwest","37":"West","38":"Middle Atlantic","39":"New England","40":"South","41":"Midwest","42":"South","43":"Southwest","44":"West","45":"New England","46":"South","47":"West","48":"South","49":"Midwest","50":"West","51":"South","52":"West","53":"Southwest","54":"South","55":"West","56":"West","57":"New England","58":"Middle Atlantic","59":"South","60":"South","61":"South","62":"West","63":"West","64":"Midwest","65":"Midwest","66":"Midwest","67":"Midwest","68":"South","69":"South","70":"New England","71":"Middle Atlantic","72":"New England","73":"Midwest","74":"Midwest","75":"South","76":"South","77":"West","78":"Midwest","79":"West","80":"New England","81":"Middle Atlantic","82":"Southwest","83":"Middle Atlantic","84":"South","85":"Midwest","86":"Midwest","87":"Southwest","88":"West","89":"Middle Atlantic","90":"New England","91":"South","92":"Midwest","93":"South","94":"Southwest","95":"West","96":"New England","97":"South","98":"West","99":"South","100":"Midwest","101":"West","102":"South","103":"West","104":"Southwest","105":"South","106":"West","107":"West","108":"New England","109":"Middle Atlantic","110":"South","111":"South","112":"South","113":"West","114":"West","115":"Midwest","116":"Midwest","117":"Midwest","118":"Midwest","119":"South","120":"South","121":"New England","122":"Middle Atlantic","123":"New England","124":"Midwest","125":"Midwest","126":"South","127":"South","128":"West","129":"Midwest","130":"West","131":"New England","132":"Middle Atlantic","133":"Southwest","134":"Middle Atlantic","135":"South","136":"Midwest","137":"Midwest","138":"Southwest","139":"West","140":"Middle Atlantic","141":"New England","142":"South","143":"Midwest","144":"South","145":"Southwest","146":"West","147":"New England","148":"South","149":"West","150":"South","151":"Midwest","152":"West","153":"South","154":"West","155":"Southwest","156":"South","157":"West","158":"West","159":"New England","160":"Middle Atlantic","161":"South","162":"South","163":"South","164":"West","165":"West","166":"Midwest","167":"Midwest","168":"Midwest","169":"Midwest","170":"South","171":"South","172":"New England","173":"Middle Atlantic","174":"New England","175":"Midwest","176":"Midwest","177":"South","178":"South","179":"West","180":"Midwest","181":"West","182":"New England","183":"Middle Atlantic","184":"Southwest","185":"Middle Atlantic","186":"South","187":"Midwest","188":"Midwest","189":"Southwest","190":"West","191":"Middle Atlantic","192":"New England","193":"South","194":"Midwest","195":"South","196":"Southwest","197":"West","198":"New England","199":"South","200":"West","201":"South","202":"Midwest","203":"West","204":"South","205":"West","206":"Southwest","207":"South","208":"West","209":"West","210":"New England","211":"Middle Atlantic","212":"South","213":"South","214":"South","215":"West","216":"West","217":"Midwest","218":"Midwest","219":"Midwest","220":"Midwest","221":"South","222":"South","223":"New England","224":"Middle Atlantic","225":"New England","226":"Midwest","227":"Midwest","228":"South","229":"South","230":"West","231":"Midwest","232":"West","233":"New England","234":"Middle Atlantic","235":"Southwest","236":"Middle Atlantic","237":"South","238":"Midwest","239":"Midwest","240":"Southwest","241":"West","242":"Middle Atlantic","243":"New England","244":"South","245":"Midwest","246":"South","247":"Southwest","248":"West","249":"New England","250":"South","251":"West","252":"South","253":"Midwest","254":"West","255":"South","256":"West","257":"Southwest","258":"South","259":"West","260":"West","261":"New England","262":"Middle Atlantic","263":"South","264":"South","265":"South","266":"West","267":"West","268":"Midwest","269":"Midwest","270":"Midwest","271":"Midwest","272":"South","273":"South","274":"New England","275":"Middle Atlantic","276":"New England","277":"Midwest","278":"Midwest","279":"South","280":"South","281":"West","282":"Midwest","283":"West","284":"New England","285":"Middle Atlantic","286":"Southwest","287":"Middle Atlantic","288":"South","289":"Midwest","290":"Midwest","291":"Southwest","292":"West","293":"Middle Atlantic","294":"New England","295":"South","296":"Midwest","297":"South","298":"Southwest","299":"West","300":"New England","301":"South","302":"West","303":"South","304":"Midwest","305":"West","306":"South","307":"West","308":"Southwest","309":"South","310":"West","311":"West","312":"New England","313":"Middle Atlantic","314":"South","315":"South","316":"South","317":"West","318":"West","319":"Midwest","320":"Midwest","321":"Midwest","322":"Midwest","323":"South","324":"South","325":"New England","326":"Middle Atlantic","327":"New England","328":"Midwest","329":"Midwest","330":"South","331":"South","332":"West","333":"Midwest","334":"West","335":"New England","336":"Middle Atlantic","337":"Southwest","338":"Middle Atlantic","339":"South","340":"Midwest","341":"Midwest","342":"Southwest","343":"West","344":"Middle Atlantic","345":"New England","346":"South","347":"Midwest","348":"South","349":"Southwest","350":"West","351":"New England","352":"South","353":"West","354":"South","355":"Midwest","356":"West"}}
    '''
    return house_prics_vs_income



