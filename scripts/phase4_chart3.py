import matplotlib.pyplot as plt

# Your data
phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
times = [0.053, 0.059, 1.725, 2.866]

plt.figure()
plt.plot(phases, times, marker='o')

plt.xlabel("Phase")
plt.ylabel("File Transfer Completion Time (s)")
plt.title("Chart 3: Phase Comparison at 10% Error")

plt.grid()

plt.savefig("results/phase4_chart3.png")
plt.show()