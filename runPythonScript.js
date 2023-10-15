const { exec } = require('child_process');

// Command to run the Python script
const pythonScript = 'python saveVideo.py';

// Execute the Python script
const pythonProcess = exec(pythonScript, (error, stdout, stderr) => {
	if (error) {
		console.error(`Error: ${error}`);
		return;
	}
	console.log(`Python Script Output: ${stdout}`);
});

pythonProcess.stdin.end(); // Close the input stream
