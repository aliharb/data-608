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
  title = "Years"
)

b <- list(
  title = "State Crude Rate & Country AVG"
)


server <- function(input, output) {
  
  subsetByState<-reactive({
 
    mortality %>%
    filter(ICD.Chapter==input$CauseSelect) %>%
    select(State, Year, Deaths, Population, Crude.Rate) %>%
    group_by(Year) %>%
    mutate(Country.Avg = round((sum(Deaths) / sum(Population)) * 100000, 1)) %>%
    select(State, Year, Deaths, Population, Crude.Rate, Country.Avg) %>%
    ungroup()%>%
    filter(State==input$StateSelect) %>%
    select(Year, Crude.Rate, Country.Avg) %>%
    rename(State.Crude.Avg = Crude.Rate)
})


  output$distPlot <- renderPlotly({
    
    #mortalityCause<-mortality2010[mortality2010$ICD.Chapter==input$select,]
    
    p <- plot_ly(subsetByState(), x = ~Year, y = ~State.Crude.Avg, 
                 name = "State Crude Rate", type = 'scatter', mode = 'lines')  %>%
      add_trace(y = ~Country.Avg, name = 'Country avarge') %>%
      layout(title = "State Crude Rate Vs Country AVG",xaxis = a, yaxis = b)
    
    p
  })
}