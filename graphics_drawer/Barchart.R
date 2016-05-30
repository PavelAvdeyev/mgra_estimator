acc1 <- read.csv('proAcc.csv', dec = ',', sep = ';' )
View(acc1)
attach(acc)
library(ggplot2)

ggplot(acc1, aes(x= Folder, y = Data, fill = Measure), 
       las = 2) + geom_bar(stat = 'identity', 
          position = 'fill') + ggtitle('Procars') +
  xlab('') + ylab('') + labs(fill = '') +
  theme(axis.text.x = element_text(angle = 60, 
        hjust = 1, colour = 'black', face = 'bold'), plot.title = 
          element_text(size = 16, face = 'bold'))

