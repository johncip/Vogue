vogue
=====

Externalizes internal and inline CSS. A work in progress.

```
usage: run.py [-h] [-c CSS_PATH] [-f] [-i INPUT_DIR] [-o OUTPUT_DIR]
              [-p PREFIX]

vogue -- automatically externalize styles in HTML files.

optional arguments:
  -h, --help            show this help message and exit
  -c CSS_PATH, --css_path CSS_PATH
                        CSS output filename and path (relative to output_dir).
                        Default is "css/extracted.css".
  -f, --force           Write files even if output dir exists. May overwrite
                        existing files in output dir.
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Specifies the input directory. Default is ".".
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Specifies the output directory. Default is "./output".
  -p PREFIX, --prefix PREFIX
                        Sets the prefix for CSS class names. Must be a valid
                        CSS class identifier (omit the leading dot). Default
                        is "st_".

Note: vogue does not currently handle psuedo-elements or pseudo-classes within
style tags.
```
