import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def print_normal_cumulative_distribution(mean, std, title):
    print('mean = ' + str(mean))
    print('std = ' + str(std))
    
    def find_cell_size(min, max):
        max_number_of_cells = 15
        
        if (max - min) > max_number_of_cells:
            return (max - min) // max_number_of_cells
            
        return 1 
    
    min = int(round((mean - 4 * std)))
    max = int(round((mean + 4 * std)))
    
    x = np.linspace(min, max, 50)
    y = stats.norm.cdf(x, mean, std)

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xticks(np.arange(min, max, find_cell_size(min, max)))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    fig.suptitle(title, fontsize=14)
    plt.xlabel('Estimate', fontsize=14)
    plt.ylabel('Probability', fontsize=14)
    plt.rcParams['figure.figsize'] = [12, 6]

    plt.plot(x, y)
    plt.grid()
    plt.show()