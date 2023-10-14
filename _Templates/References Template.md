<%*
  function getKeyByValue(map, value) {
    for (const [key, value] of map.entries()) {
      if (val === value) {
        return key;
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
-%>
<%*
// tags
const tags = referenceType
  .toLowerCase()
  .replace(/\bmisc\. /g, '')
  .replace(/[./\\?%*:|"<>]/g, '')
  .replace(/ /g, '-');
-%>
<%*
// URL
const url = await tp.system.prompt(`Enter the URL for the video:`);
-%>
<% referenceType %>
<% tags %>