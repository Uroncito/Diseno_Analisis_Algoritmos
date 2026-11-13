import matplotlib.pyplot as plt
from figuras import circulo

if __name__ == "__main__":
    
    circulo()
    
    plt.grid(True, linestyle = '--', alpha = 0.5)
    plt.title("Circulo")
    plt.show()