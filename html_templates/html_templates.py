import typing

def get_html_template(content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">
    <style>
      .collapsible {{
        cursor: pointer;
        user-select: none;
        font-weight: bold;
        display: flex;
        align-items: center;
      }}
      .collapsible::before {{
        content: '\\25B8'; /* Right-pointing triangle */
        display: inline-block;
        margin-right: 8px;
        transition: transform 0.2s;
        font-size: 0.8em; /* Make the triangle smaller */
      }}
      .collapsible.active::before {{
        transform: rotate(90deg); /* Down-pointing triangle */
      }}
      .content {{
        display: none;
        padding-left: 20px;
      }}
      pre code {{
        white-space: pre-wrap;
        word-break: break-word;
      }}
      #expandAllBtn {{
        margin: 10px;
        padding: 5px 10px;
        font-size: 1em;
        cursor: pointer;
      }}
      #searchBar {{
        margin: 10px;
        padding: 5px;
        font-size: 1em;
      }}
      #searchBtn {{
        margin: 10px;
        padding: 5px 10px;
        font-size: 1em;
        cursor: pointer;
      }}
      .highlight {{
        background-color: yellow;
      }}
    </style>
    </head>
    <body>

    <input type="text" id="searchBar" placeholder="Search...">
    <button id="searchBtn">Search</button>
    <button id="expandAllBtn">Expand All</button>
    <div id="content">{content}</div>

    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <script>
      {get_collapsible_script()}
      {get_search_script()}
    </script>

    </body>
    </html>
    """

def get_collapsible_script() -> str:
    return """
    document.addEventListener("DOMContentLoaded", function() {
        const headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        headers.forEach(header => {
            let content = header.nextElementSibling;
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('content');

            let hasContent = false;
            while (content && !content.tagName.startsWith('H')) {
                const nextContent = content.nextElementSibling;
                contentDiv.appendChild(content);
                content = nextContent;
                hasContent = true;
            }

            if (hasContent) {
                header.classList.add('collapsible');
                header.insertAdjacentElement('afterend', contentDiv);

                header.addEventListener('click', function() {
                    this.classList.toggle('active');
                    contentDiv.style.display = contentDiv.style.display === 'none' ? 'block' : 'none';
                });
            }
        });

        const expandAllBtn = document.getElementById('expandAllBtn');
        let allExpanded = false;
        expandAllBtn.addEventListener('click', function() {
            headers.forEach(header => {
                if (header.classList.contains('collapsible')) {
                    const contentDiv = header.nextElementSibling;
                    if (allExpanded) {
                        header.classList.remove('active');
                        contentDiv.style.display = 'none';
                    } else {
                        header.classList.add('active');
                        contentDiv.style.display = 'block';
                    }
                }
            });
            allExpanded = !allExpanded;
            expandAllBtn.textContent = allExpanded ? 'Collapse All' : 'Expand All';
        });
    });
    """

def get_search_script() -> str:
    return """
    document.addEventListener("DOMContentLoaded", function() {
        const searchBar = document.getElementById('searchBar');
        const searchBtn = document.getElementById('searchBtn');

        searchBtn.addEventListener('click', function() {
            console.log('Search button clicked');
            const searchTerm = searchBar.value.trim().toLowerCase();
            console.log('Search term:', searchTerm);
            if (searchTerm) {
                const contentDiv = document.getElementById('content');
                console.log('Content div found:', contentDiv);
                removeHighlights(contentDiv);
                highlightMatches(contentDiv, searchTerm);
            }
        });

        function highlightMatches(node, searchTerm) {
            if (node.nodeType === 3) { // Text node
                const val = node.nodeValue.toLowerCase();
                const idx = val.indexOf(searchTerm);
                if (idx !== -1) {
                    console.log('Match found:', node.nodeValue);
                    const span = document.createElement('span');
                    span.className = 'highlight';
                    const text = node.nodeValue.substring(idx, idx + searchTerm.length);
                    span.appendChild(document.createTextNode(text));

                    const after = node.splitText(idx);
                    after.nodeValue = after.nodeValue.substring(searchTerm.length);
                    node.parentNode.insertBefore(span, after);
                }
            } else if (node.nodeType === 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
                for (let i = 0; i < node.childNodes.length; i++) {
                    if (node.childNodes[i].nodeType === 1 && node.childNodes[i].className === 'highlight') {
                        continue; // Skip already highlighted nodes
                    }
                    highlightMatches(node.childNodes[i], searchTerm);
                }
            }
        }

        function removeHighlights(node) {
            console.log('Removing highlights from node:', node);
            const highlights = node.querySelectorAll('.highlight');
            highlights.forEach(span => {
                span.replaceWith(span.firstChild);
            });
        }
    });
    """
