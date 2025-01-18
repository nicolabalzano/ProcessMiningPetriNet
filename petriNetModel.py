import pm4py.objects.conversion.log.converter as log_converter
import pm4py.algo.discovery.alpha.algorithm as alpha_miner
import pm4py.visualization.petri_net.visualizer  as pn_visualizer
import pm4py.algo.analysis.workflow_net.algorithm as wf_net
import pm4py.objects.petri_net.utils as petri_utils
import pm4py.objects.log.importer.xes.importer as xes_importer
import pm4py
import pandas as pd

#Path to the dataset file
event_log_path = "data/BPI_Challenge_2013_incidents.xes" 


#Step 1: Import the event log
def import_event_log(file_path):
    print("\n--->Step 1: Importing the event log")
    
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

# Step 4: Split the net in train and test and check the properties of the Petri net
def checking_petri_net_properties(net, initial_marking, final_marking, event_log_test):
    print("\n--->Step 4: Checking the properties of the Petri net")
    
    # Check the properties of the Petri net
    print("Number of places:", len(net.places))
    print("Number of transitions:", len(net.transitions))
    print("Number of arcs:", len(net.arcs))
    print("Initial marking:", initial_marking)
    print("Final marking:", final_marking)
    print("The petri net is a workflow net? ", wf_net.apply(net))
    print("Soundness: ",pm4py.analysis.check_soundness(net, initial_marking, final_marking)[0])
    #petri_net_invisible_transition = pm4py.analysis.reduce_petri_net_invisibles(net)
    #visualize_petri_net(petri_net_invisible_transition, initial_marking, final_marking)
    # print("Maximal decomposition: ",pm4py.analysis.maximal_decomposition(net, initial_marking, final_marking))
    print("Simplicity: ",pm4py.algo.evaluation.simplicity.algorithm.apply(net))
    print("Replay fitness: ",pm4py.algo.evaluation.replay_fitness.algorithm.apply(event_log_test, net, initial_marking, final_marking))
    print("Generalization: ",pm4py.algo.evaluation.generalization.algorithm.apply(event_log, net, initial_marking, final_marking))
    #df_diagnostics = pm4py.conformance_diagnostics_token_based_replay(event_log, net, initial_marking, final_marking, return_diagnostics_dataframe=True)
    #print("Conformance dignostics token based reply: ",df_diagnostics)
    #df_diagnostics.to_csv("data/conformance_diagnostics.csv")

#Main execution block
if __name__ == "__main__":
    print("Process Mining with PM4Py: Discovering a Petri net from an event log")

    # Import the event log
    event_log = import_event_log(event_log_path)
    (event_log_train, event_log_test) = pm4py.ml.split_train_test(event_log)

    
    # Discover the Petri net
    net, initial_marking, final_marking = discover_petri_net(event_log_train)
    
    # Check the properties of the Petri net
    checking_petri_net_properties(net, initial_marking, final_marking, event_log_test)
    
    # Visualize the Petri net
    visualize_petri_net(net, initial_marking, final_marking)
    
   