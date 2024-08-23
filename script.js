// Generate options for the puzzle number dropdown
document.addEventListener("DOMContentLoaded", function () {
	const puzzleNumberDropdown = document.getElementById("puzzleNumber");

	for (let i = 1; i <= 35; i++) {
		let option = document.createElement("option");
		option.value = i;
		option.textContent = i;
		puzzleNumberDropdown.appendChild(option);
	}
});

function showPuzzle() {
	const difficulty = document.getElementById("difficulty").value;
	const puzzleNumber = document.getElementById("puzzleNumber").value;
	const showSolution = document.getElementById("showSolution").checked;

	const puzzleContainer = document.getElementById("puzzleContainer");

	// Determine the image path based on whether the solution is being shown
	const imagePath = showSolution
		? `/jumping_julia_puzzles/boards/${difficulty}/jumping_julia_solution_${puzzleNumber}.png`
		: `/jumping_julia_puzzles/boards/${difficulty}/jumping_julia_board_${puzzleNumber}.png`;

	puzzleContainer.innerHTML = `<img src="${imagePath}" alt="Puzzle Image" style="max-width: 100%; height: auto;">`;

	// https://shaumikkhanna.github.io/jumping_julia_puzzles/boards/easy/jumping_julia_solution_1.png
	// https://shaumikkhanna.github.io/boards/easy/jumping_julia_board_1.png

	// Determine the text file path based on the selections
	const textFilePath = showSolution
		? `/jumping_julia_puzzles/boards/${difficulty}/jumping_julia_path_${puzzleNumber}.txt`
		: `/jumping_julia_puzzles/boards/${difficulty}/jumping_julia_board_${puzzleNumber}.txt`;

	// Load the text file content into the textContainer
	fetch(textFilePath)
		.then((response) => {
			if (response.ok) {
				return response.text();
			} else {
				throw new Error("Text file not found.");
			}
		})
		.then((data) => {
			document.getElementById("textContainer").textContent = data;
		})
		.catch((error) => {
			console.error("Error loading text file:", error);
			document.getElementById("textContainer").textContent =
				"No text file available for this selection.";
		});
}
