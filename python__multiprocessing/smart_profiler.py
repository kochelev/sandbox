import os
import sys
import math
import time
import networkx as nx
import statistics
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import shapiro, kstest, anderson, normaltest, ttest_ind, mannwhitneyu
from scipy.stats.stats import pearsonr
import plotly.express as px


class Logger():

    folder_name = '.profiler'

    def __init__(self):

        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)

        self.experiment_id = hash(time.time())
        self.file_name = self.folder_name + '/.' + str(self.experiment_id)
        print('Идентификатор эксперимента:', self.experiment_id)

    @staticmethod
    def calibrate():

        start = time.perf_counter() * 100_000
        x = 2 ** 10_000
        finish = time.perf_counter() * 100_000
        
        return (finish - start) / 100_000


    def mst(self, milestone_name, factors=None):

        if ';' in milestone_name:
            raise MilestoneNameError()

        t = time.perf_counter()

        if factors is not None:
            pass

        with open(self.file_name, 'a') as file:
            file.write(str(t) + ';' + str(self.calibrate()) + ';' + milestone_name + '\n')


class Monitor():

    folder_name = '.profiler'
    
    def __init__(self, experiment_id, start_name='*'):

        self.file_name = self.folder_name + '/.' + str(experiment_id)
        self.start_name = start_name
        self.structure = {}

        self.analyze()

        self.graph = nx.DiGraph()
            
        for obj in self.structure.values():
            
            self.graph.add_edge(obj['vertexes'][0], obj['vertexes'][1], **obj['stats'])

        self.graph_order = self.order_graph(self.graph)

        self.show_graph()

    
    def analyze(self):

        with open(self.file_name, 'r') as file:

            previous_tuple = None

            cbr_mean = 0

            for i, line in enumerate(file):

                ts, cbr, milestone_name = line.rstrip().split(';')
                ts = float(ts)
                cbr = float(cbr)
                cbr_mean = (cbr_mean * (i + 1) + cbr) / (i + 2)

                if previous_tuple is None:

                    previous_tuple = ts, cbr, milestone_name
                    continue

                prev_ts, prev_cbr, prev_milestone_name = previous_tuple

                key = prev_milestone_name + ' - ' + milestone_name
                
                if key not in self.structure:
                    self.structure[key] = {
                        'vertexes': [prev_milestone_name, milestone_name],
                        'deltas': [],
                        'calibration_deltas': [],
                        'calibrated_deltas': []
                    }

                self.structure[key]['deltas'].append(ts - prev_ts)
                self.structure[key]['calibration_deltas'].append((cbr + prev_cbr) / 2)
                self.structure[key]['calibrated_deltas'].append(self.structure[key]['deltas'][-1] / (cbr + prev_cbr) / 2)

                previous_tuple = ts, cbr, milestone_name

            # Поправка, в связи с калибрацией
            
            for key, edge in self.structure.items():
                edge['calibrated_deltas'] = [x * cbr_mean for x in edge['calibrated_deltas']]

            for edge_name, edge_data in self.structure.items():
                
                l = len(edge_data['deltas'])
                self.structure[edge_name]['count'] = l

                normal_deltas = [math.log(x + 0.000000000001) for x in edge_data['deltas']]
                normal_calibrated_deltas = [math.log(x + 0.000000000001) for x in edge_data['calibrated_deltas']]

                self.structure[edge_name]['stats'] = {
                    
                    'count':    l,
                    'mean':     math.exp(statistics.mean(normal_deltas)),
                    'median':   math.exp(statistics.median(normal_deltas)),
                    'mode':     math.exp(statistics.mode(normal_deltas)),
                    
                    'calibrated_mean':      math.exp(statistics.mean(normal_calibrated_deltas)),
                    'calibrated_median':    math.exp(statistics.median(normal_calibrated_deltas)),
                    'calibrated_mode':      math.exp(statistics.mode(normal_calibrated_deltas)),

                    'calibration_correlation': pearsonr(edge_data['deltas'], edge_data['calibration_deltas']),
                    
                    'sw_test':  shapiro(normal_deltas) if l >= 3 and l <= 5000 else None,
                    'ks_test':  kstest(normal_deltas, stats.norm.cdf) if l >= 3 else None,
                    'a_test':   anderson(normal_deltas) if l >= 3 else None,
                    'n_test':   normaltest(normal_deltas) if l >= 3 else None,
                    
                    'calibrated_sw_test':   shapiro(normal_calibrated_deltas) if l >= 3 and l <= 5000 else None,
                    'calibrated_ks_test':   kstest(normal_calibrated_deltas, stats.norm.cdf) if l >= 3 else None,
                    'calibrated_a_test':    anderson(normal_calibrated_deltas) if l >= 3 else None,
                    'calibrated_n_test':    normaltest(normal_calibrated_deltas) if l >= 3 else None,
                    
                }
                self.structure[edge_name]['stats'].update({
                    'mean_rounded': round(self.structure[edge_name]['stats']['mean'], 7)
                })


    def order_graph(self, G):

        order = [[self.start_name]]

        current_index = 0
        list_of_passed_vertexes = [self.start_name]

        while True:
            
            current_list_of_vertex = order[current_index]
            
            for current_vertex in current_list_of_vertex:

                for _, target_vertex in G.out_edges(current_vertex):
                    if current_index == 0 or (current_index != 0 and target_vertex not in list_of_passed_vertexes):
                        list_of_passed_vertexes.append(current_vertex)
                        if target_vertex != current_vertex:
                            try:
                                if target_vertex not in order[current_index + 1]:
                                    order[current_index + 1].append(target_vertex)
                            except IndexError:
                                order.insert(current_index + 1, [target_vertex])
                
                if current_index + 1 <= len(order) - 1:
                    for v in order[current_index + 1]:
                        for _, outbound_vertex in G.out_edges(v):
                            if outbound_vertex != v and outbound_vertex in order[current_index + 1]:
                                order[current_index + 1].remove(outbound_vertex)
                                try:
                                    if outbound_vertex not in order[current_index + 2]:
                                        order[current_index + 2].append(outbound_vertex)
                                except IndexError:
                                    order.append([outbound_vertex])

            current_index += 1

            if current_index >= len(order):
                break

        return order


    def show_graph(self, figsize = (10, 7), x_fn = lambda i, j: i, y_fn = lambda i, j: -i ** 2 / 5 - j):
        
        plt.rcParams["figure.figsize"] = figsize

        pos = {}

        for i, column in enumerate(self.graph_order):
            pos.update({vertex: (x_fn(i, j), y_fn(i, j)) for j, vertex in enumerate(column)})

        elarge = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["count"] > 50]
        esmall = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d["count"] <= 50]

        # counts = [value['stats']['count'] for value in tt.structure.values()]

        nx.draw_networkx_nodes(self.graph, pos, node_size=500, node_color='white', edgecolors='black', linewidths=0.8)
        nx.draw_networkx_labels(self.graph, pos)
        nx.draw_networkx_edges(self.graph, pos, edgelist=elarge, width=1, arrowsize=14, )
        nx.draw_networkx_edges(self.graph, pos, edgelist=esmall, width=1, arrowsize=14, alpha=0.5, edge_color="b", style="dashed")

        edge_labels = nx.get_edge_attributes(self.graph, "mean_rounded")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.20)
        # plt.rcParams["figure.figsize"] = figsize
        plt.axis("off")
        plt.show()

    
    def inspect_edge(self, edge):
        
        start, end = edge
        edge_name = start + ' - ' + end

        for key, value in self.structure[edge_name]["stats"].items():
            print(key, value)
        
        deltas = [x + 0.000000000001 for x in self.structure[edge_name]['deltas']]
        
        l = len(deltas)
        
        calibrated_deltas = [x + 0.000000000001 for x in self.structure[edge_name]['calibrated_deltas']]
        calibration_deltas = [x + 0.000000000001 for x in self.structure[edge_name]['calibration_deltas']]

        fig = px.histogram(title='Гистограмма времени выполнения участка кода', x=deltas, nbins=100)
        fig.show()

        fig = px.histogram(title='Гистограмма калибровки', x=calibration_deltas, nbins=100)
        fig.show()

        fig = px.histogram(title='Гистограмма откалиброванного времени выполнения участка кода', x=calibrated_deltas, nbins=100)
        fig.show()

        fig = px.scatter(title='Замеры времени выполнения участка кода', x=range(1, l+1), y=deltas)
        fig.show()

        fig = px.scatter(title='Замеры времени калибровки', x=range(1, l+1), y=calibration_deltas)
        fig.show()

        fig = px.scatter(title='Замеры откалиброванного времени выполнения участка кода', x=range(1, l+1), y=calibrated_deltas)
        fig.show()


