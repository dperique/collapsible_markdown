# Markdown to HTML Converter

This program converts Markdown files to HTML, with support for collapsible sections.

Markdown is nice but there are times when the document is big and we want to take advantage of the hierarchical view it provides by having collapsible sections.  This way, we can view the document
at differnet "levels"

## Installation

```bash
git clone https://github.com/dperique/collapsible-markdown.git
cd collapsible-markdown
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to use it

After installation, add some markdown files to the current directory and do this:

```bash
python ./render.py
```

The program starts an html server and allows you to navigate to each markdown file.

The program will render the markdown as html creating collapsible sections based on the headings.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.