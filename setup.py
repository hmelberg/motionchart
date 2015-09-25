from distutils.core import setup
setup(
  name = 'motionchart',
  packages = ['motionchart'], # this must be the same as the name above
  version = '0.1',
  description = 'A wrapper to make interactive motion chart visualizations from pandas dataframes',
  author = 'Hans Olav Melberg',
  author_email = 'hans.melberg@gmail.com',
  url = 'https://github.com/hmelberg/motionchart', # use the URL to the github repo
  download_url = 'https://github.com/hmelberg/motionchart/tarball/0.1', # I'll explain this in a second
  keywords = ['motion chart', 'pandas', 'visualization'], # arbitrary keywords
  classifiers = [],
  install_requires = ['webbrowser', 'pandas', 'pyperclip']
)