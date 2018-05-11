from unittest import TestCase

from TraceLight import TraceLight


class TraceLightTest(TestCase):
    def test_pars(self):
        tl = TraceLight()

        routes = tl.fetchRoutes()

        for r in routes:
            print 'Nodes:'
            for node in r.nodes('0355438a4183b37bc523f5759dcfa49a844f828ddf6ce1a05862510f358d91a242'):
                print node
            print '------'
