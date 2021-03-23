from entities.producto import Producto
from database import conexion as pgsql

def db():
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        usuarios = conn.execute(
            "SELECT * FROM usuarios "
        ).fetchall()
        for usuario in usuarios:
            print(usuario)

def productos(producto):
    sql = """
        select p.nombre_producto, p.talla, p.color, p.precio, p.url_imagen 
        from producto p, categoria_producto c
        where p.id_categoria_producto = c.id_categoria_producto """
    if producto != None:
        sql = sql + "and c.id_tipo_producto = 1 "
        if producto.nombre != None:
            sql = sql + f"and lower(p.nombre_producto) like lower('%{producto.nombre}%') "
        if producto.talla != None:
            sql = sql + f"and p.talla = '{producto.talla}' "
        if producto.color != None:
            sql = sql + f"and p.color = '{producto.color}' "

    products = []
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        productos = conn.execute(sql).fetchall()
        for prod in productos:
            p = Producto(prod[0], prod[1], prod[2])
            p.precio = prod[3]
            p.image = prod[4]
            products.append(p)
    
    return products