# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 15:33:33 2014

@author: Hans
"""


import os
import webbrowser
import pandas as pd
from IPython.display import HTML

class SocrMotionChart(object):
    def __init__(self, df, title = "Motion Chart",
        url = "http://socr.ucla.edu/htmls/HTML5/MotionChart",
        key = 1,
        x = 4,
        y = 5,
        size = 6, 
        color = 2,
        category = 2,
        xscale='linear',
        yscale='linear',
        varLabels=None):
            self.title = "Motion Chart"
            self.url = "http://socr.ucla.edu/htmls/HTML5/MotionChart"
            self.key = 1
            self.x = 4
            self.y = 5
            self.size = 6 
            self.color = 2
            self.category = 2
            self.xscale='linear'
            self.yscale='linear'
            self.varlabels = None
                
            df = df.reset_index()
            varNamesList = df.columns.tolist()                
            dataValuesString = df.to_json(orient = 'values')
            varNamesString = ",".join(['"' + str(x) + '"' for x in varNamesList])
            varNamesString = "[[" + varNamesString + "], ["
            dataValuesString = dataValuesString.lstrip("[")
            socrDataString = varNamesString + dataValuesString
           
        
            socrTemplate='''<!DOCTYPE html>
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
            <script src="{url}/js/bootstrap.js"></script>
            <script src="{url}/js/jquery.handsontable.js"></script>
            <script src="{url}/js/jquery.motionchart.js"></script>
            </head>
            <body>
            <div id="content" align="center">
            <div class="motionchart" style="width:1000px; height:600px;"></div>
            <script>
            
            var data = {data};
            
            $('.motionchart').motionchart({{
                    title: "{title}",
                    'data': data,
                    mappings: {{key: {key}, x: {x}, y: {y},
                        size: {size},  color: {color}, category: {category} }},
                    scalings: {{ x: '{xscale}', y: '{yscale}' }},
                    colorPalette: {{"Blue-Red": {{from: "rgb(0,0,255)", to: "rgb(255,0,0)"}}}},
                    color: "Red-Blue",
                    play: false,
                    loop: false
                }});
            </script>
            </div>
            </body>
            </html>
            '''
            SocrMotionChart.htmlString = socrTemplate.format(
                        title = title,
                        data = socrDataString,
                        url = "http://socr.ucla.edu/htmls/HTML5/MotionChart",
                        key = 1,x = 4,y = 5,size = 6, color = 2,category = 2,
                        xscale='linear',yscale='linear'
                        )
    
                    
    def to_browser(self):
       html = SocrMotionChart.htmlString
       path = os.path.abspath('temp.html')
       url = 'file://' + path
       # crash if multiple charts at the sam time?
       
       with open(path, 'w') as f:
           f.write(html)
       webbrowser.open(url)

    def to_notebook(self):
        htmlEncoded = SocrMotionChart.htmlString.encode('base64')
        HTML('<iframe src="data:text/html;base64,{0}" width="800" height="400"></iframe>'.format(htmlEncoded))

    def to_clipboard(self):
        pass
        # pyperclip
        
    def to_file(self):
        pass
    def to_server(self):
        pass
    
smc = SocrMotionChart(df)
smc.to_browser()


#import in webrowser    







df.to_clipboard()
a
$('.motionchart').motionchart({
                            title: "My Demo",
                            mappings: {key: 1, x: 2, y: 3, size: 5, color: 4, category: 0}
                            data: [["date","thing","key","x","y","z","unnamed: 6"], [[["date","thing","key","x","y","z","unnamed: 6"], ["08.02.2009","A","39852A",0.64367649,0.114548468,1.0,null],["08.02.2009","B","39852B",0.139936112,0.333852515,2.0,null],["08.02.2009","C","39852C",0.776886145,0.551003599,3.0,null],["08.02.2009","D","39852D",0.572737936,0.730948225,4.0,null],["08.02.2009","E","39852E",0.387230309,0.319537932,5.0,null],["08.02.2009","F","39852F",0.404173201,0.806370767,6.0,null],["09.02.2009","A","39853A",0.63867649,0.116548468,1.001,null],["09.02.2009","B","39853B",0.137936112,0.328852515,2.001,null],["09.02.2009","C","39853C",0.779886145,0.555003599,3.001,null],["09.02.2009","D","39853D",0.568737936,0.727948225,4.001,null],["09.02.2009","E","39853E",0.392230309,0.321537932,5.001,null],["09.02.2009","F","39853F",0.398173201,0.805370767,6.001,null],["10.02.2009","A","39854A",0.63367649,0.118548468,1.002,null],["10.02.2009","B","39854B",0.135936112,0.323852515,2.002,null],["10.02.2009","C","39854C",0.782886145,0.559003599,3.002,null],["10.02.2009","D","39854D",0.564737936,0.724948225,4.002,null],["10.02.2009","E","39854E",0.397230309,0.323537932,5.002,null],["10.02.2009","F","39854F",0.392173201,0.804370767,6.002,null],["11.02.2009","A","39855A",0.62867649,0.120548468,1.003,null],["11.02.2009","B","39855B",0.133936112,0.318852515,2.003,null],["11.02.2009","C","39855C",0.785886145,0.563003599,3.003,null],["11.02.2009","D","39855D",0.560737936,0.721948225,4.003,null],["11.02.2009","E","39855E",0.402230309,0.325537932,5.003,null],["11.02.2009","F","39855F",0.386173201,0.803370767,6.003,null],["12.02.2009","A","39856A",0.62367649,0.122548468,1.004,null],["12.02.2009","B","39856B",0.131936112,0.313852515,2.004,null],["12.02.2009","C","39856C",0.788886145,0.567003599,3.004,null],["12.02.2009","D","39856D",0.556737936,0.718948225,4.004,null],["12.02.2009","E","39856E",0.407230309,0.327537932,5.004,null],["12.02.2009","F","39856F",0.380173201,0.802370767,6.004,null],["13.02.2009","A","39857A",0.61867649,0.124548468,1.005,null],["13.02.2009","B","39857B",0.129936112,0.308852515,2.005,null],["13.02.2009","C","39857C",0.791886145,0.571003599,3.005,null],["13.02.2009","D","39857D",0.552737936,0.715948225,4.005,null],["13.02.2009","E","39857E",0.412230309,0.329537932,5.005,null],["13.02.2009","F","39857F",0.374173201,0.801370767,6.005,null],["14.02.2009","A","39858A",0.61367649,0.126548468,1.006,null],["14.02.2009","B","39858B",0.127936112,0.303852515,2.006,null],["14.02.2009","C","39858C",0.794886145,0.575003599,3.006,null],["14.02.2009","D","39858D",0.548737936,0.712948225,4.006,null],["14.02.2009","E","39858E",0.417230309,0.331537932,5.006,null],["14.02.2009","F","39858F",0.368173201,0.800370767,6.006,null],["15.02.2009","A","39859A",0.60867649,0.128548468,1.007,null],["15.02.2009","B","39859B",0.125936112,0.298852515,2.007,null],["15.02.2009","C","39859C",0.797886145,0.579003599,3.007,null],["15.02.2009","D","39859D",0.544737936,0.709948225,4.007,null],["15.02.2009","E","39859E",0.422230309,0.333537932,5.007,null],["15.02.2009","F","39859F",0.362173201,0.799370767,6.007,null],["16.02.2009","A","39860A",0.60367649,0.130548468,1.008,null],["16.02.2009","B","39860B",0.123936112,0.293852515,2.008,null],["16.02.2009","C","39860C",0.800886145,0.583003599,3.008,null],["16.02.2009","D","39860D",0.540737936,0.706948225,4.008,null],["16.02.2009","E","39860E",0.427230309,0.335537932,5.008,null],["16.02.2009","F","39860F",0.356173201,0.798370767,6.008,null],["17.02.2009","A","39861A",0.59867649,0.132548468,1.009,null],["17.02.2009","B","39861B",0.121936112,0.288852515,2.009,null],["17.02.2009","C","39861C",0.803886145,0.587003599,3.009,null],["17.02.2009","D","39861D",0.536737936,0.703948225,4.009,null],["17.02.2009","E","39861E",0.432230309,0.337537932,5.009,null],["17.02.2009","F","39861F",0.350173201,0.797370767,6.009,null],["18.02.2009","A","39862A",0.59367649,0.134548468,1.01,null],["18.02.2009","B","39862B",0.119936112,0.283852515,2.01,null],["18.02.2009","C","39862C",0.806886145,0.591003599,3.01,null],["18.02.2009","D","39862D",0.532737936,0.700948225,4.01,null],["18.02.2009","E","39862E",0.437230309,0.339537932,5.01,null],["18.02.2009","F","39862F",0.344173201,0.796370767,6.01,null],["19.02.2009","A","39863A",0.58867649,0.136548468,1.011,null],["19.02.2009","B","39863B",0.117936112,0.278852515,2.011,null],["19.02.2009","C","39863C",0.809886145,0.595003599,3.011,null],["19.02.2009","D","39863D",0.528737936,0.697948225,4.011,null],["19.02.2009","E","39863E",0.442230309,0.341537932,5.011,null],["19.02.2009","F","39863F",0.338173201,0.795370767,6.011,null],["20.02.2009","A","39864A",0.58367649,0.138548468,1.012,null],["20.02.2009","B","39864B",0.115936112,0.273852515,2.012,null],["20.02.2009","C","39864C",0.812886145,0.599003599,3.012,null],["20.02.2009","D","39864D",0.524737936,0.694948225,4.012,null],["20.02.2009","E","39864E",0.447230309,0.343537932,5.012,null],["20.02.2009","F","39864F",0.332173201,0.794370767,6.012,null],["21.02.2009","A","39865A",0.57867649,0.140548468,1.013,null],["21.02.2009","B","39865B",0.113936112,0.268852515,2.013,null],["21.02.2009","C","39865C",0.815886145,0.603003599,3.013,null],["21.02.2009","D","39865D",0.520737936,0.691948225,4.013,null],["21.02.2009","E","39865E",0.452230309,0.345537932,5.013,null],["21.02.2009","F","39865F",0.326173201,0.793370767,6.013,null],["22.02.2009","A","39866A",0.57367649,0.142548468,1.014,null],["22.02.2009","B","39866B",0.111936112,0.263852515,2.014,null],["22.02.2009","C","39866C",0.818886145,0.607003599,3.014,null],["22.02.2009","D","39866D",0.516737936,0.688948225,4.014,null],["22.02.2009","E","39866E",0.457230309,0.347537932,5.014,null],["22.02.2009","F","39866F",0.320173201,0.792370767,6.014,null],["23.02.2009","A","39867A",0.56867649,0.144548468,1.015,null],["23.02.2009","B","39867B",0.109936112,0.258852515,2.015,null],["23.02.2009","C","39867C",0.821886145,0.611003599,3.015,null],["23.02.2009","D","39867D",0.512737936,0.685948225,4.015,null],["23.02.2009","E","39867E",0.462230309,0.349537932,5.015,null],["23.02.2009","F","39867F",0.314173201,0.791370767,6.015,null],["24.02.2009","A","39868A",0.56367649,0.146548468,1.016,null],["24.02.2009","B","39868B",0.107936112,0.253852515,2.016,null],["24.02.2009","C","39868C",0.824886145,0.615003599,3.016,null],["24.02.2009","D","39868D",0.508737936,0.682948225,4.016,null],["24.02.2009","E","39868E",0.467230309,0.351537932,5.016,null],["24.02.2009","F","39868F",0.308173201,0.790370767,6.016,null],["25.02.2009","A","39869A",0.55867649,0.148548468,1.017,null],["25.02.2009","B","39869B",0.105936112,0.248852515,2.017,null],["25.02.2009","C","39869C",0.827886145,0.619003599,3.017,null],["25.02.2009","D","39869D",0.504737936,0.679948225,4.017,null],["25.02.2009","E","39869E",0.472230309,0.353537932,5.017,null],["25.02.2009","F","39869F",0.302173201,0.789370767,6.017,null],["26.02.2009","A","39870A",0.55367649,0.150548468,1.018,null],["26.02.2009","B","39870B",0.103936112,0.243852515,2.018,null],["26.02.2009","C","39870C",0.830886145,0.623003599,3.018,null],["26.02.2009","D","39870D",0.500737936,0.676948225,4.018,null],["26.02.2009","E","39870E",0.477230309,0.355537932,5.018,null],["26.02.2009","F","39870F",0.296173201,0.788370767,6.018,null],["27.02.2009","A","39871A",0.54867649,0.152548468,1.019,null],["27.02.2009","B","39871B",0.101936112,0.238852515,2.019,null],["27.02.2009","C","39871C",0.833886145,0.627003599,3.019,null],["27.02.2009","D","39871D",0.496737936,0.673948225,4.019,null],["27.02.2009","E","39871E",0.482230309,0.357537932,5.019,null],["27.02.2009","F","39871F",0.290173201,0.787370767,6.019,null],["28.02.2009","A","39872A",0.54367649,0.154548468,1.02,null],["28.02.2009","B","39872B",0.099936112,0.233852515,2.02,null],["28.02.2009","C","39872C",0.836886145,0.631003599,3.02,null],["28.02.2009","D","39872D",0.492737936,0.670948225,4.02,null],["28.02.2009","E","39872E",0.487230309,0.359537932,5.02,null],["28.02.2009","F","39872F",0.284173201,0.786370767,6.02,null],["01.03.2009","A","39873A",0.53867649,0.156548468,1.021,null],["01.03.2009","B","39873B",0.097936112,0.228852515,2.021,null],["01.03.2009","C","39873C",0.839886145,0.635003599,3.021,null],["01.03.2009","D","39873D",0.488737936,0.667948225,4.021,null],["01.03.2009","E","39873E",0.492230309,0.361537932,5.021,null],["01.03.2009","F","39873F",0.278173201,0.785370767,6.021,null],["02.03.2009","A","39874A",0.53367649,0.158548468,1.022,null],["02.03.2009","B","39874B",0.095936112,0.223852515,2.022,null],["02.03.2009","C","39874C",0.842886145,0.639003599,3.022,null],["02.03.2009","D","39874D",0.484737936,0.664948225,4.022,null],["02.03.2009","E","39874E",0.497230309,0.363537932,5.022,null],["02.03.2009","F","39874F",0.272173201,0.784370767,6.022,null],["03.03.2009","A","39875A",0.52867649,0.160548468,1.023,null],["03.03.2009","B","39875B",0.093936112,0.218852515,2.023,null],["03.03.2009","C","39875C",0.845886145,0.643003599,3.023,null],["03.03.2009","D","39875D",0.480737936,0.661948225,4.023,null],["03.03.2009","E","39875E",0.502230309,0.365537932,5.023,null],["03.03.2009","F","39875F",0.266173201,0.783370767,6.023,null],["04.03.2009","A","39876A",0.52367649,0.162548468,1.024,null],["04.03.2009","B","39876B",0.091936112,0.213852515,2.024,null],["04.03.2009","C","39876C",0.848886145,0.647003599,3.024,null],["04.03.2009","D","39876D",0.476737936,0.658948225,4.024,null],["04.03.2009","E","39876E",0.507230309,0.367537932,5.024,null],["04.03.2009","F","39876F",0.260173201,0.782370767,6.024,null],["05.03.2009","A","39877A",0.51867649,0.164548468,1.025,null],["05.03.2009","B","39877B",0.089936112,0.208852515,2.025,null],["05.03.2009","C","39877C",0.851886145,0.651003599,3.025,null],["05.03.2009","D","39877D",0.472737936,0.655948225,4.025,null],["05.03.2009","E","39877E",0.512230309,0.369537932,5.025,null],["05.03.2009","F","39877F",0.254173201,0.781370767,6.025,null],["06.03.2009","A","39878A",0.51367649,0.166548468,1.026,null],["06.03.2009","B","39878B",0.087936112,0.203852515,2.026,null],["06.03.2009","C","39878C",0.854886145,0.655003599,3.026,null],["06.03.2009","D","39878D",0.468737936,0.652948225,4.026,null],["06.03.2009","E","39878E",0.517230309,0.371537932,5.026,null],["06.03.2009","F","39878F",0.248173201,0.780370767,6.026,null],["07.03.2009","A","39879A",0.50867649,0.168548468,1.027,null],["07.03.2009","B","39879B",0.085936112,0.198852515,2.027,null],["07.03.2009","C","39879C",0.857886145,0.659003599,3.027,null],["07.03.2009","D","39879D",0.464737936,0.649948225,4.027,null],["07.03.2009","E","39879E",0.522230309,0.373537932,5.027,null],["07.03.2009","F","39879F",0.242173201,0.779370767,6.027,null],["08.03.2009","A","39880A",0.50367649,0.170548468,1.028,null],["08.03.2009","B","39880B",0.083936112,0.193852515,2.028,null],["08.03.2009","C","39880C",0.860886145,0.663003599,3.028,null],["08.03.2009","D","39880D",0.460737936,0.646948225,4.028,null],["08.03.2009","E","39880E",0.527230309,0.375537932,5.028,null],["08.03.2009","F","39880F",0.236173201,0.778370767,6.028,null],["09.03.2009","A","39881A",0.49867649,0.172548468,1.029,null],["09.03.2009","B","39881B",0.081936112,0.188852515,2.029,null],["09.03.2009","C","39881C",0.863886145,0.667003599,3.029,null],["09.03.2009","D","39881D",0.456737936,0.643948225,4.029,null],["09.03.2009","E","39881E",0.532230309,0.377537932,5.029,null],["09.03.2009","F","39881F",0.230173201,0.777370767,6.029,null],["10.03.2009","A","39882A",0.49367649,0.174548468,1.03,null],["10.03.2009","B","39882B",0.079936112,0.183852515,2.03,null],["10.03.2009","C","39882C",0.866886145,0.671003599,3.03,null],["10.03.2009","D","39882D",0.452737936,0.640948225,4.03,null],["10.03.2009","E","39882E",0.537230309,0.379537932,5.03,null],["10.03.2009","F","39882F",0.224173201,0.776370767,6.03,null],["11.03.2009","A","39883A",0.48867649,0.176548468,1.031,null],["11.03.2009","B","39883B",0.077936112,0.178852515,2.031,null],["11.03.2009","C","39883C",0.869886145,0.675003599,3.031,null],["11.03.2009","D","39883D",0.448737936,0.637948225,4.031,null],["11.03.2009","E","39883E",0.542230309,0.381537932,5.031,null],["11.03.2009","F","39883F",0.218173201,0.775370767,6.031,null],["12.03.2009","A","39884A",0.48367649,0.178548468,1.032,null],["12.03.2009","B","39884B",0.075936112,0.173852515,2.032,null],["12.03.2009","C","39884C",0.872886145,0.679003599,3.032,null],["12.03.2009","D","39884D",0.444737936,0.634948225,4.032,null],["12.03.2009","E","39884E",0.547230309,0.383537932,5.032,null],["12.03.2009","F","39884F",0.212173201,0.774370767,6.032,null],["13.03.2009","A","39885A",0.47867649,0.180548468,1.033,null],["13.03.2009","B","39885B",0.073936112,0.168852515,2.033,null],["13.03.2009","C","39885C",0.875886145,0.683003599,3.033,null],["13.03.2009","D","39885D",0.440737936,0.631948225,4.033,null],["13.03.2009","E","39885E",0.552230309,0.385537932,5.033,null],["13.03.2009","F","39885F",0.206173201,0.773370767,6.033,null],["14.03.2009","A","39886A",0.47367649,0.182548468,1.034,null],["14.03.2009","B","39886B",0.071936112,0.163852515,2.034,null],["14.03.2009","C","39886C",0.878886145,0.687003599,3.034,null],["14.03.2009","D","39886D",0.436737936,0.628948225,4.034,null],["14.03.2009","E","39886E",0.557230309,0.387537932,5.034,null],["14.03.2009","F","39886F",0.200173201,0.772370767,6.034,null],["15.03.2009","A","39887A",0.46867649,0.184548468,1.035,null],["15.03.2009","B","39887B",0.069936112,0.158852515,2.035,null],["15.03.2009","C","39887C",0.881886145,0.691003599,3.035,null],["15.03.2009","D","39887D",0.432737936,0.625948225,4.035,null],["15.03.2009","E","39887E",0.562230309,0.389537932,5.035,null],["15.03.2009","F","39887F",0.194173201,0.771370767,6.035,null],["16.03.2009","A","39888A",0.46367649,0.186548468,1.036,null],["16.03.2009","B","39888B",0.067936112,0.153852515,2.036,null],["16.03.2009","C","39888C",0.884886145,0.695003599,3.036,null],["16.03.2009","D","39888D",0.428737936,0.622948225,4.036,null],["16.03.2009","E","39888E",0.567230309,0.391537932,5.036,null],["16.03.2009","F","39888F",0.188173201,0.770370767,6.036,null],["17.03.2009","A","39889A",0.45867649,0.188548468,1.037,null],["17.03.2009","B","39889B",0.065936112,0.148852515,2.037,null],["17.03.2009","C","39889C",0.887886145,0.699003599,3.037,null],["17.03.2009","D","39889D",0.424737936,0.619948225,4.037,null],["17.03.2009","E","39889E",0.572230309,0.393537932,5.037,null],["17.03.2009","F","39889F",0.182173201,0.769370767,6.037,null],["18.03.2009","A","39890A",0.45367649,0.190548468,1.038,null],["18.03.2009","B","39890B",0.063936112,0.143852515,2.038,null],["18.03.2009","C","39890C",0.890886145,0.703003599,3.038,null],["18.03.2009","D","39890D",0.420737936,0.616948225,4.038,null],["18.03.2009","E","39890E",0.577230309,0.395537932,5.038,null],["18.03.2009","F","39890F",0.176173201,0.768370767,6.038,null],["19.03.2009","A","39891A",0.44867649,0.192548468,1.039,null],["19.03.2009","B","39891B",0.061936112,0.138852515,2.039,null],["19.03.2009","C","39891C",0.893886145,0.707003599,3.039,null],["19.03.2009","D","39891D",0.416737936,0.613948225,4.039,null],["19.03.2009","E","39891E",0.582230309,0.397537932,5.039,null],["19.03.2009","F","39891F",0.170173201,0.767370767,6.039,null],["20.03.2009","A","39892A",0.44367649,0.194548468,1.04,null],["20.03.2009","B","39892B",0.059936112,0.133852515,2.04,null],["20.03.2009","C","39892C",0.896886145,0.711003599,3.04,null],["20.03.2009","D","39892D",0.412737936,0.610948225,4.04,null],["20.03.2009","E","39892E",0.587230309,0.399537932,5.04,null],["20.03.2009","F","39892F",0.164173201,0.766370767,6.04,null]]
                        });
                        
               
               
               
               
               
               
               
def socrdata(df,STUB,title,key,x,y,size,color,category,xscale='linear',yscale='linear'):
        f = socrTemplate.format(
                stub=STUB,title=title,
                key=df.columns.get_loc(key),
                x=df.columns.get_loc(x),
                y=df.columns.get_loc(y),
                size=df.columns.get_loc(size),
                color=df.columns.get_loc(color),
                category=df.columns.get_loc(category),
                xscale=xscale, yscale=yscale
        )
        return f
        

 test = socrdata(df, 'mctest','mctest','date','x','y','z','thing', 'thing')






df.head()
a = df.head().to_csv()

# Creating the data
  description = {"name": ("string", "Name"),
                 "salary": ("number", "Salary"),
                 "full_time": ("boolean", "Full Time Employee")}
  data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
          {"name": "Jim", "salary": (800, "$800"), "full_time": False},
          {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
          {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Creating a JavaScript code string
  jscode = data_table.ToJSCode("jscode_data",
                               columns_order=("name", "salary", "full_time"),
                               order_by="salary")
  # Creating a JSon string
  json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
                           order_by="salary")



def motionChart(dataFrame, mainCategory, timeVar, xyVars):
     df2 = dataFrame
     df2[mainCategory] = df2[mainCategory].astype(str)
     df2['jTime'] = list(zip(df2[timeVar].dt.year, df2[timeVar].dt.month, df2[timeVar].dt.day))
     df2['jTime'] = "new Date " + df2['jTime'].astype(str)
     
     for var in xyVars:
         df2[xyVars] = df2[xyVars].astype(float)
     
     #for var in subCategoryVars:
         #df2[subCategoryVars] = df2[subCategoryVars].astype(str)  

     df2["jRows"] = list(zip(df2[mainCategory].astype(str), df2['jTime'], [df2[v] for v in xyVars]))
     
     
motionChart(dataFrame = df, mainCategory = "thing", timeVar = "date", xyVars = ["x", "y", "z"])


# consider dateutil package
# important java months start at 0 and end at 11??! http://stackoverflow.com/questions/18160848/python-vs-javascript-datetime
# what if date column is the index
# NB zip behaves differently in p2.7 and 3.4, in 3 retunrs zip objects, use list to get it back
#what if have different date formats? only weekly, or monthly data?
df['jMonth'] = df.date.dt.month
df['jMonth'] = df['jMonth'] - 1 # JavaScript month format goes from 0 to 11 (does data also do this?)

#df['jTime'] = list(zip(df.date.dt.year, df.date.dt.month, df.date.dt.day))
df['jTime'] = list(zip(df.date.dt.year, df.jMonth, df.date.dt.day)) 
df['jTime'] = "new Date " + df['jTime'].astype(str)

df["jRows"] = list(zip(df.thing, df['jTime'], df.x, df.y, df.z)).astype(str)
df["jRows"] = df["jRows"].astype(str)
timeVar = timeVar()
df["jRows"][0]
df.head()
jRowString =  df["jRows"].tolist()
jRowString2 = "".join(jRowString)
jRowString2 = jRowString2.replace(")(", "],[") 
jRowString2 = jRowString2.replace(")',", "),") 
jRowString2 = jRowString2.replace("'new Date", "new Date")

jRowString2 = jRowString2.replace("'new Date", "new Date") 
jRowString2 = jRowString2.replace("'new Date", "new Date") 
jRowString2 = jRowString2.lstrip("(") 
jRowString2 = jRowString2.rstrip(")")
jRowString2 = "[" + jRowString2 + "]"
print (jRowString2)


da = "data.addColumn("

jColumns = da + 

jColumns = """
        data.addColumn('string', 'thing');
        data.addColumn('date', 'Date');
        data.addColumn('number', 'x');
        data.addColumn('number', 'y');
        data.addColumn('number', 'z');
