# LondonTubeMap_JourneyPlanner
Here's a sample `README.md` file for your GitHub repository that explains the London Tube Map Journey Planner project. The README provides an overview of the project, instructions for setting it up, and how to use it.

---

This project is a Python-based London Tube Map Journey Planner application. It allows users to find the shortest path between two tube stations, explore line information, and display neighboring stations. The application also provides a simple graphical user interface (GUI) built using Tkinter.

## Features

- **Find Shortest Path**: Calculates the shortest path between two tube stations based on travel duration.
- **Explore Line Information**: Displays all the stations on a specific tube line.
- **Display Neighboring Stations**: Shows the neighboring stations for a selected station.
- **Provide Feedback**: Allows users to submit feedback through the GUI.

## Dependencies

This project requires the following Python libraries:

- `pandas`
- `networkx`
- `tkinter` (comes pre-installed with Python)

You can install the necessary dependencies using the following command:

```bash
pip install pandas networkx
```

## Installation and Setup

1. **Clone the Repository**:

   Clone this repository to your local machine using the following command:

   ```bash
   git clone git@github.com:aaryaya/LondonTubeMap_JourneyPlanner.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd LondonTubeMap_JourneyPlanner
   ```

3. **Prepare the Data**:

   Place the Excel file containing the tube map data in the project directory. The Excel file should have the following structure:

   - **line**: Name of the tube line.
   - **start**: Name of the starting station.
   - **end**: Name of the ending station.
   - **duration**: Travel duration between the start and end stations.

4. **Run the Application**:

   Run the following command to start the GUI application:

   ```bash
   python main.py
   ```

   Replace `main.py` with the actual filename where the code is saved.

## Usage

Once the application is running, you can:

- Enter the start and end stations to find the shortest path between them.
- Explore line information by entering the line name.
- Display neighboring stations by entering a station name.
- Provide feedback through the GUI.

### Example

1. **Find the Shortest Path**:

   - Enter "Start Station" and "End Station."
   - Click "Find Journey Details" to display the shortest path, total duration, and total stops.

2. **Explore Line Information**:

   - Enter a line name in the "Explore Line Information" field.
   - Click "Explore Line Information" to display the stations on the selected line.

3. **Display Neighboring Stations**:

   - Enter a station name in the "Start Station" field.
   - Click "Display Neighboring Stations" to display the neighboring stations.

4. **Provide Feedback**:

   - Enter feedback in the text box.
   - Click "Submit Feedback" to submit your feedback.

## Contributing

Feel free to fork this repository and contribute by submitting pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This `README.md` provides all the essential information that someone needs to understand, set up, and use the application. Make sure to adjust any specific paths or details based on your actual project setup.
