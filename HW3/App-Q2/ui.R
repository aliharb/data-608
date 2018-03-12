library(shiny)
library(dplyr)
library(tidyr)
library(plotly)


ui <- fluidPage(
  
  titlePanel("state vs Country Avarage of Selective Mortality Cause"),
  sidebarLayout(
    
    sidebarPanel(
      
      selectInput("CauseSelect", h5("Slecect A Mortality Cause"), 
                  choices = mortality$ICD.Chapter,1 ),
      
      selectInput("StateSelect", h5("Slecect A State"), 
                  choices = mortality$State, 1 )
    ),
    
    mainPanel(
      htmltools::div(style = "display:inline-block", plotlyOutput(outputId = "distPlot", width = 1000, height = 600))
    )
  )
)