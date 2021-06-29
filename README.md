# dotmm-companion-converter

This Python script can convert a (printer-friendly) pdf of the DotMM Companion to JSON files that can be imported into Foundry VTT.

## How to use

Install `pdf2text` using the following shell commmand:

```sh
pip install pdf2text
```

Next, use `pdf2text` to extract each chapter of your DotMM Companion pdf as a HTML page. An example command is provided below. Unfortunately, you will have to manually specify which pages to extract. 

```sh
pdf2txt.py -o Companion_ArcaneChambers.html -p 33,34,35,36,37,38,39 -t html -A DotMM_Companion.pdf
```

Finally, use `companionConverter.py` (from this repository) to convert the HTML page created in the previous step to a JSON file that you can import as a Journal Entry in Foundry VTT. Make sure you edit `htmlName` in `companionConverter.py` to match the name of the HTML file you made. You will need the following Python libraries to run the Python script: `codecs`, `bs4` (or `BeautifulSoup`). 

## Disclaimer
This is not a perfect converter. It meant as a tool for legitimate owners of the DotMM Companion pdf, for whom it may save a lot of manual typing / copy-pasting to get the text descriptions into Foundry. 

