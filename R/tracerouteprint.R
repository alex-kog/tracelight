library(jsonlite)
library(crayon)
outputFile=file("~/github/tracelight/tracelight/output/sample_tool_output.json")
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
  cat("Start checking route #",route$route_id,"via", length(route$hops),"hops",fill=T)
  Sys.sleep(sleep)
  from=output$origin_alias
  for (hop in route$hops){
    cat(paste("\thop:",hop$chan_id, "from",from, "to",hop$alias))
    three_dots(sleep=sleep)
    cat("\t"%+%ifelse(hop$destination_status=="online",green(hop$destination_status), red(hop$destination_status)))
    if (hop$destination_status=="offline") sleep=0
    three_dots(sleep=sleep)
    cat("\t"%+%ifelse(hop$enough_capacity,green("has"),red("no"))%+%" capacity")
    new_line()
    from=hop$alias
    
  }
}
