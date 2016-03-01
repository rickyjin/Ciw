from __future__ import division
from individual import Individual


class ArrivalNode:
    """
    Class for the arrival node on our network
    """
    def __init__(self, simulation):
        """
        Initialise a node.
        """
        self.simulation = simulation
        self.number_of_individuals = 0
        self.event_dates_dict = {nd + 1:{cls:False
            for cls in range(self.simulation.parameters['Number_of_classes'])}
            for nd in range(self.simulation.number_of_nodes)}
        self.rejection_dict = {nd + 1:{cls:[]
            for cls in range(self.simulation.parameters['Number_of_classes'])}
            for nd in range(self.simulation.number_of_nodes)}
        self.initialise_event_dates_dict()
        self.find_next_event_date()

    def __repr__(self):
        """
        Representation of an arrival node.
        """
        return 'Arrival Node'

    def find_next_event_date(self):
        """
        Finds the time of the next event at this node.
        """
        times = [[self.event_dates_dict[nd+1][cls]
            for cls in range(len(self.event_dates_dict[1]))]
            for nd in range(len(self.event_dates_dict))]
        mintimes = [min(obs) for obs in times]
        nd = mintimes.index(min(mintimes))
        cls = times[nd].index(min(times[nd]))
        self.next_node = nd + 1
        self.next_class = cls
        self.next_event_date = self.event_dates_dict[self.next_node][self.next_class]

    def have_event(self):
        """
        Send new arrival to relevent node.
        """
        self.number_of_individuals += 1
        next_individual = Individual(self.number_of_individuals, self.next_class)
        next_node = self.simulation.transitive_nodes[self.next_node-1]
        if len(next_node.individuals) < next_node.node_capacity:
            next_node.accept(next_individual, self.next_event_date)
        else:
            self.rejection_dict[next_node.id_number][self.next_class].append(self.next_event_date)
        self.event_dates_dict[self.next_node][self.next_class] += self.inter_arrival(self.next_node, self.next_class)
        self.find_next_event_date()

    def initialise_event_dates_dict(self):
        """
        Initialises the next event dates dictionary
        with random times for each node and class.
        """
        for nd in self.event_dates_dict:
            for cls in self.event_dates_dict[nd]:
                self.event_dates_dict[nd][cls] = self.simulation.inter_arrival_times[nd][cls]()

    def inter_arrival(self, nd, cls):
        """
        Samples the inter-arrival time for next class and node.
        """
        return self.simulation.inter_arrival_times[nd][cls]()

    def update_next_event_date(self):
        """
        Passes, updating next event happens at time of event.
        """
        pass
