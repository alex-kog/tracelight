library(jsonlite)
library(dplyr)
library(igraph)
TargetNode="03d3f875b88f083dd4d1d5af4bcd5483d7bf0303ec1f585879e2a1012961ec9a9d"
Capacity=1
myinfo=system("/Users/admin/gocode/bin/lncli getinfo",intern = T)
myinfo.df=fromJSON(myinfo,simplifyVector = T)
my_pub=myinfo.df$identity_pubkey
routesJson=system(paste("/Users/admin/gocode/bin/lncli queryroutes",TargetNode,Capacity),intern = T)
routes.df=fromJSON(routesJson,simplifyVector = T)[[1]]
hops=routes.df$hops
channels=do.call(rbind.data.frame, hops)
channels.uniq=channels[!duplicated(channels),]
graphJson=system(paste("/Users/admin/gocode/bin/lncli describegraph"),intern = T)
graphJson.df=fromJSON(graphJson,simplifyVector = T)
edges.df=graphJson.df$edges[,c(1,3,4,5)]
nodes.df=graphJson.df$nodes
channels=(right_join(edges.df,channels.uniq,by=c("channel_id"="chan_id")))
g_links=data.frame(from=channels$node1_pub,to=channels$node2_pub, capacity=channels$chan_capacity)
net <- graph_from_data_frame(d=g_links, directed=F) 
l=layout_with_fr(net)
V(net)$color=1
V(net)$color[V(net)$name==TargetNode]<-2
V(net)$color[V(net)$name==my_pub]<-3
plot(net,vertex.label.dist=2,vertex.label=NA,layout=l)
plot(net,vertex.label.dist=2,vertex.label=NA,layout=l
     ,ylim=c(min(l[,2]),max(l[,2])),xlim=c(min(l[,1]),max(l[,1])), asp = 0,
     rescale = FALSE)
