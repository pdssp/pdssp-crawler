# Documentation

## Generate and publish documentation

**Generate**

From `pdssp-crawler` package directory:

```shell
jupyter-book build docs/ 
```

**Publish**

From `pdssp-crawler` package directory:

```shell
ghp-import -n -p -f docs/_build/html/  
```