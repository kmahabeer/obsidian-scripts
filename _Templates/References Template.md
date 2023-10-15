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
  
  function createParameterListFromMap(map, list) {
    for (const [key, value] of map.entries()) {
      let paramPrintOut;
      paramPrintOut = `**${key}:**`;
      paramPrintOut = paramPrintOut.concat(` ${value.map(file => `[[${file}]]`).join(`, `)}`);
      paramsList.push(paramPrintOut);
    }
  }

  function getFilesInFolder(folder, query = '', ext = ['md', 'txt']) {
    let filesInFolder;
    filesInFolder = app.vault.getFiles()
      .filter(file=>file.path.includes(folder))
      .filter(tFile=>ext.includes(tFile.extension))
      .filter(tFile=>tFile.basename.toLowerCase().includes(query.toLowerCase()))
      .map(tFile=>tFile.basename);
    if (filesInFolder.length == 0) {
      filesInFolder = [];
    }
    return filesInFolder;
  }

  async function createSingleSelectMenuDialog(menuOptions, menuPlaceholder) {
    return await tp.system.suggester(menuOptions, menuOptions, false, menuPlaceholder);
  }

  async function createMultiSelectMenuDialog(menuOptions, menuPlaceholder) {   
    const selectedOptions = []; 
    while (true) {
      let updatedMenuPlaceholder = '';
      if (selectedOptions.length >= 1) {
        updatedMenuPlaceholder = `${menuPlaceholder} ${selectedOptions.map(file => file).join(`, `)}`;
      } else {
        updatedMenuPlaceholder = menuPlaceholder;
      }
      const selectedOption = await createSingleSelectMenuDialog(menuOptions, updatedMenuPlaceholder);
      if (!selectedOption) {
        break;
      } else {
        selectedOptions.push(selectedOption);
        menuOptions.splice(menuOptions.indexOf(selectedOption), 1);
      }
    }
    return selectedOptions;
  }

  async function createMultiselectSuggester(params, map, prompt) {
    for (const param of params) {
      const folderChoicePath = `${param}/`;
      const filesInFolder = getFilesInFolder(folderChoicePath);

      let menuPlaceholder = `'${param}' parameter. Press [ESC] when finished.`;
      const selectedOptions = await createMultiSelectMenuDialog(filesInFolder, menuPlaceholder);
      map.set(param, selectedOptions);
      console.log(map)
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
  // let prompt;
  await createMultiselectSuggester(params, selectedParamChoices, prompt);
  createParameterListFromMap(selectedParamChoices, paramsList);
-%>
<% frontMatter %>
## <% mediaType %>

<% paramsList.map(item => `${item}`).join(`\n`) %>