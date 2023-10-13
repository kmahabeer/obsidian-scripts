<%*
const refType = await tp.system.suggester([
  "Music", "SFX", // Audio
  "Artwork", "Figure Study", // Image
  "Motion Graphics", "Short Film", "Title Sequence", "Misc. Video" // Video
  ], [
  "Music", "SFX", // Audio
  "Artwork", "Figure Study", // Image
  "Motion Graphics", "Short Film", "Title Sequence", "Misc. Video" // Video
]);

if (refType == "Motion Graphics") {
  let media = "Video";
  let source = await tp.system.prompt("Enter URL for the reference: ");
  let videoLocation = await tp.system.suggester(["Locally", "On YouTube", "Other"], ["Locally", "On YouTube", "Other"], false, "Where is the video file saved?");

  if (videoLocation == "Locally") {
    let gif = await tp.system.prompt("Enter filename for gif: ");
    // let cover = `<img src="G:/My Drive/Obsidian-notes/Art/References/Videos/attachments/${gif}">`;
  }
}
%>

![[<%* tR += gif %>]]