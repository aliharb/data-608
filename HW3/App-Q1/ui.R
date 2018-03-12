library(shiny)
library(dplyr)
library(tidyr)
library(plotly)

# Define UI ----

ui <- fluidPage(
  
  titlePanel("Mortality Cause"),
  sidebarLayout(
    
    sidebarPanel(
      selectInput("select", h5("Slecect A Mortality Cause"), 
                  choices = mortality2010$ICD.Chapter,1 )
    ),

    mainPanel(
      htmltools::div(style = "display:inline-block", plotlyOutput(outputId = "distPlot", width = 1000, height = 600))
    )
  )
)