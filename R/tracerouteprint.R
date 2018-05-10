library(jsonlite)
library(crayon)
outputFile=file("~/github/tracelight/tracelight/output/output_02f82a1188bb4baa885de6c0d14276db056aa9da768de545c4fc7349379b5670cb_1.json")
output=fromJSON(outputFile,simplifyVector = F)
routes=output$routes
three_dots<-function(sleep=1){
  Sys.sleep(sleep)
  cat(".")
  Sys.sleep(sleep)
  cat(".")
  Sys.sleep(sleep)
  cat(".")
}
new_line<-function(){
  cat(fill=TRUE)
}
for (route in routes){
  sleep=1
  cat("\nStart checking route #",route$route_id,"via", length(route$hops),"hops",fill=T)
  Sys.sleep(sleep)
  from=output$origin_alias
  for (hop in route$hops){
    cat(paste("\thop:",hop$chan_id, "from",from, "to",hop$destination_alias))
    three_dots(sleep=sleep)
    cat("\t"%+%ifelse(hop$destination_status=="ONLINE",green(hop$destination_status), red(hop$destination_status)))
    if (hop$destination_status=="OFFLINE") sleep=0
    three_dots(sleep=sleep)
    captext=ifelse(hop$destination_status!="ONLINE",red("unknown"),ifelse(hop$enough_capacity,green("has"),red("no")))
    
    #cat("\t"%+%ifelse(hop$enough_capacity,green("has"),red("no"))%+%" capacity")
    cat("\t"%+%captext%+%" capacity")
    
    new_line()
    from=hop$destination_alias
    
  }
}
