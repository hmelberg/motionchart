# motionchart
<a href="http://www.youtube.com/watch?feature=player_embedded&v=YOUTUBE_VIDEO_ID_HERE
" target="_blank"><img src="http://img.youtube.com/vi/https://youtu.be/JkpbY08swyA/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
<BR>
Easily create an interactive motion chart from a Pandas Dataframe in Python. Publish the chart to a standalone webpage, show it in Jupyter notebook or save it as a html file
<BR>

The basics<BR>
**0. Install required modules** if they are not already installed (pandas, webbrowser)
pip install webbrowser
<BR><BR>
**1. Run the code in _motionchartv11.py_ above** (defines the motionchart class)<BR>
After running the code, you may test that works by executing the following command: motionChartDemo() 
<BR><BR>
**2. Define your own motion chart** using the columns in a pandas dataframe<BR>
Example: You have a dataframe called fruitdf and want to create a motionchart:
<BR>
smc = SocrMotionChart(df = fruitdf)
<BR><BR>
**3. Display the Motion Chart**<BR>
smc.to_browser
<BR><BR>
see http://socr.ucla.edu/htmls/HTML5/MotionChart/ for a live example
<BR><BR>
See the file "motion chart notebook" (above) for more examples and detailed instructions
<BR><BR>
http://nbviewer.ipython.org/github/hmelberg/motionchart/blob/master/motion%20chart%20notebook.ipynb
