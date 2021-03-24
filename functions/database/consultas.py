from entities.producto import Producto
from database import conexion as pgsql


def productos(producto):
    sql = """
select p.nombre_producto, p.talla, p.color, p.precio, p.url_imagen, c.descripcion, t.descripcion
from producto p, categoria_producto c, tipo_producto t
where p.id_categoria_producto = c.id_categoria_producto
and t.id_tipo_producto = c.id_tipo_producto """
    if producto != None:
        sql = sql + f"and c.id_tipo_producto = {producto.tipo} "
        # if producto.nombre != None:
        #    sql = sql + f"and lower(p.nombre_producto) like lower('%{producto.nombre}%') "
        if producto.talla != None:
            sql = sql + f"and p.talla = '{producto.talla}' "
        if producto.color != None:
            sql = sql + f"and p.color = '{producto.color}' "
    print(sql)
    products = []
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        productos = conn.execute(sql).fetchall()
        for prod in productos:
            p = Producto(prod[0], prod[1], prod[2], producto.tipo)
            p.precio = prod[3]
            p.image = prod[4]
            p.descripcion = prod[6]
            products.append(p)

    return products
