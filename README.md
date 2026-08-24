# CASTEP Docs

Documentation for the general-purpose plane-wave DFT code CASTEP.

The documentation itself is available at https://castep-docs.github.io/castep-docs/

## Contributing

You need a valid install of [python3](https://www.python.org/downloads/) with working pip, then run:

```sh
pip install -r requirements.txt
```
and you are ready.

```sh
mkdocs serve
```

puts a live copy on a local port - and the browser view updates as you add and edit pages with your favourite text editor.


If you add a document you need to update the nav list in `mkdocs.yml`.
This is needed because we want to control the order in which the pages appear.

Please do add any missing pages, or put a request in the issue tracker. All pages will be checked by one of the CASTEP developers.

See https://castep-docs.github.io/castep-docs/developer/docs_contribution for more detail.

For tutorials see the tutorials section; to begin with the [population analysis](https://castep-docs.github.io/castep-docs/tutorials/Bonding_and_Charge/mulliken_population/) follows the steps of setting up a calculation from scratch. 

The aim of these is to show input and output - and highlight key points. The sort of open ended questions that we use for teaching at a workshop are less helpful in this format (i.e. when we are not around to answer and discuss)
