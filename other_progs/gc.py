import gc, sys

def make_cycle():
    """ This method creates cyclic objects which cannot be detected by
    reference counting. In such cases, python employs a garbage collection
    algorithm to detect cyclic references and collects them.
    """
    l = {}
    l[0] = l


def main():
    collected = gc.collect()
    print ("Garbage collection. Collected %d objects" % (collected))
    print ("Creating 100 cycles")
    for i in range(100):
        make_cycle()

    collected = gc.collect()
    print ("Garbage collection, Collected %d objs" % (collected))


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
