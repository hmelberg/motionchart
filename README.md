# motionchart
Easily create an interactive motion chart from a Pandas Dataframe in Python. Publish the chart to a standalone webpage, show it in Jupyter notebook or save it as a html file

The basics<BR>
**0. install required modules** if they are not already installed (pandas, webbrowser)
pip install webbrowser
<BR><BR>
**1. Run main code below** (defines the motionchart class)<BR>
After running the code, you may test that works by executing the following command: motionChartDemo() 
<BR><BR>
**2. Define your own motion chart** using the columns in a pandas dataframe<BR>
Example: You have a dataframe called fruitdf and want to create a motionchart:
<BR>
smc = SocrMotionChart(df = fruitdf)
<BR><BR>
**3. Display the motionChart**<BR>
smc.to_browser
<BR><BR>
see http://socr.ucla.edu/htmls/HTML5/MotionChart/ for a live example
