import pandas as pd
import networkx as nx
import tkinter as tk
from tkinter import ttk, messagebox

class TubeMap:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_data()

    def load_data(self):
        self.ds = pd.read_excel(self.file_path, header=None, names=['line', 'start', 'end', 'duration'])
        self.ds = self.ds.dropna()  # Removing rows with missing or NaN values
        self.graph_original = nx.from_pandas_edgelist(self.ds, "start", "end", ["duration"], create_using=nx.DiGraph)
        
        ds_reversed = self.ds.copy()
        ds_reversed[['start', 'end']] = self.ds[['end', 'start']]
        self.graph_reversed = nx.from_pandas_edgelist(ds_reversed, "start", "end", ["duration"], create_using=nx.DiGraph)
        self.combined_graph = nx.compose(self.graph_original, self.graph_reversed)

    def find_shortest_path(self, start, end):
        try:
            shortest_path = nx.shortest_path(self.combined_graph, source=start, target=end, weight="duration")
            return shortest_path
        except nx.NetworkXNoPath:
            return None

    def calculate_total_duration(self, path):
        if path:
            total_duration = sum(self.combined_graph[path[i]][path[i + 1]]["duration"] for i in range(len(path) - 1))
            return total_duration
        else:
            return None

    def calculate_total_stops(self, path):
        if path:
            total_stops = len(path) - 1
            return total_stops
        else:
            return None

    def display_neighboring_stations(self, station_name):
        try:
            neighbors = list(self.combined_graph.neighbors(station_name))
            if neighbors:
                output_text = f"Neighboring Stations for '{station_name}':\n"
                for neighbor in neighbors:
                    stops = self.combined_graph[station_name][neighbor]["duration"]
                    output_text += f"{neighbor} - {stops} stops\n"
                return output_text
            else:
                return f"No neighboring stations found for '{station_name}'."
        except nx.NetworkXError:
            return f"Error: Station '{station_name}' not found in the dataset."

    def explore_line_information(self, line):
        line_data = self.ds[self.ds['line'] == line]

        if not line_data.empty:
            print(f"\nInformation for Tube Line '{line}':")

            # Display stations in the line
            stations = line_data['start'].unique().tolist() + line_data['end'].unique().tolist()
            unique_stations = list(set(stations))
            output_text = "\n".join(unique_stations)
            return output_text
        else:
            return f"No information found for Tube Line '{line}'."

class TubeMapInterface(TubeMap):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("London-TubeTrack")
        self.root.configure(bg='lightgrey')

        self.create_input_widgets()
        self.create_output_widget()

    def create_input_widgets(self):
        start_station_label = tk.Label(self.root, text="Start Station:", bg='lightgrey')
        start_station_label.grid(row=0, column=0, padx=10, pady=5)

        self.start_station_var = tk.StringVar(self.root)
        self.start_station_entry = ttk.Combobox(self.root, textvariable=self.start_station_var)
        self.start_station_entry.grid(row=0, column=1, padx=10, pady=5)
        self.start_station_entry.bind("<KeyRelease>", self.on_station_entry_changed)

        end_station_label = tk.Label(self.root, text="End Station:", bg='lightgrey')
        end_station_label.grid(row=1, column=0, padx=10, pady=5)

        self.end_station_var = tk.StringVar(self.root)
        self.end_station_entry = ttk.Combobox(self.root, textvariable=self.end_station_var)
        self.end_station_entry.grid(row=1, column=1, padx=10, pady=5)
        self.end_station_entry.bind("<KeyRelease>", self.on_station_entry_changed)

        select_button = tk.Button(self.root, text="Find Journey Details", command=self.perform_journey, bg='green', fg='white')
        select_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Button to display neighboring stations
        neighboring_button = tk.Button(self.root, text="Display Neighboring Stations", command=self.display_neighboring_stations_gui, bg='blue', fg='white')
        neighboring_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Entry field to enter line for exploring information
        line_entry_label = tk.Label(self.root, text="Explore Line Information:", bg='lightgrey')
        line_entry_label.grid(row=4, column=0, padx=10, pady=5)

        self.line_var = tk.StringVar(self.root)
        line_entry = tk.Entry(self.root, textvariable=self.line_var)
        line_entry.grid(row=4, column=1, padx=10, pady=5)

        # Button to explore line information
        explore_button = tk.Button(self.root, text="Explore Line Information", command=self.explore_line_information_gui, bg='orange', fg='white')
        explore_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Button to provide feedback
        feedback_button = tk.Button(self.root, text="Provide Feedback", command=self.provide_feedback, bg='red', fg='white')
        feedback_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Text widget to display feedback
        self.feedback_text = tk.Text(self.root, height=5, width=50)
        self.feedback_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # Button to submit feedback
        submit_feedback_button = tk.Button(self.root, text="Submit Feedback", command=self.submit_feedback, bg='red', fg='white')
        submit_feedback_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

    def create_output_widget(self):
        self.output_text = tk.Text(self.root, height=20, width=100)
        self.output_text.grid(row=0, column=2, rowspan=6, padx=10, pady=5)

    def perform_journey(self):
        start_station = self.start_station_var.get()
        end_station = self.end_station_var.get()

        shortest_path = self.find_shortest_path(start_station, end_station)
        total_duration = self.calculate_total_duration(shortest_path)
        total_stops = self.calculate_total_stops(shortest_path)

        if shortest_path:
            output_text = f"Shortest Path: {shortest_path}\nTotal Duration: {total_duration} minutes\nTotal Stops: {total_stops}"
            self.output_text.insert(tk.END, output_text + "\n\n")
        else:
            messagebox.showerror("Error", f"No path found from {start_station} to {end_station}")

    def on_station_entry_changed(self, event):
        suggestions = []
        typed_text = self.start_station_var.get().strip().title()

        if typed_text:
            for station in self.combined_graph.nodes():
                if station.startswith(typed_text):
                    suggestions.append(station)

        self.start_station_entry['values'] = suggestions

        end_suggestions = []
        end_typed_text = self.end_station_var.get().strip().title()

        if end_typed_text:
            for station in self.combined_graph.nodes():
                if station.startswith(end_typed_text):
                    end_suggestions.append(station)

        self.end_station_entry['values'] = end_suggestions

    def display_neighboring_stations_gui(self):
        station_name = self.start_station_var.get()
        output_text = self.display_neighboring_stations(station_name)
        self.output_text.insert(tk.END, output_text + "\n\n")

    def explore_line_information_gui(self):
        line = self.line_var.get().strip().title()
        output_text = self.explore_line_information(line)
        self.output_text.insert(tk.END, output_text + "\n\n")

    def provide_feedback(self):
        # Clear the existing feedback text
        self.feedback_text.delete(1.0, tk.END)

    def submit_feedback(self):
        feedback = self.feedback_text.get("1.0", tk.END).strip()
        if feedback:
            # Implement the feedback submission logic here
            # For now, let's print the feedback to the console
            print("Feedback received:")
            print(feedback)
            messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
        else:
            messagebox.showwarning("Empty Feedback", "Please provide your feedback before submitting.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    file_path = "/Users/aaryashirbhate/Downloads/GitLondonTube"
    tube_map_interface = TubeMapInterface(file_path)
    tube_map_interface.run()
