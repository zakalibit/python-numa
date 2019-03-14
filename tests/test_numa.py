from __future__ import print_function

import os
import numa


def test_available():
    assert numa.available()


def test_max_possible_node():
    print('NUMA max possible node: {}'.format(numa.max_possible_node()))


def test_num_possible_nodes():
    print('NUMA num possible node: {}'.format(numa.num_possible_nodes()))


def test_max_node():
    print('NUMA max node: {}'.format(numa.max_node()))


def test_num_configured_nodes():
    print('NUMA num configured nodes: {}'.format(numa.num_configured_nodes()))


def test_num_configured_cpus():
    print('NUMA num configured cpus: {}'.format(numa.num_configured_cpus()))


def test_num_task_cpus():
    print('NUMA num task cpus: {}'.format(numa.num_task_cpus()))


def test_num_task_nodes():
    print('NUMA num task nodes: {}'.format(numa.num_task_nodes()))


def test_preferred():
    print('NUMA preferred: {}'.format(numa.preferred()))



def test_set_preferred():
    max_node = numa.max_node()
    if max_node > 0:
        numa.set_preferred(max_node)
        assert numa.preferred() == max_node
    else:
        numa.set_preferred(max_node)
        print('Need more then one node available to test set_preferred')


def test_run_on_node():
    max_node = numa.max_node()
    numa.run_on_node(max_node)


def test_set_localalloc():
    numa.set_localalloc()


def test_sched_cpus_setaffinity():
    affinity = numa.sched_getaffinity(os.getpid())
    assert affinity
    if len(affinity) > 1:
        numa.sched_cpus_setaffinity(os.getpid(), str(affinity[-1]))
        assert numa.sched_getaffinity(os.getpid()) == affinity[-1:]
    else:
        print('Need more the one core to test get/set affinity')


def test_sched_nodes_setaffinity():
    max_node = numa.max_node()
    if max_node > 0:
        numa.sched_nodes_setaffinity(os.getpid(), str(max_node))
        assert numa.sched_getaffinity(os.getpid()) == max_node
    else:
        print('Need more the one core to test get/set affinity')


def test_node_size():
    assert numa.node_size(0) > 0


def test_node_free_size():
    assert numa.node_free_size(0) > 0



def test_node_of_cpu():
    assert numa.node_of_cpu(0) == 0
