import pm4py
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.conversion.log import factory as log_converter
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.visualization.petrinet import factory as pn_visualizer

#Path to the dataset file
event_log_path = "path_to_your_file.csv"  # Replace with the actual file path

#Step 1: Import the event log
def import_event_log(file_path):
    print("Importing event log...")
    # Import the CSV file as an event log
    log = csv_importer.import_event_stream(file_path)
    # Convert the imported log into a pm4py-compatible log object
    event_log = log_converter.apply(log)
    print("Event log imported successfully.")
    return event_log

#Step 2: Discover a Petri net from the log
def discover_petri_net(event_log):
    print("Discovering Petri net...")
    net, initial_marking, final_marking = alpha_miner.apply(event_log)
    print("Petri net discovered successfully.")
    return net, initial_marking, final_marking

#Step 3: Visualize the Petri net
def visualize_petri_net(net, initial_marking, final_marking):
    print("Visualizing Petri net...")
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.view(gviz)
    print("Petri net visualization complete.")

#Main execution block
if name == "main":
    # Import the event log
    event_log = import_event_log(event_log_path)

    # Discover the Petri net
    net, initial_marking, final_marking = discover_petri_net(event_log)

    # Visualize the Petri net
    visualize_petri_net(net, initial_marking, final_marking)