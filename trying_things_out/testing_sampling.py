import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

num_cap_levels = 3

n = num_cap_levels - 1
p = 0.4

fig, axes = plt.subplots(nrows=1, ncols=3, sharey=False)
fs = 10

sample_sizes = range(50, 1001, 50)

print "SAMPLING FROM DISTRIBUTION"
print "expectation", n * p

binomial_samples = [np.random.binomial(num_cap_levels - 1, p, size = num_samples) for num_samples in sample_sizes]
means = [np.mean(binomial_sample) for binomial_sample in binomial_samples]
print "means", means
axes[0].boxplot(binomial_samples, showmeans= True, labels = sample_sizes)
axes[0].set_title('binomial sample', fontsize=fs)

print "SAMPLING FROM UNIFORM"
print "expectation", (num_cap_levels-1)/2.0
samples = [np.random.randint(0, num_cap_levels, size = num_samples) for num_samples in sample_sizes]
samples_multiplied_by_probs = [[value * stats.binom.pmf(value, n, p) for value in sample] for sample in samples]
uniform_means = [np.mean(sample) for sample in samples]
#print "means", uniform_means
sums = [sum(sample) for sample in samples]
#print "sums", sums
sums_of_multiplied_values = [sum(sample) for sample in samples_multiplied_by_probs]
#print "sums_of_multiplied_values", sums_of_multiplied_values
adj_factors = [num_cap_levels / (sample_size + 0.0) for sample_size in sample_sizes]
#print "multipliers_to_compute_expectations", adj_factors
adjusted_sums = [mult_val * sum for mult_val, sum in zip(adj_factors, sums_of_multiplied_values)]
print "adjusted_sums", adjusted_sums
#print sample_sizes, adjusted_sums
axes[1].boxplot(samples, showmeans= True, labels = sample_sizes)
axes[1].set_title('uniform sample', fontsize=fs)

axes[2].plot(sample_sizes, means, '-ob', label = 'regular means')
axes[2].plot(sample_sizes, adjusted_sums, '-or')
axes[2].set_title('convergence of sample mean', fontsize=fs)
axes[2].axhline(np.mean(means), color='b', linestyle='dashed', linewidth=2)
axes[2].axhline(np.mean(adjusted_sums), color='r', linestyle='dashed', linewidth=2)
axes[2].axhline(n*p, linestyle='dashed', linewidth=2)

for ax in axes.flatten():
    ax.set_yscale('log')
    ax.set_yticklabels([])

fig.subplots_adjust(hspace=0.4)
plt.show()