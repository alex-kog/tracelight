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
TargetNode="03d3f875b88f083dd4d1d5af4bcd5483d7bf0303ec1f585879e2a1012961ec9a9d"
Capacity=1
myinfo=system("~/gocode/bin/lncli getinfo",intern = T)
myinfo.df=fromJSON(myinfo,simplifyVector = T)
my_pub=myinfo.df$identity_pubkey

graphJson=system(paste("~/gocode/bin/lncli describegraph"),intern = T)
graphJson.df=fromJSON(graphJson,simplifyVector = T)
edges.df=graphJson.df$edges[,c(1,3,4,5)]
nodes.df=graphJson.df$nodes

routesJson=system(paste("~/gocode/bin/lncli queryroutes",TargetNode,Capacity),intern = T)
routes.df=fromJSON(routesJson,simplifyVector = T)[[1]]
hops=routes.df$hops
for (i in 1:length(hops)){
  hops[[i]]$route=i
}

channels=do.call(rbind.data.frame, hops)
#channels.uniq=channels[!duplicated(channels),]
channels.uniq=channels
channels=(right_join(edges.df,channels.uniq,by=c("channel_id"="chan_id")))
g_links=data.frame(from=channels$node1_pub,to=channels$node2_pub, capacity=channels$chan_capacity,
                   color=channels$route)
net <- graph_from_data_frame(d=g_links, directed=F) 
#nodes=V(net)$name
l=layout_with_lgl(net)
#l=layout.grid(net,height = 5, width = 5)
V(net)$color=1
V(net)$color[V(net)$name==TargetNode]<-"pink"
V(net)$color[V(net)$name==my_pub]<-"blue"
#plot(net,vertex.label.dist=2,vertex.label=NA,layout=l)
plot(net,vertex.label.dist=1,
     vertex.label=left_join(data.frame(nodes=V(net)$name),nodes.df,by=c("nodes"="pub_key"))$alias,
     layout=l
     ,ylim=c(min(l[,2]),max(l[,2])),xlim=c(min(l[,1]),max(l[,1])),asp=0,
     rescale = FALSE,
     edge.width=2)

