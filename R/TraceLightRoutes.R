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


library(jsonlite)
library(dplyr)
library(igraph)

fileName=("/Users/admin/github/tracelight/tracelight/output/output_02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490_400000.json")
outputFile=file(fileName)
routesJson=fromJSON(outputFile,simplifyVector = F)
routes=routesJson$routes

g_from=vector()
g_to=vector()
g_color=vector()
g_lty=vector()
g_nodes=c(routesJson$origin_alias)
g_status=c("ONLINE")
for (i in 1:length(routes)){
  from=routesJson$origin_alias
  route=routes[[i]]
  for (hop in route$hops){
    to=hop$destination_alias
    cat ("from",from,"to", to,"\n")
    g_from=c(g_from,from)
    g_to=c(g_to,to)
    g_color=c(g_color,i)
    g_lty=c(g_lty,ifelse(hop$enough_capacity,1,2))
    if (!(hop$destination_alias %in% g_nodes )){
      g_nodes=c(g_nodes,hop$destination_alias)
      g_status=c(g_status,hop$destination_status)
    }
   
    from=to
  }
}

g_links=data.frame(from=g_from,to=g_to,color=g_color,lty=g_lty)
g_nodes=data.frame(name=g_nodes,status=g_status)
net=graph_from_data_frame(d=g_links,vertices = g_nodes, directed=T)
l=layout_with_lgl(net)
V(net)$color=1
#V(net)$color[V(net)$name==TargetNode]<-"pink"
#V(net)$color[V(net)$name==my_pub]<-"blue"
plot(net,vertex.label.dist=1,
     #vertex.label=left_join(data.frame(nodes=V(net)$name),nodes.df,by=c("nodes"="pub_key"))$alias,
     layout=l
     ,ylim=c(min(l[,2]),max(l[,2])),xlim=c(min(l[,1]),max(l[,1])),asp=0,
     rescale = FALSE,edge.arrow.size=0.7,edge.arrow.width=1,
     vertex.size=20,edge.lty=E(net)$lty,
     vertex.shape=ifelse(V(net)$status=="ONLINE","circle","square"),
     vertex.frame.color=ifelse(V(net)$status=="ONLINE","black","red"),
     edge.width=2)

