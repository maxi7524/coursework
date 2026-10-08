# TODO GD - zbieżność 
# parameters
learning_rate = 0.3
n_iter = 5
x_init = (0.1, 0.1)
interval = [-0.2, 0.2]
x_final = (0, 0)

# creating function
x, y = sp.symbols('x y')

func_sp =  (x**2 + y**2)
func_name = sp.latex(func_sp)
func = sp.lambdify((x, y), func_sp)

for i in range(1, 4 + 1):
    n_iter = i
    func_sp_gd = gradient_descent(x_init, func_sp, learning_rate, n_iter, None)
    func_sp_mgd = momentum_gradient_descent(x_init, 0.4, func_sp, learning_rate, n_iter, None)

    plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, GD_NAME, i, True)
    # plot_3d_on_2d(func, func_sp_mgd, interval, x_final, func_name, MGD_NAME, i)

    # mniejsza skala, trzeba to dac na bardzo małej odległości i pokazać w jaki sposób to maleje
    # chat wyrzuci przeliczoną funkcje z dobrym przykładem 

# TODO GD vs MTD - brak zbieżności 
# parameters
learning_rate = 0.3
x_init = (0.5, 0.5)
interval = [-0.1, 0.6]
x_final = (0, 0)

# creating function
x, y = sp.symbols('x y')

for i in range(1, 9):
    n_iter = i
    # gd nie działa ~ słaba zbieżnośc (nie minima są małe)
    func_sp = 1/20 *( x**2 + y **2)
    func_name = sp.latex(func_sp)
    func = sp.lambdify((x, y), func_sp)
    func_sp_gd = gradient_descent(x_init, func_sp, learning_rate, n_iter, None)

    plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, GD_NAME, i, True)


    # pokazanie że momentum sobie lepiej radzi 
    func_sp = 1/20 *(x**2 + y **2)
    func_name = sp.latex(func_sp)
    func = sp.lambdify((x, y), func_sp)
    func_sp_gd = momentum_gradient_descent(x_init, 0.9, func_sp, learning_rate, n_iter, None)

    plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, MGD_NAME, i, True)
    
    

# TODO GD vs MTG - skoki 
# parameters
learning_rate = 0.3
x_init = (-0.500000000000000, -0.238322211630124)
interval = [-1, 1]
x_final = (0, 0)
bool_print = True

# creating function
x, y = sp.symbols('x y')
func_sp = ( x**2 + 1.3 * y **2)
func_name = sp.latex(func_sp)
func = sp.lambdify((x, y), func_sp)

# x: -0.200000000000000, x2: -0.500000000000000, 
# y: -0.0524308865586273, y2: -0.238322211630124


for i in range(1, 14 + 1):
    n_iter = i
    # gd nie działa ~ słaba zbieżnośc (nie minima są małe)

    # gd  
    lr = 0.9
    func_sp_gd = gradient_descent(x_init, func_sp, lr, n_iter, None)
    plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, GD_NAME, i, bool_print)

    # mgd  
    # lr = 0.7
    func_sp_gd = momentum_gradient_descent(x_init, 0.9, func_sp, lr, n_iter, None)
    plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, MGD_NAME, i, bool_print)
   

# func_sp_gd = momentum_gradient_descent(x_init, 0.9, func_sp, 0.9, 2000, 1e-2)
# print(len(func_sp_gd))
# plot_3d_on_2d(func, func_sp_gd, interval, x_final, func_name, MGD_NAME, 2, bool_print)


# TODO tabela 
# parameters
learning_rate = 0.5
x_init = (212, 531)
interval = [-1, 1]
x_final = (0, 0)
bool_print = True

# creating function
x, y = sp.symbols('x y')
func_sp = ( x**2 + 1.3 * y **2)
func_name = sp.latex(func_sp)
func = sp.lambdify((x, y), func_sp)

convergence_table = []
for j in range(1, 20):
    values = []
    x_init = (5*j, 5*j)
    arg_x = np.linspace(0.01, 1, 100)
    for i in arg_x:
        item = [2000, 2000]
        func_sp_mgd = momentum_gradient_descent(x_init, 0.9, func_sp, i, 2000, 1e-5)
        func_sp_adam = adam_gradient_descent(x_init, func_sp, i , 2000, 1e-5)
        dist = func_sp_mgd[-1] - x_final, func_sp_adam[-1] - x_final
        if np.linalg.norm(func_sp_mgd[-1] - x_final) < 1e-4:
            item[0] = len(func_sp_mgd)
        if np.linalg.norm(func_sp_adam[-1] - x_final) < 1e-4:
            item[1] = len(func_sp_adam)
        values.append(item)

    values = np.array(values)
    values[:, 0].min(), values[:, 1].min()
    convergence_table.append((values[:, 0].min(), values[:, 1].min()))
convergence_table

df = pd.DataFrame(convergence_table, columns=['adam', 'mgd'])
df['diff'] = df['mgd'] - df['adam'] 
df.sort_values(by='diff')