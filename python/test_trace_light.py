# This file is part of TraceLight.
#
# TraceLight is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraceLight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toasty.  If not, see <http://www.gnu.org/licenses/>.

from TraceLight import TraceLight
from draw_graph import draw_routes


class TraceLightTest():
    def test_pars(self):
        tl = TraceLight()

        routes = tl.fetchRoutes()

        for r in routes:
            print 'Nodes:'
            for node in r.nodes('0355438a4183b37bc523f5759dcfa49a844f828ddf6ce1a05862510f358d91a242'):
                print node
            print '------'

        draw_routes(routes)


if __name__ == "__main__":
    test = TraceLightTest()
    test.test_pars()
