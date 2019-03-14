from ctypes import CDLL, byref, c_longlong
from ctypes.util import find_library


__all__ = ['available', 'bind', 'distance', 'isolated_cpus', 'max_node', 'max_possible_node', 'node_free_size', 'node_of_cpu', 'node_size', 'node_to_cpus', 'num_configured_cpus', 'num_configured_nodes', 'num_possible_nodes', 'num_task_cpus', 'num_task_nodes', 'os', 'preferred', 'run_on_node', 'sched_cpus_setaffinity', 'sched_getaffinity', 'sched_nodes_setaffinity', 'set_localalloc', 'set_membind', 'set_preferred']

LIBNUMA = CDLL(find_library("numa"))


LIBNUMA.numa_node_size64.restype = c_longlong


def _strrng2list(rng):
    '''
       Parses a string representing a range into a list
    '''
    try:
        ri = map(int, rng.split('-', 1))
        if len(ri) == 2:
            return range(ri[0], ri[1]+1)
        elif len(ri) == 1:
            return ri
    except Exception as e:
        raise ValueError(rng)


def available():
    '''
        checks if numa(3) is avalable.
    '''
    return LIBNUMA.numa_available() != -1


def max_possible_node():
    '''
        returns the number of the highest possible node in a system. 
    '''
    return LIBNUMA.numa_max_possible_node()


def num_possible_nodes():
    '''
        returns the size of kernel's node mask (kernel type nodemask_t)
    '''
    return LIBNUMA.numa_num_possible_nodes()


def max_node():
    '''
        returns the highest node number available on the current system.
    '''
    return LIBNUMA.numa_max_node()


def num_configured_nodes():
    '''
        returns the number of memory nodes in the system.
    '''
    return LIBNUMA.numa_num_configured_nodes()


def num_configured_cpus():
    '''
        returns the number of cpus in the system.
    '''
    return LIBNUMA.numa_num_configured_cpus()


def num_task_cpus():
    '''
        returns the number of cpus that the calling task is allowed to use.
    '''
    return LIBNUMA.numa_num_task_cpus()


def num_task_nodes():
    '''
        returns the number of nodes on which the calling task is allowed to allocate memory.
    '''
    return LIBNUMA.numa_num_task_nodes()


def preferred():
    '''
        returns the preferred node of the current task.
    '''
    return LIBNUMA.numa_preferred()


def set_preferred(node):
    '''
        sets the preferred node for the current task to node.
    '''
    if node < 0 or node > max_node():
        raise ValueError(node)
    LIBNUMA.numa_set_preferred(node)



def bind(nodes):
    '''
        binds the current task and its children to the nodes specified in node.
    '''
    bitmask = LIBNUMA.numa_parse_nodestring(nodes)
    if not bitmask:
        raise ValueError(nodes)
    LIBNUMA.numa_bind(bitmask)
    numa_bitmask_free(bitmask)


def set_membind(nodes):
    '''
        sets the memory allocation specified nodes
    '''
    bitmask = LIBNUMA.numa_parse_nodestring(nodes)
    if not bitmask:
        raise ValueError(nodes)
    LIBNUMA.numa_set_membind(bitmask)
    LIBNUMA.numa_bitmask_free(bitmask)


def run_on_node(node):
    '''
        runs the current task and its children on a specific node.
    '''
    if node < 0 or node > max_node():
        raise ValueError(node)

    return LIBNUMA.numa_run_on_node(node)


def set_localalloc():
    '''
        sets the memory allocation policy for the calling task to local allocation.
    '''
    LIBNUMA.numa_set_localalloc()


def sched_cpus_setaffinity(pid, cpus):
    '''
        sets a task's allowed cpus to specified ones.
    '''
    bitmask = LIBNUMA.numa_parse_cpustring(cpus)
    if not bitmask:
        raise ValueError(cpus)

    LIBNUMA.numa_sched_setaffinity(pid, bitmask)
    LIBNUMA.numa_bitmask_free(bitmask)

    
def sched_nodes_setaffinity(pid, nodes):
    '''
        sets a task's allowed nodes to specified ones
    '''
    bitmask = LIBNUMA.numa_parse_nodestring(nodes)
    if not bitmask:
        raise ValueError(nodes)

    LIBNUMA.numa_sched_setaffinity(pid, bitmask)
    LIBNUMA.numa_bitmask_free(bitmask)


def sched_getaffinity(pid):
    '''
        returns a list of the cpus on which a task may run.
    '''
    bitmask = LIBNUMA.numa_allocate_cpumask()
    LIBNUMA.numa_sched_getaffinity(pid, bitmask)

    cpus = [c for c in range(0, num_configured_cpus()) if LIBNUMA.numa_bitmask_isbitset(bitmask, c)]
    LIBNUMA.numa_bitmask_free(bitmask)
    return cpus
    

def isolated_cpus():
    '''
        returns a list of isolated cpus
    '''
    with open('/sys/devices/system/cpu/isolated', 'r') as f:
        isolated = f.read().strip()
        if not isolated: return []

        result = []
        for rng in isolated.split(','):
            result += _strrng2list(rng)

        return result


def node_size(node):
    '''
        returns the memory size of a node.
    '''
    if node < 0 or node > max_node():
        raise ValueError(node)

    return LIBNUMA.numa_node_size64(node, 0)


def node_free_size(node):
    '''
        returns the amount of free memory on the node.
    '''
    if node < 0 or node > max_node():
        raise ValueError(node)

    free = c_longlong()
    LIBNUMA.numa_node_size64(node, byref(free))
    return free.value


def node_of_cpu(cpu):
    '''
        returns the node that a cpu belongs to.
    '''
    return LIBNUMA.numa_node_of_cpu(cpu)


def node_to_cpus(node):
    '''
        returns a list of cpus on specified node
    '''
    if node < 0 or node > max_node():
        raise ValueError(node)

    return [c for c in range(0, num_configured_cpus()) if node_of_cpu(c) == node]


def distance(node1, node2):
    '''
        reports the distance in the machine topology between two nodes.
    '''
    if node1 < 0 or node1 > max_node():
        raise ValueError(node1)

    if node2 < 0 or node2 > max_node():
        raise ValueError(node2)

    return LIBNUMA.numa_distance(node1, node2)
