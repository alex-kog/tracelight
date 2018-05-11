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
library(crayon)
options <- commandArgs(trailingOnly = TRUE)
if (length(options)  != 2) {
  fileName=("~/github/tracelight/tracelight/output/output_02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490_400000.json")
} else  {
  fileName=(paste0("~/github/tracelight/tracelight/output/output_",options[1],"_",options[2],".json"))
}
#outputFile=file("~/github/tracelight/tracelight/output/output_02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490_400001.json")
#cat("file name is" %+% fileName)
outputFile=file(fileName)
output=fromJSON(outputFile,simplifyVector = F)
cat("\nAnalysing routes to "%+%blue(options[1])%+%" alias:("%+%green(output$origin_alias)%+%") for capacity of "%+%yellow(options[2])%+%"\n")
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
