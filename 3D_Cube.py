from py5 import *

# only decorator is needed, you can name the function
# whatever you want
@setup_
def f():
    global img1, img2
    size(600, 337)
    # loop the program till, 10
    # keep adding 0.001
    dT(0.001)

angle = 0.0
size = 50

# projection matrix to make it 3D
proj_ = np.array([
    [1, 0, 0],
    [0, 1, 0]
])

# points of a cube, as numpy vectors.
a_ = np.array([
    [-size],
    [-size],
    [size]])

b_ = np.array([
    [size],
    [-size],
    [size]])

c_ = np.array([
    [size],
    [size],
    [size]])

d_ = np.array([
    [-size],
    [size],
    [size]])

e_ = np.array([
    [-size],
    [-size],
    [-size]])

f_ = np.array([
    [size],
    [-size],
    [-size]])

g_ = np.array([
    [size],
    [size],
    [-size]])

h_ = np.array([
    [-size],
    [size],
    [-size]])


# again, decorator only !.
@draw_
def g():
    global angle
    # background is important, always use it.
    # hex code, no alpha. Tkinter does'nt support alpha
    # use can use alpha with PyImage, but i'll be slow
    # or a color name
    #background('#ffffff')
    background('black')
    
    # width is W()
    # height is H()
    translate(W()/2, H()/2)
    
    # X rotation matrix
    rot_ = np.array([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])
    
    # Y rotation matrix
    rot_y = np.array([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    
	# Z rotation matrix
    # rotZ = np.array([
    #     [cos(angle), -sin(angle), 0],
    #     [sin(angle), 0, cos(angle), 0],
    #     [0, 0, 1]
    # ])
    
    # applying the rotation to all the points
    # you can do it in a more efficent way
    
    a = rot_ @ a_
    a = rot_y @ a
    a = proj_ @ a
    circle(a[0, 0], a[1, 0], 10)

    b = rot_ @ b_
    b = rot_y @ b
    b = proj_ @ b
    circle(b[0, 0], b[1, 0], 10)

    c = rot_ @ c_
    c = rot_y @ c
    c = proj_ @ c
    circle(c[0, 0], c[1, 0], 10)

    d = rot_ @ d_
    d = rot_y @ d
    d = proj_ @ d
    circle(d[0, 0], d[1, 0], 10)

    e = rot_ @ e_
    e = rot_y @ e
    e = proj_ @ e
    circle(e[0, 0], e[1, 0], 10)
    
    f = rot_ @ f_
    f = rot_y @ f
    f = proj_ @ f
    circle(f[0, 0], f[1, 0], 10)

    g = rot_ @ g_
    g = rot_y @ g
    g = proj_ @ g
    circle(g[0, 0], g[1, 0], 10)

    h = rot_ @ h_
    h = rot_y @ h
    h = proj_ @ h
    circle(h[0, 0], h[1, 0], 10)

    # lines ...
    stroke('#ff00ff')
    line(a[0, 0], a[1, 0], b[0, 0], b[1, 0])
    line(b[0, 0], b[1, 0], c[0, 0], c[1, 0])
    line(c[0, 0], c[1, 0], d[0, 0], d[1, 0])
    line(d[0, 0], d[1, 0], a[0, 0], a[1, 0])

    line(a[0, 0], a[1, 0], e[0, 0], e[1, 0])
    line(b[0, 0], b[1, 0], f[0, 0], f[1, 0])
    line(c[0, 0], c[1, 0], g[0, 0], g[1, 0])
    line(d[0, 0], d[1, 0], h[0, 0], h[1, 0])

    line(e[0, 0], e[1, 0], f[0, 0], f[1, 0])
    line(f[0, 0], f[1, 0], g[0, 0], g[1, 0])
    line(g[0, 0], g[1, 0], h[0, 0], h[1, 0])
    line(h[0, 0], h[1, 0], e[0, 0], e[1, 0])
     
    angle += 0.001
#
