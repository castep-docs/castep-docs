# CASTEP Docs

Documentation for the general-purpose plane-wave DFT code CASTEP.

The documentation itself is available at https://castep-docs.github.io/castep-docs/

## Contributing

You need python3 set as default then
```
 pip install mkdocs-material
 pip install mkdocs-bibtex
```
And you are ready.  
``` 
   mkdocs serve
```
Puts a live copy on a local port - and the browser view updates as you add and edit pages with your favourite text editor.

If you add a document you need to update the nav list in mkdocs.yml
This is needed because we want to control the order in which the pages appear

Please do add any pages missing, or put a request in the issue tracker. All pages will be checked by one of the CASTEP developers.

For the tutorial see the Semiconductor example. The aim is to show input and output - and highlight key points. The sort of open ended questions that we use for teaching at a workshop are less helpful in this format (i.e. when we are not around to answer and discuss)
