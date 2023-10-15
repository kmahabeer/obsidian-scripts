<%*
  function getKeyByValue(map, val) {
    for (const [key, value] of map.entries()) {
      for (const element of value) {
        if (val === element) {
          return key;
        }
      }
    }
  }

  function iterateOverMap(map, array) {
    for (const [key, value] of map.entries()) {
      for (const val of value) {
        array.push(val);
      }
    }
  }
  
  function printMap(map, array) {
    for (const [key, value] of map.entries()) {
      array.push(`**${key}:** [[${value}]]`);
    }
  }
  
  function createParameterListFromMap(map, list) {
    for (const [key, value] of map.entries()) {
      let paramPrintOut;
      paramPrintOut = `**${key}:**`;
      paramPrintOut = paramPrintOut.concat(` ${value.map(file => `[[${file}]]`).join(`, `)}`);
      paramsList.push(paramPrintOut);
    }
  }

  async function createMultiselectSuggester(params, map, prompt) {
    for (const param of params) {
      
      const selectedFiles = [];
      const folderChoicePath = `${param}/`;
      const filesInFolder = app.vault.getMarkdownFiles()
        .filter(file => file.path.includes(folderChoicePath))
        .map(tFile=>tFile.basename);
      
      while (true) {
        prompt = `'${param}' parameter. Press [ESC] when finished.`;
        if (selectedFiles.length >= 1) {
          prompt = prompt.concat(` {${selectedFiles.map(file => file).join(`, `)}}`);
        }
        const selectedFile = await tp.system.suggester(filesInFolder, filesInFolder, false, prompt);
        if (!selectedFile) {
          break;
        } else {
          selectedFiles.push(selectedFile);
          map.set(param, selectedFiles);
          filesInFolder.splice(filesInFolder.indexOf(selectedFile), 1);
        }
      }
    }
    return map;
  }
-%>
<%*
  // User prompt for type of reference
  const referenceTypes = new Map();
  referenceTypes.set("Audio", ["Music", "SFX"]);
  referenceTypes.set("Image", ["Artwork", "Figure Study"]);
  referenceTypes.set("Video", ["Motion Graphics", "Short Film", "Title Sequence", "Misc. Video"]);
  const referenceTypesList = [];
  iterateOverMap(referenceTypes, referenceTypesList);
  const referenceType = await tp.system.suggester(referenceTypesList, referenceTypesList,
    false, "Select the type of reference: ");
  const mediaType = getKeyByValue(referenceTypes, referenceType);
-%>
<%*
  // tags
  const tag = referenceType
    .toLowerCase()
    .replace(/\bmisc\. /g, '')
    .replace(/[./\\?%*:|"<>]/g, '')
    .replace(/ /g, '-');
-%>
<%*
  // URL
  const url = await tp.system.prompt(`Enter the URL for the ${referenceType.toLowerCase()}:`);
-%>
<%*
  // Frontmatter
  const frontMatter = `---\ntags:\n  - reference\n  - ${tag}\nsource: ${url}\n---`;
-%>
<%*
  // Image Parameters
  const paramMap = new Map();
  paramMap.set('User Prompts', ['Title', 'Date', 'Location', 'Dimensions']);
  paramMap.set('Multi Select', ['Style', 'Art Period', 'Subject Matter', 'Media', 'Vibes']);
  paramMap.set('Single Select', ['Artist']);
  if (referenceType == "Artwork") {
    params = ['Title', 'Artist', 'Date', 'Style', 'Art Period', 'Genre / Subject Matter', 'Media', 'Location', 'Dimensions', 'Vibes'];
  }
-%>
<%*
  // Video Parameters
  let defaultParams = [];
  let params = [];
  let paramsList = [];
  let selectedParamChoices = new Map();

  if (referenceType == "Motion Graphics" || referenceType == "Title Sequence") {
    defaultParams = ['Design and Animation', 'Music and SFX', 'Vibes'];
    if (referenceType === 'Motion Graphics') {
      params = params.concat('Brands', defaultParams);
    }
    if (referenceType === 'Title Sequence') {
      params = params.concat('Movie and TV', defaultParams);
    }
  }
  
  // Multi-select
  let prompt;
  await createMultiselectSuggester(params, selectedParamChoices, prompt);
  createParameterListFromMap(selectedParamChoices, paramsList);
-%>
<% frontMatter %>
## <% mediaType %>

<% paramsList.map(item => `${item}`).join(`\n`) %>