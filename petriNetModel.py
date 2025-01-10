import pm4py.objects.conversion.log.converter as log_converter
import pm4py.algo.discovery.alpha.algorithm as alpha_miner
import pm4py.visualization.petri_net.visualizer  as pn_visualizer
import pm4py.algo.analysis.workflow_net.algorithm as wf_net
import pm4py.objects.petri_net.utils as petri_utils
import pm4py.objects.log.importer.xes.importer as xes_importer
import pm4py
import pandas as pd

#Path to the dataset file
event_log_path = "data/Insurance_claims_event_log.csv"  # Replace with the actual file path
#event_log_path = "data/edited_hh102_weekends.xes"  # Replace with the actual file path

#Step 1: Import the event log
def import_event_log(file_path):
    print("\n--->Step 1: Importing the event log")
    # Import the CSV file as an event log
    
    """
    pd_data = pd.read_csv(file_path)
    pd_data.columns = ['case:concept:name','concept:name','time:timestamp','claimant_name','agent_name','adjuster_name','claim_amount','claimant_age','type_of_policy','car_make','car_model','car_year','type_of_accident','user_type']
    
    pd_data['time:timestamp'] = pd.to_datetime(pd_data['time:timestamp'])
    event_log = log_converter.apply(pd_data, variant=log_converter.Variants.TO_EVENT_LOG)
    """
    
    event_log = xes_importer.apply(file_path)

    print("Event log imported successfully.")
    return event_log

#Step 2: Discover a Petri net from the log
def discover_petri_net(event_log):
    print("\n--->Step 2: Discover a Petri net from the log")
    print("Discovering Petri net...")
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    print("Petri net discovered successfully.")
    return net, initial_marking, final_marking

#Step 3: Visualize the Petri net
def visualize_petri_net(net, initial_marking, final_marking):
    print("\n--->Step 3: Visualize the Petri net")
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.view(gviz)
    print("Petri net visualization complete.")

def checking_petri_net_properties(net, initial_marking, final_marking):
    print("\n--->Step 4: Checking the properties of the Petri net")
    # Check the properties of the Petri net
    print("Number of places:", len(net.places))
    print("Number of transitions:", len(net.transitions))
    print("Number of arcs:", len(net.arcs))
    print("Initial marking:", initial_marking)
    print("Final marking:", final_marking)
    print("The petri net is a workflow net? ", wf_net.apply(net))
    #print("The petri net is a sound? ", petri_utils.check_soundness(net, initial_marking, final_marking))

#Main execution block
if __name__ == "__main__":
    print("Process Mining with PM4Py: Discovering a Petri net from an event log")
    
    # Import the event log
    event_log = import_event_log(event_log_path)
    #print(event_log.__dict__)
    
    # Discover the Petri net
    net, initial_marking, final_marking = discover_petri_net(event_log)
    
    # Check the properties of the Petri net
    checking_petri_net_properties(net, initial_marking, final_marking)
    
    # Visualize the Petri net
    visualize_petri_net(net, initial_marking, final_marking)