# Contributing to these Docs

## Getting Started

The documentation source is available publically at
https://github.com/castep-docs/castep-docs

Clone the repo there with `git`, ensure that you have a valid install of
[python3](https://www.python.org/downloads/) with working pip, then
run:

```sh
pip install -r requirements.txt
```
in the root of the cloned repository and you are ready.

```sh
mkdocs serve
```

puts a live copy on a local port - and the browser view updates as you
add and edit pages with your favourite text editor.

## Writing documentation

It is often helpful to divide your documentation into several
sections, which may span multiple pages:

1. A brief descriptive summary for beginners to understand the
   context in which the functionality might be used. This might
   include common use cases, as well as a basic summary
   of the theory described by the functionality. It is often useful to
   include reference to experimental models which may be represented
   by the theory.
2. An in-depth introduction to the theory with reference to the
   original papers, relevant equations and methods implemented in the
   functionality.
3. A summary description of the use in CASTEP of the functionality,
   how to use it and what features are included.
4. Details of all related keywords, their effects and their use within
   the context of the functionality.
5. Description of the expected outputs, along with recommendations for
   how to process them including references to external tools if needed.

Documentation should be written to be informative about the options
and features available, as well as describing the common use cases for
the functionality in question to give users an idea.

## Style Guide

!!! note

    The CASTEP docs pages are written in [Markdown](https://www.markdownguide.org/)
    through [mkdocs](https://www.mkdocs.org/), their pages have more detail on how
    to use the language and renderers.

### Parameters

When referencing CASTEP parameters within the documentation it is
important that they are denoted as such by being in either fences:

    ```
    like_this
    ```

or inline verbatim
```markdown
Somewhat `like_this`
```

For cases where parameters might have multiple possible values, this is shown by using the pipe (`|`) symbol, e.g:

```
setting : choice_1 | choice_2 | choice_3
```

For cases where parameters might have optional values, these are denoted by being placed in square brackets, e.g.:

```
setting : value [optional_value]
```

### References

The CASTEP Documentation uses BibTeX references in order to refer to
papers. To use this, add the appropriate BibTeX formatted reference
into the `refs.bib` in the root folder of the repository.

To cite the reference in-text use:

```markdown
[@cite-key]
```

where `cite-key` is the cite key for the reference to import.
These citations are inserted as footnotes, e.g: [@vanSanten2015].

### Internal Links

Linking between documentation sources should be done by relative
references **to the source file**.

!!! warning

    While it may appear that internal links of the form:

    ```markdown
    /documentation/Getting_Started/built_in_help
    ```

    work on your local documentation, they may fail
    when rendered in the online documentation.

    The most reliable form of the above reference would be:

    ```markdown
    ../Getting_Started/built_in_help.md
    ```

## Adding to the Toctree

Once you have created your page of documentation, you will need to add
it to the toc-tree (table of contents) to make it accessible in the sidebar.

This is done by adding an entry into the YAML formatted `mkdocs.yml`
in the root folder of the repository.

Each level of the main list is a sub-folder in the toc-tree, the label
for which will be the key.

Each page is a value (the key is the name which appears in the
side-bar) which points to the page's source file within the
documentation relative to the root folder.

## GitHub

Once you have made your changes to the documentation, you will need to
make a PR ready for review.

!!! note

    that `castep-docs` runs on a forked repository model, this means
    that to contribute you need to fork a personal copy of the `castep-docs` repo.

    See [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) to find out how.
