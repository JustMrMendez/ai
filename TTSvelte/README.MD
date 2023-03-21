## TTSvelte 0.0.1
### Convert site built with tailwind into a svelte app

#### steps
1. go to the site you want to convert
2. open the console
3. paste the code below
```js
function createTree(element, includeAttributes = false) {
  const tree = {
    tagName: element.tagName.toLowerCase(),
    children: [],
  };

  if (includeAttributes) {
    const attributes = Array.from(element.attributes).reduce((acc, attr) => {
      acc[attr.nodeName] = attr.nodeValue;
      return acc;
    }, {});

    tree.attributes = attributes;
  }

  Array.from(element.children).forEach(child => {
    tree.children.push(createTree(child, includeAttributes));
  });

  return tree;
}

// Usage:
const siteTree = createTree(document.body, true); // set the second argument to `false` to exclude attributes
console.log(JSON.stringify(siteTree, null, 2));

function saveFile(content, fileName) {
  const fileContent = new Blob([content], { type: 'application/json' });
  const downloadLink = document.createElement('a');
  
  downloadLink.href = URL.createObjectURL(fileContent);
  downloadLink.download = fileName;
  downloadLink.click();

  // Clean up to avoid memory leaks.
  setTimeout(() => {
    URL.revokeObjectURL(downloadLink.href);
    downloadLink.remove();
  }, 0);
}

// Usage:
const siteTree = createTree(document.body, true);
saveFile(JSON.stringify(siteTree, null, 2), 'site_tree.json');
```

4. copy the fille `site_tree.json` to the root of your project

run the following command to install the dependencies
```bash
pip install -r requirements.txt
```

5. run the TTsvelte compiler
```bash
ttsvelte -t site_tree.json -n <name of the app>
```
