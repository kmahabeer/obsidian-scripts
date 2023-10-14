<%*
// User prompt for type of reference
const referenceTypes = new Map();
referenceTypes.set("Audio", ["Music", "SFX"]);
referenceTypes.set("Image", ["Artwork", "Figure Study"]);
referenceTypes.set("Video", ["Motion Graphics", "Short Film", "Title Sequence", "Misc. Video"]);
const referenceTypesList = [];
for (const [key, value] of referenceTypes.entries()) {
  for (const element of value) {
    referenceTypesList.push(element);
  }
}
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