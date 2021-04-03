from entities.producto import Producto
from entities.usuario import Usuario
from database import conexion as pgsql


def usuario(username):
    sql = f"""
select u.nombre, u.apellido, u.talla_calzado, u.talla_pantalon, u.talla_polera, u.genero, u.id_usuario
from usuario u
where estado = 'ACTIVO'
and telegram = '{username}' """
    print(sql)
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        u = conn.execute(sql).fetchone()
        if u != None:
            user = Usuario(username)
            user.nombre(u[0])
            user.apellido(u[1])
            user.talla_calzado(u[2])
            user.talla_pantalon(u[3])
            user.talla_polera(u[4])
            user.genero(u[5])
            user.id(u[6])
            return user

    return None


def productos(producto: Producto):
    sql = """
select p.nombre_producto, p.talla, p.color, TO_NUMBER(p.precio, 'L99999.99') precio, p.url_imagen, c.descripcion, 
t.descripcion, p.id_producto, p.id_genero
from producto p, categoria_producto c, tipo_producto t
where p.id_categoria_producto = c.id_categoria_producto
and t.id_tipo_producto = c.id_tipo_producto
and p.precio is not null """
    if producto != None:
        sql = sql + f"and c.id_tipo_producto = {producto.tipo} "
        # if producto.nombre != None:
        #    sql = sql + f"and lower(p.nombre_producto) like lower('%{producto.nombre}%') "
        if producto.talla != None:
            sql = sql + f"and p.talla = '{producto.talla}' "
        if producto.color != None:
            sql = sql + f"and p.color = '{producto.color}' "
        if producto.get_genero() != None:
            sql = sql + f"and p.id_genero = {producto.get_genero()} "
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
            p.codigo = prod[7]
            p.genero(prod[8])
            products.append(p)

    return products