"""


jAll ="""
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["motionchart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        """ + jColumns + "data.addRows([" + jRowString2 + """
        ]);

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


print (jAll)




df['jDate'] = df.Date.apply(lambda x: "new Date(" + x.dt.year + ", " + x.dt.month + ", " + x.dt.day +")")
df['jDate'] = df.Date.apply(lambda x: "new Date(" + x.year + ", " + x.month + ", " + x.day +")")



varNames = df.columns.tolist()
varTypes = df.dtypes.tolist()

        data.addColumn('string', 'Fruit');
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Sales');
        data.addColumn('number', 'Expenses');
        data.addColumn('string', 'Location');
        data.addRows([
          ['Apples',  new Date (1988,0,1), 1000, 300, 'East'],
          ['Oranges', new Date (1988,0,1), 1150, 200, 'West'],
          ['Bananas', new Date (1988,0,1), 300,  250, 'West'],
          ['Apples',  new Date (1989,6,1), 1200, 400, 'East'],
          ['Oranges', new Date (1989,6,1), 750,  150, 'West'],
          ['Bananas', new Date (1989,6,1), 788,  617, 'West']
          
          
  http://stackoverflow.com/questions/21197774/assign-pandas-dataframe-column-dtypes
  



df['jDate'] = list(zip(df.Date.dt.year, df.Date.dt.month, df.Date.dt.day))
df['jDate'] = "new Date " + df.jDate.astype(str)
  
  j = df.to_json()
j
df = pd.read_clipboard()
df.X.replace("%","", inplace = True)
df.Y.replace("%","", inplace = True)

df['X'] = df['X'].map(lambda x: x.lstrip(' ').rstrip('%'))
df['Y'] = df['Y'].map(lambda x: x.lstrip(' ').rstrip('%'))
df['X'] = df['X'].astype(float)
df['Y'] = df['Y'].astype(float)
df['Z'] = df['Z'].astype(float)

df['X'] = df['X'].map(lambda x: x.replace(',', '.'))
df['Y'] = df['Y'].map(lambda x: x.replace(',', '.'))
df['Z'] = df['Z'].map(lambda x: x.replace(',', '.'))

for x in columns:
    
categories = df.Thing
timeVar = df.Date
xyVars = [df.X, df.Y]

api
createDataTable(dataframe, timeVar, )

orjust 

MotionChart(timeVar, categoryVars, xyVars)
# Options and labels
categoryVarsLables
xyVarsLabels


df.Date = pd.to_datetime(df.Date)

df.Date.dt.year 

for point in timeVar:
    timeVar
    
years = df.Date.dt.year.tolist()
months = df.Date.dt.month.tolist()
days = df.Date.dt.day.tolist()

jDates = zip(years, months, days)
print (jDates)
len(years)
len(months)
len(days)



import cgi
import StringIO
import csv
import datetime
try:
  import json
except ImportError:
  import simplejson as json
import types