class FnRunner():
    

    def __init__(self, fn):

        self.fn = fn


    def run(self, times, *args, **kwargs):
        
        lgr = Logger()

        for i in range(times):

            lgr.mst('*')

            y = self.fn(*args, **kwargs)

            lgr.mst('1')
            
            sys.stdout.write("Итерация %d из %d  \r" % (i+1, times) )
            sys.stdout.flush()

            lgr.mst('2')

        mst = Monitor(lgr.experiment_id)

        return mst
    

class MilestoneNameError(BaseException):

    def __init__(self):
        self.message = 'Недопустимый символ в названии вехи'

    def __str__(self):
        return self.message


def compare_edges(obj_1, edges_1, obj_2, edges_2):

    edge_1_1, edge_1_2 = edges_1
    edge_2_1, edge_2_2 = edges_2

    deltas_1 = [x + 0.000000000001 for x in obj_1.structure[edge_1_1 + ' - ' + edge_1_2]["calibrated_deltas"]]
    normal_deltas_1 = [math.log(x) for x in deltas_1]

    deltas_2 = [x + 0.000000000001 for x in obj_2.structure[edge_2_1 + ' - ' + edge_2_2]["calibrated_deltas"]]
    normal_deltas_2 = [math.log(x) for x in deltas_2]

    return {
        't_test': ttest_ind(normal_deltas_1, normal_deltas_2, equal_var=True),
        'mw_test': mannwhitneyu(normal_deltas_1, normal_deltas_2, alternative='two-sided', use_continuity=True)
    }
