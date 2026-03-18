set terminal pngcairo size 1400,800
set output "results/phase3_plot.png"
set title "Phase 3: Completion Time vs Loss/Error Rate"
set xlabel "loss/error rate (%)"
set ylabel "completion time (seconds)"
set grid
set key left top
set xtics rotate by 45
set datafile separator ","
plot "results/phase3_avg.csv" using 1:2 with linespoints title "Option 1 (No loss/errors)", \
     "results/phase3_avg.csv" using 1:4 with linespoints title "Option 2 (ACK bit-errors)", \
     "results/phase3_avg.csv" using 1:6 with linespoints title "Option 3 (DATA bit-errors)", \
     "results/phase3_avg.csv" using 1:8 with linespoints title "Option 4 (ACK loss)", \
     "results/phase3_avg.csv" using 1:10 with linespoints title "Option 5 (DATA loss)"
