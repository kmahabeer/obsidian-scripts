const { exec } = require('child_process');
const uuid = require('uuid');
const os = require('os');
const fs = require('fs');
const path = require('path');

const currentDir = process.cwd();
const saveDir = path.join(currentDir, 'References', 'Videos', 'attachments');

if (!fs.existsSync(saveDir)) {
	fs.mkdirSync(saveDir, { recursive: true });
}

const askQuestion = (query) => {
	return new Promise((resolve) => {
		const readline = require('readline').createInterface({
			input: process.stdin,
			output: process.stdout,
		});

		readline.question(query, (answer) => {
			readline.close();
			resolve(answer);
		});
	});
};

const runCommand = (command) => {
	return new Promise((resolve, reject) => {
		exec(command, (error, stdout, stderr) => {
			if (error) {
				reject(error);
			} else {
				resolve(stdout);
			}
		});
	});
};

async function main() {
	// os.chdir(saveDir); // doesn't work

	// Ask user for video URL
	const videoUrl = await askQuestion('Enter the URL of the video: ');

	console.log('\n---Media Type---');
	console.log('0 - 1080p video + audio');
	console.log('1 - audio only');
	const option = await askQuestion('Select an option for media type: ');

	let isGifCompress = '0';
	if (option === '1') {
		isGifCompress = '0';
	} else {
		console.log('\n---Compression---');
		console.log('0 - do NOT compress');
		console.log('1 - compression');
		isGifCompress = await askQuestion('Select an option for compression: ');
	}

	const uuidStr = uuid.v4();
	let ext = '';

	if (option === '0') {
		// Download the video using yt-dlp
		const downloadCmd = `yt-dlp -f "bestvideo*[height<=1080][ext=mp4]+bestaudio*[ext=m4a]/best[ext=mp4]/best" -o "ref-${uuidStr}.%(ext)s" ${videoUrl}`;
		await runCommand(downloadCmd);
	} else if (option === '1') {
		// Download audio only from the video using yt-dlp
		const downloadAudioCmd = `yt-dlp -f "ba[ext=m4a]" -o "ref-${uuidStr}.%(ext)s" ${videoUrl}`;
		await runCommand(downloadAudioCmd);
	}

	let outputString = 'Video download complete.';

	// GIF parameters
	const fpsValues = [12];
	const speedValues = [2];
	const scaleValues = [480];

	// Compression parameters
	const lossyValues = [90];
	const colorValues = [128];

	for (const fps of fpsValues) {
		for (const speed of speedValues) {
			for (const scaleWidth of scaleValues) {
				if (fs.existsSync(`ref-${uuidStr}.mkv`)) {
					ext = 'mkv';
				}
				if (fs.existsSync(`ref-${uuidStr}.mp4`)) {
					ext = 'mp4';
				}

				// Convert the downloaded video to a GIF
				const vid2gifCmd = `ffmpeg -i "ref-${uuidStr}.${ext}" -filter:v "fps=${fps},setpts=${
					1 / speed
				}*PTS,scale=${scaleWidth}:-1" -y "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}.gif"`;
				await runCommand(vid2gifCmd);
				outputString += '\nVideo to GIF conversion complete.';

				if (isGifCompress === '1') {
					for (const lossy of lossyValues) {
						for (const color of colorValues) {
							// Compress the GIF
							const compressCmd = `gifsicle -O3 --lossy=${lossy} --colors ${color} "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}.gif" -o "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}-compressed-lossy_${lossy}-colors_${color}.gif"`;
							await runCommand(compressCmd);
							outputString += '\nGIF compression complete.';
						}
					}
				}
			}
		}
	}

	process.chdir(currentDir);
	console.log(outputString);
	console.log(`Video file: ref-${uuidStr}.${ext}`);
	console.log(
		`GIF file: ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}.gif`
	);
}

main();
