library(shiny)
library(dplyr)
library(tidyr)
library(plotly)



url<-"https://raw.githubusercontent.com/charleyferrari/CUNY_DATA608/master/lecture3/data/cleaned-cdc-mortality-1999-2010-2.csv"
mortality <- read.csv(file=url, header=TRUE, sep=",")

mortality2010 <- mortality %>%
  filter(Year == 2010) %>%
  group_by(State, ICD.Chapter)


a <- list(
  title = "Crude Death Rate per 100,000 Persons",
  autotick = TRUE,
  tickcolor = toRGB("blue")
)

b <- list(
  title = "States",
  autotick = FALSE,
  tickcolor = toRGB("blue")
)

# Define server logic ----
server <- function(input, output) {
  
  
  output$distPlot <- renderPlotly({
    
    mortalityCause<-mortality2010[mortality2010$ICD.Chapter==input$select,]
    
    p<- plot_ly(mortalityCause, x = ~(mortalityCause$Crude.Rate), y = ~(reorder(mortalityCause$State, mortalityCause$Crude.Rate)), 
                type = 'bar',
                name = 'Primary Product',
                orientation = 'h',
                marker = list(color = 'rgb(49,130,189)'))
    
    p %>%layout(xaxis = a, yaxis = b)
    
  })
}