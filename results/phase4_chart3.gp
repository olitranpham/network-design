set terminal png
set output "results/phase4_chart3.png"

set title "Chart 3: Phase Comparison at 10% Error"
set xlabel "Phase"
set ylabel "Completion Time (seconds)"

set style data histograms
set style fill solid
set boxwidth 0.5

plot "results/phase4_chart3.dat" using 2:xtic(1) title "Time"
